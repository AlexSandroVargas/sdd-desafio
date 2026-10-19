# Data Model — Motor de Cálculo de Reembolso

Este documento descreve as entidades, campos, relacionamentos e regras de
validação extraídas de `specs/001-motor-reembolso/spec.md`. Não inclui decisões
de implementação (linguagem, bibliotecas, estrutura de pastas), que ficam em
`plan.md` e `research.md`.

---

## Entidades

### 1. Colaborador

Representa o titular das despesas do período.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string | sim | Identificador único do colaborador |
| `nome` | string | sim | Nome do colaborador |
| `centro_custo` | string | sim | Centro de custo do colaborador |

**Validações:**
- Todos os campos são obrigatórios.
- Deve ser reproduzido na saída sem alteração.

---

### 2. Período

Define o intervalo de competência das despesas.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `competencia` | string | sim | Mês de competência no formato `YYYY-MM` |
| `inicio` | string | sim | Data inicial no formato `YYYY-MM-DD` |
| `fim` | string | sim | Data final no formato `YYYY-MM-DD` |

**Validações:**
- Todos os campos são obrigatórios.
- `inicio` e `fim` devem ser datas válidas.
- `inicio` deve ser anterior ou igual a `fim`.
- O `competencia` deve ser coerente com `inicio`/`fim` (mesmo mês/ano).
- Deve ser reproduzido na saída sem alteração.

---

### 3. Despesa

Item de gasto declarado pelo colaborador. É a unidade processada pelas regras
de negócio.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string | sim | Identificador único da despesa |
| `data` | string | sim | Data da despesa no formato `YYYY-MM-DD` |
| `categoria` | string | sim | Categoria da despesa |
| `descricao` | string | sim | Descrição livre; na hospedagem pode indicar `internacional`, check-in, checkout e diárias para determinar os dias de viagem |
| `fornecedor` | string | sim | Nome do fornecedor |
| `valor` | número | sim | Valor declarado da despesa |
| `tem_nota_fiscal` | boolean | sim | Indica se há nota fiscal |

**Validações:**
- Todos os campos são obrigatórios.
- `data` deve ser uma data válida.
- `categoria` é comparada de forma case-insensitive (RN-008).
- `valor` pode ser negativo (estorno) ou positivo (RN-009).
- `tem_nota_fiscal` é booleano.

---

### 4. Resultado da Despesa

Representa o resultado do cálculo para uma única despesa.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | Identificador da despesa (mesmo da entrada) |
| `data` | string | Data da despesa (mesmo da entrada) |
| `categoria` | string | Categoria da despesa (normalizada para minúsculas) |
| `valor_declarado` | número | Valor declarado original, sem alteração |
| `valor_reembolsavel` | número | Valor que será reembolsado |
| `valor_nao_reembolsavel` | número | Parte do valor declarado que não será reembolsada |
| `status` | string | `aprovado`, `parcial`, `rejeitado` ou `estorno` |
| `motivo` | string | Justificativa da decisão |

**Regras derivadas da spec:**
- `valor_reembolsavel` + `valor_nao_reembolsavel` ≤ `valor_declarado` quando
  `valor_declarado` ≥ 0.
- Valores negativos sempre têm `valor_reembolsavel = 0`, `valor_nao_reembolsavel = 0`
  e `status = estorno`.
- `status = rejeitado` quando a despesa é invalidada por categoria, período,
  nota fiscal ou duplicata.
- `status = parcial` quando o valor reembolsável é maior que zero, mas menor
  que o valor declarado.
- `status = aprovado` quando o valor reembolsável é igual ao valor declarado.
- Todos os valores financeiros são arredondados para duas casas decimais
  (RN-010).

---

### 5. Resumo

Agregação dos valores do período.

| Campo | Tipo | Descrição |
|---|---|---|
| `total_declarado` | número | Soma dos valores declarados de todas as despesas |
| `total_reembolsavel` | número | Soma dos valores efetivamente reembolsáveis |
| `total_nao_reembolsavel` | número | Soma dos valores acima dos limites, excedentes não pagos |
| `total_rejeitado` | número | Soma dos valores de despesas inteiramente recusadas |
| `quantidade_despesas` | número | Quantidade total de despesas processadas |

**Regras derivadas da spec:**
- `total_declarado` é a soma dos `valor` de todas as despesas da entrada, incluindo
  estornos e itens rejeitados.
- `total_reembolsavel` é a soma dos `valor_reembolsavel` das despesas, menos o
  valor absoluto dos estornos (RN-009).
- `total_nao_reembolsavel` é a soma dos `valor_nao_reembolsavel` das despesas
  parciais.
- `total_rejeitado` é a soma dos `valor_declarado` das despesas com
  `status = rejeitado`.
- `quantidade_despesas` é a quantidade de itens no array `despesas` da entrada.
- Todos os valores financeiros são arredondados para duas casas decimais
  (RN-010).

---

### 6. Alerta

Alerta transversal sobre o conjunto de despesas.

| Campo | Tipo | Descrição |
|---|---|---|
| `tipo` | string | Tipo do alerta, ex.: `duplicata` |
| `despesas` | array de strings | Identificadores das despesas envolvidas |

**Regras derivadas da spec:**
- Atualmente o único tipo previsto é `duplicata` (RN-006).
- Lista os IDs das despesas que foram detectadas como duplicatas (exceto a
  primeira ocorrência, que é processada normalmente).

---

## Relacionamentos

```text
Colaborador 1───* Despesa *───1 Período
                │
                └──► ResultadoDaDespesa
                │
                └──► Alerta (quando duplicata)

Resumo ←── agrega ── ResultadoDaDespesa
```

- Um `Colaborador` está associado a um conjunto de `Despesa`s dentro de um
  `Período`.
- Cada `Despesa` gera exatamente um `ResultadoDaDespesa`.
- O `Resumo` é calculado a partir dos `ResultadoDaDespesa`s.
- `Alerta`s são gerados a partir do conjunto de `Despesa`s.

---

## Estados de uma Despesa

O campo `status` do `ResultadoDaDespesa` pode assumir os seguintes valores:

| Status | Condição |
|---|---|
| `aprovado` | Valor declarado reembolsável integralmente |
| `parcial` | Parte do valor declarado é reembolsável |
| `rejeitado` | Valor declarado inteiramente recusado |
| `estorno` | Valor declarado negativo; reduz o total reembolsável |

---

## Regras de negócio mapeadas para entidades

| Regra | Entidade afetada | Efeito |
|---|---|---|
| RN-001 | `Despesa` / `ResultadoDaDespesa` | Limite diário de alimentação |
| RN-002 | `Despesa` / `ResultadoDaDespesa` | Limite diário de transporte urbano |
| RN-003 | `Despesa` / `ResultadoDaDespesa` | Limite de hospedagem por diária |
| RN-004 | `Despesa` / `ResultadoDaDespesa` | Rejeição por falta de nota fiscal |
| RN-005 | `Despesa` / `ResultadoDaDespesa` | Limites ampliados em viagem |
| RN-006 | `Despesa` / `Alerta` | Tratamento de duplicatas |
| RN-007 | `Despesa` / `ResultadoDaDespesa` | Rejeição fora do período |
| RN-008 | `Despesa` / `ResultadoDaDespesa` | Rejeição de categorias fora da política |
| RN-009 | `Despesa` / `Resumo` | Estorno reduz total reembolsável |
| RN-010 | `ResultadoDaDespesa` / `Resumo` | Arredondamento half-up para centavos |
