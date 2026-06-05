<<<<<<< HEAD
# API de Agregação de Dados Climáticos e Geográficos

API REST desenvolvida em Python + FastAPI para a disciplina **Técnicas de Integração de Sistemas (N703)**.

Integra dados geográficos e climáticos de cidades brasileiras consumindo APIs públicas externas.

---

## Tecnologias

| Tecnologia | Versão | Função |
|------------|--------|--------|
| Python | 3.10+ | Linguagem principal |
| FastAPI | 0.111.0 | Framework da API REST |
| Uvicorn | 0.29.0 | Servidor ASGI |
| HTTPX | 0.27.0 | Cliente HTTP assíncrono |
| Pytest | 8.2.0 | Testes automatizados |

**Por que Python + FastAPI?**
FastAPI é o framework Python mais rápido para APIs REST, com validação automática via Pydantic, documentação Swagger integrada e suporte nativo a requisições assíncronas — ideal para agregar múltiplas APIs externas sem bloquear o servidor.

---

## APIs Externas Utilizadas

| API | Uso | URL |
|-----|-----|-----|
| **Nominatim (OpenStreetMap)** | Geocoding: cidade → lat/lon + estado | nominatim.openstreetmap.org |
| **Open-Meteo** | Dados climáticos por lat/lon (gratuita, sem chave) | open-meteo.com |
| **BrasilAPI (IBGE)** | Lista de municípios por estado | brasilapi.com.br |

>  Todas as coordenadas são obtidas **dinamicamente** via Nominatim. Nenhuma coordenada está fixa no código.

---


