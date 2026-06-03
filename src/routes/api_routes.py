"""
Definição das rotas da API.

Separa a configuração das rotas da lógica dos controllers,
seguindo o princípio de Separação de Responsabilidades (SOLID - SRP).
"""

from fastapi import APIRouter, Query
from src.controllers.clima_controller import obter_clima_cidade
from src.controllers.cidades_controller import listar_cidades_por_uf
from src.controllers.health_controller import verificar_health
from src.config.settings import CIDADES_LIMITE_DEFAULT

# Router com prefixo /api/v1
router = APIRouter(prefix="/api/v1")


@router.get(
    "/health",
    summary="Health Check",
    description="Verifica se a API está operacional.",
    tags=["Health"],
)
async def health():
    return await verificar_health()


@router.get(
    "/clima/{nome_cidade}",
    summary="Dados climáticos de uma cidade",
    description="Retorna dados geográficos e climáticos de uma cidade brasileira.",
    tags=["Clima"],
)
async def clima(nome_cidade: str):
    return await obter_clima_cidade(nome_cidade)


@router.get(
    "/cidades/{sigla_uf}",
    summary="Lista cidades de um estado",
    description="Retorna municípios de um estado brasileiro filtrados pelo limite.",
    tags=["Cidades"],
)
async def cidades(
    sigla_uf: str,
    limite: int = Query(
        default=CIDADES_LIMITE_DEFAULT,
        ge=1,
        le=100,
        description="Quantidade máxima de cidades a retornar (1-100)",
    ),
):
    return await listar_cidades_por_uf(sigla_uf, limite)