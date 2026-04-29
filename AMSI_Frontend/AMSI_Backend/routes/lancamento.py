from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.lancamento import Lancamento
from models.usuario import Usuario
from models.cliente_fornecedor import ClienteFornecedor
from models.tipo_Lancamento import TipoLancamento
from schemas.lancamento import LancamentoCreate, LancamentoUpdate, LancamentoResponse
from auth.dependencies import get_current_user
from typing import List

router = APIRouter(
    prefix="/lancamento",
    tags=["Lançamento"]
)

@router.get("/", response_model=List[LancamentoResponse])
def listar_lancamentos(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Lancamento).all()

@router.get("/{id_lancamento}", response_model=LancamentoResponse)
def buscar_lancamento(id_lancamento: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    lancamento = db.query(Lancamento).filter(Lancamento.id_lancamento == id_lancamento).first()
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    return lancamento

@router.get("/por-clifor/{id_clifor}", response_model=List[LancamentoResponse])
def listar_lancamentos_por_clifor(id_clifor: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Lancamento).filter(Lancamento.id_clifor_relacionado_fk == id_clifor).all()

@router.get("/por-usuario/{id_usuario}", response_model=List[LancamentoResponse])
def listar_lancamentos_por_usuario(id_usuario: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Lancamento).filter(Lancamento.id_usuario_fk_lancamento == id_usuario).all()

@router.post("/", response_model=LancamentoResponse)
def criar_lancamento(dados: LancamentoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if not db.query(Usuario).filter(Usuario.id_usuario == dados.id_usuario_fk_lancamento).first():
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not db.query(ClienteFornecedor).filter(ClienteFornecedor.id_clifor == dados.id_clifor_relacionado_fk).first():
        raise HTTPException(status_code=404, detail="Cliente/Fornecedor não encontrado")
    if not db.query(TipoLancamento).filter(TipoLancamento.id_tipo_lancamento == dados.id_tipo_lancamento_fk).first():
        raise HTTPException(status_code=404, detail="Tipo de lançamento não encontrado")
    lancamento = Lancamento(**dados.model_dump())
    db.add(lancamento)
    db.commit()
    db.refresh(lancamento)
    return lancamento

@router.put("/{id_lancamento}", response_model=LancamentoResponse)
def fechar_lancamento(id_lancamento: int, dados: LancamentoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    lancamento = db.query(Lancamento).filter(Lancamento.id_lancamento == id_lancamento).first()
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    if dados.id_usuario_fk_fechamento:
        if not db.query(Usuario).filter(Usuario.id_usuario == dados.id_usuario_fk_fechamento).first():
            raise HTTPException(status_code=404, detail="Usuário de fechamento não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(lancamento, campo, valor)
    db.commit()
    db.refresh(lancamento)
    return lancamento

@router.delete("/{id_lancamento}")
def deletar_lancamento(id_lancamento: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    lancamento = db.query(Lancamento).filter(Lancamento.id_lancamento == id_lancamento).first()
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    db.delete(lancamento)
    db.commit()
    return {"mensagem": "Lançamento deletado com sucesso"}