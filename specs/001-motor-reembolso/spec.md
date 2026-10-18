# Spec — Motor de Cálculo de Reembolso

**Versão:** 1.1 · **Status:** rascunho · **Última alteração:** 2026-10-18

> **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ. Nenhuma linha
> aqui pode citar linguagem, biblioteca, classe, função ou estrutura de pasta.
> Se apareceu solução, o lugar dela é o `plan.md`.
>
> **Teste de aceitação da própria spec:** uma pessoa que nunca viu o projeto
> consegue, lendo só este arquivo, verificar se o sistema está correto?

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
| `despesas[].valor` | número | Valor declarado da despesa | sim |
| `despesas[].tem_nota_fiscal` | boolean | Indica se há nota fiscal | sim |

**Saída:** definida por este spec. Estrutura e significado de cada campo:

| Campo | Tipo | Significado |
|---|---|---|
| `colaborador` | objeto | Dados do colaborador, iguais à entrada |
| `periodo` | objeto | Dados do período, iguais à entrada |
| `resumo.total_declarado` | número | Soma dos valores declarados de todas as despesas |
| `resumo.total_reembolsavel` | número | Soma dos valores efetivamente reembolsáveis |
| `resumo.total_nao_reembolsavel` | número | Soma dos valores acima dos limites, excedentes não pagos |
| `resumo.total_rejeitado` | número | Soma dos valores de despesas inteiramente recusadas |
| `resumo.quantidade_despesas` | número | Quantidade total de despesas processadas |
| `despesas` | array | Lista de despesas com resultado do cálculo |
| `despesas[].id` | string | Identificador da despesa |
| `despesas[].data` | string | Data da despesa |
| `despesas[].categoria` | string | Categoria da despesa |
| `despesas[].valor_declarado` | número | Valor declarado original |
| `despesas[].valor_reembolsavel` | número | Valor que será reembolsado |
| `despesas[].valor_nao_reembolsavel` | número | Parte do valor declarado que não será reembolsada |
| `despesas[].status` | string | `aprovado`, `parcial`, `rejeitado` ou `estorno` |
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
mesma data é limitado a R$ 60,00 por dia. Quando o colaborador está em viagem,
o limite sobe para R$ 90,00. As despesas do dia são ordenadas por valor
declarado decrescente (empate preserva a ordem de entrada); o teto é aplicado
sequencialmente: cada despesa é reembolsada integralmente enquanto couber no
teto restante; a primeira que não couber integralmente recebe o valor restante
como reembolso parcial; as demais são rejeitadas.
**Origem:** política do RH, itens 1 e 6 (com AMB-001, AMB-003 e AMB-005)
**Aceite:** duas refeições de R$ 72,50 e R$ 38,00 no mesmo dia → ordenadas como
R$ 72,50 e R$ 38,00; limite R$ 60,00; a primeira recebe R$ 60,00 (parcial) e a
segunda é rejeitada.

### RN-002 — Limite diário de transporte urbano

**Regra:** O valor reembolsável das despesas da categoria `transporte_urbano` em
uma mesma data é limitado a R$ 80,00 por dia. Quando o colaborador está em
viagem, o limite sobe para R$ 120,00. As despesas do dia são ordenadas por valor
declarado decrescente (empate preserva a ordem de entrada); o teto é aplicado
sequencialmente: cada despesa é reembolsada integralmente enquanto couber no
teto restante; a primeira que não couber integralmente recebe o valor restante
como reembolso parcial; as demais são rejeitadas.
**Origem:** política do RH, itens 2 e 6 (com AMB-001, AMB-003 e AMB-005)
**Aceite:** uma corrida de R$ 100,00 no dia → reembolsável R$ 80,00, não
reembolsável R$ 20,00.

### RN-003 — Limite de hospedagem por diária

