"""
Testes automatizados dos endpoints da API.

Teste 1: Cidade válida (Fortaleza) deve retornar HTTP 200 com dados corretos
Teste 2: Cidade inexistente deve retornar HTTP 404 com código CIDADE_NAO_ENCONTRADA
Teste 3: Nome inválido (1 caractere) deve retornar HTTP 400 com código NOME_INVALIDO
Teste 4: Endpoint cidades por UF válida deve retornar HTTP 200
Teste 5: UF inválida deve retornar HTTP 400 com código SIGLA_UF_INVALIDA
Teste 6: Health check deve retornar HTTP 200

Como executar:
    pip install -r requirements.txt
    py -m pytest tests/ -v
"""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# ══════════════════════════════════════════════════════════
# Testes do Endpoint /api/v1/health
# ══════════════════════════════════════════════════════════

def test_health_retorna_200():
    """O health check deve sempre retornar HTTP 200."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_retorna_campos_obrigatorios():
    """A resposta deve conter os campos: status, versao, timestamp."""
    response = client.get("/api/v1/health")
    dados = response.json()

    assert "status" in dados
    assert "versao" in dados
    assert "timestamp" in dados


def test_health_status_valido():
    """O campo status deve ser 'healthy' ou 'degraded'."""
    response = client.get("/api/v1/health")
    dados = response.json()

    assert dados["status"] in ("healthy", "degraded")


# ══════════════════════════════════════════════════════════
# Testes do Endpoint /api/v1/clima/{nome_cidade}
# ══════════════════════════════════════════════════════════

def test_clima_cidade_valida_retorna_200():
    """
    TESTE 1 (obrigatório): Cidade válida deve retornar HTTP 200.
    """
    response = client.get("/api/v1/clima/Fortaleza")

    assert response.status_code == 200


def test_clima_cidade_valida_retorna_estrutura_correta():
    """A resposta deve conter todos os campos obrigatórios."""
    response = client.get("/api/v1/clima/Fortaleza")
    dados = response.json()

    assert "nome" in dados
    assert "estado" in dados
    assert "clima" in dados
    assert "consultado_em" in dados

    clima = dados["clima"]

    assert "temperatura_min" in clima
    assert "temperatura_max" in clima
    assert "condicao" in clima
    assert "unidades" in clima
    assert clima["unidades"]["temperatura"] == "°C"


def test_clima_cidade_valida_estado_correto():
    """Fortaleza deve retornar CE."""
    response = client.get("/api/v1/clima/Fortaleza")
    dados = response.json()

    assert dados["estado"] == "CE"


def test_clima_cidade_inexistente_retorna_404():
    """
    TESTE 2 (obrigatório): Cidade inexistente deve retornar HTTP 404.
    """
    response = client.get("/api/v1/clima/CidadeQueNaoExisteXYZ123")

    assert response.status_code == 404


def test_clima_cidade_inexistente_retorna_codigo_correto():
    """Erro deve retornar CIDADE_NAO_ENCONTRADA."""
    response = client.get("/api/v1/clima/CidadeQueNaoExisteXYZ123")
    dados = response.json()["detail"]

    assert dados["codigo"] == "CIDADE_NAO_ENCONTRADA"
    assert dados["erro"] is True


def test_clima_nome_invalido_retorna_400():
    """Nome com 1 caractere deve retornar HTTP 400."""
    response = client.get("/api/v1/clima/X")

    assert response.status_code == 400


def test_clima_nome_invalido_retorna_codigo_correto():
    """Erro deve retornar NOME_INVALIDO."""
    response = client.get("/api/v1/clima/X")
    dados = response.json()["detail"]

    assert dados["codigo"] == "NOME_INVALIDO"
    assert dados["erro"] is True


# ══════════════════════════════════════════════════════════
# Testes do Endpoint /api/v1/cidades/{sigla_uf}
# ══════════════════════════════════════════════════════════

def test_cidades_uf_valida_retorna_200():
    """Estado CE deve retornar HTTP 200."""
    response = client.get("/api/v1/cidades/CE")

    assert response.status_code == 200


def test_cidades_uf_valida_retorna_estrutura_correta():
    """A resposta deve conter estrutura válida."""
    response = client.get("/api/v1/cidades/CE")
    dados = response.json()

    assert "uf" in dados
    assert "quantidade_retornada" in dados
    assert "cidades" in dados
    assert "consultado_em" in dados
    assert dados["uf"] == "CE"
    assert isinstance(dados["cidades"], list)


def test_cidades_limite_respeitado():
    """O parâmetro limite deve ser respeitado."""
    response = client.get("/api/v1/cidades/CE?limite=5")
    dados = response.json()

    assert dados["quantidade_retornada"] == 5
    assert len(dados["cidades"]) == 5


def test_cidades_uf_invalida_formato_retorna_400():
    """UF com mais de 2 caracteres deve retornar HTTP 400."""
    response = client.get("/api/v1/cidades/ceara")

    assert response.status_code == 400


def test_cidades_uf_invalida_retorna_codigo_correto():
    """Erro deve retornar SIGLA_UF_INVALIDA."""
    response = client.get("/api/v1/cidades/ceara")
    dados = response.json()["detail"]

    assert dados["codigo"] == "SIGLA_UF_INVALIDA"
    assert dados["erro"] is True


def test_cidades_uf_inexistente_retorna_404():
    """UF inexistente deve retornar HTTP 404."""
    response = client.get("/api/v1/cidades/XX")

    assert response.status_code == 404


def test_cidades_uf_inexistente_retorna_codigo_correto():
    """Erro deve retornar UF_NAO_ENCONTRADA."""
    response = client.get("/api/v1/cidades/XX")
    dados = response.json()["detail"]

    assert dados["codigo"] == "UF_NAO_ENCONTRADA"
    assert dados["erro"] is True