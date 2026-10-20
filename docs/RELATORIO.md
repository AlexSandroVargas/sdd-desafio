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
    constitution.sdd-desafio.md|pedi pra IA criar com base nas regras do desafio e todos os documentos, uma constitution especifica para regrar o desafio.|Valeu a pena
skills
    challenge-doc|pedi para a IA criar uma skill que fizesse os commits, pushs, etc e registrasse em log|Valeu a pena
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
No reembolso parcial ele propôs, no caso de mais de uma despesa no mesmo dia, uma distribuição proporcional entre as despesas.

**Por que estava errado:**
Está errado porque teríamos várias despesas reembolsadas parcialmente, ao invés das maiores reembolsadas primeiro, eo se sobrar saldo ir pra próxima. Rejeitando as seguintes assim que se esgotar o saldo do dia para a despesa.

**Como eu detectei:** <li o diff? o teste quebrou? só percebi dias depois?
Detectei verificando o resultado.json

**O que eu fiz:**
Solicitei alteração na regra de negócio.

**Onde está a evidência:** `docs\sessions\04-ajuste-AMB-003.md`, trecho linha 16 e seguintes

### Caso 2 *(opcional)*

**O que ele propôs:**
Nas despesas em viagem ele propôs que uma única hospedagem no período, ou seja, no mês, determinaria que todas as despesas teriam o limite de viagem.

**Por que estava errado:**
Está errado porque uma única hospedagem de um dia aumentaria todos os limites das despesas no mês todo.

**Como eu detectei:** <li o diff? o teste quebrou? só percebi dias depois?
Detectei verificando o resultado.json

**O que eu fiz:**
Solicitei alteração na regra de negócio.

**Onde está a evidência:** `docs\sessions\08-ajuste-rn-005-viagem.md`, trecho linha 13 e seguintes


**Padrão que eu notei:** <em que tipo de tarefa ele erra mais? teve um sinal
recorrente que passou a te deixar em alerta?>
As vezes ele faz tarefas que cabem ao usuário, preenche relatórios, etc
Algumas vezes são bem vindas, porém precisamos verificar.
---

## Diligência

*O que você verificou antes de aceitar.*

**Meu procedimento de verificação:** <o que você de fato fazia — não o que
deveria ter feito>
Eu verificava as regras de negócio e listas das ambiguidades na spec, e depois o resultado.json.

**Li o diff inteiro em que porcentagem das entregas?** <seja honesto; a
honestidade aqui vale ponto e a maquiagem custa>
Nos commits iniciais e pequenos li inteiro. Também os que envolviam documentação.
Nos commits em que foram entregues códigos python, li por cima, me ative ao teste em execução.

**O que aceitei sem verificar direito, e o que me custou:**
Aceitei o código python e os testes. Ainda não custou, porém ainda vou abrir o envelope.

**Testes: quem escreveu, e como você sabe que eles testam a coisa certa?**
Os testes foram escritos pelo Devin antes da implementação e inicialmente falharam com 11 erros de importação, registrando o estado vermelho do TDD. Depois da implementação, 24 testes passaram. A revisão humana ainda é necessária porque o mesmo agente escreveu testes e código. Evidências: `tests/test_regras/`, `tests/test_motor.py`, `tests/test_cli.py` e a execução descrita na sessão exportada desta implementação.

---

## O envelope

*A mudança de requisito do Dia 2.*

**Quantos arquivos toquei na mão:** `nenhum (apenas o RELATORIO.md)`
**Quanto tempo levou:** `~3 horas`
**Diff de absorção:** `47 arquivos, +1791/-291 linhas` (`git diff <hash-antes> HEAD --stat`)

**Absorveu de graça:** Já suportava viagens internacionais e nacionais para calcular periodo em viagem.

**Resistiu:** A regra que define viagem internacional antes do envelope não utiliava moeda estrangeira.

**Ordem em que fiz:** <spec → tasks → código? ou código → spec? seja honesto:
spec → plan → tasks → implement
foi mais de um ciclo, as vezes com clarify

**Se eu tivesse escrito a spec original sabendo desta mudança:**
Bom, teria sido doferente, mas não sei extamente o que responder ... honestamente

**O que a spec me poupou, em concreto:**
Vou responder considerando "spec" como toda a skill spec-kit
A spec-kit me poupou muito, muito tempo, além de não me preocupar com formatos de arquivos, código, sintaxe, etc, e até mesmo a lingua portuguesa. Apenas revisei as regras de negócio, ambiguidades detectadas, etc. A skill escreveu tudo.

---

## Fechamento

**Para qual tamanho de projeto isto valeu a pena?**
Projetos de uma única aplicação, que era este caso. Eu antes deste desafio já estava utilizando SDD com a spec-kit para documentar uma app java legada, para gerar regras de negócio. 

**Para qual não valeria?**
Honestamente não sei como seria utilizar em um conjunto de apps interagindo entre si,
então consideraria uma app por vez.

**O que eu faria diferente:**
Acho que não faria diferente, talvez testar melhor a skill para registrar commits e fazer push, que gerou um pouco mais do que eu gostaria no inicio.

**A coisa mais desconfortável que aprendi sobre como eu trabalho com IA:**
Ao mesmo tempo que é rápida e automatiza, precisa de maturidade na supervisão.