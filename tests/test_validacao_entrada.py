import pytest

from src.motor import ErroEstrutural, processar


def test_contrato_rejeita_campo_raiz_ausente():
    with pytest.raises(ErroEstrutural, match="despesas"):
        processar({"colaborador": {}, "periodo": {}})


def test_contrato_rejeita_tipo_booleano_invalido(entrada_base):
    entrada_base["despesas"][0]["tem_nota_fiscal"] = "sim"
    with pytest.raises(ErroEstrutural, match="tem_nota_fiscal"):
        processar(entrada_base)


def test_contrato_rejeita_periodo_invertido(entrada_base):
    entrada_base["periodo"]["inicio"] = "2026-08-01"
    with pytest.raises(ErroEstrutural, match="inicio"):
        processar(entrada_base)


def test_contrato_rejeita_propriedade_nao_prevista(entrada_base):
    entrada_base["despesas"][0]["moeda"] = "BRL"
    with pytest.raises(ErroEstrutural, match="não permitido"):
        processar(entrada_base)
