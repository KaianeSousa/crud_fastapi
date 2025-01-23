from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_model=List[schemas.RecebedorBase])
def listar_recebedores(request: Request, db: Session = Depends(get_db)):
    print("Iniciando listagem de recebedores")
    try:
        doadores = db.query(models.Doador).all()
        print(doadores) 
        return templates.TemplateResponse("recebedores.html", {"request": request, "recebedores": doadores})
    except Exception as e:
        print(f"Erro: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar recebedores: {str(e)}")

@router.get("/{recebedor_id}", response_model=schemas.RecebedorBase)
def pesquisar_recebedor_por_id(recebedor_id: int, db: Session = Depends(get_db)):
    recebedor = crud.get_recebedor(db, recebedor_id)
    if not recebedor:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")
    return recebedor

@router.post("/adicionar", response_model=schemas.RecebedorBase)
def adicionar_recebedor(recebedor: schemas.RecebedorBase, db: Session = Depends(get_db)):
    recebedor_existente = db.query(models.Recebedor).filter(models.Recebedor.nome == recebedor.nome).first()
    if recebedor_existente:
        raise HTTPException(status_code=400, detail="Recebedor já cadastrado")
    return crud.create_recebedor(db=db, recebedor=recebedor)

@router.put("/atualizar/{recebedor_id}", response_model=schemas.RecebedorBase)
def atualizar_recebedor(recebedor_id: int, recebedor: schemas.RecebedorBase, db: Session = Depends(get_db)):
    recebedor_existente = crud.get_recebedor(db, recebedor_id)
    if not recebedor_existente:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")
    return crud.update_recebedor(db=db, id=recebedor_id, recebedor=recebedor)

@router.delete("/deletar/{recebedor_id}")
def deletar_recebedor(recebedor_id: int, db: Session = Depends(get_db)):
    recebedor_existente = crud.get_recebedor(db, recebedor_id)
    if not recebedor_existente:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")
    crud.delete_recebedor(db=db, id=recebedor_id)
    return {"message": f"Recebedor {recebedor_id} deletado com sucesso"}
