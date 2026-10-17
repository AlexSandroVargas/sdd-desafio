---
name: challenge-doc
description: Documenta a sessão atual do desafio SDD em docs/sessions com numeração sequencial, registra em log.md e faz commit rastreável. Use ao final de cada sessão de trabalho ou quando o usuário pedir para registrar/exportar a sessão.
---

# challenge-doc — Registro de sessão do desafio SDD

Documenta a sessão de trabalho atual seguindo as regras de rastreabilidade do
desafio (`constitution.sdd-desafio.md`, princípio VII: evidência ou não aconteceu).

## Procedimento

### 1. Solicitar o nome da tarefa

Pergunte ao usuário o **nome da tarefa** da sessão (ex.: `motor-reembolso-spec`,
`T-003-limite-alimentacao`). Normalize para slug: minúsculas, sem espaços,
sem acentos, separado por hífens. **Não prossiga sem esse nome.**

### 2. Determinar o número sequencial

Liste os arquivos em `docs/sessions/` que seguem o padrão `NN-*.md`
(dois dígitos, hífen). O novo número é o maior encontrado + 1, com zero à
esquerda (`01`, `02`, ..., `10`, `11`). Se nenhum existir, comece em `01`.

Ignore `log.md` e qualquer arquivo que não siga o padrão.

### 3. Gerar o arquivo da sessão

Crie `docs/sessions/<NN>-<nome-da-tarefa>.md` contendo:

- Cabeçalho: título `# Sessão — <nome-da-tarefa>`, data, hora, branch e o
  número sequencial.
- **Conteúdo incremental da sessão**, em ordem cronológica: transcreva o
  transcript desta conversa (perguntas do usuário e respostas do agente)
  **somente a partir do ponto onde a sessão anterior terminou**.

  Regra de corte: leia o arquivo `NN-1` (a sessão imediatamente anterior).
  O conteúdo novo é tudo que ocorreu nesta conversa **depois** do último
  evento registrado naquele arquivo — mesmo que a sessão anterior também
  tenha sido incremental. Nunca duplique conteúdo já registrado em sessões
  anteriores; nunca inclua conteúdo anterior à última sessão registrada.

  Se o `/export` nativo estiver disponível e produzir ATIF/JSON, converta o
  trecho incremental para Markdown no formato pergunta/resposta. Se não
  estiver (flag de inicialização), transcreva o transcript diretamente.

### 4. Commit

Faça commit do arquivo da sessão **e** do `log.md` (juntos) com a mensagem:

```
docs(sessions): <nome-da-tarefa>
```

### 5. Atualizar log.md

Arquivo: `docs/sessions/log.md`.

- Se não existir, crie com cabeçalho `# Log de Sessões` e a tabela:

  ```
  | Data | Hora | Tarefa | Commit |
  |---|---|---|---|
  ```

- Se existir, faça **append** de uma linha ao final (ordem cronológica):

  ```
  | <AAAA-MM-DD> | <HH:MM> | [<NN>-<tarefa>.md](<NN>-<tarefa>.md) | <hash curto do commit> |
  ```

Ordem de execução: escreva a linha do log, depois faça um **amend** ou inclua
o `log.md` no mesmo commit do passo 4 — preferencial: gere o commit do arquivo
de sessão primeiro para obter o hash, depois escreva o log e faça
`git commit --amend --no-edit` incluindo o log. Alternativa simples aceitável:
commite os dois arquivos juntos e use `git rev-parse --short HEAD` para o hash,
registrando-o num segundo commit `docs(sessions): log <nome-da-tarefa>` — prefira
a primeira opção (amend) para manter um commit por sessão.

## Verificações antes de finalizar

- [ ] Nome da tarefa foi fornecido pelo usuário (não inventado)
- [ ] Número sequencial correto (último + 1)
- [ ] Conteúdo incremental — sem duplicar o que já está na sessão NN-1
- [ ] `log.md` tem uma linha por sessão, em ordem cronológica
- [ ] Commit existe e a mensagem contém o nome da tarefa
