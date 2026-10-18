from .arredondamento import decimal


def eh_estorno(valor) -> bool:
    return decimal(valor) < 0
