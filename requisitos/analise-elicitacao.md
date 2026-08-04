# Análise do Documento de Elicitação — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C10 (Engenharia de Requisitos com GenAI) |
| **Documento** | Análise crítica da elicitação: requisitos, regras de negócio, RNFs, lacunas e ambiguidades |
| **Data** | 2026-08-04 |
| **Versão do documento** | 2.0 (atualizado após a implementação dos ajustes) |
| **Documento-fonte analisado** | `docs/escopo-mvp.md` (produto da etapa de elicitação) |
| **Evidências complementares** | `src/generator.py`, `src/cli_argparse.py`, `src/main.py`, `tests/test_generator.py`, `README.md`, execução real da CLI |

## 1. Objetivo

Este documento registra a **análise crítica** do artefato produzido na etapa de elicitação
(`docs/escopo-mvp.md`), com apoio de Inteligência Artificial Generativa. O objetivo é separar, a partir
de um texto de escopo escrito em linguagem corrente, quatro categorias distintas que ali aparecem
misturadas:

- **Requisitos funcionais (RF)** — o que o sistema faz;
- **Regras de negócio (RN)** — as restrições e decisões que governam esse comportamento;
- **Requisitos não funcionais (RNF)** — atributos de qualidade;
- **Lacunas (L) e ambiguidades (A)** — o que falta e o que está aberto a mais de uma interpretação.

A especificação propriamente dita é tratada nos documentos complementares
(`requisitos/historias-usuario.md`, `requisitos/casos-de-uso.md`, `requisitos/prototipo-cli.md` e
`requisitos/rastreabilidade.md`).

## 2. Método

A análise foi feita em três passadas:

1. **Leitura isolada do documento de elicitação**, sem consultar o código, para capturar o que um
   analista entenderia lendo apenas o escopo.
2. **Confronto com a implementação real** (`src/`, `tests/`) e com a **execução da CLI**, para descobrir
   regras que existem no produto mas *não* estão escritas — e afirmações escritas que *não* se sustentam.
3. **Classificação** de cada achado em RF, RN, RNF, lacuna ou ambiguidade.

> **Observação metodológica:** a passada (2) foi decisiva. A maior parte das lacunas encontradas não é
> de requisito "esquecido no papel", e sim de **regra de negócio implementada por decisão técnica e nunca
> validada com o solicitante** — o tipo de problema que só aparece quando se compara documento e produto.

## 3. Requisitos funcionais consolidados

Os requisitos abaixo estavam **explícitos** no documento de elicitação e foram mantidos com a numeração
original, para preservar rastreabilidade.

| ID | Requisito | Situação |
|----|-----------|----------|
| RF01 | Gerar senha com fonte criptograficamente segura | Implementado (`secrets`) |
| RF02 | Permitir informar o tamanho via `--length` | Implementado |
| RF03 | Aplicar tamanho padrão de 16 quando não informado | Implementado |
| RF04 | Validar faixa de 8 a 32 caracteres | Implementado |
| RF05 | Habilitar/desabilitar letras minúsculas | Implementado (`--lower/--no-lower`) |
| RF06 | Habilitar/desabilitar letras maiúsculas | Implementado (`--upper/--no-upper`) |
| RF07 | Habilitar/desabilitar números | Implementado (`--number/--no-number`) |
| RF08 | Habilitar/desabilitar caracteres especiais | Implementado (`--wildcards/--no-wildcards`) |
| RF09 | Validar que ao menos uma classe esteja ativa | Implementado |
| ~~RF10~~ | ~~Validar compatibilidade entre tamanho e critérios~~ | **Removido** — era código morto, inalcançável por qualquer entrada (ver 7.1) |
| RF11 | Expor entrypoint CLI com `argparse` | Implementado (`src/main.py`) |
| RF12 | Exibir a senha em `stdout`, em uma linha | Implementado |
| RF13 | Manter testes automatizados | Implementado (11 testes) |

### 3.1 Requisitos funcionais derivados da análise

