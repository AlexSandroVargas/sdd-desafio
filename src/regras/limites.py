import re
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal

from .arredondamento import arredondar, decimal
from .politica import Politica, limites_do_centro


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


def _data_viagem_hospedagem(data_despesa: str, descricao: str) -> str:
    checkin = re.search(
        r"check[ -]?in\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})",
        descricao,
        re.IGNORECASE,
    )
    if checkin:
        return _converter_data(checkin.group(1)).isoformat()
    return data_despesa


def _fator_viagem(politica: Politica, data: str, descricao: str, dias_em_viagem: set[str]) -> Decimal:
    data_viagem = _data_viagem_hospedagem(data, descricao) if descricao else data
    if data_viagem in dias_em_viagem:
        return Decimal("1") + (decimal(politica.acrescimo_em_viagem_percentual) / Decimal("100"))
    return Decimal("1")


def _limite_do_centro(
    politica: Politica, centro_custo: str, categoria: str, data: str, descricao: str, dias_em_viagem: set[str]
) -> Decimal:
    limites = limites_do_centro(politica, centro_custo)
    teto_categoria = limites[categoria]["limite"]
    fator = _fator_viagem(politica, data, descricao, dias_em_viagem)
    if categoria == "hospedagem":
        return decimal(teto_categoria) * fator * inferir_diarias(descricao)
    return decimal(teto_categoria) * fator


def _valor_para_limite(despesa: dict) -> Decimal:
    return decimal(despesa.get("valor_brl", despesa["valor"]))


def aplicar_limites(
    despesas: list[dict],
    dias_em_viagem: set[str],
    centro_custo: str,
    politica: Politica,
) -> dict[str, dict]:
    resultados: dict[str, dict] = {}
    grupos = defaultdict(list)
    for despesa in despesas:
        categoria = despesa["categoria"]
        if categoria == "hospedagem":
            teto = _limite_do_centro(politica, centro_custo, categoria, despesa["data"], despesa["descricao"], dias_em_viagem)
            declarado = _valor_para_limite(despesa)
            if teto == 0:
                resultados[despesa["id"]] = {
                    "valor_reembolsavel": Decimal("0.00"),
                    "valor_nao_reembolsavel": arredondar(declarado),
                    "status": "nao_reembolsavel",
                    "motivo": "Hospedagem não reembolsável para este centro de custo",
                }
            else:
                reembolsavel = arredondar(min(declarado, teto))
                nao_reembolsavel = arredondar(declarado - reembolsavel)
                status = "aprovado" if nao_reembolsavel == 0 else "parcial"
                resultados[despesa["id"]] = {
                    "valor_reembolsavel": reembolsavel,
                    "valor_nao_reembolsavel": nao_reembolsavel,
                    "status": status,
                    "motivo": "Despesa aprovada" if status == "aprovado" else "Limite de hospedagem excedido",
                }
        else:
            grupos[(despesa["data"], categoria)].append(despesa)
    for ((data, categoria), itens) in grupos.items():
        teto = _limite_do_centro(politica, centro_custo, categoria, data, "", dias_em_viagem)
        restante = teto
        for despesa in sorted(itens, key=lambda item: (-_valor_para_limite(item), item["indice"])):
            declarado = _valor_para_limite(despesa)
            if restante == 0:
                resultados[despesa["id"]] = {
                    "valor_reembolsavel": Decimal("0.00"),
                    "valor_nao_reembolsavel": Decimal("0.00"),
                    "status": "rejeitado",
                    "motivo": "Limite diário esgotado",
                }
                continue
            reembolso = min(declarado, restante)
            restante = max(restante - reembolso, Decimal("0"))
            nao_reembolsavel = arredondar(declarado - reembolso)
            status = "aprovado" if nao_reembolsavel == 0 else "parcial"
            resultados[despesa["id"]] = {
                "valor_reembolsavel": arredondar(reembolso),
                "valor_nao_reembolsavel": nao_reembolsavel,
                "status": status,
                "motivo": "Despesa aprovada" if status == "aprovado" else "Limite diário excedido",
            }
    return resultados
