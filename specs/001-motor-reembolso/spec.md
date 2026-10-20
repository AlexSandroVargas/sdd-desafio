# Spec — Motor de Cálculo de Reembolso

**Versão:** 1.2 · **Status:** rascunho · **Última alteração:** 2026-10-18

> **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ. Nenhuma linha
> aqui pode citar linguagem, biblioteca, classe, função ou estrutura de pasta.
> Se apareceu solução, o lugar dela é o `plan.md`.
>
> **Teste de aceitação da própria spec:** uma pessoa que nunca viu o projeto
> consegue, lendo só este arquivo, verificar se o sistema está correto?
>
> **Mudança vigente:** a política de reembolso passou para a versão 4 (v4).
> Os limites deixam de ser únicos para toda a empresa e passam a variar por
> centro de custo. A entrada passa a admitir despesas em moeda estrangeira. Esta
> spec reflete essas mudanças e as novas ambiguidades que elas trouxeram.

---

## 1. Problema

O financeiro da empresa reembolsa despesas de colaboradores de forma manual,
conferindo cada item contra a política do RH. O processo é lento, propenso a
inconsistências e não deixa rastro claro de por que uma despesa foi aceita,
recusada ou pagada parcialmente.

## 2. Objetivo

Criar um motor de cálculo que, dado o conjunto de despesas de um colaborador
num período, determine o valor reembolsável de cada item, justifique cada
decisão e apresente o total devido ao colaborador.

## Clarifications

### Session 2026-10-18

- Q: A própria despesa de hospedagem deve receber o limite ampliado de R$ 375,00 por diária nos dias considerados de viagem? → A: Sim, hospedagem recebe R$ 375,00 por diária.
- Q: Quando várias despesas da mesma categoria no mesmo dia ultrapassarem o limite, como o valor disponível deve ser distribuído? → A: Aplicação sequencial por valor declarado decrescente.

## 3. Fora de escopo

- Não faz interface web, mobile ou formulário de lançamento. A entrada é um
  JSON e a saída é um JSON.
- Não faz pagamento, transferência bancária ou integração com sistema
  financeiro.
- Não faz aprovação hierárquica, análise humana ou workflow de revisão.
- Não valida CNPJ do fornecedor, CPF do colaborador ou dados fiscais.
- Não corrige ou completa despesas com campos faltantes: registra o erro e
  continua processando as demais.
- Não emite nota fiscal; a entrada já informa se a nota existe.

## 4. Entrada e saída

**Entrada:** conforme `exemplos/despesas-exemplo.json`. Campos e significado:

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `colaborador.id` | string | Identificador único do colaborador | sim |
| `colaborador.nome` | string | Nome do colaborador | sim |
| `colaborador.centro_custo` | string | Centro de custo do colaborador | sim |
| `periodo.competencia` | string | Mês de competência no formato `YYYY-MM` | sim |
| `periodo.inicio` | string | Data inicial do período no formato `YYYY-MM-DD` | sim |
| `periodo.fim` | string | Data final do período no formato `YYYY-MM-DD` | sim |
| `despesas` | array | Lista de despesas do colaborador | sim |
| `despesas[].id` | string | Identificador único da despesa | sim |
| `despesas[].data` | string | Data da despesa no formato `YYYY-MM-DD` | sim |
| `despesas[].categoria` | string | Categoria da despesa | sim |
| `despesas[].descricao` | string | Descrição livre da despesa | sim |
| `despesas[].fornecedor` | string | Nome do fornecedor | sim |
| `despesas[].valor` | número | Valor declarado da despesa na moeda informada | sim |
| `despesas[].moeda` | string | Código ISO 4217 da moeda da despesa; quando ausente, assume-se `BRL` | não |
| `despesas[].tem_nota_fiscal` | boolean | Indica se há nota fiscal | sim |

**Saída:** definida por este spec. Estrutura e significado de cada campo:

| Campo | Tipo | Significado |
|---|---|---|
| `colaborador` | objeto | Dados do colaborador, iguais à entrada |
| `periodo` | objeto | Dados do período, iguais à entrada |
| `resumo.total_declarado` | número | Soma dos valores declarados de todas as despesas |
| `resumo.total_reembolsavel` | número | Soma dos valores efetivamente reembolsáveis |
| `resumo.total_nao_reembolsavel` | número | Soma dos valores acima dos limites (excedentes não pagos) e dos valores de despesas com status `nao_reembolsavel` |
| `resumo.total_rejeitado` | número | Soma dos valores de despesas inteiramente recusadas |
| `resumo.quantidade_despesas` | número | Quantidade total de despesas processadas |
| `despesas` | array | Lista de despesas com resultado do cálculo |
| `despesas[].id` | string | Identificador da despesa |
| `despesas[].data` | string | Data da despesa |
| `despesas[].categoria` | string | Categoria da despesa |
| `despesas[].valor_declarado` | número | Valor declarado original |
| `despesas[].valor_reembolsavel` | número | Valor que será reembolsado |
| `despesas[].valor_nao_reembolsavel` | número | Parte do valor declarado que não será reembolsada |
| `despesas[].status` | string | `aprovado`, `parcial`, `nao_reembolsavel`, `rejeitado` ou `estorno` |
| `despesas[].motivo` | string | Justificativa da decisão |
| `alertas` | array | Alertas transversais, como duplicatas |
| `alertas[].tipo` | string | Tipo do alerta, ex.: `duplicata` |
| `alertas[].despesas` | array | Identificadores das despesas envolvidas |

