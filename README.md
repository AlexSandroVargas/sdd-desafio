# Motor de Cálculo de Reembolso

Este projeto implementa um motor de cálculo de reembolso de despesas corporativas
guiado por uma especificação viva (`spec.md`). O motor lê uma política de
reembolso externa (JSON) e uma tabela de câmbio (JSON), processa as despesas de
um colaborador e emite um relatório com valores reembolsáveis, não reembolsáveis
e rejeitados.

O trabalho foi desenvolvido durante o Desafio Prático de Spec Driven Development
(SDD), com foco em rastreabilidade, decisões documentadas e testes automatizados.

---

## O que foi construído

- **Especificação viva** em `specs/001-motor-reembolso/spec.md` (v1.2), com 15
  ambiguidades documentadas e decididas.
- **Motor de processamento** em `src/motor.py`, com regras puras e stateless.
- **Regras modulares** em `src/regras/`:
  - `politica.py` — carrega a política v4 por centro de custo.
  - `cambio.py` — carrega taxas de câmbio e converte moedas.
  - `moeda.py` — converte valores para BRL antes de comparações.
  - `categoria.py` — valida categorias segundo a tabela do centro de custo.
  - `limites.py` — aplica limites diários/por diária, viagem e centro de custo.
  - `viagem.py` — identifica dias de viagem (incluindo moeda estrangeira).
  - `nota_fiscal.py`, `duplicata.py`, `estorno.py`, `periodo.py`, `arredondamento.py`.
- **CLI** em `src/cli.py`, com subcomando `calcular` e flags `--politica` e
  `--cambio`.
- **Testes automatizados** em `tests/`, cobrindo unidades, integração e os
  exemplos do envelope.

---

## Pré-requisitos

- Python 3.11+
- `pytest` (instalável via `pip install -r requirements-dev.txt`)

---

## Como rodar

### Processar um arquivo de despesas

```bash
python -m reembolso calcular \
  --input exemplos/envelope/despesas-envelope.json \
  --output resultado.json \
  --politica exemplos/envelope/politica-v4.json \
  --cambio exemplos/envelope/cambio.json
```

O resultado será gravado em `resultado.json`.

### Processar o exemplo de centro de custo desconhecido

```bash
python -m reembolso calcular \
  --input exemplos/envelope/despesas-envelope-cc-desconhecido.json \
  --output resultado-desconhecido.json \
  --politica exemplos/envelope/politica-v4.json \
  --cambio exemplos/envelope/cambio.json
```

---

## Como testar

### Suite completa

```bash
python -m pytest tests/ -v
```

Resumo rápido:

```bash
python -m pytest tests/ -q
```

### Testes específicos

Testes dos exemplos do envelope:

```bash
python -m pytest tests/test_motor.py -v -k envelope
```

Testes das regras de viagem:

```bash
python -m pytest tests/test_regras/test_viagem.py -v
```

---

## Estrutura do projeto

```text
sdd-desafio/
├── src/
│   ├── cli.py                  # interface de linha de comando
│   ├── motor.py                # orquestração do processamento
│   ├── regras/                 # regras de negócio
│   └── ...
├── tests/                      # testes automatizados
├── specs/001-motor-reembolso/  # especificação, plano, tasks e decisões
├── exemplos/envelope/          # política v4, câmbio e despesas de exemplo
└── docs/sessions/              # registro das sessões de trabalho
```

---

## Decisões principais

- **Limites por centro de custo**: cada centro tem sua própria tabela na
  política v4; centros desconhecidos usam a tabela `padrao`.
- **Moeda estrangeira**: valores são convertidos para BRL pela taxa da data antes
  das verificações de limite e nota fiscal. Cotação ausente rejeita a despesa.
- **Moeda estrangeira como viagem**: na RN-005, um dia que contém despesa em
  moeda estrangeira é considerado dia de viagem internacional, ampliando os
  limites daquele dia pelo percentual configurado na política.
- **Hospedagem com limite zero**: em centros como `CC-ENG-PLATAFORMA`, a
  hospedagem é válida como categoria, mas recebe status `nao_reembolsavel`.
- **Fila de aprovação manual**: fora de escopo, conforme comunicado do RH.

Decisões completas em:

- <ref_file file="C:\Users\Dell\Documents\ASV\Carreira\Projetos\sdd-desafio\specs\001-motor-reembolso\DECISIONS.md" />
- <ref_file file="C:\Users\Dell\Documents\ASV\Carreira\Projetos\sdd-desafio\DECISIONS.md" />
