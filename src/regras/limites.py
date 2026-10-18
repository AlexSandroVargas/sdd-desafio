import re
from collections import defaultdict
from decimal import Decimal

from .arredondamento import arredondar, decimal
from .config import FATOR_VIAGEM, LIMITES


def inferir_diarias(descricao: str) -> int:
    correspondencia = re.search(r"(\d+)\s*(?:di[aá]rias?|noites?)", descricao, re.IGNORECASE)
    return int(correspondencia.group(1)) if correspondencia else 1


def aplicar_limites(despesas: list[dict], em_viagem: bool) -> dict[str, Decimal]:
    fator = FATOR_VIAGEM if em_viagem else Decimal("1")
    reembolsos: dict[str, Decimal] = {}
    grupos = defaultdict(list)
    for despesa in despesas:
        if despesa["categoria"] == "hospedagem":
            teto = LIMITES["hospedagem"] * fator * inferir_diarias(despesa["descricao"])
            reembolsos[despesa["id"]] = arredondar(min(decimal(despesa["valor"]), teto))
        else:
            grupos[(despesa["data"], despesa["categoria"])].append(despesa)
    for (_, categoria), itens in grupos.items():
        restante = LIMITES[categoria] * fator
        for despesa in sorted(itens, key=lambda item: (-decimal(item["valor"]), item["indice"])):
            reembolso = min(decimal(despesa["valor"]), restante)
            reembolsos[despesa["id"]] = arredondar(max(reembolso, Decimal("0")))
            restante = max(restante - reembolso, Decimal("0"))
    return reembolsos
