---
name: challenge-doc
description: Documenta a sessão atual do desafio SDD em docs/sessions com numeração sequencial, registra em log-session.md, mantém log-commit.md com histórico de commits, faz commit rastreável e push. Use ao final de cada sessão de trabalho ou quando o usuário pedir para registrar/exportar a sessão.
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

Ignore `log-session.md`, `log-commit.md` e qualquer arquivo que não siga o padrão
`NN-*.md`.

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

### 4. Commit e push

1. Verifique se `log.md` ainda existe e `log-session.md` ainda não existe.
   Se essa condição for verdadeira, **renomeie** `log.md` para
   `log-session.md` e atualize as referências em `docs/sessions/NN-*.md`.

2. Atualize `docs/sessions/log-session.md` conforme o passo 5.

3. Execute `git add` para o arquivo da sessão e para `log-session.md` caso
   ainda não estejam staged.

4. Faça commit dos dois arquivos juntos com a mensagem:

   ```
   docs(sessions): <nome-da-tarefa>
   ```

5. Faça push para o repositório remoto: `git push`.

### 5. Atualizar log-session.md

Arquivo: `docs/sessions/log-session.md`.

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
o `log-session.md` no mesmo commit do passo 4 — preferencial: gere o commit do
arquivo de sessão primeiro para obter o hash, depois escreva o log e faça
`git commit --amend --no-edit` incluindo o log. Alternativa simples aceitável:
commite os dois arquivos juntos e use `git rev-parse --short HEAD` para o hash,
registrando-o num segundo commit `docs(sessions): log <nome-da-tarefa>` — prefira
a primeira opção (amend) para manter um commit por sessão.

### 6. Atualizar log-commit.md

Arquivo: `docs/sessions/log-commit.md`.

Regenere este arquivo a cada execução do `challenge-doc`, incluindo **todos os
commits do repositório** (local e remoto). **Não commite este arquivo**: se ele
fizer parte de um commit, o log teria que se referir a si mesmo, gerando
recursão.

Formato:

```markdown
# Log de Commits

| Data | Hora | Descrição | Commit | Componentes |
|---|---|---|---|---|
| <AAAA-MM-DD> | <HH:MM> | <mensagem do commit> | <hash curto> | <arquivo1>; <arquivo2>; ... |
```

Para preencher a coluna **Componentes**, use os arquivos afetados por cada
commit (saída de `git show --name-only <hash>`), separados por ponto e vírgula.

Após gerar `log-commit.md`, **não execute `git add` nem `git commit`** para ele.

## Verificações antes de finalizar

- [ ] Nome da tarefa foi fornecido pelo usuário (não inventado)
- [ ] Número sequencial correto (último + 1)
- [ ] Conteúdo incremental — sem duplicar o que já está na sessão NN-1
- [ ] `log-session.md` tem uma linha por sessão, em ordem cronológica
- [ ] `log-commit.md` existe e lista todos os commits com componentes
- [ ] Commit existe e a mensagem contém o nome da tarefa
- [ ] Push foi realizado
