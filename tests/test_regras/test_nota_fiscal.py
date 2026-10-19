from decimal import Decimal

from src.regras.nota_fiscal import nota_fiscal_valida


def test_rn004_cem_reais_nao_exige_nota():
    assert nota_fiscal_valida(100, False)


def test_rn004_acima_de_cem_reais_exige_nota():
    assert not nota_fiscal_valida(100.01, False)


def test_rn004_limiar_aplica_ao_valor_convertido_para_brl():
    # EUR 22,00 * 5,93 = 130,46 BRL > 100 BRL
    assert not nota_fiscal_valida(Decimal("130.46"), False)
    # EUR 10,00 * 5,93 = 59,30 BRL <= 100 BRL
    assert nota_fiscal_valida(Decimal("59.30"), False)
