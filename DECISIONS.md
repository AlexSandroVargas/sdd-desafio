# Log de Decisões e Mudanças de Spec

Ordem cronológica inversa: a mais recente primeiro.

## D-006 — Moeda estrangeira aciona ampliação de limites no dia da despesa · `2026-10-19`

**Gatilho:** Reinterpretação da `RN-005` após análise do envelope v4.

**Decisão:** Se houver qualquer despesa declarada em moeda estrangeira em um dia,
esse dia específico é considerado dia de viagem internacional, ampliando os
limites das despesas elegíveis naquele dia pelo percentual configurado na política
do centro de custo. Na ausência de moeda estrangeira no dia, a verificação de
viagem segue os critérios originais de hospedagem nacional/internacional. O
percentual de ampliação passa a ser lido da política externa em vez de valor fixo
na redação.

**Por quê:** A moeda estrangeira indica operação internacional na data da despesa,
não em todo o período de competência, evitando ampliação indevida de despesas
nacionais em dias sem viagem.

**O que isso invalidou:** Interpretação anterior de que moeda estrangeira
ampliava limites em todo o período; interpretação anterior de que apenas menção
`internacional` ou hospedagem identificavam viagem; redação da RN-005 com
percentual fixo de 50%.

**Tasks afetadas:** T055–T070 (implementação v4), especialmente T059 e T063.

**Custo:** Ajuste de `spec.md`, `src/regras/viagem.py`, `src/regras/limites.py` e
revisão dos testes de envelope.

---

## D-005 — Adoção da Política de Reembolso v4 · `2026-10-18`

**Gatilho:** Comunicado do RH no envelope `exemplos/envelope/00-ENVELOPE-LACRADO.md`
revisou a política para vigência imediata, retroativa à competência atual.

**Decisão:** Atualizada a `specs/001-motor-reembolso/spec.md` para refletir a
política v4: limites por centro de custo; nova categoria `representacao`;
hospedagem não reembolsável em determinados centros recebe status
`nao_reembolsavel`; despesas em moeda estrangeira com conversão pela taxa da
data; e rejeição quando a cotação está ausente. A fila de aprovação manual
(item C) permanece fora de escopo.

**Por quê:** A política deixa de ser única e passa a ser lida de arquivo externo.
A spec precisava incorporar as novas ambiguidades antes de qualquer código.

**O que isso invalidou:** Limites constantes da v3, suposição de despesas apenas
em BRL, lista fixa de categorias reembolsáveis, e a suposição de que hospedagem
sempre é reembolsável.

**Tasks afetadas:** T007, T012, T023–T029, T033–T036; novas tasks para política
externa e câmbio.

**Custo:** Atualização de spec, DECISIONS.md e tasks.md; novos módulos e testes.

---

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
