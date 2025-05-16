from app.dao.base_dao import BaseDAO
from app.model.identidade import Identidade


class IdentidadeDAO(BaseDAO[Identidade]):

    def __init__(self):
        super().__init__(Identidade)
