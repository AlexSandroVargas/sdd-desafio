---
name: challenge-doc
description: Documenta a sessão atual do desafio SDD em docs/sessions com numeração sequencial, registra em log-session.md, mantém log-commit.md com histórico de commits, faz commit rastreável e push. Use ao final de cada sessão de trabalho ou quando o usuário pedir para registrar/exportar a sessão.
---

# challenge-doc — Registro de sessão do desafio SDD

> **Nota:** existe uma cópia desta skill em `docs/skills/challenge-doc.md`.
> Sempre que este arquivo for alterado, mantenha a cópia sincronizada.
>
> **Regra de commits/pushs:** a partir de agora, commits e pushs no projeto
> só ocorrem durante a execução desta skill. O agente não deve fazer commits
> ou pushs fora do `challenge-doc`.

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

### 4. Commit único e push

1. Verifique se `log.md` ainda existe e `log-session.md` ainda não existe.
   Se essa condição for verdadeira, **renomeie** `log.md` para
   `log-session.md` e atualize as referências em `docs/sessions/NN-*.md`.

2. Execute `git add -A` para incluir todas as alterações pendentes, inclusive
   os logs deixados em staging pela execução anterior e o arquivo da sessão atual.

3. Faça **exatamente um commit** com a mensagem:

   ```
   docs(sessions): <nome-da-tarefa>
   ```

4. Faça push desse commit para o repositório remoto: `git push`.

5. Não execute outro commit, `git commit --amend` ou outro push nesta execução.
   Todas as alterações realizadas após o commit, inclusive as atualizações dos
   logs nos passos 5 e 6, devem permanecer em staging até a próxima execução.

### 5. Atualizar log-session.md após o push

Arquivo: `docs/sessions/log-session.md`.

Depois do commit e do push do passo 4, obtenha o hash criado e:

- Se o arquivo não existir, crie com cabeçalho `# Log de Sessões` e a tabela:

  ```
  | Data | Hora | Tarefa | Commit | Link commit |
  |---|---|---|---|---|
  ```

- Faça **append** de uma linha ao final (ordem cronológica):

  ```
  | <AAAA-MM-DD> | <HH:MM> | [<NN>-<tarefa>.md](<NN>-<tarefa>.md) | <hash curto do commit> | [link](<url-do-repo>/commit/<hash>) |
  ```

Não faça amend nem crie um segundo commit para registrar essa linha. Ela será
incluída no commit da próxima execução da skill.

### 6. Atualizar log-commit.md após o push

Arquivo: `docs/sessions/log-commit.md`.

Regenere este arquivo a cada execução do `challenge-doc`, incluindo **todos os
commits do repositório** (local e remoto), inclusive o commit criado no passo 4.
A versão atualizada será incluída no commit da próxima execução, evitando que o
commit tente registrar a si mesmo.

Formato:

```markdown
# Log de Commits

| Data | Hora | Descrição | Commit | Link commit | Componentes |
|---|---|---|---|---|---|
| <AAAA-MM-DD> | <HH:MM> | <mensagem do commit> | <hash curto> | [link](<url-do-repo>/commit/<hash>) | <arquivo1>; <arquivo2>; ... |
```

Para preencher a coluna **Componentes**, use os arquivos afetados por cada
commit (saída de `git show --name-only <hash>`), separados por ponto e vírgula.

Para preencher a coluna **Link commit**, descubra a URL do repositório remoto
com `git remote get-url origin`, remova `.git` do final e monte o link como
`<url>/commit/<hash>`.

Após atualizar os dois logs, execute
`git add docs/sessions/log-session.md docs/sessions/log-commit.md` para deixá-los
em staging. **Não execute commit nem push novamente**; essas alterações serão
incluídas somente na próxima execução da skill.

## Verificações antes de finalizar

- [ ] Nome da tarefa foi fornecido pelo usuário (não inventado)
- [ ] Número sequencial correto (último + 1)
- [ ] Conteúdo incremental — sem duplicar o que já está na sessão NN-1
- [ ] Exatamente um commit foi criado com a mensagem contendo o nome da tarefa
- [ ] Esse único commit foi enviado por push
- [ ] `log-session.md` tem uma linha por sessão, em ordem cronológica
- [ ] `log-commit.md` existe e lista todos os commits com componentes
- [ ] As atualizações dos dois logs estão em staging para a próxima execução
- [ ] Nenhum amend, segundo commit ou segundo push foi executado
