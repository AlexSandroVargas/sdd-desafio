from .arredondamento import decimal
from .config import LIMIAR_NOTA_FISCAL


def nota_fiscal_valida(valor, tem_nota_fiscal: bool) -> bool:
    return decimal(valor) <= LIMIAR_NOTA_FISCAL or tem_nota_fiscal
