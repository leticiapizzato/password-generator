# Protótipo de Interface (CLI) — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C10 (Engenharia de Requisitos com GenAI) |
| **Documento** | Protótipo de interface — sessões de terminal |
| **Data** | 2026-08-04 |
| **Versão do documento** | 1.0 |
| **Natureza das amostras** | **Saídas reais**, capturadas com Python 3.10.11 no Windows 11 |

## 1. O que é "protótipo" em uma aplicação de terminal

Em um produto com interface gráfica, o protótipo é um wireframe ou mockup. Aqui não há tela: **a
interface é o texto**. O equivalente funcional é a **transcrição de sessão de terminal** — ela congela
exatamente o que o usuário digita e o que o sistema responde, incluindo o texto literal das mensagens.

Isso resolve diretamente duas ambiguidades da elicitação:

- **A02** — "erro amigável" deixa de ser adjetivo e passa a ser uma string exata, verificável em teste;
- **A04** — "sem informações sensíveis adicionais" deixa de ser interpretação e passa a ser um formato
  de saída observável.

> **Todas as amostras abaixo foram capturadas executando o projeto**, não redigidas à mão. Onde o
> comportamento observado diverge do documentado, isso está sinalizado.

## 2. Ajuda de uso (UC02 / US05)

```console
$ password-gen-argparse --help
usage: main.py [-h] [--upper | --no-upper] [--lower | --no-lower]
               [--number | --no-number] [--wildcards | --no-wildcards]
               [--length LENGTH]

Gerador de senhas seguras (argparse).

options:
  -h, --help            show this help message and exit
  --upper, --no-upper   Habilita ou desabilita letras maiusculas (padrao:
                        desabilitado). (default: False)
  --lower, --no-lower   Habilita ou desabilita letras minusculas (padrao:
                        habilitado). (default: True)
  --number, --no-number
                        Habilita ou desabilita numeros (padrao: desabilitado).
                        (default: False)
  --wildcards, --no-wildcards
                        Habilita ou desabilita caracteres especiais (padrao:
                        desabilitado). (default: False)
  --length LENGTH       Quantidade de caracteres da senha (entre 8 e 32,
                        padrao: 16).
```

**Achados de usabilidade (RNF03), visíveis apenas no protótipo:**

1. O `usage` mostra **`main.py`**, e não o nome do comando instalado (`password-gen-argparse`), porque o
   `argparse` usa `sys.argv[0]`. Para quem instalou via `make install`, a ajuda cita um arquivo que a
   pessoa nunca digitou.
2. Cada opção **repete o padrão duas vezes**: "(padrao: desabilitado)" escrito à mão e "(default: False)"
   inserido pelo `argparse`. Além de redundante, mistura português e inglês.
3. A ajuda **não informa** quais caracteres compõem a classe "especiais" (**RN06** / lacuna **L03**).

## 3. Fluxo principal — configuração padrão (UC01 / US01)

```console
$ password-gen-argparse
iborqgmdotcairsw

$ echo $?
0
```

> **⚠️ Evidência da lacuna L02 / regra RN09.** A saída acima é real. O comando "sem configuração" — o
> mais provável de ser usado pela persona — devolve **16 caracteres apenas minúsculos**. O documento de
> elicitação promete "senhas fortes" e nunca especificou a composição padrão; o protótipo torna a
> consequência dessa omissão **visível em uma linha**.
>
> Comparação de espaço de busca para 16 caracteres:
>
> | Composição | Alfabeto | Entropia aproximada |
> |------------|----------|---------------------|
> | Padrão atual (só minúsculas) | 26 | ≈ 75 bits |
> | Quatro classes ativas | 94 | ≈ 105 bits |

## 4. Fluxo principal — todas as classes ativas (UC01 / US03)