Requisitos que **o produto já atende**, mas que não constavam do documento de elicitação. Foram
promovidos a requisito para poderem ser testados e rastreados:

| ID | Requisito | Origem |
|----|-----------|--------|
| RF14 | O sistema deve garantir que a senha contenha **ao menos um caractere de cada classe ativa** | `src/generator.py:62` |
| RF15 | O sistema deve retornar **código de saída 0** em sucesso e **2** em erro de validação, com a mensagem em `stderr` | Execução real da CLI |
| RF16 | O sistema deve oferecer **ajuda de uso** (`--help`) descrevendo todos os parâmetros e seus padrões | `argparse` (comportamento nativo) |

## 4. Regras de negócio

Regras extraídas do documento **e** do comportamento observado. A coluna "Documentada?" é o principal
resultado desta seção: cinco das dez regras que governam o produto **não estavam escritas em lugar nenhum**.

| ID | Regra de negócio | Documentada? | Evidência |
|----|------------------|--------------|-----------|
| RN01 | O tamanho padrão da senha é **16** caracteres | Sim (RF03) | `cli_argparse.py:71` |
| RN02 | O tamanho deve estar entre **8 e 32**, limites **inclusivos** | Sim (RF04) | `cli_argparse.py:27` |
| RN03 | Ao menos **uma** classe de caractere deve estar ativa | Sim (RF09) | `generator.py:53` |
| RN04 | A senha deve conter **ao menos um caractere de cada classe ativa** | **Não** | `generator.py:62` |
| ~~RN05~~ | ~~O tamanho deve ser **≥ ao número de classes ativas**~~ | — | **Removida** junto com o RF10 (ver 7.1) |
| RN06 | Alfabetos: `a–z`, `A–Z`, `0–9` e os **32 símbolos** de `string.punctuation` (`` !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ``) | **Não** | `generator.py:44-51` |
| RN07 | A aleatoriedade deve vir de **CSPRNG** (`secrets`), nunca de `random` | Sim (RF01/RNF06) | `generator.py:62-68` |
| RN08 | A aplicação **não persiste** a senha em arquivo, banco ou log | Parcial (só como "fora de escopo") | Ausência de I/O em `src/` |
| RN09 | A composição **padrão** ativa **as quatro classes** | **Não** (era omissa; decidida nesta análise) | `cli_argparse.py` + assinatura de `generate_password` |
| RN10 | Sucesso → senha em `stdout` + saída 0; erro → mensagem em `stderr` + saída 2 | **Não** | Execução real |

> **RN09 foi o achado mais relevante da análise — e já está resolvido.** O documento de elicitação
> prometia "senhas fortes" logo no objetivo, mas nunca especificava a composição padrão. A implementação
> havia decidido por *apenas minúsculas*, e `password-gen-argparse` **sem argumentos** produzia algo como
> `iborqgmdotcairsw` — 16 caracteres de um alfabeto de 26 símbolos (≈75 bits). Não era defeito de código:
> era uma **decisão de negócio tomada por omissão do requisito**.
>
> Após validação com o solicitante, o padrão passou a ativar **as quatro classes** (≈105 bits para 16
> caracteres). A justificativa: numa ferramenta de segurança o padrão deve ser a opção mais forte, e
> reduzir a composição passa a ser escolha explícita do usuário. Com isso, a causa do risco **R03**
> deixa de existir.

## 5. Requisitos não funcionais

### 5.1 RNFs do documento original

| ID | RNF | Verificável? | Observação |
|----|-----|--------------|------------|
| RNF01 | Python 3.10.5 | Parcial | Ambíguo: versão exata ou mínima? (ver A01) |
| RNF02 | Qualidade de código (PEP 8, docstrings, organização) | **Não** | Sem métrica nem ferramenta de verificação declarada |
| RNF03 | Usabilidade em terminal (`--help`, erros compreensíveis) | **Não** | "Compreensível" não é critério objetivo (ver A02) |
| RNF04 | Portabilidade (ambiente Python local) | Parcial | Não declara quais SOs são suportados |
| RNF05 | Reprodutibilidade do ambiente | Sim | `pyproject.toml` + `.gitignore` + extra `[dev]` |
| RNF06 | Segurança básica (evitar práticas inseguras) | Parcial | Não há teste que **impeça** a troca de `secrets` por `random` |

