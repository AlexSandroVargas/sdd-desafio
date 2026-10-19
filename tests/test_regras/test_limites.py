from decimal import Decimal

import pytest

from src.regras.limites import aplicar_limites
from src.regras.politica import Politica


@pytest.fixture
def politica():
    return Politica("exemplos/envelope/politica-v4.json")


def despesa(id_, categoria, valor, descricao="Despesa", data="2026-07-03"):
    return {"id": id_, "data": data, "categoria": categoria, "descricao": descricao, "valor": Decimal(str(valor)), "indice": int(id_.split("-")[-1])}


def _valor(resultado, id_):
    return resultado[id_]["valor_reembolsavel"]


def test_rn001_teto_sequencial_prioriza_maior_valor(politica):
    valores = aplicar_limites([despesa("d-1", "alimentacao", 72.5), despesa("d-2", "alimentacao", 38)], set(), "CC-PADRAO", politica)
    assert _valor(valores, "d-1") == Decimal("60.00")
    assert _valor(valores, "d-2") == Decimal("0.00")


def test_rn002_transporte_respeita_limite_diario(politica):
    valores = aplicar_limites([despesa("d-1", "transporte_urbano", 100)], set(), "CC-PADRAO", politica)
    assert _valor(valores, "d-1") == Decimal("80.00")


def test_rn003_hospedagem_infere_diarias(politica):
    valores = aplicar_limites([despesa("d-1", "hospedagem", 480, "Hotel - 2 diarias")], set(), "CC-PADRAO", politica)
    assert _valor(valores, "d-1") == Decimal("480.00")


def test_rn003_hospedagem_sem_quantidade_assume_uma_diaria(politica):
    valores = aplicar_limites([despesa("d-1", "hospedagem", 300)], set(), "CC-PADRAO", politica)
    assert _valor(valores, "d-1") == Decimal("250.00")


def test_rn003_rn005_hospedagem_em_viagem_recebe_limite_ampliado(politica):
    valores = aplicar_limites(
        [despesa("d-1", "hospedagem", 800, "Hotel - 2 diarias")],
        {"2026-07-03", "2026-07-04"},
        "CC-PADRAO",
        politica,
    )
    assert _valor(valores, "d-1") == Decimal("750.00")


def test_rn005_viagem_amplia_limites_em_cinquenta_por_cento(politica):
    valores = aplicar_limites(
        [
            despesa("d-1", "alimentacao", 72.5),
            despesa("d-2", "alimentacao", 38),
            despesa("d-3", "alimentacao", 70, data="2026-07-04"),
        ],
        {"2026-07-03"},
        "CC-PADRAO",
        politica,
    )
    assert _valor(valores, "d-1") == Decimal("72.50")
    assert _valor(valores, "d-2") == Decimal("17.50")
    assert _valor(valores, "d-3") == Decimal("60.00")
