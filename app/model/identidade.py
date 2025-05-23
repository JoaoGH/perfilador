from app.model.document import Document
from app.model.endereco import Endereco


class Identidade:
    def __init__(self):
        self.nome = None
        self.cpf = None
        self.rg = None
        self.orgao_emissor = None
        self.data_nascimento = None
        self.email = None
        self.endereco: Endereco = Endereco()
        self.telefone = None
        self.profissao = None
        self.document: Document = Document()

    def process_entity(self, entities) -> None:
        for ent in entities:
            tipo = ent.get("entity_group", "").lower()
            valor = ent["word"].strip()
            match tipo:
                case "name":
                    self.nome = valor
                case "cpf":
                    self.cpf = valor
                case "id":
                    self.rg = valor
                case "id_issuer":
                    self.orgao_emissor = valor
                case "birthday":
                    self.data_nascimento = valor
                case "email":
                    self.email = valor
                case "phone":
                    self.telefone = valor
                case "professional_id":
                    if self.profissao is None:
                        self.profissao = []
                    self.profissao.append(valor)

    @staticmethod
    def get_table_name() -> str:
        return "identidades"

    def to_dict(self):
        dictionary = {
            "nome": self.nome,
            "cpf": self.cpf,
            "rg": self.rg,
            "rg_orgao_emissor": self.orgao_emissor,
            "data_nascimento": self.data_nascimento,
            "email": self.email,
            "endereco": self.endereco.formatado() if self.endereco.hasValue() else None,
            "endereco_id": self.endereco.id if self.endereco.hasValue() else None,
            "telefone": self.telefone,
            "profissao": str(self.profissao) if self.profissao else None,
            "documento_id": self.document.id,
        }

        return dictionary