**Regra:** O valor reembolsável de uma despesa de hospedagem é limitado a
R$ 250,00 multiplicado pelo número de diárias indicado na descrição; quando não
houver indicação, considera-se uma única diária. Em viagem, o limite por diária
sobe para R$ 375,00. O excedente é não reembolsável.
**Origem:** política do RH, itens 3 e 6 (com AMB-002 e AMB-005)
**Aceite:** despesa de R$ 480,00 descrita como "Hotel Rio - 2 diarias" → limite
R$ 500,00; reembolsável R$ 480,00.

### RN-004 — Nota fiscal obrigatória acima de R$ 100,00

**Regra:** Toda despesa com valor declarado estritamente superior a R$ 100,00 e
sem nota fiscal (`tem_nota_fiscal` = `false`) é rejeitada, com valor
reembolsável zero. Despesas de exatamente R$ 100,00 ou menos não exigem nota.
**Origem:** política do RH, item 5 (com AMB-004)
**Aceite:** uma corrida de R$ 100,01 sem nota → rejeitada; uma corrida de
R$ 100,00 sem nota → pode ser reembolsada dentro do limite diário.

### RN-005 — Limites ampliados em viagem

**Regra:** O colaborador é considerado em viagem quando houver ao menos uma
despesa da categoria `hospedagem` dentro do período de competência. Nesse caso,
os limites diários de alimentação, transporte urbano e hospedagem são aumentados
em 50%.
**Origem:** política do RH, item 6 (com AMB-005)
**Aceite:** presença de uma hospedagem no período → limite de alimentação passa
a R$ 90,00, transporte para R$ 120,00 e hospedagem para R$ 375,00 por diária.

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

**Regra:** Apenas as categorias `alimentacao`, `transporte_urbano` e
`hospedagem` são reembolsáveis. A comparação é case-insensitive. Qualquer outra
categoria é rejeitada como fora da política.
**Origem:** política do RH, item 9 (com AMB-008)
**Aceite:** despesa da categoria `coworking` → rejeitada; despesa da categoria
`ALIMENTACAO` → tratada como `alimentacao`.

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
mesma categoria no mesmo dia competem pelo teto diário. O valor reembolsável
acima do limite é distribuído proporcionalmente entre os itens do dia.
**Justificativa:** Evita abuso por meio de múltiplos lançamentos pequenos e
reflete a intenção de controle de gasto diário; a divisão proporcional é justa
com todas as despesas do dia.
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
sistema deve determinar que o colaborador está em viagem? Os limites ampliados
valem para todas as categorias?
**Decisão:** O colaborador é considerado em viagem quando houver ao menos uma
despesa de hospedagem dentro do período de competência. O acréscimo de 50%
aplica-se aos limites diários de alimentação, transporte urbano e hospedagem.
**Justificativa:** Hospedagem é o indicador objetivo de deslocamento disponível
na entrada; ampliar todas as categorias reflete o aumento real de custos durante
uma viagem.
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
fora da política?
**Decisão:** As categorias reembolsáveis são `alimentacao`, `transporte_urbano` e
`hospedagem`, comparadas de forma case-insensitive. Qualquer outro valor é
considerado fora da política e não reembolsável.
**Justificativa:** Tolerância a variação de digitação reduz suporte operacional;
restringir a três categorias evita expansão silenciosa do escopo.
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

---

## 7. Casos de borda

