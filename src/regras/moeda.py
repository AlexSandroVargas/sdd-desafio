from .arredondamento import arredondar, decimal
from .cambio import Cambio, cotacao


def moeda_invalida(despesa: dict, cambio: Cambio) -> bool:
    moeda = despesa.get("moeda", "BRL")
    if moeda == "BRL":
        return False
    return cotacao(cambio, despesa["data"], moeda) is None


def converter_para_brl(despesa: dict, cambio: Cambio) -> decimal:
    moeda = despesa.get("moeda", "BRL")
    if moeda == "BRL":
        return decimal(despesa["valor"])
    taxa = cotacao(cambio, despesa["data"], moeda)
    return arredondar(decimal(despesa["valor"]) * taxa)
