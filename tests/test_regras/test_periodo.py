from src.regras.periodo import dentro_do_periodo


def test_rn007_limites_do_periodo_sao_inclusivos(periodo):
    assert dentro_do_periodo(periodo["inicio"], periodo)
    assert dentro_do_periodo(periodo["fim"], periodo)


def test_rn007_rejeita_data_fora_do_periodo(periodo):
    assert not dentro_do_periodo("2026-04-15", periodo)
