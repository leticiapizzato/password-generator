# Histórias de Usuário e Critérios de Aceite — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C10 (Engenharia de Requisitos com GenAI) |
| **Documento** | Histórias de usuário com critérios de aceite em Gherkin |
| **Data** | 2026-08-04 |
| **Versão do documento** | 1.0 |
| **Base** | `requisitos/analise-elicitacao.md` |

## 1. Ator

O documento de elicitação não identificava o usuário (lacuna **L06**). A persona abaixo foi definida
nesta etapa e é o ator de todas as histórias:

> **Dev/Analista de terminal** — pessoa com familiaridade em linha de comando que precisa de uma senha
> forte no meio de outra tarefa (criar um usuário de banco, um token de serviço, uma conta de teste).
> Valoriza **rapidez** e **previsibilidade**: quer a senha em uma linha, pronta para copiar, sem sair do
> terminal e sem instalar nada além do projeto.

**Consequência de projeto:** por essa persona, o caminho mais curto (`password-gen-argparse` sem
argumentos) é o mais usado — o que torna a lacuna **L02/RN09** (composição padrão) especialmente crítica.

## 2. Convenções

- Critérios escritos em **Gherkin** (`Dado / Quando / Então`), em português.
- Cada critério é **verificável**: existe (ou deve existir) um teste automatizado correspondente.
- A rastreabilidade completa está em `requisitos/rastreabilidade.md`.
- Legenda de status: ✅ coberto por teste automatizado · ⚠️ implementado sem teste · ❌ não implementado.

---

## US01 — Gerar uma senha rapidamente com a configuração padrão

> **Como** dev/analista de terminal,
> **quero** gerar uma senha executando o comando sem nenhum argumento,
> **para** obter um segredo utilizável no menor número possível de passos.

**Requisitos:** RF01, RF03, RF12 · **Regras:** RN01, RN07, RN09, RN10

### Critérios de aceite

```gherkin
Cenário: Geração com todos os padrões
  Dado que a CLI está instalada
  Quando eu executo "password-gen-argparse" sem argumentos
  Então uma senha de 16 caracteres é exibida em stdout
  E a saída contém exatamente uma linha
  E o código de saída é 0
```
✅ `test_cli_integration_success`, `test_cli_parser_defaults`

```gherkin
Cenário: A saída contém apenas a senha
  Quando eu executo "password-gen-argparse" sem argumentos
  Então a saída não contém rótulos, prefixos nem eco dos parâmetros
  E a saída pode ser copiada e usada diretamente como senha
```
⚠️ resolve a ambiguidade **A04**

```gherkin
Cenário: Duas execuções não produzem a mesma senha
  Quando eu executo "password-gen-argparse" duas vezes seguidas
  Então as duas senhas geradas são diferentes
```
❌ lacuna de teste — corresponde ao risco **R07**

> **⚠️ Ponto em aberto (RN09 / L02):** hoje este cenário produz uma senha **apenas com minúsculas**
> (ex.: `iborqgmdotcairsw`). Se a decisão pendente nº 1 da análise for "ativar as quatro classes por
> padrão", os critérios desta história mudam. **A história não deve ser considerada aceita até que essa
> decisão seja tomada.**

---

## US02 — Definir o tamanho da senha

> **Como** dev/analista de terminal,
> **quero** informar quantos caracteres a senha deve ter,
> **para** atender à política de tamanho do sistema em que vou cadastrá-la.

**Requisitos:** RF02, RF04 · **Regras:** RN02

### Critérios de aceite

```gherkin
Cenário: Tamanho válido dentro da faixa
  Quando eu executo "password-gen-argparse --length 20"
  Então uma senha de exatamente 20 caracteres é exibida
  E o código de saída é 0
```
✅ `test_generate_password_has_expected_length`

```gherkin
Esquema do Cenário: Limites da faixa são aceitos
  Quando eu executo "password-gen-argparse --length <tamanho>"
  Então uma senha de <tamanho> caracteres é exibida
  E o código de saída é 0

  Exemplos:
    | tamanho |
    | 8       |
    | 32      |
```
⚠️ os limites **inclusivos** (RN02) não têm teste dedicado

```gherkin
Esquema do Cenário: Tamanho fora da faixa é rejeitado
  Quando eu executo "password-gen-argparse --length <tamanho>"
  Então a mensagem "O valor de --length deve estar entre 8 e 32." é exibida em stderr
  E o código de saída é 2

  Exemplos:
    | tamanho |
    | 7       |
    | 33      |
```
✅ `test_cli_integration_error_for_invalid_length` (cobre 33)

```gherkin
Cenário: Tamanho não numérico é rejeitado
  Quando eu executo "password-gen-argparse --length abc"
  Então a mensagem "O valor de --length deve ser um numero inteiro." é exibida em stderr
  E o código de saída é 2
```
⚠️ coberto no core (`test_generate_password_fails_for_invalid_length_type`), não na CLI

---

## US03 — Escolher as classes de caracteres

> **Como** dev/analista de terminal,
> **quero** ligar e desligar minúsculas, maiúsculas, números e símbolos,
> **para** gerar uma senha que o sistema de destino realmente aceite.

**Requisitos:** RF05, RF06, RF07, RF08, RF14 · **Regras:** RN04, RN06

### Critérios de aceite

```gherkin
Cenário: Todas as classes ativas
  Quando eu executo "password-gen-argparse --length 20 --upper --number --wildcards"
  Então a senha contém ao menos uma letra minúscula
  E contém ao menos uma letra maiúscula
  E contém ao menos um dígito
  E contém ao menos um caractere especial
```
✅ `test_generate_password_contains_all_selected_classes` — formaliza **RN04**, que não estava documentada

