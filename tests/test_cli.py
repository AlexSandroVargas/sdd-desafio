import json

from src.cli import main


def test_cli_le_entrada_e_grava_saida(tmp_path, entrada_base):
    entrada = tmp_path / "entrada.json"
    saida = tmp_path / "saida.json"
    entrada.write_text(json.dumps(entrada_base), encoding="utf-8")
    assert main(["calcular", "--input", str(entrada), "--output", str(saida)]) == 0
    assert json.loads(saida.read_text(encoding="utf-8"))["despesas"][0]["status"] == "aprovado"


def test_cli_grava_saida_parcial_quando_uma_despesa_e_invalida(tmp_path, entrada_base):
    entrada_base["despesas"].append(dict(entrada_base["despesas"][0], id="d-2", valor=20))
    entrada_base["despesas"][0]["tem_nota_fiscal"] = "sim"
    entrada = tmp_path / "entrada.json"
    saida = tmp_path / "saida.json"
    entrada.write_text(json.dumps(entrada_base), encoding="utf-8")
    assert main(["calcular", "--input", str(entrada), "--output", str(saida)]) == 0
    assert [item["status"] for item in json.loads(saida.read_text(encoding="utf-8"))["despesas"]] == [
        "rejeitado", "aprovado"
    ]


def test_cli_reporta_json_invalido_em_stderr(tmp_path, capsys):
    entrada = tmp_path / "entrada.json"
    entrada.write_text("{", encoding="utf-8")
    assert main(["calcular", "--input", str(entrada), "--output", str(tmp_path / "saida.json")]) != 0
    assert "Erro" in capsys.readouterr().err
