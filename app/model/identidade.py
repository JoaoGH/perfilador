from app.model.endereco import Endereco
from app.model.registro_geral import RegistroGeral


class Identidade:
    def __init__(self):
        self.nome = None
        self.cpf = None
        self.rg = RegistroGeral()
        self.data_nascimento = None
        self.email = None
        self.endereco = Endereco()
        self.telefone = None
        self.profissao = None

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
                    self.rg.numero = valor
                case "id_issuer":
                    self.rg.orgao_emissor = valor
                case "birthday":
                    self.data_nascimento = valor
                case "email":
                    self.email = valor
                case "address":
                    self.endereco.logradouro = valor
                case "number_a":
                    self.endereco.numero = valor
                case "city":
                    self.endereco.cidade = valor
                case "district":
                    self.endereco.bairro = valor
                case "postal":
                    self.endereco.cep = valor
                case "uf":
                    self.endereco.uf = valor
                case "phone":
                    self.telefone = valor
                case "professional_id":
                    if self.profissao is None:
                        self.profissao = []
                    self.profissao.append(valor)

    def to_dict(self):
        dictionary = {
            "nome": self.nome,
            "cpf": self.cpf,
            "rg": self.rg.formatado() if self.rg.numero else None,
            "data_nascimento": self.data_nascimento,
            "email": self.email,
            "endereco": self.endereco.formatado() if self.endereco else None,
            "telefone": self.telefone,
            "profissao": str(self.profissao)

        }

        if self.rg.numero is not None:
            dictionary["rg"] = self.rg.formatado()

        if self.endereco.hasValue():
            dictionary["endereco"] = self.endereco.formatado()

        return dictionary
