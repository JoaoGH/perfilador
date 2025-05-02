from typing import Optional


class Endereco:
    def __init__(
        self,
        logradouro: Optional[str] = None,
        numero: Optional[str] = None,
        cidade: Optional[str] = None,
        bairro: Optional[str] = None,
        cep: Optional[str] = None,
        uf: Optional[str] = None
    ):
        self.logradouro = logradouro
        self.numero = numero
        self.cidade = cidade
        self.bairro = bairro
        self.cep = cep
        self.uf = uf

    def formatado(self):
        partes = [
            self.logradouro,
            f"nº {self.numero}" if self.numero else None,
            self.bairro,
            self.cidade,
            f"CEP: {self.cep}" if self.cep else None,
            f" - {self.uf}" if self.uf else None,
        ]
        return ", ".join([p for p in partes if p])

    def hasValue(self) -> bool:
        return (
                self.logradouro is not None
                or self.numero is not None
                or self.cidade is not None
                or self.bairro is not None
                or self.cep is not None
                or self.uf is not None
        )
