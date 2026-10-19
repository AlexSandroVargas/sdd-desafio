from decimal import Decimal

import pytest

from src.regras.cambio import Cambio
from src.regras.moeda import converter_para_brl, moeda_invalida


@pytest.fixture
def cambio():
    return Cambio("exemplos/envelope/cambio.json")


def test_converte_eur_para_brl(cambio):
    despesa = {"valor": 22.00, "moeda": "EUR", "data": "2026-07-14"}
    assert converter_para_brl(despesa, cambio) == Decimal("130.46")


def test_moeda_brl_nao_altera_valor(cambio):
    despesa = {"valor": 50.00, "data": "2026-07-13"}
    assert converter_para_brl(despesa, cambio) == Decimal("50.00")


def test_moeda_explicitamente_brl(cambio):
    despesa = {"valor": 50.00, "moeda": "BRL", "data": "2026-07-13"}
    assert converter_para_brl(despesa, cambio) == Decimal("50.00")


def test_moeda_sem_cotacao_rejeitada(cambio):
    despesa = {"valor": 55.00, "moeda": "GBP", "data": "2026-07-13"}
    assert moeda_invalida(despesa, cambio) is True


def test_moeda_com_cotacao_valida(cambio):
    despesa = {"valor": 22.00, "moeda": "EUR", "data": "2026-07-14"}
    assert moeda_invalida(despesa, cambio) is False


def test_data_sem_cotacao_rejeitada(cambio):
    despesa = {"valor": 10.00, "moeda": "USD", "data": "2026-07-19"}
    assert moeda_invalida(despesa, cambio) is True
