# Casos de Uso — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C10 (Engenharia de Requisitos com GenAI) |
| **Documento** | Casos de uso expandidos |
| **Data** | 2026-08-04 |
| **Versão do documento** | 2.0 (atualizado após a implementação dos ajustes) |
| **Base** | `requisitos/analise-elicitacao.md`, `requisitos/historias-usuario.md` |

## 1. Por que caso de uso *além* de história de usuário

As histórias de usuário descrevem bem o **valor** e o **caminho feliz**, mas nesta aplicação a maior
parte do comportamento está nos **desvios**: três validações distintas, cada uma com mensagem e código de
saída próprios. O caso de uso expandido é o artefato que dá lugar de destaque a **fluxos alternativos e
de exceção**, e por isso complementa — não substitui — as histórias.

Foram especificados **dois** casos de uso. Não se produziu um caso de uso por requisito: isso duplicaria
as histórias sem acrescentar informação (over-specification).

## 2. Diagrama de contexto

```mermaid
flowchart LR
    ator(["👤 Dev/Analista<br/>de terminal"])

    subgraph sistema["Password Generator (CLI)"]
        uc1["UC01<br/>Gerar senha segura"]
        uc2["UC02<br/>Consultar ajuda de uso"]
    end

    so[("Sistema Operacional<br/>fonte de entropia<br/>(os.urandom)")]

    ator --> uc1
    ator --> uc2
    uc1 -.->|"«usa»"| so
```

**Ator principal:** Dev/Analista de terminal (persona definida em `requisitos/historias-usuario.md`).
**Ator secundário (sistema de apoio):** Sistema Operacional, que fornece a entropia consumida por
`secrets` — dependência que o documento de elicitação não explicitava.

---

## UC01 — Gerar senha segura

| Campo | Valor |
|-------|-------|
| **Identificador** | UC01 |
| **Nome** | Gerar senha segura |
| **Ator principal** | Dev/Analista de terminal |
| **Ator secundário** | Sistema Operacional (fonte de entropia) |
| **Objetivo** | Obter uma senha aleatória que atenda aos critérios de composição informados |
| **Pré-condições** | Python ≥ 3.10.5 disponível; projeto instalado (`make install`) ou acessível via `python src/main.py` |
| **Pós-condição de sucesso** | A senha é exibida em `stdout` e o processo encerra com código 0. Nenhum dado é gravado em disco |
| **Pós-condição de falha** | Mensagem de erro em `stderr`, `stdout` vazio, processo encerra com código 2 |
| **Gatilho** | O usuário executa o comando no terminal |
| **Frequência estimada** | Esporádica e interativa (várias vezes ao dia, sob demanda) |
| **Histórias relacionadas** | US01, US02, US03, US04, US06 |
| **Regras associadas** | RN01–RN10, exceto RN05 (removida) |

### Fluxo principal (caminho de sucesso)

| # | Ator | Sistema |
|---|------|---------|
| 1 | Executa `password-gen-argparse` com zero ou mais parâmetros | |
| 2 | | Interpreta os argumentos e aplica os padrões ausentes (RN01, RN09) |
| 3 | | Converte `--length` para inteiro (argparse) |
| 4 | | Valida a faixa de tamanho, no core, como fonte única (RN02) |
| 5 | | Valida que há ao menos uma classe ativa (RN03) |
| 6 | | Monta o alfabeto a partir das classes ativas (RN06) |
| 7 | | Sorteia **um caractere de cada classe ativa** para garantir representatividade (RN04) |
| 8 | | Sorteia os caracteres restantes no alfabeto completo, via CSPRNG (RN07) |
| 9 | | Embaralha o resultado com `SystemRandom().shuffle` |
| 10 | | Exibe a senha em `stdout`, em uma linha, e encerra com código 0 (RN10) |
| 11 | Copia a senha e a utiliza | |

> **Observação sobre o passo 7:** essa é a regra **RN04**, que existe no código desde o início mas
> **nunca foi documentada** na elicitação. Sem o passo 7, uma senha com "números ativados" poderia sair
> sem nenhum dígito e ser rejeitada pelo formulário de destino — exatamente o problema que o usuário
> tentava evitar ao ligar a opção.