Exemplo de saída para uma entrada pequena:

```json
{
  "colaborador": { "id": "c-0001", "nome": "Ana", "centro_custo": "CC-001" },
  "periodo": { "competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31" },
  "resumo": {
    "total_declarado": 172.50,
    "total_reembolsavel": 80.00,
    "total_nao_reembolsavel": 12.50,
    "total_rejeitado": 80.00,
    "quantidade_despesas": 3
  },
  "despesas": [
    {
      "id": "d-01",
      "data": "2026-07-03",
      "categoria": "alimentacao",
      "valor_declarado": 72.50,
      "valor_reembolsavel": 60.00,
      "valor_nao_reembolsavel": 12.50,
      "status": "parcial",
      "motivo": "Limite diário de alimentação excedido"
    },
    {
      "id": "d-02",
      "data": "2026-07-06",
      "categoria": "transporte_urbano",
      "valor_declarado": 100.01,
      "valor_reembolsavel": 0,
      "valor_nao_reembolsavel": 0,
      "status": "rejeitado",
      "motivo": "Nota fiscal obrigatória acima de R$ 100,00 ausente"
    },
    {
      "id": "d-03",
      "data": "2026-07-11",
      "categoria": "transporte_urbano",
      "valor_declarado": -45.00,
      "valor_reembolsavel": 0,
      "valor_nao_reembolsavel": 0,
      "status": "estorno",
      "motivo": "Estorno reduz o total reembolsável do período"
    }
  ],
  "alertas": []
}
```

## 5. Regras de negócio

Cada regra recebe um ID (`RN-001`, ...). As tasks vão referenciar esses IDs.

### RN-001 — Limite diário de alimentação

**Regra:** O valor reembolsável das despesas da categoria `alimentacao` em uma
mesma data é limitado ao teto diário definido na tabela do centro de custo do
colaborador. Quando a data da despesa é um dia de viagem, o teto sobe em 50%.
As despesas do dia são ordenadas por valor declarado decrescente (empate
preserva a ordem de entrada); o teto é aplicado sequencialmente: cada despesa é
reembolsada integralmente enquanto couber no teto restante; a primeira que não
couber integralmente recebe o valor restante como reembolso parcial; as demais
são rejeitadas.
**Origem:** política do RH v4, item A (com AMB-001, AMB-003, AMB-005 e AMB-011)
**Aceite:** colaborador do `CC-ADM` (teto de alimentação R$ 45,00) com duas
refeições de R$ 72,50 e R$ 38,00 no mesmo dia → ordenadas como R$ 72,50 e R$ 38,00;
limite R$ 45,00; a primeira recebe R$ 45,00 (parcial) e a segunda é rejeitada.

### RN-002 — Limite diário de transporte urbano

**Regra:** O valor reembolsável das despesas da categoria `transporte_urbano` em
uma mesma data é limitado ao teto diário definido na tabela do centro de custo
do colaborador. Quando a data da despesa é um dia de viagem, o teto sobe em 50%.
As despesas do dia são ordenadas por valor declarado decrescente (empate
preserva a ordem de entrada); o teto é aplicado sequencialmente: cada despesa é
reembolsada integralmente enquanto couber no teto restante; a primeira que não
couber integralmente recebe o valor restante como reembolso parcial; as demais
são rejeitadas.
**Origem:** política do RH v4, item A (com AMB-001, AMB-003, AMB-005 e AMB-011)
**Aceite:** colaborador do `CC-COMERCIAL` (teto de transporte R$ 150,00) com uma
corrida de R$ 100,00 no dia → reembolsável R$ 100,00, não reembolsável R$ 0,00.

### RN-003 — Limite de hospedagem por diária

