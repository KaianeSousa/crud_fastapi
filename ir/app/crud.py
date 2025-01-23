from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException

# DOADORES
def get_doador(db: Session, doador_id: int):
    return db.query(models.Doador).filter(models.Doador.id == doador_id).first()

def create_doador(db: Session, doador: schemas.DoadorBase):
    db_doador = models.Doador(**doador.dict())
    db.add(db_doador)
    db.commit()
    db.refresh(db_doador)
    return db_doador

def update_doador(db: Session, id: int, doador: schemas.DoadorBase):
    db_doador = db.query(models.Doador).filter(models.Doador.id == id).first()
    if not db_doador:
        raise HTTPException(status_code=404, detail="Doador não encontrado")
    for key, value in doador.dict().items():
        setattr(db_doador, key, value)
    db.commit()
    db.refresh(db_doador)
    return db_doador

def delete_doador(db: Session, id: int):
    db_doador = db.query(models.Doador).filter(models.Doador.id == id).first()
    if not db_doador:
        raise HTTPException(status_code=404, detail="Doador não encontrado")
    db.delete(db_doador)
    db.commit()
    return {"message": "Doador deletado com sucesso"}

# RECEBEDORES

# RECEBEDORES
def get_recebedor(db: Session, recebedor_id: int):
    return db.query(models.Recebedor).filter(models.Recebedor.id == recebedor_id).first()

def create_recebedor(db: Session, recebedor: schemas.RecebedorBase):
    db_recebedor = models.Recebedor(**recebedor.dict())  # Desestruturando o objeto do schema
    db.add(db_recebedor)
    db.commit()
    db.refresh(db_recebedor)
    return db_recebedor

def update_recebedor(db: Session, id: int, recebedor: schemas.RecebedorBase):
    db_recebedor = db.query(models.Recebedor).filter(models.Recebedor.id == id).first()
    if not db_recebedor:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")
    for key, value in recebedor.dict(exclude_unset=True).items():  # Não tenta atualizar o valor original se não foi enviado
        setattr(db_recebedor, key, value)
    db.commit()
    db.refresh(db_recebedor)
    return db_recebedor

def delete_recebedor(db: Session, id: int):
    db_recebedor = db.query(models.Recebedor).filter(models.Recebedor.id == id).first()
    if not db_recebedor:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")
    db.delete(db_recebedor)
    db.commit()
    return {"message": f"Recebedor {db_recebedor.nome} deletado com sucesso"}  # Retorna o nome do recebedor deletado

# DOAÇÕES
def create_doacao(db: Session, doacao: schemas.DoacaoBase):
    db_doacao = models.Doacao(**doacao.dict())
    db.add(db_doacao)
    db.commit()
    db.refresh(db_doacao)
    return db_doacao
