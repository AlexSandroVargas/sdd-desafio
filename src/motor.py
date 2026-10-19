from datetime import date
from decimal import Decimal

from .regras.arredondamento import arredondar, decimal
from .regras.cambio import Cambio
from .regras.categoria import normalizar_categoria
from .regras.config import Configuracao
from .regras.duplicata import chave_duplicata
from .regras.estorno import eh_estorno
from .regras.limites import aplicar_limites
from .regras.moeda import converter_para_brl, moeda_invalida
from .regras.nota_fiscal import nota_fiscal_valida
from .regras.periodo import dentro_do_periodo
from .regras.politica import Politica
from .regras.viagem import dias_em_viagem


class ErroEstrutural(ValueError):
    pass


MOEDA_PADRAO = "BRL"


def _exigir_campos(objeto: dict, campos: tuple[str, ...], contexto: str) -> None:
    if not isinstance(objeto, dict):
        raise ErroEstrutural(f"{contexto} deve ser um objeto")
    ausentes = [campo for campo in campos if campo not in objeto]
    if ausentes:
        raise ErroEstrutural(f"Campo obrigatório ausente em {contexto}: {', '.join(ausentes)}")
    extras = [campo for campo in objeto if campo not in campos]
    if extras:
        raise ErroEstrutural(f"Campo não permitido em {contexto}: {', '.join(extras)}")


def validar_entrada(entrada: dict) -> None:
    _exigir_campos(entrada, ("colaborador", "periodo", "despesas"), "entrada")
    _exigir_campos(entrada["colaborador"], ("id", "nome", "centro_custo"), "colaborador")
    _exigir_campos(entrada["periodo"], ("competencia", "inicio", "fim"), "periodo")
    if not all(isinstance(valor, str) for valor in entrada["colaborador"].values()):
        raise ErroEstrutural("Campos de colaborador devem ser textuais")
    if not all(isinstance(entrada["periodo"][campo], str) for campo in ("competencia", "inicio", "fim")):
        raise ErroEstrutural("Campos de periodo devem ser textuais")
    if not isinstance(entrada["despesas"], list):
        raise ErroEstrutural("despesas deve ser uma lista")
    try:
        inicio = date.fromisoformat(entrada["periodo"]["inicio"])
        fim = date.fromisoformat(entrada["periodo"]["fim"])
        if inicio > fim:
            raise ErroEstrutural("periodo.inicio deve ser anterior ou igual a periodo.fim")
        if entrada["periodo"]["competencia"] != inicio.strftime("%Y-%m") or inicio.strftime("%Y-%m") != fim.strftime("%Y-%m"):
            raise ErroEstrutural("periodo.competencia deve corresponder a inicio e fim")
    except (TypeError, ValueError) as erro:
        raise ErroEstrutural(f"Data de período inválida: {erro}") from erro


def _erro_estrutural_despesa(despesa: object, indice: int, ids: set[str]) -> str | None:
    contexto = f"despesas[{indice}]"
    campos = ("id", "data", "categoria", "descricao", "fornecedor", "valor", "tem_nota_fiscal")
    campos_opcionais = ("moeda",)
    campos_permitidos = campos + campos_opcionais
    if not isinstance(despesa, dict):
        return f"{contexto} deve ser um objeto"
    ausentes = [campo for campo in campos if campo not in despesa]
    if ausentes:
        return f"Campo obrigatório ausente em {contexto}: {', '.join(ausentes)}"
    extras = [campo for campo in despesa if campo not in campos_permitidos]
    if extras:
        return f"Campo não permitido em {contexto}: {', '.join(extras)}"
    if not all(isinstance(despesa[campo], str) for campo in ("id", "data", "categoria", "descricao", "fornecedor")):
        return f"{contexto} contém campo textual inválido"
    if despesa["id"] in ids:
        return f"{contexto}.id deve ser único"
    try:
        date.fromisoformat(despesa["data"])
        decimal(despesa["valor"])
    except (TypeError, ValueError):
        return f"{contexto} contém data ou valor inválido"
    if not isinstance(despesa["tem_nota_fiscal"], bool):
        return f"{contexto}.tem_nota_fiscal deve ser booleano"
    if "moeda" in despesa and not isinstance(despesa["moeda"], str):
        return f"{contexto}.moeda deve ser textual"
    ids.add(despesa["id"])
    return None


def _rejeitado_estrutural(despesa: object, indice: int, motivo: str) -> dict:
    item = despesa if isinstance(despesa, dict) else {}
    try:
        valor = float(decimal(item.get("valor", 0)))
    except (TypeError, ValueError):
        valor = 0.0
    return {
        "id": item.get("id") if isinstance(item.get("id"), str) else f"despesa-{indice}",
        "data": item.get("data") if isinstance(item.get("data"), str) else "",
        "categoria": item.get("categoria", "").lower() if isinstance(item.get("categoria"), str) else "",
        "valor_declarado": valor, "valor_reembolsavel": 0.0,
        "valor_nao_reembolsavel": 0.0, "status": "rejeitado",
        "motivo": f"Erro estrutural: {motivo}",
    }