```console
$ password-gen-argparse --length 20 --upper --number --wildcards
j5`pq0{1LeG5WAs9~$QJ

$ echo $?
0
```

Conferência visual dos critérios de aceite de **US03** sobre esta amostra:

| Classe | Presente? | Exemplos na amostra |
|--------|-----------|---------------------|
| Minúsculas | ✅ | `j`, `p`, `q`, `e`, `s` |
| Maiúsculas | ✅ | `L`, `G`, `W`, `A`, `Q`, `J` |
| Números | ✅ | `5`, `0`, `1`, `9` |
| Especiais | ✅ | `` ` ``, `{`, `~`, `$` |
| Tamanho | ✅ | 20 caracteres |

A presença simultânea das quatro classes não é coincidência: é a regra **RN04**, garantida pelo código e
formalizada nesta especificação.

## 5. Fluxos de exceção (UC01 / US04)

O protótipo fixa o **texto exato** de cada mensagem — é o que transforma "erro amigável" em critério
testável.

### FE02 — Tamanho fora da faixa

```console
$ password-gen-argparse --length 33
usage: main.py [-h] [--upper | --no-upper] [--lower | --no-lower]
               [--number | --no-number] [--wildcards | --no-wildcards]
               [--length LENGTH]
main.py: error: argument --length: O valor de --length deve estar entre 8 e 32.

$ echo $?
2
```

### FE03 — Nenhuma classe de caractere ativa

```console
$ password-gen-argparse --no-lower --no-upper --no-number --no-wildcards
usage: main.py [-h] [--upper | --no-upper] [--lower | --no-lower]
               [--number | --no-number] [--wildcards | --no-wildcards]
               [--length LENGTH]
main.py: error: Selecione ao menos uma classe de caractere.

$ echo $?
2
```

### FE01 — Tamanho não numérico

```console
$ password-gen-argparse --length abc
usage: main.py [-h] [--upper | --no-upper] [--lower | --no-lower]
               [--number | --no-number] [--wildcards | --no-wildcards]
               [--length LENGTH]
main.py: error: argument --length: O valor de --length deve ser um numero inteiro.

$ echo $?
2
```

### FE04 — Tamanho incompatível com o nº de classes: **não reproduzível**

Tentativa pela CLI — barrada antes, por FE02:

```console
$ password-gen-argparse --length 3 --upper --number --wildcards
usage: main.py [-h] [--upper | --no-upper] [--lower | --no-lower]
               [--number | --no-number] [--wildcards | --no-wildcards]
               [--length LENGTH]
main.py: error: argument --length: O valor de --length deve estar entre 8 e 32.
```

Tentativa pelo core, como biblioteca — **também não produz a mensagem esperada**:

```pycon
>>> from generator import generate_password
>>> generate_password(length=3, upper=True, lower=True, number=True, wildcards=True)
ValueError: O tamanho minimo recomendado e 8 caracteres.
```

A mensagem obtida é a da regra **RN02**, não a da RN05. O protótipo, ao tentar simplesmente *reproduzir*
o fluxo documentado, expôs que **RF10 é código morto** — e que o teste que o cobre passa pelo motivo
errado. A análise completa está em `requisitos/analise-elicitacao.md`, seção 7.1.

## 6. Contrato de saída (RN10 / RF15)

Consolidação do comportamento observado — informação que **não existia** no documento de elicitação
(lacuna **L05**) e que é essencial para uso em scripts:

| Situação | `stdout` | `stderr` | Código |
|----------|----------|----------|--------|
| Senha gerada | a senha, uma linha, sem rótulo | vazio | **0** |
| `--help` | texto de ajuda | vazio | **0** |
| Qualquer erro de validação | **vazio** | `usage` + `error: <mensagem>` | **2** |

Consequência prática, agora garantida por especificação:

```console
$ PASSWORD=$(password-gen-argparse --length 24 --upper --number)
$ echo "senha capturada com sucesso"
```

Como as mensagens de erro nunca vão para `stdout`, uma falha jamais contamina a variável com texto de
erro — a captura é segura.

## 7. Ajustes propostos a partir do protótipo

Achados que só ficaram evidentes ao materializar a interface:

| # | Ajuste | Origem | Prioridade |
|---|--------|--------|-----------|
| 1 | Definir `prog="password-gen-argparse"` no `ArgumentParser` para o `usage` refletir o comando real | Seção 2, item 1 | Média |
| 2 | Remover a duplicação de padrões na ajuda (usar apenas o do `argparse`, ou desligar sua inserção automática) | Seção 2, item 2 | Baixa |
| 3 | Listar o conjunto de caracteres especiais na ajuda de `--wildcards` | Seção 2, item 3 / **L03** | Média |
| 4 | Decidir a composição padrão (**L02/RN09**) — maior impacto de todos | Seção 3 | **Alta** |
| 5 | Documentar o contrato de saída no README | Seção 6 / **L05** | Média |

> Os itens acima são **propostas de especificação**, não alterações já realizadas. Nenhum código de
> `src/` foi modificado nesta etapa: o objetivo desta unidade é especificar, e a implementação seria uma
> mudança de escopo em cima de um MVP já entregue.
