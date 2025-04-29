import os
from typing import List

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from app.document import Document
from app.document_manager import DocumentManager
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

        entities = self.ner_pipeline(document.normalized)

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

    def extract_relations(self, document: Document, entities: List[str]) -> List[str]:
        """
        Extrai relações entre entidades

        :param document:
        :param entities:
        :return:
        """

        if not document.normalized or not entities:
            return []

        relations = []
        current_identity = []

        for entity in entities:
            if current_identity and entity["entity_group"] == "name":
                relations.append(current_identity)
                current_identity = []
            current_identity.append(entity)

        if current_identity:
            relations.append(current_identity)

        formatted_relations = []
        for group in relations:
            identidade = {
                'nome': None,
                'cpf': None,
                'rg': None,
                'data_nascimento': None,
                'email': None,
                'endereco': None,
                'telefone': None,
                'profissao': None
            }
            rg_partes = {'numero': '', 'orgao': ''}
            endereco_partes = {'logradouro': '', 'numero': '', 'cidade': '', 'bairro': '', 'cep': '', 'uf': ''}

            for ent in group:
                tipo = ent.get('entity_group', '').lower()
                valor = ent['word'].strip()
                if 'name' in tipo:
                    identidade['nome'] = valor
                elif 'cpf' in tipo:
                    identidade['cpf'] = valor
                elif 'id' in tipo:
                    rg_partes['numero'] = valor
                elif 'id_issuer' in tipo:
                    rg_partes['orgao'] = valor
                elif 'birthday' in tipo:
                    identidade['data_nascimento'] = valor
                elif 'email' in tipo:
                    identidade['email'] = valor
                elif 'address' in tipo:
                    endereco_partes['logradouro'] = valor
                elif 'number_a' in tipo:
                    endereco_partes['numero'] = valor
                elif 'city' in tipo:
                    endereco_partes['cidade'] = valor
                elif 'district' in tipo:
                    endereco_partes['bairro'] = valor
                elif 'postal' in tipo:
                    endereco_partes['cep'] = valor
                elif 'uf' in tipo:
                    endereco_partes['uf'] = valor
                elif 'phone' in tipo:
                    identidade['telefone'] = valor
                elif 'professional_id' in tipo:
                    if identidade['profissao'] is None:
                        identidade['profissao'] = []
                    identidade['profissao'].append(valor)

            endereco_formatado = ', '.join([
                endereco_partes['logradouro'],
                endereco_partes['numero'],
                endereco_partes['bairro'],
                endereco_partes['cidade'],
                endereco_partes['cep'],
                endereco_partes['uf'],
            ]).strip(', ')
            identidade['endereco'] = endereco_formatado if endereco_formatado else None

            rg_formatado = ' - '.join([
                rg_partes['numero'],
                rg_partes['orgao']
            ]).strip(' - ')
            identidade['rg'] = rg_formatado if rg_formatado else None

            formatted_relations.append(identidade)

        return formatted_relations

    def execute(self, preprocessor: PreProcessor) -> None:
        doc_index = int(input("Digite o índice do documento: "))

        if len(self.document_manager.files) < doc_index:
            print(f"Não há arquivo com index '{doc_index}'.")
            return

        selected_doc = self.document_manager.files[doc_index - 1]
        preprocessor.execute_by_document(selected_doc)

        entities = self.extract_entities(selected_doc)
        relations = self.extract_relations(selected_doc, entities)

        print(f"Documento: [{doc_index:02d}] - {selected_doc.name}")
        print("\nEntidades encontradas:")
        for ent in entities:
            print(ent)

        print("\nRelações encontradas:")
        for rel in relations:
            print(rel)