**Regra:** O valor reembolsável de uma despesa de hospedagem é limitado ao teto
por diária definido na tabela do centro de custo do colaborador multiplicado
pelo número de diárias indicado na descrição; quando não houver indicação,
considera-se uma única diária. Quando a hospedagem corresponde a dias de viagem,
o limite por diária sobe em 50%. Se o teto por diária do centro de custo for zero,
a hospedagem não é reembolsável e recebe status `nao_reembolsavel`. O excedente
é não reembolsável e recebe status `parcial`.
**Origem:** política do RH v4, itens A e B (com AMB-002, AMB-005, AMB-011 e AMB-013)
**Aceite:** colaborador do `CC-ENG-PLATAFORMA` (hospedagem não reembolsável) com
despesa de R$ 800,00 descrita como "Hotel - 2 diarias" em dia de viagem →
reembolsável R$ 0,00, não reembolsável R$ 800,00, status `nao_reembolsavel`.

### RN-004 — Nota fiscal obrigatória acima de R$ 100,00

**Regra:** Toda despesa cujo valor em BRL seja estritamente superior a R$ 100,00
e sem nota fiscal (`tem_nota_fiscal` = `false`) é rejeitada, com valor
reembolsável zero. Despesas de exatamente R$ 100,00 ou menos (após conversão para
BRL, quando aplicável) não exigem nota. A conversão para BRL, quando necessária,
segue a RN-011.
**Origem:** política do RH v4, item 5 (com AMB-004, AMB-011 e AMB-015)
**Aceite:** uma refeição de EUR 22,00 sem nota em data com taxa EUR 5,93 → valor
em BRL R$ 130,46; rejeitada por falta de nota. Uma corrida de R$ 100,00 sem nota
→ pode ser reembolsada dentro do limite diário.

### RN-005 — Limites ampliados em viagem

**Regra:** A ampliação de limites obedece ao percentual definido na política do
centro de custo para dias "em viagem". A verificação de viagem ocorre em duas
etapas, nesta ordem:

1. **Moeda estrangeira:** se houver pelo menos uma despesa declarada em moeda
   estrangeira no dia, esse dia é considerado dia de viagem
   internacional. Nesse caso, os limites de todas as despesas elegíveis neste dia são
   ampliados pelo percentual de viagem da política, sem necessidade de outro
   indicador de viagem.
2. **Moeda nacional:** na ausência de qualquer despesa em moeda estrangeira, a
   verificação segue os critérios originais de viagem. Em hospedagem nacional,
   são dias de viagem o check-in e os dias de hospedagem contados a partir dele;
   se a descrição não informar check-in, usa-se a data da hospedagem, apoiada
   por transporte para aeroporto ou hotel na mesma data, quando disponível. Em
   hospedagem internacional, identificada pela menção `internacional` na
   descrição, também pode ser dia de viagem a véspera do check-in e o dia
   posterior ao último dia de hospedagem ou checkout, desde que haja, na
   respectiva data adjacente, uma despesa de transporte urbano cuja descrição
   mencione aeroporto ou hotel. Sem a menção `internacional`, a hospedagem é
   nacional. Check-in e checkout informados na descrição prevalecem sobre a data
   da despesa e a quantidade de diárias; sem checkout, o último dia é obtido pela
   quantidade de diárias, assumindo uma quando não informada. Somente datas dentro
   do período de competência recebem ampliação.
**Origem:** política do RH v4, itens A e B (com AMB-005)
**Aceite:** colaborador do `CC-COMERCIAL` (alimentação R$ 90,00) com uma despesa
em EUR no período → todos os limites ampliados em 50%. Colaborador do
`CC-COMERCIAL` em hospedagem nacional de duas diárias com check-in em 10/07, sem
moeda estrangeira → limite ampliado para R$ 135,00 somente em 10/07 e 11/07.

### RN-006 — Tratamento de duplicatas

**Regra:** Despesas com mesma data, categoria, valor e fornecedor são
duplicatas. Mantém-se apenas a primeira ocorrência para fins de reembolso; as
demais são rejeitadas como duplicatas e não consomem limites diários.
**Origem:** política do RH, item 8 (com AMB-006)
**Aceite:** duas despesas idênticas de R$ 54,90 no mesmo dia → a primeira é
processada normalmente e a segunda é rejeitada.

### RN-007 — Período de competência

**Regra:** Apenas despesas com data entre `periodo.inicio` e `periodo.fim`,
ambos inclusive, são elegíveis. Despesas fora desse intervalo são rejeitadas e
não consomem limites diários.
**Origem:** política do RH, item 7 (com AMB-007)
**Aceite:** despesa de R$ 41,00 em abril dentro de um período de julho →
rejeitada com motivo "fora do período de competência".

### RN-008 — Categorias fora da política

**Regra:** As categorias reembolsáveis são aquelas listadas na tabela do centro de
custo do colaborador. Se o centro de custo não tiver tabela própria, aplicam-se
as categorias da política padrão (`alimentacao`, `transporte_urbano` e
`hospedagem`). A comparação é case-insensitive. Qualquer outra categoria é
rejeitada como fora da política. A categoria `representacao` é reembolsável
apenas quando presente na tabela do centro de custo.
**Origem:** política do RH v4, item A (com AMB-008, AMB-011 e AMB-012)
**Aceite:** despesa da categoria `coworking` em qualquer centro de custo →
rejeitada; despesa da categoria `representacao` no `CC-COMERCIAL` → reembolsável
com teto próprio; despesa da categoria `representacao` no `CC-ADM` → rejeitada;
despesa da categoria `ALIMENTACAO` → tratada como `alimentacao`.

