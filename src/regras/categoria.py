CATEGORIAS_REEMBOLSAVEIS = {"alimentacao", "transporte_urbano", "hospedagem"}


def normalizar_categoria(categoria: str) -> str | None:
    normalizada = categoria.lower()
    return normalizada if normalizada in CATEGORIAS_REEMBOLSAVEIS else None
