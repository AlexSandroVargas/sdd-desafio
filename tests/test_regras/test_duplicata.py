from src.regras.duplicata import chave_duplicata


def test_rn006_mesma_data_categoria_valor_e_fornecedor_e_duplicata(despesa_base):
    outra = dict(despesa_base, id="d-002", categoria="ALIMENTACAO")
    assert chave_duplicata(despesa_base) == chave_duplicata(outra)