### RN-009 — Estornos

**Regra:** Despesas com valor declarado negativo são estornos. Não são
reembolsáveis individualmente, mas reduzem o total reembolsável do período. Não
consomem limites diários.
**Origem:** gap identificado no exemplo (com AMB-009)
**Aceite:** uma despesa de transporte de R$ -45,00 → status `estorno`, total
reembolsável do período reduzido em R$ 45,00.

### RN-010 — Precisão monetária

**Regra:** Valores reembolsáveis e não reembolsáveis são arredondados para
duas casas decimais, usando arredondamento half-up. O valor declarado é
preservado sem alteração.
**Origem:** gap identificado no exemplo (com AMB-010)
**Aceite:** despesa de R$ 33,333 declarada → valor reembolsável arredondado
para R$ 33,33.

### RN-011 — Conversão de moeda estrangeira

**Regra:** Despesas informadas com `moeda` diferente de `BRL` são convertidas
para reais antes de qualquer comparação com limites ou com o limiar de nota
fiscal. A conversão usa a taxa de câmbio da data da despesa publicada na tabela
de câmbio. O valor reembolsável é sempre devolvido em BRL. Quando `moeda` não for
informada, assume-se `BRL`.
**Origem:** política do RH v4, item B (com AMB-014 e AMB-015)
**Aceite:** despesa de EUR 22,00 em 2026-07-14 com taxa EUR 5,93 → valor em BRL
R$ 130,46; compara-se a esse valor os limites e o limiar de nota fiscal.

### RN-012 — Taxa de câmbio ausente

**Regra:** Se a data da despesa não possuir taxa publicada para a moeda
informada, a despesa é rejeitada com motivo indicando ausência de cotação. A
rejeição ocorre antes da aplicação dos demais limites.
**Origem:** política do RH v4, item B (com AMB-014)
**Aceite:** despesa de GBP 55,00 em data sem cotação para GBP → rejeitada com
motivo "moeda ou data sem cotação disponível".

---

## 6. Ambiguidades identificadas e decisões

> **Esta seção é o coração da spec e vale a maior parte dos 25 pontos do critério 1.**
> Uma ambiguidade que você resolveu no código sem registrar aqui conta como
> não resolvida.

### AMB-001 — "por dia" nas categorias alimentação e transporte

**Texto original do RH:** "Alimentação tem limite de R$ 60 por dia" e
"Transporte urbano tem limite de R$ 80 por dia"
**O que não está claro:** O limite se aplica por despesa ou pelo total das
despesas do dia? Se for por dia, duas refeições no mesmo dia somam ou cada uma
tem limite próprio? Como dividir o reembolso entre várias despesas do mesmo dia
quando o total ultrapassa o limite?
**Decisão:** O limite é agregado por categoria e por data. Todas as despesas da
mesma categoria no mesmo dia competem pelo teto diário e são ordenadas por valor
declarado decrescente, preservando a ordem de entrada em caso de empate. O teto
é aplicado sequencialmente: cada item recebe o valor integral enquanto houver
saldo; o primeiro item que exceder o saldo recebe o restante, e os seguintes são
rejeitados.
**Justificativa:** Evita abuso por meio de múltiplos lançamentos pequenos e torna
a distribuição determinística, auditável e consistente com o tratamento de
reembolso parcial.
**Regra afetada:** RN-001, RN-002

### AMB-002 — "por diária" na hospedagem

**Texto original do RH:** "Hospedagem tem limite de R$ 250 por diária"
**O que não está claro:** A entrada traz apenas o valor total da estadia, sem
um campo que diga quantas diárias foram pagas. Quantas diárias cada despesa de
hospedagem representa?
**Decisão:** O número de diárias é inferido a partir da descrição quando ela
contiver uma indicação explícita (por exemplo, "2 diárias", "3 noites"). Caso a
descrição não indique quantidade, considera-se uma única diária.
**Justificativa:** A descrição é o único dado disponível na entrada para
identificar estadias longas; sem essa regra, o limite por diária fica
inaplicável e a política perde o sentido para viagens.
**Regra afetada:** RN-003

### AMB-003 — "reembolsadas parcialmente"

