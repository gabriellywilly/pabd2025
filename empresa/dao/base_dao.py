'''
  *** BaseDAO ***
  Classe abstrata base para DAOs (Data Access Objects)
  Operações CRUD genéricas
'''

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from supabase import Client

# TypeVar - tornar a classe genérica
T = TypeVar('T')

class BaseDAO(ABC, Generic[T]):

  def __init__(self, client: Client, table_name: str):
    self._client = client
    self._table_name = table_name


  # Do formato JSON (dict) para modelo de dados (T)
  @abstractmethod
  def to_model(self, data: dict) -> T:
    pass #os filhos devem decidir como será feito a implementação

  # Do modelo de dados (T) para formato JSON (dict)
  @abstractmethod
  def to_dict(self, model: T) -> dict:
    pass #os filhos devem decidir como será feito a implementação

  ### Create (Atividade)
  #Criar algo na tabela: 
  def create(self, model: T) -> Optional[T]: #recebe um modelo genérico T
        try:
            data = self.to_dict(model)
            response = self.client.table(self.table_name).insert(data).execute()
            if response.data: 
                return self.to_model(response.data[0])
            return None #retorna
        #Caso de errado:
        except Exception as e:
            print(f"Erro ao criar registro: {e}") #mensagem de erro
            return None 
    
  ### Read (Atividade)
  def read(self, pk: str, value: T) -> Optional[T]:
    try:
      response = self._client.table(self._table_name).select('*').eq(pk, value).execute()
      if response.data and len(response.data) > 0: # retornar alguma resposta
        return self.to_model(response.data[0])
      return None
    except Exception as e:
      print(f'Erro ao buscar registro: {e}')
      return None #indica se o registro existe ou não
  
  # Read All - Retorna todos os valores de uma tabela 
  def read_all(self) -> List[T]:
    try:
      response = self._client.table(self._table_name).select('*').execute()
      if response.data:
        return [self.to_model(item) for item in response.data]
      return None
    except Exception as e:
      print(f'Erro ao buscar todos os registros: {e}')
      return None
    
  ### Update (Atividade)
  def update(self, record_id: int, model: T) -> Optional[T]:
        try:
            data = self.to_dict(model)
            response = self._client.table(self._table_name).update(data).eq('id', record_id).execute()
            if response.data:
                return self.to_model(response.data[0])
            return None #retorna nada
        #caso de erro:
        except Exception as e:
            print(f"Erro ao atualizar registro: {e}") #mensagem de erro
            return None #retorna nada
  
  ### Delete (Atividade)
  def delete(self, record_id: int) -> bool: #retornar valores lógicos (V ou F)
        try:
            response = self._client.table(self._table_name).delete().eq('id', record_id).execute()
            return bool(response.data) #retorna V se o registro for deletado
        #caso de erro:
        except Exception as e:
            print(f"Erro ao deletar registro: {e}") #mensagem de erro
            return None #retorna F