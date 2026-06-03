"""
Funções auxiliares reutilizáveis em toda a aplicação.
"""

from datetime import datetime, timezone


def timestamp_agora() -> str:
    """Retorna o timestamp atual em formato ISO 8601 UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalizar_uf(uf: str) -> str:
    """Converte a sigla UF para maiúsculas e remove espaços."""
    return uf.strip().upper()


def codigo_wmo_para_condicao(codigo: int) -> str:
    """
    Converte o código WMO (Open-Meteo) para descrição em português.
    Referência: https://open-meteo.com/en/docs
    """
    tabela = {
        0:  "Céu Limpo",
        1:  "Predominantemente Limpo",
        2:  "Parcialmente Nublado",
        3:  "Nublado",
        45: "Névoa",
        48: "Névoa com Geada",
        51: "Garoa Leve",
        53: "Garoa Moderada",
        55: "Garoa Intensa",
        61: "Chuva Leve",
        63: "Chuva Moderada",
        65: "Chuva Forte",
        71: "Neve Leve",
        73: "Neve Moderada",
        75: "Neve Intensa",
        80: "Pancadas de Chuva Leve",
        81: "Pancadas de Chuva Moderada",
        82: "Pancadas de Chuva Forte",
        95: "Tempestade",
        96: "Tempestade com Granizo Leve",
        99: "Tempestade com Granizo Forte",
    }
    return tabela.get(codigo, "Condição Desconhecida")