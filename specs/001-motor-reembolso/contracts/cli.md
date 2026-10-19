# Interface da CLI

O sistema expõe uma única interface de linha de comando: um subcomando
`calcular` que lê um JSON de entrada e escreve um JSON de saída.

---

## Comando

```text
python -m reembolso calcular --input <caminho-entrada> --output <caminho-saida> [--politica <caminho-politica>] [--cambio <caminho-cambio>]
```

Ou, se houver um entry-point configurado:

```text
reembolso calcular --input <caminho-entrada> --output <caminho-saida> [--politica <caminho-politica>] [--cambio <caminho-cambio>]
```

---

## Argumentos

| Argumento | Obrigatório | Descrição |
|---|---|---|
| `--input`, `-i` | sim | Caminho para o arquivo JSON de entrada (ver `input-schema.json`) |
| `--output`, `-o` | sim | Caminho onde o arquivo JSON de saída será gravado (ver `output-schema.json`) |
| `--politica`, `-p` | não | Caminho para o arquivo JSON da política de reembolso v4 (default: `exemplos/envelope/politica-v4.json`) |
| `--cambio`, `-c` | não | Caminho para o arquivo JSON de cotações (default: `exemplos/envelope/cambio.json`) |

---

## Comportamento

- O arquivo em `--input` deve existir e ser um JSON válido.
- Os arquivos em `--politica` e `--cambio`, quando informados, devem existir e
  ser JSONs válidos com a estrutura esperada.
- Campos obrigatórios ausentes ou mal formatados geram erro em `stderr` e
  retorno diferente de zero.
- O arquivo em `--output` é sobrescrito com o resultado.
- Em caso de sucesso, o programa retorna `0`.

---

## Exemplo

```text
python -m reembolso calcular --input exemplos/envelope/despesas-envelope.json --output resultado.json
```

Com política e câmbio explícitos:

```text
python -m reembolso calcular \
  --input exemplos/envelope/despesas-envelope.json \
  --output resultado.json \
  --politica exemplos/envelope/politica-v4.json \
  --cambio exemplos/envelope/cambio.json
```

---

## Schemas

- Entrada: [`input-schema.json`](input-schema.json)
- Saída: [`output-schema.json`](output-schema.json)