### 5.2 RNFs propostos (reescritos para serem mensuráveis)

O problema central dos RNFs originais é que a maioria é **declaração de intenção**, não critério de
aceite. Abaixo, a reescrita proposta:

| ID | RNF proposto | Critério objetivo |
|----|--------------|-------------------|
| RNF07 | Desempenho | Gerar uma senha em **< 200 ms** em máquina de desenvolvimento padrão |
| RNF08 | Isolamento | A aplicação **não realiza acesso à rede** nem coleta telemetria |
| RNF09 | Cobertura de testes | Manter cobertura de linhas **≥ 90%** em `src/` |
| RNF10 | Portabilidade verificada | Suíte verde em **Windows e Linux** (matriz de CI) |
| RNF11 | Qualidade de código automatizada | `ruff`/`flake8` sem violações no CI (torna o RNF02 verificável) |
| RNF12 | Não retenção do segredo | A senha não deve ser gravada em disco, log, variável de ambiente ou histórico **pela aplicação** |

## 6. Lacunas identificadas

Itens **ausentes** no documento de elicitação:

| ID | Lacuna | Impacto |
|----|--------|---------|
| L01 | "Senha forte" nunca é definida — não há **limiar de entropia** nem referência a norma (ex.: NIST SP 800-63B) | Alto: impossível aceitar ou rejeitar o produto objetivamente |
| L02 | A **composição padrão** não é especificada (RF05–RF08 falam em habilitar/desabilitar, mas não dizem o estado inicial) | Alto: originou RN09 sem validação |
| L03 | O **conjunto de caracteres especiais** não é enumerado | Médio: muitos sistemas-alvo rejeitam símbolos específicos |
| L04 | A **regra de representatividade** (RN04) não foi elicitada | Médio: comportamento relevante e não acordado |
| L05 | **Contrato de saída** (códigos de retorno, canal de erro) não especificado | Médio: bloqueia uso confiável em scripts e pipelines |
| L06 | **Ator e contexto de uso** não identificados (quem usa, com que frequência, em que ambiente) | Médio: sem persona, os RNFs de usabilidade ficam sem referência |
| L07 | **Geração em lote** (ex.: `--count N`) não considerada | Baixo: candidato natural a v1.1 |
| L08 | **Exclusão de caracteres ambíguos** (`l`/`1`/`I`, `O`/`0`) não considerada | Baixo: usabilidade em transcrição manual |
| L09 | **Requisitos de desempenho** ausentes | Baixo: mitigado por RNF07 |
| L10 | Requisito **explícito** de ausência de rede/telemetria ausente (hoje apenas implícito no "fora de escopo") | Médio: relevante para uma ferramenta de segurança |
| L11 | **Critérios de aceite por requisito** ausentes — a seção 5 do escopo cobre o MVP como um todo, não requisito a requisito | Alto: motivou a escolha dos artefatos (ver seção 8) |
| L12 | **Idioma e acentuação** das mensagens não especificados (hoje pt-BR sem acentos, por decisão implícita) | Baixo |

## 7. Ambiguidades identificadas

Itens **presentes**, mas abertos a mais de uma leitura:

