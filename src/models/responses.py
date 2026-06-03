"""
Modelos Pydantic que representam os formatos de resposta da API.
O FastAPI usa esses modelos para validar e serializar dados automaticamente.
"""

from pydantic import BaseModel
from typing import Optional, List


class UnidadesClima(BaseModel):
    temperatura: str = "°C"


class DadosClima(BaseModel):
    temperatura_min: float
    temperatura_max: float
    condicao: str
    unidades: UnidadesClima


class RespostaClima(BaseModel):
    nome: str
    estado: str
    clima: DadosClima
    consultado_em: str


class CidadeItem(BaseModel):
    nome: str


class RespostaCidades(BaseModel):
    uf: str
    quantidade_retornada: int
    cidades: List[CidadeItem]
    consultado_em: str


class RespostaHealth(BaseModel):
    status: str
    versao: str
    timestamp: str
    motivo: Optional[str] = None


class RespostaErro(BaseModel):
    erro: bool = True
    codigo: str
    mensagem: str
    nome_informado: Optional[str]    = None
    sigla_uf_informada: Optional[str] = None
    servico: Optional[str]           = None