import re
from datetime import date, datetime, timedelta

from .limites import inferir_diarias


_DATA = r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})"


def _data_descrita(descricao: str, rotulo: str) -> date | None:
    correspondencia = re.search(rf"{rotulo}\s*[:\-]?\s*{_DATA}", descricao, re.IGNORECASE)
    if not correspondencia:
        return None
    valor = correspondencia.group(1)
    return date.fromisoformat(valor) if "-" in valor else datetime.strptime(valor, "%d/%m/%Y").date()


def _eh_transporte_de_viagem(despesa: dict) -> bool:
    return (
        despesa["categoria"].lower() == "transporte_urbano"
        and re.search(r"aeroporto|hotel", despesa["descricao"], re.IGNORECASE) is not None
    )


def _intervalo(inicio: date, fim: date) -> set[date]:
    return {inicio + timedelta(days=indice) for indice in range((fim - inicio).days + 1)}


def dias_em_viagem(despesas: list[dict], periodo: dict) -> set[str]:
    inicio_periodo = date.fromisoformat(periodo["inicio"])
    fim_periodo = date.fromisoformat(periodo["fim"])
    transportes = {
        date.fromisoformat(despesa["data"])
        for despesa in despesas
        if _eh_transporte_de_viagem(despesa)
    }
    dias = set()
    for despesa in despesas:
        if despesa["categoria"].lower() != "hospedagem":
            continue
        descricao = despesa["descricao"]
        checkin = _data_descrita(descricao, r"check[ -]?in") or date.fromisoformat(despesa["data"])
        checkout = _data_descrita(descricao, r"check[ -]?out")
        fim_hospedagem = checkout or checkin + timedelta(days=inferir_diarias(descricao) - 1)
        if fim_hospedagem < checkin:
            continue
        dias.update(_intervalo(checkin, fim_hospedagem))
        if re.search(r"internacional", descricao, re.IGNORECASE):
            vespera = checkin - timedelta(days=1)
            dia_seguinte = fim_hospedagem + timedelta(days=1)
            if vespera in transportes:
                dias.add(vespera)
            if dia_seguinte in transportes:
                dias.add(dia_seguinte)
    return {
        dia.isoformat()
        for dia in dias
        if inicio_periodo <= dia <= fim_periodo
    }


def esta_em_viagem(despesas: list[dict], periodo: dict) -> bool:
    return bool(dias_em_viagem(despesas, periodo))