| ID | Ambiguidade | Leituras possíveis | Resolução proposta |
|----|-------------|--------------------|--------------------|
| A01 | RNF01: "deve ser desenvolvido em **Python 3.10.5**" | (a) exatamente 3.10.5; (b) 3.10.5 ou superior | `pyproject.toml` já adota `>=3.10.5`. Adotar (b) e corrigir o texto |
| A02 | "erro **amigável**" (RF04, RF10), "mensagens **compreensíveis**" (RNF03) | Subjetivo; sem formato, canal ou idioma definidos | Substituir por RN10 + critérios em Gherkin com a mensagem exata |
| A03 | RF10: "**inviabilidade**" entre tamanho e critérios | (a) `length < nº de classes`; (b) tamanho insuficiente para representar todas as classes com folga | ✅ **Resolvida por remoção.** A leitura (a) tornava o requisito inócuo: com `length ≥ 8` validado antes e no máximo 4 classes, a condição nunca era verdadeira. RF10 e RN05 foram removidos. Ver 7.1 |
| A04 | RF12: "sem informações **sensíveis adicionais**" | A própria senha é sensível; o que exatamente é vedado? | Reescrever: "a saída deve conter exclusivamente a senha, sem prefixo, rótulo ou eco dos parâmetros" |
| A05 | RF13: "estrutura **mínima** de testes" | Sem meta de cobertura | Substituir por RNF09 (≥ 90%) |
| A06 | RF02 não menciona limites; a faixa só aparece em RF04 | Leitura isolada de RF02 sugere tamanho livre | Referenciar RN02 dentro do RF02 |
| A07 | RNF02, RNF04 e RNF05 são intenções sem critério de aceitação | Não testáveis | Ver RNFs propostos (5.2) |
| A08 | "habilitar ou **desabilitar**" (RF05–RF08) não define a sintaxe da CLI | Flag dupla, valor booleano, lista de classes… | A implementação adotou `--x/--no-x` (`BooleanOptionalAction`). Documentar como decisão |

### 7.1 Achado crítico — RF10 é código morto, e seu teste é falso-positivo

A ambiguidade **A03** revelou o achado mais grave da análise. Ao tentar reproduzir o fluxo de exceção do
RF10, verificou-se que **ele não é atingível por nenhuma entrada**:

```python
# src/generator.py
if length < 8:                       # (1) barra tudo abaixo de 8
    raise ValueError(...)
if length > 32:
    raise ValueError(...)
...
if length < len(selected_sets):      # (2) len(selected_sets) ∈ {1,2,3,4}
    raise ValueError(...)            #     e length ≥ 8 ⇒ CONDIÇÃO SEMPRE FALSA
```

Após a guarda (1), `length ≥ 8`; e como há no máximo 4 classes, `length < len(selected_sets)` é sempre
falsa. Uma **varredura exaustiva** de `length` ∈ [0, 39] × classes ativas ∈ [1, 4] confirmou:
**nenhuma combinação** alcança a linha (2). O requisito RF10 não tem efeito observável no produto.

Pior: o teste que deveria cobri-lo **passa pelo motivo errado**.

```python
def test_generate_password_fails_for_incompatible_length_and_classes() -> None:
    with pytest.raises(ValueError):          # <- sem match=
        generate_password(length=3, upper=True, lower=True, number=True, wildcards=True)
```

Com `length=3`, a exceção efetivamente levantada é `"O tamanho minimo recomendado e 8 caracteres."`
— ou seja, a regra **RN02**, não a RN05. Como o `pytest.raises` não usa o parâmetro `match=`, ele aceita
qualquer `ValueError` e o teste fica **verde testando outro requisito**. RF10 aparece como coberto na
suíte, mas não está.

### 7.2 Encaminhamento aplicado

O achado foi corrigido em dois commits, deliberadamente nessa ordem:

1. **Expor antes de corrigir.** O `match=` foi adicionado ao teste, que passou a falhar. Para manter a
   CI verde sem esconder o defeito, o teste foi marcado com `@pytest.mark.xfail(strict=True)` e uma
   referência a esta seção. O `strict=True` importa: se a regra voltar a ser alcançável, o teste falha
   por *passar inesperadamente*. O defeito ficou registrado no código, não só na documentação.
2. **Corrigir a causa.** A faixa 8..32 passou a viver em `MIN_LENGTH`/`MAX_LENGTH` no gerador, com a CLI
   importando as constantes em vez de repeti-las — o que resolve também o risco **R08** (validação e
   mensagens duplicadas entre camadas). A validação inalcançável foi removida, junto com o teste
   marcado como `xfail` e com os requisitos RF10/RN05.

