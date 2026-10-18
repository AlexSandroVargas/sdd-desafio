# Quickstart — Motor de Cálculo de Reembolso

Guia de validação do feature `001-motor-reembolso`. Siga os passos para verificar
que a CLI processa `exemplos/despesas-exemplo.json` e produz uma saída coerente
com a spec.

---

## Pré-requisitos

- Python 3.11 ou superior instalado.
- `pip` disponível.
- Cópia local do repositório.

---

## Instalação

No diretório raiz do repositório:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements-dev.txt
```

O arquivo `requirements-dev.txt` contém apenas `pytest` e dependências de teste;
o runtime utiliza a biblioteca padrão do Python.

---

## Validar o schema de entrada

```bash
python -m json.tool exemplos/despesas-exemplo.json
```

A saída deve ser um JSON válido com a estrutura documentada em
[`contracts/input-schema.json`](contracts/input-schema.json).

---

## Executar o cálculo

```bash
python -m reembolso calcular --input exemplos/despesas-exemplo.json --output resultado.json
```

Ou, com entry-point configurado:

```bash
reembolso calcular --input exemplos/despesas-exemplo.json --output resultado.json
```

---

## Verificar a saída

```bash
python -m json.tool resultado.json
```

A saída deve conter:

- `colaborador` e `periodo` iguais aos da entrada.
- `resumo` com totais calculados conforme `data-model.md`.
- `despesas` com `status` e `motivo` para cada item.
- `alertas` listando duplicatas detectadas.

O schema completo está em [`contracts/output-schema.json`](contracts/output-schema.json).

---

## Executar os testes

```bash
pytest
```

Resultado esperado: todos os testes passam. Cada regra de negócio (`RN-001` a
`RN-010`) possui testes correspondentes.

---

## Cenários de validação manual

Use os casos de borda da `spec.md` para conferir o comportamento:

| Cenário | Entrada de teste | Resultado esperado |
|---|---|---|
| Duas refeições no mesmo dia | `d-001` e `d-002` | `d-001` parcial (R$ 60,00); `d-002` rejeitado |
| Transporte no limiar da nota | `d-003` (R$ 100,00, sem nota) | aprovado dentro do limite diário |
| Transporte acima do limiar da nota | `d-004` (R$ 100,01, sem nota) | rejeitado |
| Categoria fora da política | `d-005` (`coworking`) | rejeitado |
| Duplicata | `d-006` e `d-007` | primeira aprovada, segunda rejeitada como duplicata |
| Fora do período | `d-008` (`2026-04-15`) | rejeitado |
| Estorno | `d-009` (R$ -45,00) | status `estorno` |
| Hospedagem com diárias | `d-010` (2 diárias, R$ 480,00) | aprovado |
| Arredondamento | `d-011` (R$ 33,333) | valor reembolsável R$ 33,33 |
| Caixa diferente | `d-014` (`ALIMENTACAO`) | tratado como `alimentacao` |

---

## Verificar rastreabilidade

1. Abra `specs/001-motor-reembolso/spec.md` e escolha uma regra (`RN-001` a
   `RN-010`).
2. No código, localize o módulo correspondente em `src/regras/`.
3. Em `tests/`, localize o teste com o mesmo nome da regra.
4. Execute apenas esse teste:

```bash
pytest tests/test_regras/test_limites.py -v
```

---

## Próximos passos

Após validar o quickstart, a implementação segue as tasks em
`specs/001-motor-reembolso/tasks.md`.
