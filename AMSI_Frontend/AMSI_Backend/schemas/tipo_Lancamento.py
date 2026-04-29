from pydantic import BaseModel
from typing import Optional
from enum import Enum


class NaturezaEnum(str, Enum):
    Debito = "Debito"
    Credito = "Credito"


# O que o frontend manda para criar um tipo de lançamento
class TipoLancamentoCreate(BaseModel):
    descricao_conta: str
    natureza_conta: NaturezaEnum
    observacao: Optional[str] = None


# O que o frontend manda para atualizar um tipo de lançamento
class TipoLancamentoUpdate(BaseModel):
    descricao_conta: Optional[str] = None
    natureza_conta: Optional[NaturezaEnum] = None
    observacao: Optional[str] = None


# O que a API devolve
class TipoLancamentoResponse(BaseModel):
    id_tipo_lancamento: int
    descricao_conta: str
    natureza_conta: NaturezaEnum
    observacao: Optional[str] = None

    class Config:
        from_attributes = True