```gherkin
Cenário: Classe desligada não aparece na senha
  Quando eu executo "password-gen-argparse --no-lower --upper --number"
  Então a senha não contém nenhuma letra minúscula
  E contém ao menos uma letra maiúscula
  E contém ao menos um dígito
```
❌ sem teste

```gherkin
Cenário: Conjunto de caracteres especiais é o previsto
  Dado que a classe de especiais está ativa
  Quando uma senha é gerada
  Então todo caractere especial pertence ao conjunto !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
```
❌ sem teste — formaliza **RN06** (lacuna **L03**)

---

## US04 — Receber mensagens de erro claras

> **Como** dev/analista de terminal,
> **quero** entender imediatamente por que o comando falhou,
> **para** corrigir o parâmetro sem precisar abrir a documentação.

**Requisitos:** RF09, RF15 · **Regras:** RN03, RN10

### Critérios de aceite

```gherkin
Cenário: Nenhuma classe de caractere selecionada
  Quando eu executo "password-gen-argparse --no-lower --no-upper --no-number --no-wildcards"
  Então a mensagem "Selecione ao menos uma classe de caractere." é exibida em stderr
  E nenhuma senha é exibida em stdout
  E o código de saída é 2
```
✅ `test_generate_password_fails_when_no_class_is_active` (core) · ⚠️ sem teste na CLI

```gherkin
Cenário: Erros vão para stderr e não poluem stdout
  Dado qualquer comando com parâmetro inválido
  Quando o comando falha
  Então stdout permanece vazio
  E a mensagem de erro é escrita em stderr
  E o código de saída é 2
```
⚠️ formaliza **RN10** (lacuna **L05**) — comportamento verificado manualmente, sem teste

```gherkin
Cenário: A mensagem de erro indica o parâmetro problemático
  Quando eu executo um comando com --length inválido
  Então a mensagem de erro cita "--length"
  E a linha de uso (usage) é exibida junto
```
⚠️ resolve a ambiguidade **A02** ("erro amigável")

---

## US05 — Consultar a ajuda da CLI

> **Como** dev/analista de terminal que usa a ferramenta esporadicamente,
> **quero** ver todos os parâmetros e seus padrões em um único comando,
> **para** montar a chamada certa sem consultar o README.

**Requisitos:** RF16 · **RNF:** RNF03

### Critérios de aceite

```gherkin
Cenário: Ajuda lista todos os parâmetros
  Quando eu executo "password-gen-argparse --help"
  Então a ajuda lista --length, --lower, --upper, --number e --wildcards
  E cada parâmetro exibe seu valor padrão
  E o código de saída é 0
```
❌ sem teste

```gherkin
Cenário: Ajuda informa a faixa válida de tamanho
  Quando eu executo "password-gen-argparse --help"
  Então a descrição de --length informa a faixa "entre 8 e 32"
  E informa o padrão 16
```
❌ sem teste — mitiga a ambiguidade **A06**

---

## US06 — Confiar na qualidade criptográfica da senha

> **Como** dev/analista responsável por credenciais,
> **quero** garantia de que a senha vem de uma fonte criptograficamente segura,
> **para** poder usá-la em ambientes reais sem introduzir uma fraqueza.

**Requisitos:** RF01 · **RNF:** RNF06, RNF08, RNF12 · **Regras:** RN07, RN08

### Critérios de aceite

```gherkin
Cenário: A geração usa CSPRNG
  Dado o módulo de geração de senhas
  Quando uma senha é gerada
  Então a aleatoriedade provém do módulo "secrets"
  E o módulo "random" não é utilizado para escolher caracteres
```
❌ sem teste — corresponde diretamente ao risco **R01**

```gherkin
Cenário: A aplicação não persiste o segredo
  Quando uma senha é gerada
  Então nenhum arquivo é criado ou modificado pela aplicação
  E nenhuma requisição de rede é realizada
```
❌ sem teste — formaliza **RN08** e **RNF08/RNF12** (lacuna **L10**)

```gherkin
Cenário: Senhas geradas não colidem
  Quando eu gero 1000 senhas de 16 caracteres com as quatro classes ativas
  Então todas as 1000 senhas são distintas
```
❌ sem teste — corresponde ao risco **R07**

---

## 3. Backlog derivado (fora do MVP)

Histórias identificadas a partir das lacunas **L07** e **L08**, registradas para a v1.1 e **não**
comprometidas no MVP:

| ID | História | Lacuna |
|----|----------|--------|
| US07 | Como usuário, quero gerar N senhas de uma vez (`--count`), para preparar vários cadastros | L07 |
| US08 | Como usuário, quero excluir caracteres ambíguos (`l`, `1`, `I`, `O`, `0`), para transcrever a senha sem erro | L08 |
| US09 | Como usuário, quero ver a entropia estimada da senha (`--show-entropy`), para justificar a escolha dos parâmetros | L01 |

## 4. Situação da cobertura

| Status | Critérios | Observação |
|--------|-----------|-----------|
| ✅ Coberto por teste | 5 | Faixa de tamanho, classes ativas, padrões, integração CLI |
| ⚠️ Implementado sem teste | 6 | Sobretudo o contrato de saída (RN10) e limites inclusivos |
| ❌ Não implementado / sem teste | 8 | Concentrados em US05 e US06 (ajuda e garantias de segurança) |

O agrupamento revela onde está a dívida: **as garantias de segurança (US06) são as menos verificadas**,
apesar de serem a razão de existir do produto. Essa é a mesma conclusão a que a gestão de riscos chegou
por outro caminho (R01, R07), o que reforça a prioridade.
