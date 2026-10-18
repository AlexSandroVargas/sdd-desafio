from decimal import Decimal

from src.regras.arredondamento import arredondar


def test_rn010_arredonda_half_up_para_duas_casas():
    assert arredondar("33.335") == Decimal("33.34")
    assert arredondar("33.333") == Decimal("33.33")
