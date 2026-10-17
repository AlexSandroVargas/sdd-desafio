# Constitution — sdd-desafio

> Princípios inegociáveis deste projeto, destilados de `DESAFIO.md`, `RUBRICA.md`,
> `FAQ.md` e `template/CLAUDE.md`. Este documento governa o trabalho do agente e
> do humano. Em conflito entre conveniência e estes princípios, vencem os princípios.
>
> **Premissa central:** o desafio não mede se o código funciona — mede se o
> *processo* funciona. O produto vale 10 dos 100 pontos; spec, rastreabilidade,
> resposta à mudança e relatório valem os outros 90.

---

## I. A spec é a fonte da verdade

1. `specs/001-motor-reembolso/spec.md` define **o quê** e **o porquê**.
   `plan.md` define **o como**. `tasks.md` define **em que ordem**.
2. Quando código e spec discordam, a spec está certa e o código é o bug —
   a menos que a spec esteja errada; nesse caso corrige-se a spec **primeiro**
   e registra-se em `DECISIONS.md`.
3. A spec é proibida de conter solução: nada de linguagem, biblioteca, classe,
   função ou estrutura de pastas. Se apareceu solução, ela vai para `plan.md`.
   Teste de fronteira: *se eu trocasse de linguagem amanhã, isso mudaria?* Se sim,
   é `plan.md`.
4. Critério de qualidade da spec: uma pessoa que nunca viu o projeto consegue,
   lendo só a spec, verificar se o sistema está correto. Spec longa não é spec boa.

## II. Ambiguidade é o trabalho, não o obstáculo

1. A política do RH contém no mínimo oito ambiguidades reais, distribuídas em três
   tipos: *unidade de aplicação*, *fronteira* e *dado ausente*. Encontrá-las e
   resolvê-las é o exercício — vale 25 pontos.
2. Não existe interpretação "certa" e não há quem perguntar. Para cada ambiguidade:
   **registrar** que existe, **decidir** explicitamente a interpretação adotada,
   **justificar** em uma linha com critério de negócio (não conveniência técnica),
   e deixar tudo em `spec.md` com ID (`AMB-00X`) e regra afetada (`RN-00X`).
3. Ambiguidade resolvida silenciosamente no código conta como **não resolvida**.
   Uma spec que apenas copia a política do RH está reprovada.
4. `exemplos/despesas-exemplo.json` não é decoração: cada item existe por um
   motivo. Caso presente na entrada e não coberto pela spec é buraco — nem que a
   resposta seja declará-lo explicitamente fora de escopo.

## III. Rastreabilidade é uma cadeia, não um documento

1. Toda regra de negócio recebe um ID (`RN-00X`). Toda task referencia requisitos
   da spec. Todo commit referencia uma task: `feat(T-003): <descrição>`,
   `test(T-003): <...>`. Mudanças de documentação: `docs(spec):`, `docs(plan):`,
   `docs(tasks):`.
2. **Nenhum commit sem task.** Uma task deve ser pequena o suficiente para virar
   um commit. O `git log` é trilha de auditoria — será lido na correção.
3. **Nenhuma regra de negócio entra sem teste.** Testes automatizados são
   obrigatórios; sem eles a rastreabilidade não fecha. A saída do sistema é
   conferida contra a spec do próprio projeto, não contra gabarito único.
4. Deve ser possível pegar qualquer regra da spec e chegar, sem adivinhar, à
   linha de código e ao teste que a implementam — e vice-versa.
5. Não reescrever histórico para maquiar. Histórico honesto imperfeito vale mais
   que histórico reescrito; registra-se a falha no relatório e segue-se a convenção.

## IV. Explicação no chat que não está na spec é bug de spec

1. Se o usuário explicar uma regra de negócio, decisão ou restrição que não está
   escrita na spec — **pare e diga isso antes de escrever código**.
