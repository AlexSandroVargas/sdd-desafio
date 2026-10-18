from datetime import date


def dentro_do_periodo(data_despesa: str, periodo: dict) -> bool:
    data = date.fromisoformat(data_despesa)
    return date.fromisoformat(periodo["inicio"]) <= data <= date.fromisoformat(periodo["fim"])