> **Observação sobre os passos 3 e 4:** originalmente a faixa de tamanho era validada **duas vezes**, na
> CLI e no core, com mensagens diferentes (risco **R08**). A validação passou a viver apenas no core; a
> CLI só faz a conversão de tipo. Por isso o antigo passo de "compatibilidade entre tamanho e nº de
> classes" desapareceu: era o RF10, removido por ser inalcançável.

### Fluxos alternativos

**FA01 — Usuário aceita todos os padrões**
Ocorre no passo 1, quando nenhum argumento é informado.
O sistema aplica tamanho 16 e **as quatro classes de caractere** (RN01, RN09) e segue do passo 4.

**FA02 — Usuário desabilita uma classe**
Ocorre no passo 1, com `--no-wildcards` (ou equivalente), mantendo ao menos uma classe ativa.
O sistema remove a classe do alfabeto e segue normalmente. A senha **não conterá** aquela classe.
Uso típico: sistemas de destino que rejeitam símbolos.

### Fluxos de exceção

| ID | Condição | Passo | Resposta do sistema | Código |
|----|----------|-------|---------------------|--------|
| **FE01** | `--length` não conversível para inteiro | 3 | `usage` + `argument --length: O valor de --length deve ser um numero inteiro.` em `stderr` | 2 |
| **FE02** | `--length` fora de 8..32 | 4 | `usage` + `O tamanho da senha deve estar entre 8 e 32.` em `stderr` | 2 |
| **FE03** | Nenhuma classe de caractere ativa | 5 | `usage` + `Selecione ao menos uma classe de caractere.` em `stderr` | 2 |

> **O antigo FE04 foi removido.** Ele previa erro quando o tamanho fosse menor que o número de classes
> ativas. A tentativa de reproduzi-lo durante a elaboração do protótipo revelou que era **inatingível por
> qualquer caminho**: `generate_password()` valida `length ≥ 8` antes de contar as classes, e há no
> máximo 4. Uma varredura exaustiva confirmou que nenhuma combinação de entrada alcançava a validação.
> O requisito **RF10** e a regra **RN05** foram removidos, junto com o código correspondente.
>
> O caso ilustra por que a especificação foi confrontada com execução real: pelo documento de elicitação,
> o RF10 parecia um requisito implementado e testado.
>
> Note também que **FE02 mudou de mensagem e de passo**: antes era barrado pelo argparse no passo 3, com
> texto próprio; agora é validado no core, com mensagem única.

### Requisitos especiais

- A senha **não** deve ser registrada em log, arquivo ou variável de ambiente pela aplicação (RN08, RNF12).
- A operação deve concluir em **< 200 ms** (RNF07).
- Nenhum acesso à rede é realizado (RNF08).

---

## UC02 — Consultar ajuda de uso

| Campo | Valor |
|-------|-------|
| **Identificador** | UC02 |
| **Nome** | Consultar ajuda de uso |
| **Ator principal** | Dev/Analista de terminal |
| **Objetivo** | Descobrir os parâmetros disponíveis e seus valores padrão |
| **Pré-condições** | Aplicação instalada ou acessível |
| **Pós-condição** | Texto de ajuda exibido em `stdout`; processo encerra com código 0 |
| **Histórias relacionadas** | US05 |
| **Requisitos** | RF16 · **RNF:** RNF03 |

### Fluxo principal

| # | Ator | Sistema |
|---|------|---------|
| 1 | Executa `password-gen-argparse --help` | |
| 2 | | Exibe a linha de uso, a descrição do programa e a lista de parâmetros |
| 3 | | Para cada parâmetro, exibe descrição e valor padrão |
| 4 | | Encerra com código 0 sem gerar senha |

### Fluxo de exceção

Nenhum. `--help` é tratado pelo `argparse` antes de qualquer validação e não pode falhar por
configuração do usuário.

> **Nota de usabilidade — resolvida.** O texto de ajuda repetia o valor padrão ("(padrao: desabilitado)"
> escrito à mão junto do "(default: False)" inserido pelo `argparse`) e o `usage` exibia `main.py` em vez
> do nome real do comando. Ambos foram corrigidos, e a ajuda passou a enumerar o conjunto de caracteres
> especiais. A saída atual está em `requisitos/prototipo-cli.md`, seção 2.

---

## 3. Rastreamento

A relação entre casos de uso, requisitos, regras, histórias e testes está consolidada em
`requisitos/rastreabilidade.md`.
