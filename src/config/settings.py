"""
Configurações centralizadas da aplicação.
Todas as URLs de APIs externas e constantes globais ficam aqui.
"""

API_VERSION = "1.0.0"
API_PORT    = 3000

# URLs das APIs externas
BRASIL_API_BASE  = "https://brasilapi.com.br/api"
OPEN_METEO_BASE  = "https://api.open-meteo.com/v1"
NOMINATIM_BASE   = "https://nominatim.openstreetmap.org"

# Timeout em segundos para chamadas externas
REQUEST_TIMEOUT = 10

# Limites do parâmetro ?limite
CIDADES_LIMITE_DEFAULT = 10
CIDADES_LIMITE_MIN     = 1
CIDADES_LIMITE_MAX     = 100

# Siglas de estados válidos do Brasil
ESTADOS_VALIDOS = {
    "AC","AL","AP","AM","BA","CE","DF","ES","GO",
    "MA","MT","MS","MG","PA","PB","PR","PE","PI",
    "RJ","RN","RS","RO","RR","SC","SP","SE","TO",
}