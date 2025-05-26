from app.dao.base_dao import BaseDAO
from app.model.endereco import Endereco


class EnderecoDAO(BaseDAO[Endereco]):

    def __init__(self):
        super().__init__(Endereco)
