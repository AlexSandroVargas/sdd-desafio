# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

---

## D-006 — Moeda estrangeira aciona ampliação de limites no dia da despesa · `2026-10-19`

**Gatilho:** Reinterpretação da `RN-005` após análise do envelope: a política v4
considera que despesas em moeda estrangeira indicam viagem internacional apenas
nos dias em que ocorrem.

**O que mudou na spec:**
- `RN-005` foi reescrita em duas etapas:
  1. Se houver qualquer despesa declarada em moeda estrangeira em um dia, esse
     dia específico é considerado dia de viagem internacional e os limites das
     despesas elegíveis naquele dia são ampliados pelo percentual definido na
     política do centro de custo.
  2. Na ausência de despesa em moeda estrangeira no dia, a verificação de viagem
     segue os critérios originais (hospedagem nacional/internacional,
     check-in/checkout e transporte para aeroporto/hotel).
- O percentual de ampliação deixa de ser fixo em 50% na redação da regra e passa
  a ser o valor configurado na política externa (`acrescimo_em_viagem_percentual`).

**Por quê:** A moeda estrangeira indica operação internacional na data da despesa,
não em todo o período de competência. Isso evita ampliação indevida de despesas
nacionais em dias sem viagem.

**O que isso invalidou:**
- A interpretação anterior de que a presença de moeda estrangeira ampliava
  limites em todo o período.
- A interpretação anterior de que apenas menção `internacional` na descrição ou
  hospedagem identificavam viagem internacional.
- A suposição de ampliação fixa de 50% na redação da regra (o valor continua
  vindo da política, que na v4 é 50%).
- Testes de integração do envelope `CC-COMERCIAL`, que agora esperam ampliação
  apenas nos dias com despesas em EUR.

**Tasks afetadas:** T055–T070 (implementação v4), especialmente T063 (wiring do
motor), T059 (limites) e os testes de integração T064–T065.

**Custo:** Ajuste da `spec.md`, atualização de `src/regras/viagem.py` e
`src/regras/limites.py`, revisão dos testes de envelope.

---

## D-005 — Adoção da Política de Reembolso v4 · `2026-10-18`

**Gatilho:** Comunicado do RH (envelope lacrado `00-ENVELOPE-LACRADO.md`)
revisou a política para vigência imediata, retroativa à competência atual.

**O que mudou na spec:**
- Versão da spec: `1.1` → `1.2`.
- **Limites por centro de custo:** `RN-001`, `RN-002`, `RN-003` e `RN-005`
  passaram a referenciar a tabela do centro de custo do colaborador em vez de
  valores constantes. O `padrao` da política v4 é usado para centros sem tabela
  própria.
- **Nova categoria `representacao`:** incluída em `RN-008` como reembolsável
  apenas quando presente na tabela do centro de custo (ex.: `CC-COMERCIAL`).
- **Hospedagem não reembolsável por centro:** `RN-003` agora permite teto zero
  (ex.: `CC-ENG-PLATAFORMA`), classificando o valor como `nao_reembolsavel`
  (reembolso zero, valor declarado todo como não reembolsável).
- **Conversão cambial:** adicionadas `RN-011` e `RN-012`. Despesas com `moeda`
  diferente de `BRL` são convertidas pela taxa da data antes de comparações de
  limite e nota fiscal. Ausência de cotação rejeita a despesa.
- **Ordem de regras:** inseridos `RN-011`/`RN-012` após `RN-007` e antes de
  `RN-004`, para garantir valores em BRL antes do limiar de nota fiscal.
- **Ambiguidades novas:** registradas `AMB-011` a `AMB-015` com decisões
  documentadas.
- **Casos de borda:** adicionados cenários de centro com/sem tabela, hospedagem
  proibida, moeda estrangeira conhecida/desconhecida e nota fiscal após
  conversão.
- **Critérios de aceite:** incluídos itens sobre centros de custo, moeda
  estrangeira e cotação ausente.
- **Em aberto:** fila de aprovação manual (item C do comunicado) foi mantida
  fora de escopo; adicionada nota sobre status `pendente` caso venha a ser
  incluída.

**Por quê:** A política v4 exige que o motor leia limites de fora do código e
lide com despesas internacionais. Centralizar as mudanças na spec primeiro
preserva a rastreabilidade e evita retrabalho na implementação.

**O que isso invalidou:**
- A regra de limites constantes para toda a empresa (valores fixos de
  `RN-001`, `RN-002` e `RN-003`).
- A regra de que `hospedagem` sempre era reembolsável.
- A regra de que apenas `alimentacao`, `transporte_urbano` e `hospedagem` eram
  reembolsáveis (`representacao` entra condicionalmente).
- A suposição de que todas as despesas são em BRL.
- Testes e implementação que não carregam a política de um arquivo externo.

**Tasks afetadas:** Toda a fase de limites (T024–T029), configuração centralizada
(T007), validação de entrada (T012), testes de limite (T025), integração do
motor (T023, T029), output (T033–T036). Novas tasks necessárias para leitura
da política v4, conversão cambial e testes de centros de custo.

**Custo:** Atualização da spec, DECISIONS.md e tasks.md; novos módulos para
política externa e câmbio; ajustes em limites, validação e saída.

---

## D-001 — Altera alocação do teto diário de proporcional para sequencial decrescente · `2026-10-18`

**Gatilho:** Revisão de negócio durante a elaboração da spec: a alocação
proporcional original distribuía o teto por todos os itens do dia, mas a
interpretação desejada prioriza as despesas maiores e rejeita as demais após
o esgotamento do limite.

**O que mudou na spec:**
- `AMB-003`: a decisão de "distribuição proporcional" passou para "ordenação
  por valor decrescente + aplicação sequencial do teto, com reembolso parcial
  da despesa que atingir o limite e rejeição das demais".
- `RN-001` e `RN-002`: atualizados para descrever a ordenação decrescente e a
  aplicação sequencial do teto.
- Casos de borda: ajustados os exemplos de duas refeições no mesmo dia (com e
  sem viagem) para refletir a nova alocação.
- Critérios de aceite: item 3 reformulado para deixar clara a rejeição das
  demais despesas do agrupamento.

**Por quê:** A nova regra é determinística, mais simples de auditar e reflete
uma política de reembolso que prioriza as despesas de maior valor no dia,
rejeitando explicitamente os itens que extrapolam o teto.

**O que isso invalidou:** Os valores de aceite anteriores de `RN-001` e dos
exemplos de borda que usavam divisão proporcional. Qualquer implementação ou
teste baseado na alocação proporcional precisa ser refeito.

**Tasks afetadas:** Nenhuma task havia sido gerada ainda. As futuras tasks
`T-001` a `T-00N` devem implementar a nova alocação sequencial.

**Custo:** 1 arquivo de spec editado, 1 arquivo `DECISIONS.md` criado. Tempo
estimado: curto.
