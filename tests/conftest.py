import pytest


@pytest.fixture
def periodo():
    return {"competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31"}


@pytest.fixture
def despesa_base():
    return {
        "id": "d-001",
        "data": "2026-07-03",
        "categoria": "alimentacao",
        "descricao": "Almoco",
        "fornecedor": "Restaurante",
        "valor": 50.0,
        "tem_nota_fiscal": True,
    }


@pytest.fixture
def entrada_base(periodo, despesa_base):
    return {
        "colaborador": {"id": "c-1", "nome": "Ana", "centro_custo": "CC-1"},
        "periodo": periodo,
        "despesas": [despesa_base],
    }
