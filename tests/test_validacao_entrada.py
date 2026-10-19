import pytest

from src.motor import ErroEstrutural, processar


def test_contrato_rejeita_campo_raiz_ausente():
    with pytest.raises(ErroEstrutural, match="despesas"):
        processar({"colaborador": {}, "periodo": {}})


def test_contrato_rejeita_apenas_despesa_com_tipo_booleano_invalido(entrada_base):
    entrada_base["despesas"][0]["tem_nota_fiscal"] = "sim"
    item = processar(entrada_base)["despesas"][0]
    assert item["status"] == "rejeitado"
    assert "tem_nota_fiscal" in item["motivo"]


def test_contrato_rejeita_periodo_invertido(entrada_base):
    entrada_base["periodo"]["inicio"] = "2026-08-01"
    with pytest.raises(ErroEstrutural, match="inicio"):
        processar(entrada_base)


def test_contrato_rejeita_apenas_despesa_com_propriedade_nao_prevista(entrada_base):
    entrada_base["despesas"].append(dict(entrada_base["despesas"][0], id="d-2", valor=20))
    entrada_base["despesas"][0]["moeda"] = "BRL"
    itens = processar(entrada_base)["despesas"]
    assert [item["status"] for item in itens] == ["rejeitado", "aprovado"]
    assert "não permitido" in itens[0]["motivo"]