2. Procedimento: corrigir a spec, registrar no `DECISIONS.md`, e só então continuar.
3. O chat é volátil; a spec é o que fica. Todo conhecimento que só existe no chat
   é conhecimento que será perdido. (−5 por ocorrência na correção, teto −15.)
4. Antes de implementar qualquer coisa, ler a task correspondente em `tasks.md`.
   Se o pedido não é coberto por nenhuma task, avisar em vez de implementar.

## V. A spec é um artefato vivo

1. Spec que não muda em dois dias é spec que ninguém consultou. Mudar a spec no
   meio não é apenas permitido — é esperado.
2. **Toda** mudança de spec gera uma entrada no `DECISIONS.md`: o que mudou
   (de → para, com ID de regra), por quê, o que invalidou, tasks afetadas e custo.
3. `DECISIONS.md` ausente havendo mudança de spec: −5 pontos.

## VI. Mudança de requisito entra pela spec

1. O envelope do Dia 2 (mudança de requisito, 20 pontos) é absorvido nesta ordem:
   **spec → `DECISIONS.md` → tasks → código**. Nunca código primeiro.
2. Meia implementação com spec correta vale mais que implementação completa com
   spec desatualizada. A mudança não ficar 100% completa não penaliza; entrar por
   fora da spec, sim.
3. O diff ideal é cirúrgico: a arquitetura absorve a mudança em vez de resistir.

## VII. Evidência ou não aconteceu

1. Exportar a sessão ao final de **cada** sessão de trabalho para
   `docs/sessions/NN-descricao-curta.md`. Sessão não exportada é esforço invisível
   para a correção. Ausência total zera o critério de relatório; sessão única no
   último minuto limita a faixa.
2. O `RELATORIO.md` é evidência, não redação: toda afirmação vem com arquivo,
   hash de commit ou trecho de sessão exportada.
3. A seção de Discernimento exige **pelo menos um erro concreto do agente**:
   o que foi proposto, por que estava errado, como foi detectado, o que foi feito —
   com link para o trecho da sessão. Sem caso verificável, a seção vale zero.
4. Honestidade vale ponto. Relatório que diz "correu tudo bem" é avaliado como
   sinal de que ninguém estava conferindo. Lacunas se declaram, não se escondem.

## VIII. Delegação com verificação

1. As decisões sobre ambiguidade são **do humano** — o agente pode redigir, mas a
   spec gerada exige revisão antes de ser aceita. Spec aceita sem revisão "tem
   um cheiro característico" e aparece na correção.
2. Verificar antes de aceitar cada entrega do agente: rodar os testes, ler o diff.
   Teste escrito pelo mesmo agente que escreveu o código não é verificação suficiente.
3. Subagentes, skills, MCP e hooks são permitidos — e seu uso deve ser relatado
   (o que configurou, se valeu a pena) na seção de Delegação.

## IX. Hierarquia de sacrifício

Se faltar tempo, a ordem de corte é invertida ao peso da nota:

1. Primeiro: features e escopo de produto (vale 10 pontos — um bug conhecido
   documentado custa pouco).
2. Nunca: spec, `DECISIONS.md`, convenção de commits, `docs/sessions/` e
   `RELATORIO.md` — juntos valem 90.
3. Um projeto incompleto com spec impecável e trilha limpa tira nota alta. Um
   produto perfeito com spec fraca tira nota baixa. Isso é intencional.

---

## Penalidades a evitar (checklist)

- [ ] Regra de negócio só no chat: −5 por ocorrência (teto −15)
- [ ] `DECISIONS.md` ausente havendo mudança: −5
- [ ] `CLAUDE.md` ausente: −3
- [ ] README que não permite rodar o projeto: −3
- [ ] Repositório sem histórico (commit único): −15 e rastreabilidade ≤ 8
- [ ] Spec sem nenhuma ambiguidade mencionada: zera o critério 1 (25 pts)
- [ ] Sem caso de Discernimento no relatório: zera a seção (−8 no critério)
- [ ] Sem `docs/sessions/`: zera o critério 4 (20 pts)
