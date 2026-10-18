from decimal import Decimal

LIMITES = {
    "alimentacao": Decimal("60.00"),
    "transporte_urbano": Decimal("80.00"),
    "hospedagem": Decimal("250.00"),
}
FATOR_VIAGEM = Decimal("1.50")
LIMIAR_NOTA_FISCAL = Decimal("100.00")
