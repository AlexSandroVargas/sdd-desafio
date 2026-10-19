import json
from pathlib import Path


class Politica:
    def __init__(self, caminho: str):
        with Path(caminho).open(encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        self.versao = dados["versao"]
        self.vigencia = dados["vigencia"]
        self.moeda_base = dados["moeda_base"]
        self.padrao = dados["padrao"]
        self.centros_custo = dados["centros_custo"]
        self.nota_fiscal_obrigatoria_acima_de = dados["nota_fiscal_obrigatoria_acima_de"]
        self.acrescimo_em_viagem_percentual = dados["acrescimo_em_viagem_percentual"]


def limites_do_centro(politica: Politica, centro_custo: str) -> dict:
    return politica.centros_custo.get(centro_custo, politica.padrao)
