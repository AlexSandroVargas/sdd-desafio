# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

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
