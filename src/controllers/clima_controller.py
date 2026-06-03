"""
Controller do Endpoint 1: GET /api/v1/clima/{nome_cidade}

Orquestra: validação → busca cidade → coordenadas dinâmicas → clima → resposta
"""

import httpx
from fastapi import HTTPException
from src.services.brasil_api_service import buscar_cidade_por_nome, buscar_coordenadas
from src.services.clima_service import buscar_clima
from src.models.responses import RespostaClima, DadosClima, UnidadesClima
from src.utils.helpers import timestamp_agora


async def obter_clima_cidade(nome_cidade: str) -> RespostaClima:
    """
    Fluxo completo:
        nome_cidade → buscar_cidade_por_nome() → buscar_coordenadas()
                   → buscar_clima(lat, lon) → RespostaClima
    """

    # 1. Validação de entrada
    if not nome_cidade or len(nome_cidade.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail={
                "erro": True,
                "codigo": "NOME_INVALIDO",
                "mensagem": "O nome da cidade deve conter pelo menos 2 caracteres",
                "nome_informado": nome_cidade,
            },
        )

    nome_cidade = nome_cidade.strip()

    # 2. Buscar informações geográficas
    try:
        cidade_info = await buscar_cidade_por_nome(nome_cidade)
    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                "servico": "NOMINATIM",
            },
        )

    if cidade_info is None:
        raise HTTPException(
            status_code=404,
            detail={
                "erro": True,
                "codigo": "CIDADE_NAO_ENCONTRADA",
                "mensagem": "Nenhuma cidade encontrada com o nome informado",
                "nome_informado": nome_cidade,
            },
        )

    # 3. Obter coordenadas dinamicamente
    try:
        coords = await buscar_coordenadas(cidade_info["nome"], cidade_info["estado"])
    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                "servico": "NOMINATIM",
            },
        )

    if coords is None:
        raise HTTPException(
            status_code=404,
            detail={
                "erro": True,
                "codigo": "CIDADE_NAO_ENCONTRADA",
                "mensagem": "Nenhuma cidade encontrada com o nome informado",
                "nome_informado": nome_cidade,
            },
        )

    # 4. Buscar dados climáticos com coordenadas dinâmicas
    try:
        dados_clima = await buscar_clima(coords["lat"], coords["lon"])
    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                "servico": "OPEN_METEO",
            },
        )

    # 5. Montar e retornar resposta padronizada
    return RespostaClima(
        nome=cidade_info["nome"],
        estado=cidade_info["estado"],
        clima=DadosClima(
            temperatura_min=dados_clima["temperatura_min"],
            temperatura_max=dados_clima["temperatura_max"],
            condicao=dados_clima["condicao"],
            unidades=UnidadesClima(temperatura="°C"),
        ),
        consultado_em=timestamp_agora(),
    )