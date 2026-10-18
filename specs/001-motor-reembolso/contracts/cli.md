# Interface da CLI

O sistema expõe uma única interface de linha de comando: um subcomando
`calcular` que lê um JSON de entrada e escreve um JSON de saída.

---

## Comando

```text
python -m reembolso calcular --input <caminho-entrada> --output <caminho-saida>
```

Ou, se houver um entry-point configurado:

```text
reembolso calcular --input <caminho-entrada> --output <caminho-saida>
```

---

## Argumentos

| Argumento | Obrigatório | Descrição |
|---|---|---|
| `--input`, `-i` | sim | Caminho para o arquivo JSON de entrada (ver `input-schema.json`) |
| `--output`, `-o` | sim | Caminho onde o arquivo JSON de saída será gravado (ver `output-schema.json`) |

---

## Comportamento

- O arquivo em `--input` deve existir e ser um JSON válido.
- Campos obrigatórios ausentes ou mal formatados geram erro em `stderr` e
  retorno diferente de zero.
- O arquivo em `--output` é sobrescrito com o resultado.
- Em caso de sucesso, o programa retorna `0`.

---

## Exemplo

```text
python -m reembolso calcular --input exemplos/despesas-exemplo.json --output resultado.json
```

---

## Schemas

- Entrada: [`input-schema.json`](input-schema.json)
- Saída: [`output-schema.json`](output-schema.json)
