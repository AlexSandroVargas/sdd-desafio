from .arredondamento import decimal


def chave_duplicata(despesa: dict) -> tuple:
    return (
        despesa["data"],
        despesa["categoria"].lower(),
        decimal(despesa["valor"]),
        despesa["fornecedor"],
    )
