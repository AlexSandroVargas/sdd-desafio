import json

from src.cli import main


def test_cli_le_entrada_e_grava_saida(tmp_path, entrada_base):
    entrada = tmp_path / "entrada.json"
    saida = tmp_path / "saida.json"
    entrada.write_text(json.dumps(entrada_base), encoding="utf-8")
    assert main(["calcular", "--input", str(entrada), "--output", str(saida)]) == 0
    assert json.loads(saida.read_text(encoding="utf-8"))["despesas"][0]["status"] == "aprovado"


def test_cli_reporta_json_invalido_em_stderr(tmp_path, capsys):
    entrada = tmp_path / "entrada.json"
    entrada.write_text("{", encoding="utf-8")
    assert main(["calcular", "--input", str(entrada), "--output", str(tmp_path / "saida.json")]) != 0
    assert "Erro" in capsys.readouterr().err
