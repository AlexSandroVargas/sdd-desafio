from decimal import Decimal

import pytest

from src.regras.limites import aplicar_limites
from src.regras.politica import Politica
from src.regras.viagem import dias_em_viagem


@pytest.fixture
def politica():
    return Politica("exemplos/envelope/politica-v4.json")


def test_alimentacao_no_cc_comercial(politica):
    despesas = [
        {"id": "e-008", "data": "2026-07-23", "categoria": "alimentacao", "descricao": "Almoco", "fornecedor": "Tavola", "valor": 95.00, "tem_nota_fiscal": True, "indice": 0},
    ]
    resultado = aplicar_limites(despesas, set(), "CC-COMERCIAL", politica)
    assert resultado["e-008"]["valor_reembolsavel"] == Decimal("90.00")
    assert resultado["e-008"]["valor_nao_reembolsavel"] == Decimal("5.00")
    assert resultado["e-008"]["status"] == "parcial"


def test_representacao_no_cc_comercial(politica):
    despesas = [
        {"id": "e-001", "data": "2026-07-13", "categoria": "representacao", "descricao": "Jantar", "fornecedor": "Casa Trindade", "valor": 340.00, "tem_nota_fiscal": True, "indice": 0},
    ]
    resultado = aplicar_limites(despesas, set(), "CC-COMERCIAL", politica)
    assert resultado["e-001"]["valor_reembolsavel"] == Decimal("300.00")
    assert resultado["e-001"]["valor_nao_reembolsavel"] == Decimal("40.00")
    assert resultado["e-001"]["status"] == "parcial"


def test_hospedagem_zero_na_eng_plataforma(politica):
    despesas = [
        {"id": "f-002", "data": "2026-07-17", "categoria": "hospedagem", "descricao": "Pousada - 1 diaria", "fornecedor": "Pousada do Vale", "valor": 310.00, "tem_nota_fiscal": True, "indice": 0},
    ]
    resultado = aplicar_limites(despesas, set(), "CC-ENG-PLATAFORMA", politica)
    assert resultado["f-002"]["valor_reembolsavel"] == Decimal("0.00")
    assert resultado["f-002"]["valor_nao_reembolsavel"] == Decimal("310.00")
    assert resultado["f-002"]["status"] == "nao_reembolsavel"


def test_limite_ampliado_em_viagem(politica):
    despesas = [
        {"id": "h-001", "data": "2026-07-20", "categoria": "alimentacao", "descricao": "Almoco", "fornecedor": "X", "valor": 130.00, "tem_nota_fiscal": True, "indice": 0},
        {"id": "h-002", "data": "2026-07-20", "categoria": "hospedagem", "descricao": "Hotel - internacional - check-in 2026-07-18 - 3 noites", "fornecedor": "Y", "valor": 1200.00, "tem_nota_fiscal": True, "indice": 1},
    ]
    dias = dias_em_viagem(despesas, {"inicio": "2026-07-01", "fim": "2026-07-31"})
    resultado = aplicar_limites(despesas, dias, "CC-COMERCIAL", politica)
    assert resultado["h-001"]["valor_reembolsavel"] == Decimal("130.00")
    assert resultado["h-001"]["status"] == "aprovado"
