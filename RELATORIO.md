# Relatório — Desafio SDD

## Delegação

| Atividade | Responsável | Evidência |
|---|---|---|
| Identificar e redigir ambiguidades | Devin, com decisões revisadas pelo usuário | `specs/001-motor-reembolso/spec.md` |
| Planejar a arquitetura | Devin | `specs/001-motor-reembolso/plan.md` |
| Implementar e escrever testes | Devin, com revisão humana pendente | `src/`, `tests/` e `specs/001-motor-reembolso/tasks.md` |
| Decidir a ampliação da hospedagem | Usuário | Clarificação registrada em `specs/001-motor-reembolso/spec.md` |

Foram usados os skills Speckit de especificação, análise, clarificação,
convergência e implementação. O skill `challenge-doc` mantém a trilha de sessões
e commits. Não houve uso de subagentes nesta etapa. O MCP do GitHub estava
disponível, mas não foi necessário para as alterações locais.

## Descrição

A política dizia que colaboradores em viagem recebem limites ampliados, mas não
definia quais dias compõem a viagem. A primeira versão ampliava todo o período
quando existia hospedagem. A versão atual limita a ampliação aos dias hospedados
e, em viagens internacionais, aos dias adjacentes comprovados por transporte.

Evidências:

- Regra final: `specs/001-motor-reembolso/spec.md`, RN-005.
- Registro da mudança: `DECISIONS.md`, D-003.
- Implementação: `src/regras/viagem.py` e `src/regras/limites.py`.
- Testes: `tests/test_regras/test_viagem.py`,
  `tests/test_regras/test_limites.py` e `tests/test_motor.py`.

## Discernimento

### Caso verificável

**O que o agente propôs:** inicialmente tratou a existência de hospedagem como
um booleano que ampliava os limites de todas as despesas do período.

**Por que estava errado:** o requisito posterior esclareceu que apenas as datas
efetivas de hospedagem e deslocamento são dias de viagem.

**Como foi detectado:** o usuário corrigiu explicitamente a interpretação da
RN-005. A análise cruzada também encontrou conflito entre o aceite de hospedagem
e a ampliação de 50%.

**O que foi feito:** a spec foi alterada, os dias passaram a ser calculados por
data, a distribuição proporcional remanescente em AMB-001 foi corrigida e foram
adicionados testes nacionais, internacionais e de hospedagem ampliada.

**Onde está a evidência:** `DECISIONS.md`, D-002 e D-003;
`specs/001-motor-reembolso/spec.md`, seção Clarifications e RN-005; e
`tests/test_regras/test_viagem.py`.

## Diligência

Os testes automatizados são executados após cada grupo de mudanças e ao final da
implementação. O diff é verificado contra `spec.md`, `plan.md`, `tasks.md` e a
constituição. Como o mesmo agente escreveu testes e código, a revisão humana do
diff e dos cenários continua obrigatória.

Evidências técnicas:

- Configuração: `pyproject.toml`.
- Suíte: `tests/`.
- Contratos: `specs/001-motor-reembolso/contracts/`.
- Checklist: `specs/001-motor-reembolso/checklists/requirements.md`.

## O envelope

A mudança entrou pela especificação, foi formalizada em `DECISIONS.md`, gerou
tarefas de convergência e então alterou testes e código. A separação entre
`viagem.py` e `limites.py` absorveu a maior parte da mudança; a resistência
principal foi substituir o fator global por identificação de datas e associar o
limite da hospedagem ao check-in quando a data da despesa difere.

## Fechamento

O processo é especialmente útil quando regras de negócio têm fronteiras e dados
ausentes que podem produzir resultados financeiros diferentes. Para um script
sem ambiguidade e descartável, toda a estrutura teria custo excessivo. Neste
desafio, a trilha de decisões tornou visível uma interpretação incorreta antes
de ela permanecer como comportamento implícito.
