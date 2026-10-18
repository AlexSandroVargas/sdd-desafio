from src.regras.nota_fiscal import nota_fiscal_valida


def test_rn004_cem_reais_nao_exige_nota():
    assert nota_fiscal_valida(100, False)


def test_rn004_acima_de_cem_reais_exige_nota():
    assert not nota_fiscal_valida(100.01, False)
