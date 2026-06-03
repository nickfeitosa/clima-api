"""
Controller do Endpoint 2: GET /api/v1/cidades/{sigla_uf}

Orquestra: validação UF → buscar municípios → aplicar limite → resposta
"""

import httpx
from fastapi import HTTPException
from src.services.brasil_api_service import buscar_municipios_por_uf
from src.models.responses import RespostaCidades, CidadeItem
from src.utils.helpers import normalizar_uf, timestamp_agora
from src.config.settings import (
    ESTADOS_VALIDOS,
    CIDADES_LIMITE_DEFAULT,
    CIDADES_LIMITE_MIN,
    CIDADES_LIMITE_MAX,
)


async def listar_cidades_por_uf(
    sigla_uf: str,
    limite: int = CIDADES_LIMITE_DEFAULT,
) -> RespostaCidades:
    """
    Retorna lista de municípios de um estado.

    Validações:
        - sigla_uf deve ter exatamente 2 letras
        - limite deve estar entre 1 e 100
    """

    sigla_uf = normalizar_uf(sigla_uf)

    # 1. Validar formato da sigla UF
    if len(sigla_uf) != 2 or not sigla_uf.isalpha():
        raise HTTPException(
            status_code=400,
            detail={
                "erro": True,
                "codigo": "SIGLA_UF_INVALIDA",
                "mensagem": "A sigla do estado deve conter exatamente 2 letras",
                "sigla_uf_informada": sigla_uf,
            },
        )

    # 2. Validar se é um estado válido do Brasil
    if sigla_uf not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=404,
            detail={
                "erro": True,
                "codigo": "UF_NAO_ENCONTRADA",
                "mensagem": "Estado com a sigla informada não foi encontrado",
                "sigla_uf_informada": sigla_uf,
            },
        )

    # 3. Validar o parâmetro limite
    if not (CIDADES_LIMITE_MIN <= limite <= CIDADES_LIMITE_MAX):
        raise HTTPException(
            status_code=400,
            detail={
                "erro": True,
                "codigo": "LIMITE_INVALIDO",
                "mensagem": f"O limite deve estar entre {CIDADES_LIMITE_MIN} e {CIDADES_LIMITE_MAX}",
                "sigla_uf_informada": sigla_uf,
            },
        )

    # 4. Buscar municípios na BrasilAPI
    try:
        municipios = await buscar_municipios_por_uf(sigla_uf)
    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                "servico": "BRASIL_API",
            },
        )

    if not municipios:
        raise HTTPException(
            status_code=404,
            detail={
                "erro": True,
                "codigo": "UF_NAO_ENCONTRADA",
                "mensagem": "Estado com a sigla informada não foi encontrado",
                "sigla_uf_informada": sigla_uf,
            },
        )

    # 5. Aplicar limite e retornar
    cidades_limitadas = municipios[:limite]

    return RespostaCidades(
        uf=sigla_uf,
        quantidade_retornada=len(cidades_limitadas),
        cidades=[CidadeItem(nome=c["nome"]) for c in cidades_limitadas],
        consultado_em=timestamp_agora(),
    )