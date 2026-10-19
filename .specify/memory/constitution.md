<!--
Sync Impact Report
- Version change: unversioned placeholder → 1.0.0
- Modified principles:
  - Placeholder principles → I. A especificação é a fonte da verdade
  - Placeholder principles → II. Ambiguidades devem ser resolvidas explicitamente
  - Placeholder principles → III. Rastreabilidade completa é obrigatória
  - Placeholder principles → IV. Mudanças entram pela especificação
  - Placeholder principles → V. Evidência e verificação são parte da entrega
- Added sections:
  - Restrições e prioridades do desafio
  - Fluxo de desenvolvimento e qualidade
- Removed sections: none; placeholders were replaced by project governance
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): confirmar a data original de adoção da constituição do projeto
-->
# sdd-desafio Constitution

## Core Principles

### I. A especificação é a fonte da verdade

`specs/001-motor-reembolso/spec.md` MUST definir o que o sistema faz e por quê.
`plan.md` MUST definir como a solução será construída, e `tasks.md` MUST definir a ordem do
trabalho. Quando código e especificação divergirem, o código MUST ser tratado como defeituoso,
a menos que a especificação seja corrigida primeiro. A especificação MUST NOT conter escolhas de
linguagem, biblioteca, classe, função ou estrutura de arquivos. Uma pessoa sem contexto prévio
MUST conseguir verificar o comportamento esperado lendo somente a especificação.

Racional: o desafio avalia principalmente a qualidade e a auditabilidade do processo, não apenas
o funcionamento do produto.

### II. Ambiguidades devem ser resolvidas explicitamente

Cada ambiguidade de unidade, fronteira ou dado ausente MUST ser registrada em `spec.md` com ID
`AMB-00X`, decisão explícita, justificativa de negócio e referência às regras `RN-00X` afetadas.
Decisões de negócio MUST NOT existir somente no chat ou ser resolvidas silenciosamente no código.
Quando o usuário fornecer uma regra nova, o trabalho de implementação MUST pausar até que a
especificação e uma task correspondente sejam atualizadas. Itens existentes no exemplo de entrada
MUST ser cobertos pela especificação ou declarados explicitamente fora de escopo.

Racional: tornar a interpretação verificável é parte central do desafio e evita conhecimento
volátil ou implícito.

### III. Rastreabilidade completa é obrigatória

Toda regra de negócio MUST possuir um ID `RN-00X`, tasks relacionadas e testes automatizados.
Toda task MUST referenciar a regra, história ou requisito que atende e ser pequena o suficiente
para produzir um commit rastreável. Nenhum commit de implementação MUST existir sem task, e
mensagens de commit MUST indicar a task ou o tipo de artefato documental alterado. Deve ser
possível navegar de qualquer regra para sua task, código, teste e commit, e realizar o caminho
inverso sem inferências. Histórico Git MUST NOT ser reescrito para ocultar falhas.

Racional: a cadeia `spec → task → código → teste → commit` constitui a evidência auditável da
entrega.

### IV. Mudanças entram pela especificação

Toda mudança de requisito MUST seguir a ordem `spec → DECISIONS.md → tasks → código → testes`.
Cada alteração da especificação MUST gerar uma entrada em `DECISIONS.md` contendo a mudança de
estado anterior para novo, regra afetada, motivação, artefatos invalidados, tasks impactadas e
custo. A especificação é um artefato vivo e MUST ser atualizada antes da implementação. Uma
entrega parcial com especificação correta é preferível a uma implementação completa com
especificação desatualizada.

Racional: mudanças controladas demonstram que a arquitetura e o processo absorvem novos
requisitos sem perder rastreabilidade.

### V. Evidência e verificação são parte da entrega

Cada sessão de trabalho MUST ser exportada para `docs/sessions/NN-descricao-curta.md`.
`RELATORIO.md` MUST sustentar afirmações com referências a arquivos, commits ou sessões e MUST
incluir pelo menos um erro concreto do agente, sua detecção e correção. Testes MUST ser executados
e o diff MUST ser revisado antes de aceitar uma entrega; testes escritos pelo mesmo agente que
implementou o código não constituem verificação humana suficiente. Uso de skills, subagentes,
MCP ou hooks MUST ser registrado na seção de delegação do relatório.

Racional: trabalho sem evidência reproduzível não pode ser avaliado nem auditado com confiança.

## Restrições e prioridades do desafio

- A especificação, `DECISIONS.md`, a convenção de commits, `docs/sessions/` e `RELATORIO.md` MUST
  ser preservados mesmo quando houver restrição de tempo.
- Escopo adicional de produto SHOULD ser cortado antes dos artefatos de processo, pois estes
  concentram a maior parte da avaliação.
- A solução SHOULD permanecer simples, modular e suficiente para o escopo documentado.
  Complexidade adicional MUST possuir justificativa explícita no plano.
- Regras de negócio MUST possuir testes automatizados. Casos de borda documentados MUST possuir
  cenários de teste correspondentes.
- Lacunas conhecidas MUST ser declaradas; relatórios e histórico MUST refletir o processo real.

## Fluxo de desenvolvimento e qualidade

1. Ler a especificação e a task correspondente antes de implementar.
2. Se o pedido não estiver coberto, atualizar primeiro `spec.md`, `DECISIONS.md` e `tasks.md`.
3. Escrever ou atualizar o teste, confirmar que ele falha pelo motivo esperado e só então alterar
   a implementação.
4. Executar testes relevantes e a suíte completa conforme o impacto da mudança.
5. Revisar o diff contra a especificação, o plano, as tasks e esta constituição.
6. Registrar decisões, evidências e limitações antes de considerar a sessão concluída.
7. Criar commits pequenos e rastreáveis; alterações documentais MUST usar prefixos coerentes,
   como `docs(spec):`, `docs(plan):` e `docs(tasks):`.

As revisões MUST verificar, no mínimo: consistência entre artefatos, cobertura de cada RN, ausência
de regra somente no chat, atualização de `DECISIONS.md`, execução dos testes e exportação da
sessão.

## Governance

Esta constituição governa todos os artefatos e práticas do projeto. Em caso de conflito, seus
princípios prevalecem sobre conveniência, plano, tasks e implementação.

Emendas MUST ser propostas de forma explícita, revisadas pelo responsável humano e acompanhadas
de relatório de impacto. Mudanças incompatíveis em princípios ou governança incrementam a versão
MAJOR; novos princípios ou expansão material incrementam MINOR; esclarecimentos sem mudança
semântica incrementam PATCH. A data de última alteração MUST ser atualizada em toda emenda.

Toda revisão de especificação, plano, tasks ou código MUST verificar conformidade com esta
constituição. Violações MUST ser corrigidas ou justificadas no plano antes da implementação. A
constituição histórica da raiz, `constitution.sdd-desafio.md`, pode servir como referência, mas
este arquivo é a autoridade operacional consumida pelo Spec Kit.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirmar data original | **Last Amended**: 2026-10-18
