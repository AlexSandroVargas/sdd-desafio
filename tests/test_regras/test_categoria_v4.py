import pytest

from src.regras.categoria import normalizar_categoria
from src.regras.politica import Politica


@pytest.fixture
def politica():
    return Politica("exemplos/envelope/politica-v4.json")


def test_alimentacao_no_cc_comercial(politica):
    assert normalizar_categoria("ALIMENTACAO", "CC-COMERCIAL", politica) == "alimentacao"


def test_representacao_no_cc_comercial(politica):
    assert normalizar_categoria("representacao", "CC-COMERCIAL", politica) == "representacao"


def test_representacao_no_cc_adm_rejeitada(politica):
    assert normalizar_categoria("representacao", "CC-ADM", politica) is None


def test_representacao_em_centro_desconhecido_rejeitada(politica):
    assert normalizar_categoria("representacao", "CC-SUPORTE-N2", politica) is None


def test_categoria_fora_da_politica(politica):
    assert normalizar_categoria("coworking", "CC-COMERCIAL", politica) is None


def test_hospedagem_reconhecida_mesmo_com_limite_zero(politica):
    assert normalizar_categoria("hospedagem", "CC-ENG-PLATAFORMA", politica) == "hospedagem"


def test_hospedagem_ausente_no_cc_adm(politica):
    assert normalizar_categoria("hospedagem", "CC-ADM", politica) is None
