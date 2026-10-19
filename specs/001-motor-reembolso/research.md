# Research — Motor de Cálculo de Reembolso

Este documento consolida as decisões técnicas tomadas durante o planejamento do
feature `001-motor-reembolso`. O objetivo é justificar cada escolha com base no
contexto do desafio: produto simples (JSON-in / JSON-out), prazo curto (2 dias) e
avaliação centrada em processo, rastreabilidade e especificação.

---

## R-001 — Linguagem e runtime

**Decision:** Python 3.11+ *(confirmado pelo usuário como linguagem de domínio)*

**Rationale:**
- O desafio permite stack livre e o domínio é puro processamento de dados.
- Python 3.11 oferece `argparse`, `json`, `decimal` e `unittest` na biblioteca
  padrão, eliminando dependências de runtime.
- A sintaxe é legível para quem for revisar a spec e o código na correção.
- É multiplataforma (Windows, Linux, macOS), o que facilita a reprodução do
  quickstart.

**Alternatives considered:**
- Node.js + TypeScript: ecossistema rico, mas exige `npm install` e decisões
  adicionais sobre arredondamento decimal (`decimal.js` ou inteiros em centavos).
- Go: binário único e performance, mas verboso para uma lógica de regras que
  exige muitos testes de casos de borda.
- Java: pesado para um CLI simples.

---

## R-002 — Framework de CLI

**Decision:** `argparse` (biblioteca padrão do Python).

**Rationale:**
- A interface fixa do desafio exige apenas: `<comando> calcular --input <arq> --output <arq>`.
- `argparse` é suficiente para subcomando `calcular` e flags `--input`/`--output`.
- Zero dependências externas.

**Alternatives considered:**
- `click`: mais elegante, mas adiciona uma dependência sem ganho funcional para
  dois argumentos.
- `typer`: mesma razão acima, ainda mais overhead.

---

## R-003 — Parsing e validação de JSON

**Decision:** `json` da biblioteca padrão + funções de validação explícitas.

**Rationale:**
- O schema de entrada é pequeno e fixo (colaborador, período, lista de despesas).
- Validação manual permite mensagens de erro claras e rastreáveis a requisitos
  da spec.
- Evita dependências como `pydantic` ou `jsonschema`.

**Alternatives considered:**
- `pydantic`: forte para validação, mas adiciona dependência e pode mascarar
  regras de negócio como schema.
- `jsonschema`: exige schema externo; mais útil se a API evoluísse rapidamente.

---

## R-004 — Aritmética monetária

**Decision:** `decimal.Decimal` com precisão padrão e arredondamento `ROUND_HALF_UP`.

**Rationale:**
- O spec exige arredondamento half-up para duas casas decimais (RN-010).
- `Decimal` representa centavos sem erros de ponto flutuante e suporta
  `ROUND_HALF_UP` nativamente.
- Facilita testes porque `Decimal('0.1') + Decimal('0.2') == Decimal('0.3')`.

**Alternatives considered:**
- `float`: rejeitado — imprecisão em dinheiro gera diferenças de centavos.
- Inteiros em centavos (`int`): preciso e rápido, mas força conversões frequentes
  e torna a legibilidade das regras pior (ex.: `6000` em vez de `60.00`).
- `fractions.Fraction`: overkill para valores já arredondados em centavos.

---

## R-005 — Framework de testes

**Decision:** `pytest` como dependência de desenvolvimento.

**Rationale:**
- Testes são obrigatórios no desafio e a rastreabilidade exige nomes claros.
- `pytest` permite nomes descritivos, fixtures e execução simples via `pytest`.
- A curva de aprendizado é baixa e é o padrão da comunidade Python.

**Alternatives considered:**
- `unittest` (stdlib): funciona, mas a saída e a organização de fixtures são
  menos convenientes.

---

## R-006 — Estrutura de diretórios do código

**Decision:** Layout simples com `src/` e `tests/` na raiz.

**Rationale:**
- O desafio não prevê múltiplos pacotes ou frontends.
- Separação clara entre código-fonte (`src/`) e testes (`tests/`).
- Facilita a rastreabilidade: cada arquivo de regra pode ser mapeado a um
  requisito da spec.

