from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.cliente_fornecedor import ClienteFornecedor
from models.usuario import Usuario
from schemas.cliente_fornecedor import ClienteFornecedorCreate, ClienteFornecedorUpdate, ClienteFornecedorResponse
from auth.dependencies import get_current_user
from typing import List

router = APIRouter(
    prefix="/cliente_fornecedor",
    tags=["Cliente/Fornecedor"]
)

@router.get("/", response_model=List[ClienteFornecedorResponse])
def listar_clifors(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(ClienteFornecedor).all()

@router.get("/{id_clifor}", response_model=ClienteFornecedorResponse)
def buscar_clifor(id_clifor: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    clifor = db.query(ClienteFornecedor).filter(ClienteFornecedor.id_clifor == id_clifor).first()
    if not clifor:
        raise HTTPException(status_code=404, detail="Cliente/Fornecedor não encontrado")
    return clifor

@router.post("/", response_model=ClienteFornecedorResponse)
def criar_clifor(dados: ClienteFornecedorCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if dados.id_usuario_fk:
        if not db.query(Usuario).filter(Usuario.id_usuario == dados.id_usuario_fk).first():
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    clifor = ClienteFornecedor(**dados.model_dump())
    db.add(clifor)
    db.commit()
    db.refresh(clifor)
    return clifor

@router.put("/{id_clifor}", response_model=ClienteFornecedorResponse)
def atualizar_clifor(id_clifor: int, dados: ClienteFornecedorUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    clifor = db.query(ClienteFornecedor).filter(ClienteFornecedor.id_clifor == id_clifor).first()
    if not clifor:
        raise HTTPException(status_code=404, detail="Cliente/Fornecedor não encontrado")
    if dados.id_usuario_fk:
        if not db.query(Usuario).filter(Usuario.id_usuario == dados.id_usuario_fk).first():
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(clifor, campo, valor)
    db.commit()
    db.refresh(clifor)
    return clifor

@router.delete("/{id_clifor}")
def deletar_clifor(id_clifor: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    clifor = db.query(ClienteFornecedor).filter(ClienteFornecedor.id_clifor == id_clifor).first()
    if not clifor:
        raise HTTPException(status_code=404, detail="Cliente/Fornecedor não encontrado")
    db.delete(clifor)
    db.commit()
    return {"mensagem": "Cliente/Fornecedor deletado com sucesso"}