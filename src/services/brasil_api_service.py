"""
Serviço responsável por consumir a BrasilAPI e o Nominatim (OpenStreetMap).

- Nominatim: geocoding (nome → lat/lon e estado)
- BrasilAPI: lista de municípios por UF

IMPORTANTE: as coordenadas são sempre obtidas DINAMICAMENTE via Nominatim.
Nenhuma coordenada é fixa no código (conforme requisito da atividade).
"""

import httpx
from typing import List, Dict, Optional
from src.config.settings import BRASIL_API_BASE, NOMINATIM_BASE, REQUEST_TIMEOUT

# Headers obrigatórios do Nominatim (identifica o uso da API)
NOMINATIM_HEADERS = {
    "User-Agent": "API-Agregacao-Climatica/1.0 (projeto-academico)"
}


async def buscar_municipios_por_uf(sigla_uf: str) -> List[Dict]:
    """
    Retorna lista de municípios de um estado via BrasilAPI.
    Retorna lista vazia se o estado não for encontrado (404).
    Levanta httpx.HTTPError para outros erros de rede.
    """
    url = f"{BRASIL_API_BASE}/ibge/municipios/v1/{sigla_uf}"

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url)

    if response.status_code == 404:
        return []  # estado inválido

    response.raise_for_status()
    municipios = response.json()
    return [{"nome": m["nome"]} for m in municipios]


async def buscar_cidade_por_nome(nome_cidade: str) -> Optional[Dict]:
    """
    Encontra uma cidade brasileira pelo nome usando Nominatim.
    Retorna dict {"nome": str, "estado": str} ou None se não encontrada.

    Estratégia:
        1. Faz busca no Nominatim com "nome, Brazil"
        2. Extrai o estado (sigla) do campo ISO3166-2-lvl4
        3. Retorna nome oficial + sigla UF
    """
    params = {
        "q":            f"{nome_cidade}, Brazil",
        "format":       "json",
        "limit":        1,
        "addressdetails": 1,
        "countrycodes": "br",
    }

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(
            f"{NOMINATIM_BASE}/search",
            params=params,
            headers=NOMINATIM_HEADERS,
        )

    response.raise_for_status()
    resultados = response.json()

    if not resultados:
        return None

    item     = resultados[0]
    endereco = item.get("address", {})

    # Extrai sigla do estado (formato "BR-CE" → "CE")
    estado_raw = (
        endereco.get("ISO3166-2-lvl4", "")
        or endereco.get("state_code", "")
    )
    sigla_uf = estado_raw.replace("BR-", "").upper()

    # Nome oficial da cidade
    nome_oficial = (
        endereco.get("city")
        or endereco.get("town")
        or endereco.get("village")
        or endereco.get("county")
        or nome_cidade
    )

    if not sigla_uf:
        return None

    return {"nome": nome_oficial, "estado": sigla_uf}


async def buscar_coordenadas(nome_cidade: str, sigla_uf: str) -> Optional[Dict]:
    """
    Retorna latitude e longitude DINÂMICAS de uma cidade via Nominatim.
    Retorna dict {"lat": float, "lon": float} ou None se não encontrada.
    """
    params = {
        "q":            f"{nome_cidade}, {sigla_uf}, Brazil",
        "format":       "json",
        "limit":        1,
        "addressdetails": 1,
    }

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(
            f"{NOMINATIM_BASE}/search",
            params=params,
            headers=NOMINATIM_HEADERS,
        )

    response.raise_for_status()
    resultados = response.json()

    if not resultados:
        return None

    primeiro = resultados[0]
    return {
        "lat": float(primeiro["lat"]),
        "lon": float(primeiro["lon"]),
    }