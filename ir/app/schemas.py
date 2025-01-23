from pydantic import BaseModel
from typing import List, Optional

class DoadorBase(BaseModel):
    nome: str
    idade: int
    tipo_sanguineo: str
    data_da_ultima_doacao: str

    class Config:
        from_attribute = True
        populate_by_namee = True
        from_attributes = True

class RecebedorBase(BaseModel):
    nome: str
    idade: int
    tipo_sanguineo: str
    necessidades_de_sangue: str

    class Config:
        from_attribute = True
        populate_by_namee = True
        from_attributes = True

class DoacaoBase(BaseModel):
    doador_id: int
    recebedor_id: int

    class Config:
        from_attribute = True
        populate_by_namee = True
        from_attributes = True
