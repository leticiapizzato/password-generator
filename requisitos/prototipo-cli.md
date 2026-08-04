# Protótipo de Interface (CLI) — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C10 (Engenharia de Requisitos com GenAI) |
| **Documento** | Protótipo de interface — sessões de terminal |
| **Data** | 2026-08-04 |
| **Versão do documento** | 2.0 (transcrições recapturadas após a implementação dos ajustes) |
| **Natureza das amostras** | **Saídas reais** do entrypoint instalado, Python 3.10.11 no Windows 11 |

## 1. O que é "protótipo" em uma aplicação de terminal

Em um produto com interface gráfica, o protótipo é um wireframe ou mockup. Aqui não há tela: **a
interface é o texto**. O equivalente funcional é a **transcrição de sessão de terminal** — ela congela
exatamente o que o usuário digita e o que o sistema responde, incluindo o texto literal das mensagens.

Isso resolve diretamente duas ambiguidades da elicitação:

- **A02** — "erro amigável" deixa de ser adjetivo e passa a ser uma string exata, verificável em teste;
- **A04** — "sem informações sensíveis adicionais" deixa de ser interpretação e passa a ser um formato
  de saída observável.

> **Todas as amostras abaixo foram capturadas executando o projeto**, não redigidas à mão.

## 2. Ajuda de uso (UC02 / US05)

```console
$ password-gen-argparse --help
usage: password-gen-argparse [-h] [--upper | --no-upper]
                             [--lower | --no-lower] [--number | --no-number]
                             [--wildcards | --no-wildcards] [--length LENGTH]

Gerador de senhas seguras. Por padrao a senha usa as quatro classes de
caractere; desligue as que o sistema de destino nao aceitar com --no-upper,
--no-number ou --no-wildcards.

options:
  -h, --help            show this help message and exit
  --upper, --no-upper   Habilita ou desabilita letras maiusculas. (default:
                        True)
  --lower, --no-lower   Habilita ou desabilita letras minusculas. (default:
                        True)
  --number, --no-number
                        Habilita ou desabilita numeros. (default: True)
  --wildcards, --no-wildcards
                        Habilita ou desabilita caracteres especiais
                        (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~). (default: True)
  --length LENGTH       Quantidade de caracteres da senha (entre 8 e 32,
                        padrao: 16).
```

Os três achados de usabilidade da versão 1.0 deste documento foram corrigidos: o `usage` agora exibe o
**nome real do comando** (antes mostrava `main.py`), os padrões aparecem **uma única vez** (antes havia
`(padrao: desabilitado)` escrito à mão junto de `(default: False)` do argparse) e o **conjunto de
caracteres especiais está enumerado** (lacuna **L03**).

> **Nota de implementação.** Colocar `string.punctuation` no texto de ajuda quebrou o `--help`: o
> argparse aplica `%`-formatting nas mensagens, e o `%` do conjunto foi interpretado como diretiva de
> formato. O defeito foi capturado pelo teste `test_cli_help_lists_all_parameters`, escrito a partir dos
> critérios de aceite de **US05**, e corrigido escapando o caractere. É um exemplo direto de critério de
> aceite pegando uma regressão que a revisão visual não pegaria.

## 3. Fluxo principal — configuração padrão (UC01 / US01)

```console
$ password-gen-argparse
z%rlfc$e7!D4_=3P

$ echo $?
0
```

A composição padrão agora ativa as **quatro** classes. Na versão anterior deste protótipo, o mesmo
comando devolvia `iborqgmdotcairsw` — 16 caracteres apenas minúsculos —, evidência que motivou a
correção da lacuna **L02** / regra **RN09**.

| Composição | Alfabeto | Entropia para 16 caracteres |
|------------|----------|------------------------------|
| Padrão anterior (só minúsculas) | 26 | ≈ 75 bits |
| Padrão atual (quatro classes) | 94 | ≈ 105 bits |

## 4. Fluxo alternativo — desligando uma classe (UC01 / FA02)

Para sistemas de destino que rejeitam símbolos:

```console
$ password-gen-argparse --length 20 --no-wildcards
5VqWhPKBDioYoiVVO7b3

$ echo $?
0
```