**Texto original do RH:** "Despesas acima do limite são reembolsadas parcialmente"
**O que não está claro:** "Parcialmente" significa pagar o limite e cortar o
excedente, ou recusar o item inteiro? E se várias despesas do mesmo dia
ultrapassarem o limite em conjunto, como se distribui o valor do teto?
**Decisão:** O sistema reembolsa até o limite aplicável e descarta o excedente;
não recusa o item inteiro. No agrupamento diário, as despesas são ordenadas por
valor declarado decrescente (empate preserva a ordem de entrada). O teto é
aplicado sequencialmente: cada despesa é reembolsada integralmente enquanto
couber no teto restante; a primeira que não couber integralmente recebe o valor
restante como reembolso parcial; todas as demais despesas do agrupamento são
rejeitadas. Para hospedagem, que não usa agrupamento diário, mantém-se o limite
por diária individual.
**Justificativa:** A palavra "parcialmente" implica pagamento parcial, não
recusa total; ordenar por valor decrescente prioriza as despesas maiores e
torna a aplicação do teto determinística, auditável e previsível para o
usuário.
**Regra afetada:** RN-001, RN-002, RN-003

### AMB-004 — "acima de R$ 100" na nota fiscal

**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100"
**O que não está claro:** "Acima" inclui o valor exato de R$ 100,00? O limiar
se aplica ao valor declarado ou ao valor reembolsável após os limites? Se faltar
nota, recusa-se a despesa inteira ou apenas o valor acima de R$ 100?
**Decisão:** "Acima de R$ 100" significa valor declarado estritamente maior que
R$ 100,00; portanto, R$ 100,00 não exige nota. Se o valor declarado for superior
a R$ 100,00 e não houver nota, a despesa inteira é recusada.
**Justificativa:** Clareza operacional: um centavo acima do limiar já exige
comprovação; recusar o item inteiro é mais simples de auditar do que reembolsar
parcialmente sem nota.
**Regra afetada:** RN-004

### AMB-005 — "em viagem"

**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%"
**O que não está claro:** A entrada não possui um campo `em_viagem`. Como o
sistema deve determinar quais datas são dias de viagem? Como diferenciar viagens
nacionais e internacionais e tratar chegada e retorno?
**Decisão:** A ampliação é determinada por data, e não para todo o período. A
descrição da hospedagem informa, quando disponíveis, se a viagem é internacional
e as datas de check-in e checkout; a ausência de `internacional` indica viagem
nacional. Viagens nacionais abrangem somente os dias de hospedagem. Viagens
internacionais podem incluir a véspera e o dia posterior à hospedagem quando
existir transporte para aeroporto ou hotel exatamente nesses dias adjacentes.
Sem datas explícitas, a data da hospedagem inicia a contagem das diárias, e os
transportes adjacentes servem como evidência dos dias adicionais previstos.
**Justificativa:** Vincular a ampliação às datas efetivas evita elevar os limites
do mês inteiro por causa de uma única hospedagem, enquanto o transporte fornece
evidência objetiva para os dias de deslocamento internacional.
**Regra afetada:** RN-005

### AMB-006 — "duplicatas devem ser tratadas"

**Texto original do RH:** "Duplicatas devem ser tratadas"
**O que não está claro:** O que caracteriza uma duplicata — mesmo ID, mesma
data, mesma categoria, mesmo valor, mesmo fornecedor? E qual é o tratamento:
rejeitar, ignorar, mesclar ou marcar sem recusar?
**Decisão:** Duplicata é uma segunda despesa com mesma data, categoria, valor e
fornecedor. A primeira ocorrência é processada normalmente; as seguintes são
rejeitadas como duplicatas e não consomem limites diários.
**Justificativa:** Evita reembolso duplo de lançamentos repetidos; usar data,
categoria, valor e fornecedor captura erros de digitação sem bloquear despesas
legítimas no mesmo dia.
**Regra afetada:** RN-006

### AMB-007 — "dentro do período de competência"

**Texto original do RH:** "Despesas devem ser lançadas dentro do período de competência"
**O que não está claro:** Despesas fora do período são ignoradas, recusadas ou
reembolsadas mesmo assim? Elas consomem limites diários do período?
**Decisão:** Despesas com data anterior a `periodo.inicio` ou posterior a
`periodo.fim` são rejeitadas e não consomem limites diários.
**Justificativa:** Garante que o reembolso respeite o período informado;
incluir fora do período nos limites distorceria o controle do mês.
**Regra afetada:** RN-007

### AMB-008 — categorias fora da política

**Texto original do RH:** "Categorias fora da política não são reembolsáveis"
**O que não está claro:** Quais categorias estão cobertas? Variações de caixa
(por exemplo, "ALIMENTACAO" maiúsculo) e erros de digitação são considerados
fora da política? A lista muda com a política v4 por centro de custo.
**Decisão:** As categorias reembolsáveis são aquelas listadas na tabela do centro
de custo do colaborador (ou no `padrao`, quando o centro não tem tabela), com
comparação case-insensitive. O `padrao` da v4 cobre `alimentacao`,
`transporte_urbano` e `hospedagem`; o `CC-COMERCIAL` adiciona `representacao`.
Qualquer outro valor é considerado fora da política e não reembolsável.
**Justificativa:** Tolerância a variação de digitação reduz suporte operacional;
usar a tabela do centro preserva a flexibilidade introduzida pela v4 sem
expandir o escopo arbitrariamente.
**Regra afetada:** RN-008

