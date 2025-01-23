from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.models import Doacao  # Substitua pelo nome correto do seu modelo, se necessário.

router = APIRouter()

@router.post("/adicionar", response_model=dict)
async def realizar_doacao(doacao: schemas.DoacaoBase, db: Session = Depends(get_db)):
    doador = crud.get_doador(db, doacao.doador_id)
    recebedor = crud.get_recebedor(db, doacao.recebedor_id)

    if not doador:
        raise HTTPException(status_code=404, detail="Doador não encontrado")
    if not recebedor:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")

    tabela_de_compatibilidade_sanguinea = {
        "O-": {"doa_para": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], "recebe_de": ["O-"]},
        "O+": {"doa_para": ["A+", "B+", "AB+", "O+"], "recebe_de": ["O+", "O-"]},
        "A-": {"doa_para": ["A+", "A-", "AB+", "AB-"], "recebe_de": ["A-", "O-"]},
        "A+": {"doa_para": ["A+", "AB+"], "recebe_de": ["A+", "A-", "O+", "O-"]},
        "B-": {"doa_para": ["B+", "B-", "AB+", "AB-"], "recebe_de": ["B-", "O-"]},
        "B+": {"doa_para": ["B+", "AB+"], "recebe_de": ["B+", "B-", "O+", "O-"]},
        "AB-": {"doa_para": ["AB+", "AB-"], "recebe_de": ["A-", "B-", "AB-", "O-"]},
        "AB+": {"doa_para": ["AB+"], "recebe_de": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]},
        "Rh-nulo": {"doa_para": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Rh-nulo"], "recebe_de": ["Rh-nulo"]},
    }

    tipo_doador = doador.tipo_sanguineo
    tipo_recebedor = recebedor.tipo_sanguineo

    if tipo_recebedor not in tabela_de_compatibilidade_sanguinea[tipo_doador]["doa_para"]:
        return {
            "mensagem": f"Incompatibilidade: {tipo_doador} ({doador.nome}) não pode doar para {tipo_recebedor} ({recebedor.nome})."
        }

    crud.create_doacao(db=db, doacao=doacao)

    return {
        "mensagem": f"Doação compatível: {doador.nome} ({tipo_doador}) pode doar para {recebedor.nome} ({tipo_recebedor}).",
    }

@router.delete("/deletar/{id}", response_model=dict)
async def deletar(id: int, db: Session = Depends(get_db)):
    tupla = db.query(Doacao).filter(Doacao.id == id).first()

    if not tupla:
        raise HTTPException(status_code=404, detail="Registro com o ID fornecido não encontrado")

    db.delete(tupla)
    db.commit()

    return {"mensagem": f"Registro com ID {id} foi deletado com sucesso"}
