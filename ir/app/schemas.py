from pydantic import BaseModel
from typing import List, Optional

class DoadorBase(BaseModel):
    id: Optional[int] 
    nome: str
    idade: int
    tipo_sanguineo: str
    data_da_ultima_doacao: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        from_attributes = True

class RecebedorBase(BaseModel):
    id: Optional[int] 
    nome: str
    idade: int
    tipo_sanguineo: str
    necessidades_de_sangue: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        from_attributes = True

class DoacaoBase(BaseModel):
    doador_id: int
    recebedor_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        from_attributes = True