**Estrutura proposta:**

```text
src/
├── cli.py              # ponto de entrada argparse
├── motor.py            # orquestração do cálculo
├── regras/
│   ├── __init__.py
│   ├── categoria.py    # RN-008
│   ├── periodo.py      # RN-007
│   ├── nota_fiscal.py  # RN-004
│   ├── duplicata.py    # RN-006
│   ├── estorno.py      # RN-009
│   ├── viagem.py       # RN-005
│   ├── limites.py      # RN-001, RN-002, RN-003
│   ├── arredondamento.py  # RN-010
│   ├── politica.py     # carregamento da política v4
│   ├── cambio.py       # carregamento das taxas de câmbio
│   └── moeda.py        # RN-011, RN-012
└── modelos.py          # dataclasses de entrada/saída

tests/
├── conftest.py
├── test_regras/
│   ├── test_categoria.py
│   ├── test_periodo.py
│   ├── test_nota_fiscal.py
│   ├── test_duplicata.py
│   ├── test_estorno.py
│   ├── test_viagem.py
│   ├── test_limites.py
│   ├── test_arredondamento.py
│   ├── test_politica.py
│   ├── test_cambio.py
│   └── test_moeda.py
└── test_motor.py
```

**Alternatives considered:**
- Monolito único em `src/motor.py`: rejeitado porque dificulta mapear regras a
  testes e commits individuais.
- Múltiplos pacotes (`packages/`): overkill para um único CLI.

---

## R-007 — Representação da política de limites

**Decision:** Política de limites lida de arquivo JSON externo
(`exemplos/envelope/politica-v4.json`), com módulo `regras/politica.py`
expondo `limites_do_centro(centro_custo)`.

**Rationale:**
- A política v4 exige explicitamente que limites variem por centro de custo e
  sejam mantidos pelo financeiro fora do código.
- O arquivo JSON segue o formato fornecido no envelope lacrado.
- A função de lookup encapsula o fallback para o bloco `padrao` quando o centro
  não tem tabela própria (AMB-011).

**Alternatives considered:**
- Constantes em `regras/config.py`: válido para a v3, mas não atende mais ao
  requisito de limites por centro de custo.
- Arquivo YAML externo: equivalência funcional, mas o desafio fornece o formato
  em JSON.
- Hard-coded espalhado: dificulta manutenção e testes.

---

## R-009 — Conversão de moeda estrangeira

**Decision:** Taxas de câmbio lidas de arquivo JSON externo
(`exemplos/envelope/cambio.json`), com módulo `regras/cambio.py` expondo
`cotacao(data, moeda)` e `regras/moeda.py` realizando a conversão.

**Rationale:**
- A v4 introduz despesas em moeda estrangeira com conversão pela taxa da data.
- O arquivo fornecido publica taxas apenas em dias úteis bancários.
- Centralizar a conversão permite rejeitar despesas sem cotação de forma
  previsível (RN-012).

**Alternatives considered:**
- Consumir API externa de câmbio: adicionaria dependência de rede e complexidade.
- Hard-code taxas no código: impossibilitaria atualização pelo financeiro.
- Interpolar taxas de datas adjacentes: rejeitado porque não há respaldo na
  política (AMB-014).

---

## R-008 — Tratamento de erros estruturais

**Decision:** Erros estruturais no documento, colaborador ou período interrompem
o processamento com mensagem em `stderr` e retorno diferente de zero. Uma
despesa individual malformada é registrada como rejeitada, sem interromper as
demais.

**Rationale:**
- Colaborador e período definem o contexto de todo o cálculo e precisam ser
  válidos para qualquer resultado ser produzido.
- Uma despesa é uma unidade independente; rejeitá-la preserva o processamento
  das demais conforme a spec.

**Alternatives considered:**
- Falhar rápido diante de qualquer item inválido: rejeitado porque descartaria
  despesas válidas sem necessidade.
- Tentar completar campos ausentes: rejeitado porque inventaria dados.