Efeito colateral positivo: a mensagem de erro de faixa passou a ser **única**. Antes, a mesma regra
produzia "O valor de --length deve estar entre 8 e 32." pela CLI e "O tamanho minimo recomendado e 8
caracteres." pelo core.

Todos os `pytest.raises` da suíte usam `match=` — sem isso, testes de exceção não distinguem qual regra
falhou, que foi exatamente como o defeito passou despercebido.

## 8. Consequência para a escolha dos artefatos

A análise mostra que o documento de elicitação é **forte em intenção e fraco em verificabilidade**:
enumera bem *o que* o sistema faz (RF01–RF13), mas quase nunca diz *como saber se está certo* (L11, A02,
A05, A07). Isso direciona a especificação para artefatos **orientados a critério de aceite**:

- **Histórias de usuário com critérios em Gherkin** — atacam L11, A02 e A05, porque cada critério vira
  um teste executável;
- **Caso de uso expandido** — ataca L05 e L06, porque explicita ator, pré-condições e, sobretudo, os
  **fluxos de exceção**, que são a maior parte do comportamento desta CLI;
- **Tabela de regras de negócio** (seção 4) — ataca L02, L03 e L04, separando regra de interface;
- **Protótipo de terminal** — ataca A02 e A04, congelando o texto exato das mensagens;
- **Matriz de rastreabilidade** — garante que nenhum RF/RN fique sem história, critério e teste.

A justificativa completa da escolha está em `requisitos/rastreabilidade.md`, seção 1.

## 9. Decisões

### 9.1 Decisões tomadas

| # | Questão | Decisão |
|---|---------|---------|
| 1 | Composição padrão (RN09/L02) | ✅ **Ativar as quatro classes.** Numa ferramenta de segurança o padrão deve ser a opção mais forte; reduzir a composição vira escolha explícita |
| 5 | O core é produto de biblioteca? (RF10/RN05) | ✅ **Não.** É detalhe interno da CLI. Por isso a validação foi centralizada no core como fonte única, e a regra inalcançável foi removida |

### 9.2 Decisões ainda pendentes

Dependem do solicitante e **não** bloqueiam a v1.0.0:

1. Existe entropia mínima aceitável para o produto (L01)? Qual referência normativa adotar?
2. Há sistemas-alvo que restringem caracteres especiais (L03)? Se sim, quais símbolos excluir?
3. A regra de representatividade (RN04) é desejada? Ela **reduz** ligeiramente o espaço de busca em
   troca de garantir a aceitação da senha por validadores de formulário.
4. Geração em lote (L07) entra na v1.1?
5. As mensagens devem passar a usar acentuação correta (L12)?

## 10. Resumo

| Categoria | Quantidade |
|-----------|-----------|
| Requisitos funcionais originais | 13 (RF01–RF13), sendo **RF10 removido** → 12 vigentes |
| Requisitos funcionais derivados | 3 (RF14–RF16) |
| Regras de negócio | 10 (RN01–RN10), sendo **RN05 removida** → 9 vigentes; **5 não estavam documentadas** |
| RNFs originais | 6 (RNF01–RNF06) — **apenas 1 plenamente verificável** |
| RNFs propostos | 6 (RNF07–RNF12) |
| Lacunas | 12 (L01–L12) |
| Ambiguidades | 8 (A01–A08) |

O documento de elicitação cumpria bem o papel de **delimitar escopo**, mas não servia como base de
aceitação: metade das regras que governam o produto não estava escrita, e a maioria dos RNFs não era
testável. As lacunas de maior severidade eram **L01, L02 e L11** — todas ligadas à mesma causa raiz: o
termo "senha forte" foi tratado como autoexplicativo e nunca convertido em critério.

**Situação após os ajustes:** L02 foi fechada pela decisão de composição padrão; L03, L05 e L11 foram
fechadas pela documentação das regras e pelos critérios de aceite agora testados; A03 foi resolvida pela
remoção do RF10. Permanecem abertas L01 (limiar de entropia), L07 e L08 (backlog v1.1) — nenhuma
bloqueante para a v1.0.0.
