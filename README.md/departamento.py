#departamento.py

class Departamento:
    def __init__(self, id: int = None, nome: str = None, descricao: str = None):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def to_dict(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao
        }

    @staticmethod
    def from_row(row):
        # supondo row = (id, nome, descricao)
        return Departamento(id=row[0], nome=row[1], descricao=row[2])