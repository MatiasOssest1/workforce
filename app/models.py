from pydantic import BaseModel
from typing import Optional, List

class Peticion(BaseModel):
    rut : str
    proceso_id : int

class Rut(BaseModel):
    rut : str

class ModuloEstacion(BaseModel):
    estacion : int
    modulo : int

class Numero(BaseModel):
    rut: str
    numero: int
    estacion: str
    estado: str 

class Usuario(BaseModel):
    usuario: str
    password: str
    
class TokenData(BaseModel):
    user: Optional[str] = None
    token: str
    
class TIF_imp(BaseModel):
    print: int
    entrega: int
    fuente: int
    id: int
    error: Optional[str]

class listaTIF(BaseModel):
    data : List[TIF_imp]

    def get_ids_impresion(self):
        ids = ""
        for tif in self.data:
            if tif.print:
                ids+=str(tif.id)+","
        return ids[:-1] if len(ids) > 1 else "''"

    
    def get_ids_entrega(self):
        ids = ""
        for tif in self.data:
            if tif.entrega:
                ids+=str(tif.id)+","
        return ids[:-1] if len(ids) > 1 else "''"
    
    def get_ids_fuente(self):
        ids = ""
        for tif in self.data:
            if tif.fuente:
                ids+=str(tif.id)+","
        return ids[:-1] if len(ids) > 1 else "''"

'''        
{'data': 
 [{'print': 1, 'entrega':0, 'fuente':0,'id': 1231231541, 'error':'algo'}, 
  {'print': 1, 'entrega':0, 'fuente':0, 'id': 7890, 'error':'algo'}, 
  {'print': 0, 'entrega':0, 'fuente':0, 'id': 12311, 'error':'algo'}]}
'''