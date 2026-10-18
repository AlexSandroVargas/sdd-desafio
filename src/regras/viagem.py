from .periodo import dentro_do_periodo


def esta_em_viagem(despesas: list[dict], periodo: dict) -> bool:
    return any(
        despesa["categoria"].lower() == "hospedagem"
        and dentro_do_periodo(despesa["data"], periodo)
        for despesa in despesas
    )