Nenhum símbolo aparece, e as três classes restantes continuam representadas (**RN04**).

## 5. Limites inclusivos da faixa (US02 / RN02)

```console
$ password-gen-argparse --length 8
4*`8JEvr

$ password-gen-argparse --length 32
*OGhLdK7#X}GUHh(D2md3s)EsOvx-WwQ
```

Ambos os extremos são aceitos — comportamento que a elicitação não deixava claro (ambiguidade **A06**) e
que hoje tem teste dedicado.

## 6. Fluxos de exceção (UC01 / US04)

O protótipo fixa o **texto exato** de cada mensagem — é o que transforma "erro amigável" em critério
testável.

### FE02 — Tamanho fora da faixa

```console
$ password-gen-argparse --length 33
usage: password-gen-argparse [-h] [--upper | --no-upper]
                             [--lower | --no-lower] [--number | --no-number]
                             [--wildcards | --no-wildcards] [--length LENGTH]
password-gen-argparse: error: O tamanho da senha deve estar entre 8 e 32.

$ echo $?
2
```

A mensagem passou a ser **única**: antes, a CLI dizia "O valor de --length deve estar entre 8 e 32." e o
core dizia "O tamanho minimo recomendado e 8 caracteres." para a mesma regra. A centralização da
validação no gerador eliminou a divergência (risco **R08**).

### FE03 — Nenhuma classe de caractere ativa

```console
$ password-gen-argparse --no-lower --no-upper --no-number --no-wildcards
usage: password-gen-argparse [-h] [--upper | --no-upper]
                             [--lower | --no-lower] [--number | --no-number]
                             [--wildcards | --no-wildcards] [--length LENGTH]
password-gen-argparse: error: Selecione ao menos uma classe de caractere.

$ echo $?
2
```

### FE01 — Tamanho não numérico

```console
$ password-gen-argparse --length abc
usage: password-gen-argparse [-h] [--upper | --no-upper]
                             [--lower | --no-lower] [--number | --no-number]
                             [--wildcards | --no-wildcards] [--length LENGTH]
password-gen-argparse: error: argument --length: O valor de --length deve ser um numero inteiro.

$ echo $?
2
```

Este erro mantém o prefixo `argument --length:` porque a conversão de tipo continua sendo
responsabilidade do argparse; apenas a validação de faixa migrou para o core.

### ~~FE04 — Tamanho incompatível com o nº de classes~~ (removido)

Fluxo **eliminado**. A tentativa de reproduzi-lo na versão 1.0 deste protótipo revelou que ele era
inatingível por qualquer entrada, e que o teste que o cobria passava capturando outra exceção. O
requisito **RF10** e a regra **RN05** foram removidos do escopo, e a validação correspondente saiu do
gerador. Histórico em `requisitos/analise-elicitacao.md`, seção 7.1.

## 7. Contrato de saída (RN10 / RF15)

Informação que **não existia** no documento de elicitação (lacuna **L05**) e que é essencial para uso em
scripts:

| Situação | `stdout` | `stderr` | Código |
|----------|----------|----------|--------|
| Senha gerada | a senha, uma linha, sem rótulo | vazio | **0** |
| `--help` | texto de ajuda | vazio | **0** |
| Qualquer erro de validação | **vazio** | `usage` + `error: <mensagem>` | **2** |

Consequência prática, hoje garantida por teste (`test_cli_error_contract` e `test_cli_success_contract`):

```console
$ PASSWORD=$(password-gen-argparse --length 24)
```

Como as mensagens de erro nunca vão para `stdout`, uma falha jamais contamina a variável com texto de
erro — a captura é segura.

## 8. Situação dos ajustes propostos na versão 1.0

| # | Ajuste proposto | Situação |
|---|-----------------|----------|
| 1 | `prog` refletindo o comando real | ✅ implementado |
| 2 | Remover duplicação de padrões na ajuda | ✅ implementado |
| 3 | Listar o conjunto de caracteres especiais | ✅ implementado |
| 4 | Decidir a composição padrão (**L02/RN09**) | ✅ decidido: quatro classes |
| 5 | Documentar o contrato de saída no README | ✅ implementado |
