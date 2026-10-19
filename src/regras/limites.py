import re
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal

from .arredondamento import arredondar, decimal
from .config import FATOR_VIAGEM, LIMITES


def _converter_data(valor: str) -> date:
    return date.fromisoformat(valor) if "-" in valor else datetime.strptime(valor, "%d/%m/%Y").date()


def inferir_diarias(descricao: str) -> int:
    datas = re.findall(
        r"check[ -]?(?:in|out)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})",
        descricao,
        re.IGNORECASE,
    )
    if len(datas) == 2:
        return max((_converter_data(datas[1]) - _converter_data(datas[0])).days + 1, 1)
    correspondencia = re.search(r"(\d+)\s*(?:di[aá]rias?|noites?)", descricao, re.IGNORECASE)
    return int(correspondencia.group(1)) if correspondencia else 1


def aplicar_limites(despesas: list[dict], dias_em_viagem: bool | set[str]) -> dict[str, Decimal]:
    def fator(data: str, descricao: str = "") -> Decimal:
        checkin = re.search(
            r"check[ -]?in\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})",
            descricao,
            re.IGNORECASE,
        )
        data_viagem = _converter_data(checkin.group(1)).isoformat() if checkin else data
        em_viagem = dias_em_viagem is True or isinstance(dias_em_viagem, set) and data_viagem in dias_em_viagem
        return FATOR_VIAGEM if em_viagem else Decimal("1")

    reembolsos: dict[str, Decimal] = {}
    grupos = defaultdict(list)
    for despesa in despesas:
        if despesa["categoria"] == "hospedagem":
            teto = LIMITES["hospedagem"] * fator(despesa["data"], despesa["descricao"]) * inferir_diarias(despesa["descricao"])
            reembolsos[despesa["id"]] = arredondar(min(decimal(despesa["valor"]), teto))
        else:
            grupos[(despesa["data"], despesa["categoria"])].append(despesa)
    for ((data, categoria), itens) in grupos.items():
        restante = LIMITES[categoria] * fator(data)
        for despesa in sorted(itens, key=lambda item: (-decimal(item["valor"]), item["indice"])):
            reembolso = min(decimal(despesa["valor"]), restante)
            reembolsos[despesa["id"]] = arredondar(max(reembolso, Decimal("0")))
            restante = max(restante - reembolso, Decimal("0"))
    return reembolsos
