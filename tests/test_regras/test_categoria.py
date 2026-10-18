from src.regras.categoria import normalizar_categoria


def test_rn008_aceita_categoria_sem_diferenciar_caixa():
    assert normalizar_categoria("ALIMENTACAO") == "alimentacao"


def test_rn008_rejeita_categoria_fora_da_politica():
    assert normalizar_categoria("coworking") is None
