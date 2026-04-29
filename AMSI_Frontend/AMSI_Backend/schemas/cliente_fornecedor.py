from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class TipoCliForEnum(str, Enum):
    Cliente = "C"
    Fornecedor = "F"
    Ambos = "A"


# O que o frontend manda para criar um cliente/fornecedor
class ClienteFornecedorCreate(BaseModel):
    id_usuario_fk: Optional[int] = None
    pessoafisica_juridica: bool
    cpf_cnpj: str
    rg_inscricaoestadual: str
    nome: str
    datanascimento: date
    tipo_clifor: TipoCliForEnum
    ativo: bool = True
    inadimplente: bool = False


# O que o frontend manda para atualizar um cliente/fornecedor
class ClienteFornecedorUpdate(BaseModel):
    id_usuario_fk: Optional[int] = None
    pessoafisica_juridica: Optional[bool] = None
    cpf_cnpj: Optional[str] = None
    rg_inscricaoestadual: Optional[str] = None
    nome: Optional[str] = None
    datanascimento: Optional[date] = None
    tipo_clifor: Optional[TipoCliForEnum] = None
    ativo: Optional[bool] = None
    inadimplente: Optional[bool] = None


# O que a API devolve
class ClienteFornecedorResponse(BaseModel):
    id_clifor: int
    id_usuario_fk: Optional[int] = None
    pessoafisica_juridica: bool
    cpf_cnpj: str
    rg_inscricaoestadual: str
    nome: str
    datanascimento: date
    tipo_clifor: TipoCliForEnum
    ativo: bool
    inadimplente: bool

    class Config:
        from_attributes = True