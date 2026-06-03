"""
Controller do Endpoint 3: GET /api/v1/health

Verifica se a API está operacional e retorna status healthy ou degraded.
"""

import httpx
from src.models.responses import RespostaHealth
from src.utils.helpers import timestamp_agora
from src.config.settings import API_VERSION, BRASIL_API_BASE, REQUEST_TIMEOUT


async def verificar_health() -> RespostaHealth:
    """
    Testa a conectividade com a BrasilAPI.
    - Se a BrasilAPI responder: retorna status "healthy"
    - Se falhar: retorna status "degraded" com o motivo
    """
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{BRASIL_API_BASE}/ibge/municipios/v1/CE")
        response.raise_for_status()
        status = "healthy"
        motivo = None
    except Exception:
        status = "degraded"
        motivo = "Serviço externo indisponível"

    return RespostaHealth(
        status=status,
        versao=API_VERSION,
        timestamp=timestamp_agora(),
        motivo=motivo,
    )