import pytest

from src.regras.politica import Politica, limites_do_centro


@pytest.fixture
def politica():
    return Politica("exemplos/envelope/politica-v4.json")


def test_versao(politica):
    assert politica.versao == "v4"


def test_moeda_base(politica):
    assert politica.moeda_base == "BRL"


def test_limite_alimentacao_cc_comercial(politica):
    assert limites_do_centro(politica, "CC-COMERCIAL")["alimentacao"]["limite"] == 90.00


def test_representacao_somente_no_cc_comercial(politica):
    assert "representacao" in limites_do_centro(politica, "CC-COMERCIAL")
    assert "representacao" not in limites_do_centro(politica, "CC-ADM")


def test_hospedagem_zero_na_eng_plataforma(politica):
    limites = limites_do_centro(politica, "CC-ENG-PLATAFORMA")
    assert limites["hospedagem"]["limite"] == 0.00


def test_centro_desconhecido_usa_padrao(politica):
    assert limites_do_centro(politica, "CC-SUPORTE-N2") == politica.padrao


def test_categoria_ausente_no_centro_nao_aparece(politica):
    limites = limites_do_centro(politica, "CC-ADM")
    assert "hospedagem" not in limites
    assert "representacao" not in limites
