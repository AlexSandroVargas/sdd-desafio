from decimal import Decimal

from src.regras.limites import aplicar_limites


def despesa(id_, categoria, valor, descricao="Despesa", data="2026-07-03"):
    return {"id": id_, "data": data, "categoria": categoria, "descricao": descricao, "valor": Decimal(str(valor)), "indice": int(id_.split("-")[-1])}


def test_rn001_teto_sequencial_prioriza_maior_valor():
    valores = aplicar_limites([despesa("d-1", "alimentacao", 72.5), despesa("d-2", "alimentacao", 38)], False)
    assert valores == {"d-1": Decimal("60.00"), "d-2": Decimal("0.00")}


def test_rn002_transporte_respeita_limite_diario():
    valores = aplicar_limites([despesa("d-1", "transporte_urbano", 100)], False)
    assert valores["d-1"] == Decimal("80.00")


def test_rn003_hospedagem_infere_diarias():
    valores = aplicar_limites([despesa("d-1", "hospedagem", 480, "Hotel - 2 diarias")], False)
    assert valores["d-1"] == Decimal("480.00")


def test_rn003_hospedagem_sem_quantidade_assume_uma_diaria():
    valores = aplicar_limites([despesa("d-1", "hospedagem", 300)], False)
    assert valores["d-1"] == Decimal("250.00")


def test_rn005_viagem_amplia_limites_em_cinquenta_por_cento():
    valores = aplicar_limites([despesa("d-1", "alimentacao", 72.5), despesa("d-2", "alimentacao", 38)], True)
    assert valores == {"d-1": Decimal("72.50"), "d-2": Decimal("17.50")}
