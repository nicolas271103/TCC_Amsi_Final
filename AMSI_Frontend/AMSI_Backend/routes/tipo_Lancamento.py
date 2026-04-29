from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.tipo_Lancamento import TipoLancamento
from schemas.tipo_Lancamento import TipoLancamentoCreate, TipoLancamentoUpdate, TipoLancamentoResponse
from auth.dependencies import get_current_user, exige_admin
from typing import List

router = APIRouter(
    prefix="/tipo_lancamento",
    tags=["Tipo de Lançamento"]
)

@router.get("/", response_model=List[TipoLancamentoResponse])
def listar_tipos(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(TipoLancamento).all()

@router.get("/{id_tipo_lancamento}", response_model=TipoLancamentoResponse)
def buscar_tipo(id_tipo_lancamento: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    tipo = db.query(TipoLancamento).filter(TipoLancamento.id_tipo_lancamento == id_tipo_lancamento).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de lançamento não encontrado")
    return tipo

@router.post("/", response_model=TipoLancamentoResponse)
def criar_tipo(dados: TipoLancamentoCreate, db: Session = Depends(get_db), _=Depends(exige_admin)):
    tipo = TipoLancamento(**dados.model_dump())
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo

@router.put("/{id_tipo_lancamento}", response_model=TipoLancamentoResponse)
def atualizar_tipo(id_tipo_lancamento: int, dados: TipoLancamentoUpdate, db: Session = Depends(get_db), _=Depends(exige_admin)):
    tipo = db.query(TipoLancamento).filter(TipoLancamento.id_tipo_lancamento == id_tipo_lancamento).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de lançamento não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tipo, campo, valor)
    db.commit()
    db.refresh(tipo)
    return tipo

@router.delete("/{id_tipo_lancamento}")
def deletar_tipo(id_tipo_lancamento: int, db: Session = Depends(get_db), _=Depends(exige_admin)):
    tipo = db.query(TipoLancamento).filter(TipoLancamento.id_tipo_lancamento == id_tipo_lancamento).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de lançamento não encontrado")
    db.delete(tipo)
    db.commit()
    return {"mensagem": "Tipo de lançamento deletado com sucesso"}