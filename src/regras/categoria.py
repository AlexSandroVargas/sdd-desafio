from .politica import Politica, limites_do_centro


def normalizar_categoria(
    categoria: str, centro_custo: str, politica: Politica
) -> str | None:
    normalizada = categoria.lower()
    limites = limites_do_centro(politica, centro_custo)
    return normalizada if normalizada in limites else None
