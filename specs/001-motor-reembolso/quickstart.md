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
python -m json.tool exemplos/envelope/despesas-envelope.json
```

A saída deve ser um JSON válido com a estrutura documentada em
[`contracts/input-schema.json`](contracts/input-schema.json). O campo `moeda` é
opcional e, quando ausente, assume-se `BRL`.

---

## Executar o cálculo

```bash
python -m reembolso calcular --input exemplos/envelope/despesas-envelope.json --output resultado.json
```

Ou, com entry-point configurado:

```bash
reembolso calcular --input exemplos/envelope/despesas-envelope.json --output resultado.json
```

A política e o câmbio são carregados por padrão de `exemplos/envelope/politica-v4.json`
e `exemplos/envelope/cambio.json`. Para usar outros arquivos:

```bash
python -m reembolso calcular \
  --input exemplos/envelope/despesas-envelope.json \
  --output resultado.json \
  --politica exemplos/envelope/politica-v4.json \
  --cambio exemplos/envelope/cambio.json
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
python -m pytest
```

Resultado esperado: todos os testes passam. Cada regra de negócio (`RN-001` a
`RN-012`) possui testes correspondentes.

---

## Cenários de validação manual

Use os casos de borda da `spec.md` para conferir o comportamento:

| Cenário | Entrada de teste | Resultado esperado |
|---|---|---|
| Duas refeições no mesmo dia | `e-008` (R$ 95,00) e outra no mesmo dia no `CC-COMERCIAL` | primeira parcial; segunda rejeitada |
| Transporte no limiar da nota | valor BRL R$ 100,00, sem nota | aprovado dentro do limite diário |
| Transporte acima do limiar após conversão | `e-005` (USD 40,00 sem nota, taxa 5,50) | rejeitado |
| Categoria fora da política | `e-009` (`coworking`) | rejeitado |
| Categoria `representacao` válida | `e-001` (`representacao`, R$ 340,00) no `CC-COMERCIAL` | rejeitado por ultrapassar limite de R$ 300,00 |
| Categoria `representacao` em centro sem tabela | `f-003` (`representacao`, `CC-SUPORTE-N2`) | rejeitado |
| Duplicata | duas despesas idênticas | primeira aprovada, segunda rejeitada como duplicata |
| Fora do período | data fora de `inicio`/`fim` | rejeitado |
| Estorno | valor negativo | status `estorno` |
| Hospedagem proibida no centro | `f-002` (`hospedagem`, `CC-ENG-PLATAFORMA`) | status `nao_reembolsavel` |
| Hospedagem com diárias em viagem | `e-007` (3 noites, BRL 1.200,00, `CC-COMERCIAL`) | parcial (limite ampliado de R$ 600,00/dia) |
| Arredondamento | valor com 3 decimais | arredondado para duas casas |
| Caixa diferente | `ALIMENTACAO` | tratado como `alimentacao` |
| Moeda estrangeira sem cotação | `e-006` (GBP 55,00) | rejeitado |

---

## Verificar rastreabilidade

1. Abra `specs/001-motor-reembolso/spec.md` e escolha uma regra (`RN-001` a
   `RN-012`).
2. No código, localize o módulo correspondente em `src/regras/`.
3. Em `tests/`, localize o teste com o mesmo nome da regra.
4. Execute apenas esse teste:

```bash
python -m pytest tests/test_regras/test_limites.py -v
```

---

## Próximos passos

Após validar o quickstart, a implementação segue as tasks em
`specs/001-motor-reembolso/tasks.md`.
