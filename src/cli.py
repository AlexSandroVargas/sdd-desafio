import argparse
import json
import sys
from pathlib import Path

from .motor import ErroEstrutural, processar
from .regras.cambio import Cambio
from .regras.politica import Politica


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reembolso")
    subcomandos = parser.add_subparsers(dest="comando", required=True)
    calcular = subcomandos.add_parser("calcular")
    calcular.add_argument("--input", "-i", required=True)
    calcular.add_argument("--output", "-o", required=True)
    calcular.add_argument("--politica", "-p", default="exemplos/envelope/politica-v4.json")
    calcular.add_argument("--cambio", "-c", default="exemplos/envelope/cambio.json")
    return parser


def main(argumentos=None) -> int:
    args = criar_parser().parse_args(argumentos)
    try:
        entrada = json.loads(Path(args.input).read_text(encoding="utf-8"))
        politica = Politica(args.politica)
        cambio = Cambio(args.cambio)
        resultado = processar(entrada, politica=politica, cambio=cambio)
        Path(args.output).write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0
    except (OSError, json.JSONDecodeError, ErroEstrutural) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
