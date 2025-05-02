from typing import Optional


class RegistroGeral:
    def __init__(
        self,
        numero: Optional[str] = None,
        orgao_emissor: Optional[str] = None,
        estado: Optional[str] = None
    ):
        self.numero = numero
        self.orgao_emissor = orgao_emissor
        self.estado = estado

    def formatado(self):
        if self.numero:
            return f"{self.numero} - {self.orgao_emissor or ''}/{self.estado or ''}".strip(" -/")
        return None