| Caso | Entrada | Comportamento esperado | Regra |
|---|---|---|---|
| Duas refeições no mesmo dia | `alimentacao` de R$ 72,50 e R$ 38,00 na mesma data | Ordenadas R$ 72,50 e R$ 38,00; limite R$ 60,00; primeira recebe R$ 60,00 (parcial) e segunda é rejeitada | RN-001 |
| Duas refeições no mesmo dia em viagem | `alimentacao` de R$ 72,50 e R$ 38,00 na mesma data, com hospedagem no período | Limite R$ 90,00; primeira recebe R$ 72,50; segunda recebe R$ 17,50 (parcial); excedente R$ 20,50 rejeitado | RN-001, RN-005 |
| Transporte exatamente no limiar da nota | `transporte_urbano` de R$ 100,00 sem nota | Reembolsável dentro do limite diário, pois R$ 100,00 não exige nota | RN-002, RN-004 |
| Transporte um centavo acima do limiar | `transporte_urbano` de R$ 100,01 sem nota | Rejeitado por falta de nota | RN-004 |
| Hospedagem com várias diárias | `hospedagem` de R$ 480,00 descrita como "2 diárias" | Limite R$ 500,00; reembolsável R$ 480,00 | RN-003 |
| Hospedagem sem indicação de diárias | `hospedagem` de R$ 300,00 sem indicação de diárias | Considera 1 diária; limite R$ 250,00; reembolsável R$ 250,00 | RN-003 |
| Despesa fora do período | `alimentacao` de R$ 41,00 em data fora de `inicio`/`fim` | Rejeitada; não entra nos limites | RN-007 |
| Categoria desconhecida | `coworking` de R$ 89,00 | Rejeitada como fora da política | RN-008 |
| Categoria com caixa diferente | `ALIMENTACAO` de R$ 61,00 | Tratada como `alimentacao`; reembolsável dentro do limite | RN-008 |
| Duplicata exata | Duas despesas idênticas de `alimentacao` R$ 54,90 no mesmo dia | Primeira processada; segunda rejeitada como duplicata | RN-006 |
| Estorno dentro do período | `transporte_urbano` de R$ -45,00 | Reduz total reembolsável; não consome limite | RN-009 |
| Valor com três decimais | `alimentacao` de R$ 33,333 | Reembolsável arredondado para R$ 33,33 | RN-010 |
| Ausência total de nota em valor baixo | `alimentacao` de R$ 50,00 sem nota | Reembolsável dentro do limite | RN-004 |

## 8. Ordem de aplicação das regras

A ordem abaixo garante que uma despesa seja descartada o mais cedo possível e
que limites diários sejam calculados apenas sobre despesas realmente elegíveis.

1. **RN-008 — Categorias fora da política:** verifica se a categoria é
   reembolsável. Se não for, rejeita e para.
2. **RN-007 — Período de competência:** verifica se a data está dentro do
   intervalo. Se não estiver, rejeita e para.
3. **RN-004 — Nota fiscal:** verifica se o valor declarado é maior que R$ 100,00
   e se há nota. Se não houver, rejeita e para.
4. **RN-006 — Duplicatas:** verifica se a despesa é duplicata de outra já
   processada. Se for, rejeita e para.
5. **RN-009 — Estornos:** valores negativos válidos são marcados como estorno e
   reduzem o total do período; não entram nos limites diários.
6. **RN-005 — Viagem:** detecta a existência de hospedagem no período para
   definir os limites ampliados.
7. **RN-001, RN-002 e RN-003 — Limites:** aplica os limites diários e por
   diária sobre as despesas restantes.
8. **RN-010 — Precisão monetária:** arredonda os valores finais para duas casas
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
- [ ] Categorias fora da política são recusadas.
- [ ] Colaboradores com ao menos uma hospedagem no período têm limites
  ampliados em 50%.
- [ ] Estornos reduzem o total reembolsável do período.
- [ ] Todos os valores são arredondados para duas casas decimais.

## 10. O que fica em aberto

- A detecção de viagem por presença de hospedagem é uma regra de negócio
  provisória. Se o RH vier a fornecer um campo explícito `em_viagem`, a regra
  deve ser substituída.
- A extração do número de diárias a partir da descrição é uma convenção
  provisória. O ideal seria um campo dedicado na entrada.
- Despesas com campos obrigatórios ausentes ou mal formatados serão rejeitadas
  com erro estrutural, mas o tratamento detalhado de erros de schema será
  definido no `plan.md`.
