import os
from typing import List

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from app.dao.documentos_dao import DocumentoDao
from app.dao.endereco_dao import EnderecoDAO
from app.dao.identidade_dao import IdentidadeDAO
from app.model.document import Document
from app.document_manager import DocumentManager
from app.model.endereco import Endereco
from app.model.identidade import Identidade
from app.pre_processor import PreProcessor


class InformationExtractor:
    def __init__(self, model_path: str = "./resources/models/LGPDBert-0320-Lowercase"):
        self.model_path = model_path
        self._load_model()
        self.document_manager = DocumentManager()

    def _load_model(self) -> None:
        """Carrega o modelo e tokenizador do diretório informado"""
        self._verify_model_files()

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            truncation=True,
            max_length=512,
            model_max_length=512)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_path)
        self.ner_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple")

    def _verify_model_files(self) -> None:
        """Verifica se os arquivos do modelo existem"""
        required_files = ['config.json', 'pytorch_model.bin', 'vocab.txt']
        for file in required_files:
            if not os.path.exists(os.path.join(self.model_path, file)):
                raise FileNotFoundError("Arquivo necessário não encontrado",
                                        f"Certifique-se que o modelo está em: {self.model_path}")

    def extract_entities(self, document: Document) -> List:
        """
        Extrai entidades nomeadas do texto pré-processado

        :param document:
        :return:
        """

        if not document.normalized:
            return []

        entities = []

        pages = document.normalized.split(self.document_manager.PAGE_SEPARATOR)
        for chunk in pages:
            entities.extend(self.ner_pipeline(chunk))

        entities = self.merge_adjacent_entities(entities)

        return entities

    def merge_adjacent_entities(self, entities):
        if not entities:
            return []

        merged = []
        current = entities[0].copy()

        for entity in entities[1:]:
            # Verifica se a entidade atual é adjacente à anterior
            if entity['start'] == current['end']:
                current['word'] += entity['word'].replace('##', '')  # Remove ## se existir
                current['end'] = entity['end']
                current['score'] = (current['score'] + entity['score']) / 2  # Média dos scores
            else:
                # Adiciona a entidade atual ao resultado e começa uma nova
                merged.append(current)
                current = entity.copy()

        # Adiciona a última entidade processada
        merged.append(current)

        return merged

    def extract_relations(self, document: Document, entities: List[str]) -> List[Identidade]:
        """
        Extrai relações entre entidades

        :param document:
        :param entities:
        :return:
        """

        if not document.normalized or not entities:
            return []

        relations = []
        groups = self._group_by_identity(entities)

        for group in groups:
            address = Endereco()
            address.process_entity(group)
            identity = Identidade()
            identity.process_entity(group)
            identity.document = document
            identity.endereco = address
            relations.append(identity)

        return relations

    def _group_by_identity(self, entities: List[str]) -> List[str]:
        relations = []
        current_identity = []

        for entity in entities:
            if current_identity and entity["entity_group"] == "name":
                relations.append(current_identity)
                current_identity = []
            current_identity.append(entity)

        if current_identity:
            relations.append(current_identity)

        return relations

    def _save_extracted_identities(self, relations: List[Identidade]) -> bool:
        dao = IdentidadeDAO()
        daoEndereco = EnderecoDAO()
        success = False
        for relation in relations:
            try:
                if relation.endereco.hasValue():
                    enderecoId = daoEndereco.insert(relation.endereco)
                    relation.endereco.id = enderecoId
                id = dao.insert(relation)
                print(f"Registro salvo com ID '{id}' na tabela '{dao.table_name}'")
                success = True
            except Exception as e:
                print(f"Erro ao salvar: {e}")

        return success

    def execute_by_document(self, preprocessor: PreProcessor) -> None:
        doc_index = int(input("Digite o índice do documento: "))

        if len(self.document_manager.files) < doc_index:
            print(f"Não há arquivo com index '{doc_index}'.")
            return

        self.execute(doc_index, preprocessor)

    def execute_for_all(self, preprocessor: PreProcessor) -> None:
        for index, document in enumerate(self.document_manager.files):
            self.execute(index+1, preprocessor)

    def execute(self, doc_index: int, preprocessor: PreProcessor) -> None:
        selected_doc = self.document_manager.files[doc_index - 1]

        if selected_doc.information_extracted:
            return

        preprocessor.execute_by_document(selected_doc)

        entities = self.extract_entities(selected_doc)
        relations = self.extract_relations(selected_doc, entities)

        print(f"Documento: [{doc_index:02d}] - {selected_doc.name}")
        print(f"{len(entities)} entidades encontradas")
        print(f"{len(relations)} relações encontradas")

        success = self._save_extracted_identities(relations)

        if success:
            selected_doc.information_extracted = True
            dao = DocumentoDao()
            dao.update(selected_doc.id, selected_doc.to_dict())