def _rejeitado(despesa: dict, categoria: str, motivo: str, moeda: str = MOEDA_PADRAO) -> dict:
    return {
        "id": despesa["id"], "data": despesa["data"], "categoria": categoria,
        "valor_declarado": despesa["valor"], "moeda": moeda,
        "valor_reembolsavel": 0.0,
        "valor_nao_reembolsavel": 0.0, "status": "rejeitado", "motivo": motivo,
    }


def _nao_reembolsavel(despesa: dict, categoria: str, motivo: str, moeda: str = MOEDA_PADRAO) -> dict:
    return {
        "id": despesa["id"], "data": despesa["data"], "categoria": categoria,
        "valor_declarado": despesa["valor"], "moeda": moeda,
        "valor_reembolsavel": 0.0,
        "valor_nao_reembolsavel": float(arredondar(decimal(despesa["valor"]))),
        "status": "nao_reembolsavel", "motivo": motivo,
    }


def processar(entrada: dict, politica: Politica | None = None, cambio: Cambio | None = None) -> dict:
    validar_entrada(entrada)
    periodo = entrada["periodo"]
    centro_custo = entrada["colaborador"]["centro_custo"]
    if politica is None or cambio is None:
        configuracao = Configuracao()
        if politica is None:
            politica = configuracao.politica
        if cambio is None:
            cambio = Cambio(str(configuracao._caminho_cambio))
    resultados: dict[int, dict] = {}
    elegiveis = []
    vistos = set()
    ids = set()
    duplicatas = []
    estornos = Decimal("0")
    for indice, original in enumerate(entrada["despesas"]):
        erro = _erro_estrutural_despesa(original, indice, ids)
        if erro:
            resultados[indice] = _rejeitado_estrutural(original, indice, erro)
            continue
        moeda = original.get("moeda", MOEDA_PADRAO)
        categoria = original["categoria"].lower()
        normalizada = normalizar_categoria(original["categoria"], centro_custo, politica)
        if normalizada is None:
            resultados[indice] = _rejeitado(original, categoria, "Categoria fora da política", moeda)
            continue
        if not dentro_do_periodo(original["data"], periodo):
            resultados[indice] = _rejeitado(original, normalizada, "Fora do período de competência", moeda)
            continue
        if moeda_invalida(original, cambio):
            resultados[indice] = _rejeitado(original, normalizada, "Moeda ou data sem cotação disponível", moeda)
            continue
        valor_brl = converter_para_brl(original, cambio)
        if not nota_fiscal_valida(valor_brl, original["tem_nota_fiscal"]):
            resultados[indice] = _rejeitado(original, normalizada, "Nota fiscal obrigatória acima de R$ 100,00 ausente", moeda)
            continue
        despesa = dict(original, categoria=normalizada, indice=indice, valor_brl=valor_brl, moeda=moeda)
        chave = chave_duplicata(despesa)
        if chave in vistos:
            resultados[indice] = _rejeitado(original, normalizada, "Despesa duplicada", moeda)
            duplicatas.append(original["id"])
            continue
        vistos.add(chave)
        if eh_estorno(original["valor"]):
            estornos += abs(decimal(original["valor"]))
            resultados[indice] = {
                "id": original["id"], "data": original["data"], "categoria": normalizada,
                "valor_declarado": original["valor"], "moeda": moeda,
                "valor_reembolsavel": 0.0,
                "valor_nao_reembolsavel": 0.0, "status": "estorno",
                "motivo": "Estorno reduz o total reembolsável do período",
            }
            continue
        elegiveis.append(despesa)
    calculados = aplicar_limites(elegiveis, dias_em_viagem(elegiveis, periodo), centro_custo, politica)
    for despesa in elegiveis:
        calculado = calculados[despesa["id"]]
        resultados[despesa["indice"]] = {
            "id": despesa["id"], "data": despesa["data"], "categoria": despesa["categoria"],
            "valor_declarado": despesa["valor"], "moeda": despesa["moeda"],
            "valor_reembolsavel": float(calculado["valor_reembolsavel"]),
            "valor_nao_reembolsavel": float(calculado["valor_nao_reembolsavel"]),
            "status": calculado["status"], "motivo": calculado["motivo"],
        }
    despesas = [resultados[indice] for indice in range(len(entrada["despesas"]))]
    total_reembolsavel = sum((decimal(item["valor_reembolsavel"]) for item in despesas), Decimal("0")) - estornos
    resumo = {
        "total_declarado": float(arredondar(sum((decimal(item["valor_declarado"]) for item in despesas), Decimal("0")))),
        "total_reembolsavel": float(arredondar(total_reembolsavel)),
        "total_nao_reembolsavel": float(arredondar(sum((decimal(item["valor_nao_reembolsavel"]) for item in despesas), Decimal("0")))),
        "total_rejeitado": float(arredondar(sum((decimal(item["valor_declarado"]) for item in despesas if item["status"] == "rejeitado"), Decimal("0")))),
        "quantidade_despesas": len(despesas),
    }
    alertas = [{"tipo": "duplicata", "despesas": duplicatas}] if duplicatas else []
    return {"colaborador": entrada["colaborador"], "periodo": periodo, "resumo": resumo, "despesas": despesas, "alertas": alertas}
