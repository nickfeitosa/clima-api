"""
Serviço responsável por buscar dados climáticos via Open-Meteo.

Open-Meteo é gratuito, sem necessidade de chave de API.
Aceita latitude/longitude (obtidos dinamicamente) e retorna
temperatura mínima/máxima e código WMO da condição climática.

Documentação: https://open-meteo.com/en/docs
"""

import httpx
from typing import Dict
from src.config.settings import OPEN_METEO_BASE, REQUEST_TIMEOUT
from src.utils.helpers import codigo_wmo_para_condicao


async def buscar_clima(lat: float, lon: float) -> Dict:
    """
    Busca dados climáticos para as coordenadas dinâmicas fornecidas.

    Parâmetros:
        lat  – latitude (obtida do geocoding, nunca fixa)
        lon  – longitude (obtida do geocoding, nunca fixa)

    Retorna:
        temperatura_min  – temperatura mínima do dia (°C)
        temperatura_max  – temperatura máxima do dia (°C)
        condicao         – condição climática em português
    """
    params = {
        "latitude":      lat,
        "longitude":     lon,
        "daily":         "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone":      "America/Sao_Paulo",
        "forecast_days": 1,
    }

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(f"{OPEN_METEO_BASE}/forecast", params=params)

    response.raise_for_status()
    dados = response.json()

    # Open-Meteo retorna listas mesmo com forecast_days=1; usamos índice [0]
    daily    = dados["daily"]
    temp_max = round(daily["temperature_2m_max"][0], 1)
    temp_min = round(daily["temperature_2m_min"][0], 1)
    wmo_code = int(daily["weathercode"][0])

    return {
        "temperatura_min": temp_min,
        "temperatura_max": temp_max,
        "condicao":        codigo_wmo_para_condicao(wmo_code),
    }