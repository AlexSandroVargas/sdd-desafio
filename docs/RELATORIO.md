# Relatório — Desafio SDD

**Aluno:** `<nome>` · **Repositório:** `<link>` · **Data:** `<data>`

> Isto não é redação. São **evidências**. Toda afirmação deve vir acompanhada de
> arquivo, hash de commit ou trecho de sessão exportada. Um parágrafo bonito sem
> evidência vale menos que uma frase curta com um hash.
>
> Vale 20 dos 100 pontos, e é a seção que mais separa notas.

---

## Delegação

*O que você fez, o que o Claude fez, e por que dividiu assim.*

**A divisão:**

| Atividade | Quem | Por quê |
|---|---|---|
| Identificar ambiguidades |Claude/devin | Não identifiquei mais ambiguidades, queria ver o que encontrariam |
| Decidir as ambiguidades |Claude/devin | Queria ver como decidiriam, depois revisei |
| Escrever a spec |Claude/devin | Utilizei a spec-kit pois já tem um padrão, especialização, etc|
| Desenhar a arquitetura | Devin, com revisão humana pendente | Seguiu `specs/001-motor-reembolso/plan.md` e os contratos da feature |
| Implementar | Devin, com revisão humana pendente | Execução rastreada pelas tasks T001–T042 em `specs/001-motor-reembolso/tasks.md` |
| Escrever testes | Devin, com revisão humana pendente | Testes por regra em `tests/test_regras/` e integração em `tests/test_motor.py` e `tests/test_cli.py` |
| Absorver o envelope | | |

**Onde deleguei e me arrependi:**

**Onde não deleguei e deveria ter delegado:**

**Usei subagentes / skills / MCP / hooks?** <se sim: o quê, como configurou,
valeu a pena. Se não: por que não.>

constitution
    constitution.sdd-desafio.md|pedi pra IA criar com base nas regras do desafio e todos os documentos
skills
    challenge-doc|pedi para a IA criar uma skill que fizesse os commits, pushs, etc e registrasse em log
    spec-kit|baixei o projeto do github e pedi pra IA instalar| Valeu a pena
MCP
    github-mcp-server|baixei no marketplace|Valeu a pena
---

## Descrição

*Como você transformou requisito ambíguo em requisito verificável.*

Pegue **um** requisito ambíguo da política do RH e mostre a evolução:

**Versão 1 (minha primeira escrita):**
> ```
> <cole>
> ```

**Versão final:**
> ```
> <cole>
> ```

**O que estava ambíguo:**

**Como percebi:** <testando? o Claude perguntou? bateu o olho no JSON de exemplo
e não soube dizer qual era a resposta certa?>

**Commit da mudança:** `<hash>`

---

## Discernimento

*Onde o Claude errou e você pegou.*

> **Sem um caso concreto e verificável, esta seção vale zero.** Não existe projeto
> de dois dias em que o modelo acertou tudo. A ausência do caso não prova que o
> modelo foi perfeito — prova que ninguém estava conferindo.

### Caso 1

**O que ele propôs:**

**Por que estava errado:**

**Como eu detectei:** <li o diff? o teste quebrou? só percebi dias depois?
"como detectei" é a informação mais útil deste relatório inteiro>

**O que eu fiz:**

**Onde está a evidência:** `docs/sessions/<arquivo>`, trecho `<...>`

### Caso 2 *(opcional)*

**Padrão que eu notei:** <em que tipo de tarefa ele erra mais? teve um sinal
recorrente que passou a te deixar em alerta?>

---

## Diligência

*O que você verificou antes de aceitar.*

**Meu procedimento de verificação:** <o que você de fato fazia — não o que
deveria ter feito>

**Li o diff inteiro em que porcentagem das entregas?** <seja honesto; a
honestidade aqui vale ponto e a maquiagem custa>

**O que aceitei sem verificar direito, e o que me custou:**

**Testes: quem escreveu, e como você sabe que eles testam a coisa certa?**
Os testes foram escritos pelo Devin antes da implementação e inicialmente falharam com 11 erros de importação, registrando o estado vermelho do TDD. Depois da implementação, 24 testes passaram. A revisão humana ainda é necessária porque o mesmo agente escreveu testes e código. Evidências: `tests/test_regras/`, `tests/test_motor.py`, `tests/test_cli.py` e a execução descrita na sessão exportada desta implementação.

---

## O envelope

*A mudança de requisito do Dia 2.*

**Quantos arquivos toquei na mão:** `<n>`
**Quanto tempo levou:** `<...>`
**Diff de absorção:** `<n> arquivos, +<n>/-<n> linhas` (`git diff <hash-antes> HEAD --stat`)

**Absorveu de graça:** <o que a arquitetura já suportava e por quê>

**Resistiu:** <o que teve que ser quebrado e por quê>

**Ordem em que fiz:** <spec → tasks → código? ou código → spec? seja honesto:
a correção vê os timestamps dos commits de qualquer forma>

**Se eu tivesse escrito a spec original sabendo desta mudança:**

**O que a spec me poupou, em concreto:**

---

## Fechamento

**Para qual tamanho de projeto isto valeu a pena?**

**Para qual não valeria?**

**O que eu faria diferente:**

**A coisa mais desconfortável que aprendi sobre como eu trabalho com IA:**
