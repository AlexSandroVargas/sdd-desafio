import json
from pathlib import Path

from src.motor import processar


def _carregar(caminho: str) -> dict:
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def test_pipeline_processa_todas_as_despesas_e_totais(entrada_base):
    entrada_base["despesas"].extend([
        dict(entrada_base["despesas"][0], id="d-2", valor=20.0),
        dict(entrada_base["despesas"][0], id="d-3", valor=-10.0, categoria="transporte_urbano"),
    ])
    resultado = processar(entrada_base)
    assert [item["status"] for item in resultado["despesas"]] == ["aprovado", "parcial", "estorno"]
    assert resultado["resumo"] == {
        "total_declarado": 60.0,
        "total_reembolsavel": 50.0,
        "total_nao_reembolsavel": 10.0,
        "total_rejeitado": 0.0,
        "quantidade_despesas": 3,
    }


def test_pipeline_gera_alerta_e_rejeita_duplicata(entrada_base):
    entrada_base["despesas"].append(dict(entrada_base["despesas"][0], id="d-2"))
    resultado = processar(entrada_base)
    assert resultado["despesas"][1]["status"] == "rejeitado"
    assert resultado["alertas"] == [{"tipo": "duplicata", "despesas": ["d-2"]}]


def test_pipeline_preserva_valor_declarado_com_tres_decimais(entrada_base):
    entrada_base["despesas"][0]["valor"] = 33.333
    item = processar(entrada_base)["despesas"][0]
    assert item["valor_declarado"] == 33.333
    assert item["valor_reembolsavel"] == 33.33
    assert item["status"] == "aprovado"


def test_pipeline_amplia_hospedagem_pelo_checkin_quando_data_da_despesa_difere(entrada_base):
    base = entrada_base["despesas"][0]
    entrada_base["despesas"] = [dict(
        base,
        id="h-1",
        categoria="hospedagem",
        descricao="Hotel; check-in 2026-07-10; checkout 2026-07-11",
        valor=800,
    )]
    item = processar(entrada_base)["despesas"][0]
    assert item["valor_reembolsavel"] == 750.0
    assert item["status"] == "parcial"


def test_pipeline_amplia_limite_somente_nos_dias_de_hospedagem(entrada_base):
    base = entrada_base["despesas"][0]
    entrada_base["despesas"] = [
        dict(base, id="h-1", categoria="hospedagem", descricao="Hotel - 2 diarias", valor=90),
        dict(base, id="a-1", data="2026-07-04", valor=70),
        dict(base, id="a-2", data="2026-07-05", valor=70),
    ]
    resultado = processar(entrada_base)
    assert [item["valor_reembolsavel"] for item in resultado["despesas"]] == [90.0, 70.0, 60.0]


def test_pipeline_exemplo_envelope_cc_comercial():
    entrada = _carregar("exemplos/envelope/despesas-envelope.json")
    resultado = processar(entrada)
    status_por_id = {item["id"]: item["status"] for item in resultado["despesas"]}
    # e-001: representacao BRL 340 > limite 300 -> parcial
    assert status_por_id["e-001"] == "parcial"
    # e-002: EUR 22 * 5,93 = 130,46 BRL; tem nota; alimentacao 90*1,5 = 135 -> aprovado
    assert status_por_id["e-002"] == "aprovado"
    # e-003: EUR 14,50 * 5,88 = 85,26 BRL <= 90*1,5 = 135, sem nota ok -> aprovado
    assert status_por_id["e-003"] == "aprovado"
    assert status_por_id["e-006"] == "rejeitado" # GBP sem cotacao
    # e-007: 3 noites * limite 400*1,5 = 1800; 1200 <= 1800 -> aprovado
    assert status_por_id["e-007"] == "aprovado"
    assert status_por_id["e-009"] == "rejeitado"  # coworking


def test_pipeline_exemplo_envelope_centro_desconhecido():
    entrada = _carregar("exemplos/envelope/despesas-envelope-cc-desconhecido.json")
    resultado = processar(entrada)
    status_por_id = {item["id"]: item["status"] for item in resultado["despesas"]}
    assert status_por_id["f-001"] == "aprovado"   # alimentacao 58 <= 60
    # f-002: hospedagem em dia de viagem -> limite 250*1,5 = 375; 310 <= 375 -> aprovado
    assert status_por_id["f-002"] == "aprovado"
    assert status_por_id["f-003"] == "rejeitado"  # representacao nao esta no padrao
    assert status_por_id["f-004"] == "aprovado"   # USD 12 * 5,48 = 65,76 BRL <= 100 e dentro do limite
