# dao/departamento_dao.py
from dao.base_dao import BaseDAO
from model.departamento import Departamento

class DepartamentoDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn, table_name="departamento", pk_name="id")

    def create_departamento(self, dept: Departamento):
        new_id = self.create(dept.to_dict())
        dept.id = new_id
        return dept

    def get_departamento(self, id):
        row = self.read(id)
        if row:
            return Departamento.from_row(row)
        return None

    def update_departamento(self, id, dept: Departamento):
        data = dept.to_dict()
        self.update(id, data)

    def delete_departamento(self, id):
        self.delete(id)

    def list_departamentos(self):
        rows = self.list_all()
        return [Departamento.from_row(row) for row in rows]