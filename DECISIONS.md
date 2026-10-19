# Log de Decisões e Mudanças de Spec

Ordem cronológica inversa: a mais recente primeiro.

## D-004 — Pipeline mantém dicionários validados · `2026-10-18`

**Gatilho:** A convergência identificou que `src/modelos.py` existe, mas o motor
não instancia as dataclasses planejadas.

**Decisão:** O pipeline permanece baseado em dicionários validados. As
dataclasses ficam como referência do modelo de domínio, sem participar do
caminho de execução.

**Por quê:** A entrada e a saída são contratos JSON, e converter cada item para
dataclass e novamente para dicionário adicionaria transformação sem benefício
para as regras atuais. As funções continuam puras e a validação permanece
explícita.

**O que isso invalidou:** A representação do plano que posicionava
`modelos.py` como camada ativa entre I/O e regras.

**Tasks afetadas:** T005, T009, T033 e T050.

**Custo:** Atualização documental, sem alteração funcional.

## D-003 — Limites ampliados somente nos dias de viagem · `2026-10-18`

**Gatilho:** O requisito do Dia 2 esclareceu que a presença de hospedagem não
amplia os limites durante todo o período de competência.

**O que mudou:**
- `RN-005` passou a determinar dias de viagem por hospedagem, check-in, checkout
  e transportes adjacentes.
- Hospedagens sem a palavra `internacional` são nacionais.
- Viagens nacionais abrangem os dias hospedados a partir do check-in.
- Viagens internacionais podem abranger a véspera e o dia posterior quando há
  transporte para aeroporto ou hotel na data adjacente.
- A própria hospedagem recebe o teto ampliado de R$ 375,00 por diária nos dias
  de viagem.

**Por quê:** A ampliação deve acompanhar os dias em que o colaborador está
viajando, sem elevar os limites das demais datas do mês.

**O que isso invalidou:** A detecção booleana de viagem para todo o período, os
testes que aplicavam um único fator global e o aceite anterior de hospedagem com
teto normal durante a viagem.

**Tasks afetadas:** T024–T029 e T045–T050.

**Custo:** Atualização da spec, detecção de datas, cálculo de limites e testes.

## D-002 — Alocação sequencial confirmada · `2026-10-18`

**Gatilho:** A clarificação formal identificou contradição entre `AMB-001` e as
regras de limite.

**Decisão:** Despesas da mesma categoria e data são ordenadas por valor
declarado decrescente, preservando a ordem de entrada nos empates. O teto é
consumido sequencialmente.

**Por quê:** O comportamento é determinístico, auditável e consistente com
`RN-001`, `RN-002` e `AMB-003`.

**O que isso invalidou:** A redação proporcional remanescente em `AMB-001`.

**Tasks afetadas:** T025, T028 e T045.

**Custo:** Correção documental; a implementação já seguia a decisão.

## D-001 — Altera alocação do teto diário de proporcional para sequencial decrescente · `2026-10-18`

**Gatilho:** A alocação proporcional original distribuía o teto por todos os
itens do dia, mas a interpretação desejada prioriza as despesas maiores.

**Decisão:** Ordenar por valor decrescente, aplicar o teto sequencialmente,
reembolsar parcialmente o item que atingir o limite e rejeitar os demais.

**Por quê:** A regra é determinística e simples de auditar.

**O que isso invalidou:** Exemplos e testes baseados em divisão proporcional.

**Tasks afetadas:** T025 e T028.

**Custo:** Atualização da spec, testes e implementação de limites.