### AMB-009 — valores negativos

**Texto original do RH:** *não menciona valores negativos*
**O que não está claro:** A política fala apenas em despesas. O exemplo contém
um valor negativo (-45,00), provavelmente um estorno. Como ele afeta o cálculo?
**Decisão:** Valores negativos são aceitos como estornos. Não são reembolsáveis
individualmente, mas reduzem o total reembolsável do período e não consomem
limites diários.
**Justificativa:** Estornos são comuns em cartões corporativos; subtrair do
total reflete o saldo líquido devido ao colaborador.
**Regra afetada:** RN-009

### AMB-010 — arredondamento de centavos

**Texto original do RH:** *não menciona arredondamento*
**O que não está claro:** O exemplo inclui um valor com três casas decimais
(R$ 33,333). Como o sistema arredonda para centavos?
**Decisão:** Todos os valores reembolsáveis e não reembolsáveis são arredondados
para duas casas decimais usando arredondamento half-up. O valor declarado é
preservado sem alteração.
**Justificativa:** Moeda real trabalha em centavos; half-up é o padrão contábil
mais comum e evita viés sistemático para baixo ou para cima.
**Regra afetada:** RN-010

### AMB-011 — "aplica-se a política padrão" para centros de custo desconhecidos

**Texto original do RH:** "Alguns centros de custo não têm entrada na tabela. Nesse caso, aplica-se a política padrão."
**O que não está claro:** A política padrão contém apenas `alimentacao`,
`transporte_urbano` e `hospedagem`. Se um colaborador de centro sem tabela
lançar `representacao` ou outra categoria extra, ela é reembolsável? Os limites
são os da política padrão ou da tabela do centro (que não existe)?
**Decisão:** Centro de custo sem entrada na tabela usa o bloco `padrao` da
política v4. Portanto, somente `alimentacao`, `transporte_urbano` e `hospedagem`
são reembolsáveis, com os limites do `padrao`. Categorias ausentes do `padrao`
são rejeitadas como fora da política.
**Justificativa:** O comunicado diz explicitamente "aplica-se a política padrão";
usar qualquer outra interpretação criaria limites inexistentes para centros
fora da tabela.
**Regra afetada:** RN-001, RN-002, RN-003, RN-008

### AMB-012 — Categorias não listadas no centro de custo

**Texto original do RH:** Cada centro de custo tem "a sua tabela".
**O que não está claro:** Se uma categoria não consta na tabela do centro, mas
consta no `padrao`, o colaborador pode reembolsá-la? E se constar na tabela com
limite zero?
**Decisão:** A lista de categorias reembolsáveis de um centro é exatamente a
união das categorias presentes na sua tabela (ou no `padrao`, quando o centro
não tem tabela). Uma categoria com limite zero dentro da tabela não é
reembolsável, mas é reconhecida como categoria válida; o valor inteiro fica
não reembolsável em vez de ser rejeitado como fora da política.
**Justificativa:** Distingue "não reembolsável por política do centro" de "não
reconhecida como categoria"; isso mantém a justificativa correta no resultado.
**Regra afetada:** RN-003, RN-008

### AMB-013 — Limite zero na hospedagem do CC-ENG-PLATAFORMA

**Texto original do RH:** "`CC-ENG-PLATAFORMA` não reembolsa `hospedagem` de forma alguma."
**O que não está claro:** O limite zero deve ser tratado como rejeição total ou
como categoria reconhecida mas inteiramente não reembolsável?
**Decisão:** A hospedagem é reconhecida como categoria válida, mas o valor
reembolsável é zero e o valor declarado inteiro é classificado como não
reembolsável. O status da despesa é `nao_reembolsavel`.
**Justificativa:** A categoria existe na tabela do centro; a política apenas diz
que não reembolsa, não que proíbe o lançamento. O status `nao_reembolsavel`
distingue o caso de uma categoria permitida que, por regra do centro, gera valor
zero de reembolso, separando-o de rejeição de categoria e de reembolso parcial.
**Regra afetada:** RN-003

### AMB-014 — "Taxa da data da despesa" sem cotação publicada

