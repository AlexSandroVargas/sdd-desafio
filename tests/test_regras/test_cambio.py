from decimal import Decimal

import pytest

from src.regras.cambio import Cambio, cotacao


@pytest.fixture
def cambio():
    return Cambio("exemplos/envelope/cambio.json")


def test_moeda_base(cambio):
    assert cambio.moeda_base == "BRL"


def test_cotacao_usd(cambio):
    assert cotacao(cambio, "2026-07-13", "USD") == Decimal("5.42")


def test_cotacao_eur(cambio):
    assert cotacao(cambio, "2026-07-14", "EUR") == Decimal("5.93")


def test_cotacao_brl_padrao(cambio):
    assert cotacao(cambio, "2026-07-13", "BRL") == Decimal("1.00")


def test_cotacao_data_inexistente(cambio):
    assert cotacao(cambio, "2026-07-19", "USD") is None


def test_cotacao_moeda_inexistente(cambio):
    assert cotacao(cambio, "2026-07-13", "GBP") is None
