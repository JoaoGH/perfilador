from app.dao.base_dao import BaseDAO

class IdentidadeDAO(BaseDAO):
    def __init__(self):
        super().__init__("identidades")