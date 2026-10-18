import argparse
import json
import sys
from pathlib import Path

from .motor import ErroEstrutural, processar


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reembolso")
    subcomandos = parser.add_subparsers(dest="comando", required=True)
    calcular = subcomandos.add_parser("calcular")
    calcular.add_argument("--input", "-i", required=True)
    calcular.add_argument("--output", "-o", required=True)
    return parser


def main(argumentos=None) -> int:
    args = criar_parser().parse_args(argumentos)
    try:
        entrada = json.loads(Path(args.input).read_text(encoding="utf-8"))
        resultado = processar(entrada)
        Path(args.output).write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0
    except (OSError, json.JSONDecodeError, ErroEstrutural) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
