"""
Ponto de entrada da aplicação FastAPI.

- Inicializa o servidor FastAPI
- Configura CORS (necessário para testes via navegador)
- Registra todas as rotas
- Configura o handler global de exceções
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.routes.api_routes import router
from src.config.settings import API_VERSION

# ── Criar instância da aplicação ───────────────────────────────────────────────
app = FastAPI(
    title="API de Agregação de Dados Climáticos e Geográficos",
    description=(
        "API REST que combina dados geográficos (BrasilAPI + OpenStreetMap) "
        "com dados climáticos (Open-Meteo) para cidades brasileiras."
    ),
    version=API_VERSION,
    docs_url="/docs",      # Swagger UI disponível em http://localhost:3000/docs
    redoc_url="/redoc",    # ReDoc disponível em http://localhost:3000/redoc
)

# ── Configurar CORS ────────────────────────────────────────────────────────────
# Permite que navegadores e Postman Web façam requisições à API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Registrar rotas ────────────────────────────────────────────────────────────
app.include_router(router)


# ── Handler global de exceções HTTP ───────────────────────────────────────────
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """
    Captura exceções não tratadas e retorna resposta padronizada.
    Evita que detalhes internos sejam expostos ao cliente.
    """
    return JSONResponse(
        status_code=500,
        content={
            "erro": True,
            "codigo": "ERRO_INTERNO",
            "mensagem": "Ocorreu um erro interno. Tente novamente mais tarde.",
        },
    )


# ── Rota raiz (informativa) ────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return {
        "mensagem": "API de Agregação de Dados Climáticos e Geográficos",
        "versao": API_VERSION,
        "documentacao": "/docs",
        "endpoints": [
            "GET /api/v1/health",
            "GET /api/v1/clima/{nome_cidade}",
            "GET /api/v1/cidades/{sigla_uf}",
        ],
    }