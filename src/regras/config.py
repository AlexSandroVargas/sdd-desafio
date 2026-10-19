from decimal import Decimal
from pathlib import Path

from .politica import Politica

FATOR_VIAGEM = Decimal("1.50")
LIMIAR_NOTA_FISCAL = Decimal("100.00")

CAMINHO_POLITICA_PADRAO = Path("exemplos/envelope/politica-v4.json")
CAMINHO_CAMBIO_PADRAO = Path("exemplos/envelope/cambio.json")


class Configuracao:
    def __init__(self, caminho_politica: str | Path | None = None, caminho_cambio: str | Path | None = None):
        self._caminho_politica = Path(caminho_politica) if caminho_politica else CAMINHO_POLITICA_PADRAO
        self._caminho_cambio = Path(caminho_cambio) if caminho_cambio else CAMINHO_CAMBIO_PADRAO
        self._politica: Politica | None = None

    @property
    def politica(self) -> Politica:
        if self._politica is None:
            self._politica = Politica(self._caminho_politica)
        return self._politica


# Backwards-compatible constant for code that imported LIMITES before v4.
# New code should use Configuracao().politica instead.
LIMITES = {
    "alimentacao": Decimal("60.00"),
    "transporte_urbano": Decimal("80.00"),
    "hospedagem": Decimal("250.00"),
}
