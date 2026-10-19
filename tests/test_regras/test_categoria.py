import pytest

from src.regras.categoria import normalizar_categoria
from src.regras.politica import Politica


@pytest.fixture
def politica():
    return Politica("exemplos/envelope/politica-v4.json")


def test_rn008_aceita_categoria_sem_diferenciar_caixa(politica):
    assert normalizar_categoria("ALIMENTACAO", "CC-DESCONHECIDO", politica) == "alimentacao"


def test_rn008_rejeita_categoria_fora_da_politica(politica):
    assert normalizar_categoria("coworking", "CC-DESCONHECIDO", politica) is None
