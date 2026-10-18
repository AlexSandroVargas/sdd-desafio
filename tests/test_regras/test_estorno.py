from src.regras.estorno import eh_estorno


def test_rn009_valor_negativo_e_estorno():
    assert eh_estorno(-45)
    assert not eh_estorno(0)
