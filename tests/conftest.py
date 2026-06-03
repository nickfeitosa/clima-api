"""
Configuração dos testes.
O TestClient do FastAPI simula requisições HTTP sem precisar
de um servidor real rodando — ideal para testes automatizados.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="module")
def client():
    """Fixture que fornece o cliente de teste para todos os testes."""
    with TestClient(app) as c:
        yield c