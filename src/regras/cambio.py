import json
from decimal import Decimal
from pathlib import Path


class Cambio:
    def __init__(self, caminho: str):
        with Path(caminho).open(encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        self.moeda_base = dados["moeda_base"]
        self.fonte = dados.get("fonte", "")
        self.observacao = dados.get("observacao", "")
        self.taxas = dados["taxas"]


def _as_decimal(valor) -> Decimal | None:
    if valor is None:
        return None
    return Decimal(str(valor))


def cotacao(cambio: Cambio, data: str, moeda: str) -> Decimal | None:
    if moeda == cambio.moeda_base:
        return Decimal("1.00")
    taxas_do_dia = cambio.taxas.get(data)
    if taxas_do_dia is None:
        return None
    return _as_decimal(taxas_do_dia.get(moeda))
