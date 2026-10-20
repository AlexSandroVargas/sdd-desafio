from src.regras.viagem import dias_em_viagem


def test_rn005_hospedagem_nacional_amplia_apenas_dias_hospedados(despesa_base, periodo):
    despesas = [dict(despesa_base, categoria="hospedagem", descricao="Hotel - 2 diarias")]
    assert dias_em_viagem(despesas, periodo) == {"2026-07-03", "2026-07-04"}


def test_rn005_hospedagem_fora_do_periodo_nao_indica_viagem(despesa_base, periodo):
    despesas = [dict(despesa_base, categoria="hospedagem", data="2026-04-01")]
    assert dias_em_viagem(despesas, periodo) == set()


def test_rn005_checkin_e_checkout_explicitos_definem_hospedagem(despesa_base, periodo):
    despesas = [dict(
        despesa_base,
        categoria="hospedagem",
        descricao="Hotel; check-in 2026-07-10; checkout 2026-07-12",
    )]
    assert dias_em_viagem(despesas, periodo) == {"2026-07-10", "2026-07-11", "2026-07-12"}


def test_rn005_internacional_inclui_vespera_e_dia_seguinte_com_transporte(despesa_base, periodo):
    despesas = [
        dict(despesa_base, id="t-1", data="2026-07-09", categoria="transporte_urbano", descricao="Transporte aeroporto"),
        dict(despesa_base, id="h-1", data="2026-07-10", categoria="hospedagem", descricao="Hotel internacional - 2 diarias"),
        dict(despesa_base, id="t-2", data="2026-07-12", categoria="transporte_urbano", descricao="Transporte hotel aeroporto"),
    ]
    assert dias_em_viagem(despesas, periodo) == {
        "2026-07-09", "2026-07-10", "2026-07-11", "2026-07-12"
    }


def test_rn005_internacional_nao_amplia_dias_externos_sem_transporte(despesa_base, periodo):
    despesas = [dict(
        despesa_base,
        categoria="hospedagem",
        data="2026-07-10",
        descricao="Hotel internacional - 2 diarias",
    )]
    assert dias_em_viagem(despesas, periodo) == {"2026-07-10", "2026-07-11"}


def test_rn005_moeda_estrangeira_considera_dias_das_despesas_em_viagem(despesa_base, periodo):
    despesas = [
        dict(despesa_base, id="a-1", data="2026-07-04", categoria="alimentacao", descricao="Almoco"),
        dict(despesa_base, id="m-1", data="2026-07-05", categoria="transporte_urbano", descricao="Metro", moeda="EUR"),
    ]
    # Apenas os dias das despesas em moeda estrangeira são considerados viagem.
    assert dias_em_viagem(despesas, periodo) == {"2026-07-05"}


def test_rn005_moeda_nacional_segue_verificacao_original(despesa_base, periodo):
    despesas = [dict(despesa_base, id="a-1", data="2026-07-04", categoria="alimentacao", descricao="Almoco")]
    assert dias_em_viagem(despesas, periodo) == set()