**Texto original do RH:** "A conversão usa a taxa da data da despesa. As taxas
estão em `cambio.json`."
**O que não está claro:** O arquivo de câmbio só publica cotações em dias úteis
bancários. E se a despesa cair em fim de semana, feriado ou em data futura? E se
a moeda não estiver listada na data?
**Decisão:** Se não existir cotação para a moeda na data exata da despesa, a
despesa é rejeitada. Não se faz interpolação, uso de taxa do dia anterior ou
taxa padrão.
**Justificativa:** Interpolação introduziria decisões adicionais sem respaldo na
política. Rejeitar é previsível e audita o problema na entrada.
**Regra afetada:** RN-011, RN-012

### AMB-015 — Limiar de nota fiscal em moeda estrangeira

**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100".
**O que não está claro:** O limiar se aplica ao valor original na moeda
estrangeira ou ao valor convertido para BRL?
**Decisão:** O limiar de R$ 100,00 é aplicado ao valor em BRL após conversão pela
taxa da data da despesa.
**Justificativa:** Os limites da política são sempre em BRL; manter o limiar na
mesma moeda evita comparações mistas e reflete o risco fiscal real.
**Regra afetada:** RN-004, RN-011

---

## 7. Casos de borda

| Caso | Entrada | Comportamento esperado | Regra |
|---|---|---|---|
| Duas refeições no mesmo dia | `alimentacao` de R$ 72,50 e R$ 38,00 na mesma data | Ordenadas R$ 72,50 e R$ 38,00; limite R$ 60,00; primeira recebe R$ 60,00 (parcial) e segunda é rejeitada | RN-001 |
| Duas refeições em dia de hospedagem | `alimentacao` de R$ 72,50 e R$ 38,00 em um dia abrangido pela hospedagem | Limite R$ 90,00; primeira recebe R$ 72,50; segunda recebe R$ 17,50 (parcial); excedente R$ 20,50 rejeitado | RN-001, RN-005 |
| Alimentação fora dos dias hospedados | Hospedagem nacional de 10/07 a 11/07 e alimentação em 12/07 | Aplica limite normal de R$ 60,00 em 12/07 | RN-001, RN-005 |
| Deslocamento internacional adjacente | Hospedagem internacional de 10/07 a 11/07 e transportes para aeroporto em 09/07 e 12/07 | 09/07 e 12/07 também recebem limites ampliados | RN-005 |
| Internacional sem transporte adjacente | Hospedagem internacional de 10/07 a 11/07 sem transporte em 09/07 ou 12/07 | Somente 10/07 e 11/07 recebem limites ampliados | RN-005 |
| Transporte exatamente no limiar da nota | `transporte_urbano` de R$ 100,00 sem nota | Reembolsável dentro do limite diário, pois R$ 100,00 não exige nota | RN-002, RN-004 |
| Transporte um centavo acima do limiar | `transporte_urbano` de R$ 100,01 sem nota | Rejeitado por falta de nota | RN-004 |
| Hospedagem com várias diárias | `hospedagem` de R$ 800,00 descrita como "2 diárias" em dias de viagem | Limite ampliado de R$ 750,00; reembolsável R$ 750,00 | RN-003, RN-005 |
| Hospedagem sem indicação de diárias | `hospedagem` de R$ 300,00 sem indicação de diárias | Considera 1 diária; limite R$ 250,00; reembolsável R$ 250,00 | RN-003 |
| Despesa fora do período | `alimentacao` de R$ 41,00 em data fora de `inicio`/`fim` | Rejeitada; não entra nos limites | RN-007 |
| Categoria desconhecida | `coworking` de R$ 89,00 | Rejeitada como fora da política | RN-008 |
| Categoria com caixa diferente | `ALIMENTACAO` de R$ 61,00 | Tratada como `alimentacao`; reembolsável dentro do limite | RN-008 |
| Duplicata exata | Duas despesas idênticas de `alimentacao` R$ 54,90 no mesmo dia | Primeira processada; segunda rejeitada como duplicata | RN-006 |
| Estorno dentro do período | `transporte_urbano` de R$ -45,00 | Reduz total reembolsável; não consome limite | RN-009 |
| Valor com três decimais | `alimentacao` de R$ 33,333 | Reembolsável arredondado para R$ 33,33 | RN-010 |
| Ausência total de nota em valor baixo | `alimentacao` de R$ 50,00 sem nota | Reembolsável dentro do limite | RN-004 |
| Centro com tabela própria | Colaborador do `CC-COMERCIAL` com `representacao` de R$ 300,00 | Reembolsável dentro do limite de representação | RN-008, RN-011 |
| Centro sem tabela (`CC-SUPORTE-N2`) | `representacao` de R$ 190,00 | Rejeitada como categoria fora da política padrão | RN-008, AMB-011 |
| Hospedagem proibida no centro | `CC-ENG-PLATAFORMA` com `hospedagem` de R$ 310,00 | Valor todo não reembolsável; status `nao_reembolsavel` | RN-003, AMB-013 |
| Despesa em moeda estrangeira conhecida | `alimentacao` de EUR 22,00 em 2026-07-14 | Convertido para BRL (R$ 130,46) e depois limitado | RN-011 |
| Despesa em moeda estrangeira sem cotação | `representacao` de GBP 55,00 em data sem cotação GBP | Rejeitada por ausência de cotação | RN-012 |
| Nota fiscal acima do limiar após conversão | Transporte de USD 25,00 sem nota em data com taxa USD 5,50 | Valor em BRL R$ 137,50 > R$ 100 → rejeitado | RN-004, RN-011 |

