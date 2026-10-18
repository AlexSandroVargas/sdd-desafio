from src.motor import processar


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
