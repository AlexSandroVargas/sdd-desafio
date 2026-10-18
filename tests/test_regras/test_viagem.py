from src.regras.viagem import esta_em_viagem


def test_rn005_hospedagem_dentro_do_periodo_indica_viagem(despesa_base, periodo):
    despesas = [dict(despesa_base, categoria="hospedagem")]
    assert esta_em_viagem(despesas, periodo)


def test_rn005_hospedagem_fora_do_periodo_nao_indica_viagem(despesa_base, periodo):
    despesas = [dict(despesa_base, categoria="hospedagem", data="2026-04-01")]
    assert not esta_em_viagem(despesas, periodo)