## 8. Ordem de aplicação das regras

A ordem abaixo garante que uma despesa seja descartada o mais cedo possível e
que limites diários sejam calculados apenas sobre despesas realmente elegíveis.

1. **RN-008 — Categorias fora da política:** verifica se a categoria consta na
   tabela do centro de custo (ou na política padrão, se o centro não tiver
   tabela). Se não for reembolsável, rejeita e para.
2. **RN-007 — Período de competência:** verifica se a data está dentro do
   intervalo. Se não estiver, rejeita e para.
3. **RN-011 e RN-012 — Conversão cambial:** converte o valor declarado para BRL
   usando a taxa da data da despesa; se não houver cotação, rejeita e para.
4. **RN-004 — Nota fiscal:** verifica se o valor em BRL é maior que R$ 100,00 e
   se há nota. Se não houver, rejeita e para.
5. **RN-006 — Duplicatas:** verifica se a despesa é duplicata de outra já
   processada. Se for, rejeita e para.
6. **RN-009 — Estornos:** valores negativos válidos são marcados como estorno e
   reduzem o total do período; não entram nos limites diários.
7. **RN-005 — Viagem:** determina os dias de hospedagem e, em viagens
   internacionais, valida transportes nos dias adjacentes para definir em quais
   datas os limites são ampliados.
8. **RN-001, RN-002 e RN-003 — Limites:** aplica os tetos diários e por diária
   do centro de custo sobre as despesas restantes.
9. **RN-010 — Precisão monetária:** arredonda os valores finais para duas casas
   decimais.

## 9. Critérios de aceite

O sistema está pronto quando:

- [ ] Para cada despesa da entrada, a saída informa o valor reembolsável, o
  valor não reembolsável, o status e a justificativa.
- [ ] O total reembolsável do período é a soma dos valores reembolsáveis das
  despesas, menos os estornos.
- [ ] Despesas acima do limite diário são parcialmente reembolsadas até o
  limite; a despesa que faz o teto ser atingido recebe o valor restante, e as
  demais despesas do mesmo agrupamento são rejeitadas.
- [ ] Despesas acima de R$ 100,00 sem nota fiscal são inteiramente recusadas.
- [ ] Duplicatas de mesma data, categoria, valor e fornecedor são recusadas,
  mantendo apenas a primeira.
- [ ] Despesas fora do período de competência são recusadas e não consomem
  limites.
- [ ] Categorias fora da política são recusadas; a lista de categorias
  reembolsáveis obedece à tabela do centro de custo ou à política padrão.
- [ ] Categorias presentes na tabela do centro de custo, mesmo com limite zero,
  são tratadas como válidas e têm o valor não reembolsável separado do valor
  rejeitado, com status `nao_reembolsavel` quando o reembolso for zero.
- [ ] Somente despesas em dias de hospedagem têm limites ampliados em 50% sobre
  o teto do centro de custo; em viagens internacionais, a véspera e o dia
  posterior também são ampliados quando comprovados por transporte para
  aeroporto ou hotel na data adjacente.
- [ ] Estornos reduzem o total reembolsável do período.
- [ ] Todos os valores são arredondados para duas casas decimais.
- [ ] Despesas em moeda estrangeira são convertidas para BRL pela taxa da data
  da despesa antes de qualquer comparação com limites ou limiar de nota fiscal.
- [ ] Despesas em moeda ou data sem cotação disponível são rejeitadas com
  justificativa clara.

## 10. O que fica em aberto

- A detecção de viagem depende da descrição livre da hospedagem para identificar
  `internacional`, check-in e checkout. Campos estruturados poderão substituir
  essa convenção sem alterar os períodos de viagem definidos na RN-005.
- A extração do número de diárias a partir da descrição é uma convenção
  provisória. O ideal seria um campo dedicado na entrada.
- Despesas com campos obrigatórios ausentes ou mal formatados serão rejeitadas
  com erro estrutural, mas o tratamento detalhado de erros de schema será
  definido no `plan.md`.
- Fila de aprovação manual para itens acima de R$ 500,00 reembolsáveis (item C do
  comunicado v4) permanece **fora de escopo** nesta versão. Se for incluída, a
  saída passará a ter um status adicional de `pendente` e o campo
  `valor_reembolsavel` passará a representar um valor condicional, não garantido.
