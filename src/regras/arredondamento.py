from decimal import Decimal, ROUND_HALF_UP


def decimal(valor) -> Decimal:
    return Decimal(str(valor))


def arredondar(valor) -> Decimal:
    return decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
