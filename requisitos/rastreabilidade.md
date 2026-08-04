# Rastreabilidade e Justificativa dos Artefatos — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C10 (Engenharia de Requisitos com GenAI) |
| **Documento** | Justificativa da seleção de artefatos e matriz de rastreabilidade |
| **Data** | 2026-08-04 |
| **Versão do documento** | 2.0 (atualizado após a implementação dos ajustes) |

## 1. Por que estes artefatos

A escolha não partiu de um catálogo genérico de "artefatos de especificação", mas do **diagnóstico**
feito em `requisitos/analise-elicitacao.md`. O documento de elicitação tinha um perfil bem definido:

> forte em **intenção** (13 requisitos funcionais enumerados), fraco em **verificabilidade** (nenhum
> critério de aceite por requisito, RNFs não mensuráveis, metade das regras de negócio não escritas).

Cada artefato foi escolhido para atacar um desses defeitos:

| Artefato produzido | Defeito que corrige | Por que é o mais adequado aqui |
|--------------------|---------------------|--------------------------------|
| **Tabela de regras de negócio** (análise, seção 4) | 5 de 10 regras não documentadas | Separa **regra** de **interface**. RN04 e RN06 governam o produto e sobreviveriam a uma troca completa da CLI — precisam de vida própria |
| **Histórias de usuário + critérios em Gherkin** | Ausência de critério de aceite (L11, A02, A05) | Escopo pequeno e incremental, um único ator. Cada critério em Gherkin vira **um teste pytest** — o artefato fecha o ciclo requisito → teste |
| **Caso de uso expandido** | Fluxos de exceção invisíveis (L05) | Nesta CLI, **a maior parte do comportamento é desvio**: 3 fluxos de exceção e 2 alternativos para 1 fluxo principal. Histórias descrevem valor; caso de uso é o formato que dá estrutura a pré-condições, pós-condições e exceções |
| **Protótipo de terminal** | "Erro amigável" não verificável (A02, A04) | Em uma CLI **a interface é o texto**. Congelar a transcrição real substitui o wireframe e transforma adjetivo em string testável |
| **Matriz de rastreabilidade** (este doc) | Risco de perder requisito no caminho | Único artefato que responde "todo requisito virou critério e teste?" — e foi ele que expôs o RF10 órfão |

### 1.1 Artefatos deliberadamente descartados

Tão importante quanto escolher é justificar o que **não** se produziu:

| Artefato | Por que foi descartado |
|----------|------------------------|
| **BPMN / diagrama de processo** | Não há processo de negócio multi-ator nem fluxo com aprovações. É um comando único e síncrono — o diagrama seria uma caixa só |
| **SRS completo (IEEE 830)** | Peso desproporcional a um MVP de 3 módulos e ~150 linhas; duplicaria `docs/escopo-mvp.md` e criaria uma segunda fonte de verdade para manter em sincronia |
| **Protótipo visual (Figma/wireframe)** | Interface gráfica está explicitamente **fora de escopo**. Um mockup de tela especificaria um produto que não existe |
| **Diagramas de classe / sequência** | São artefatos de **projeto**, não de requisitos. Com 3 módulos e uma função de núcleo, não agregam informação sobre *o que* o sistema deve fazer |
| **Um caso de uso por requisito funcional** | Geraria 16 casos de uso quase idênticos, redundantes com as histórias. Optou-se por **2 casos de uso** e 6 histórias — over-specification é um custo de manutenção, não um sinal de rigor |
| **Matriz CRUD / modelo de dados** | A aplicação **não tem entidade persistida** (RN08). Não há dado para modelar |

## 2. Matriz de rastreabilidade

Legenda: ✅ coberto por teste automatizado · ⚠️ implementado sem teste · ❌ sem verificação

| Requisito | Regra | História | Caso de uso | Teste automatizado | Status |
|-----------|-------|----------|-------------|--------------------|--------|
| RF01 | RN07 | US01, US06 | UC01 | `test_generate_password_uses_secrets_module`, `test_generator_does_not_import_insecure_random` | ✅ |
| RF02 | RN02 | US02 | UC01 | `test_generate_password_has_expected_length` | ✅ |
| RF03 | RN01 | US01 | UC01 / FA01 | `test_cli_parser_defaults` | ✅ |
| RF04 | RN02 | US02 | UC01 / FE02 | `test_..._below_minimum`, `test_..._above_maximum`, `test_..._accepts_inclusive_bounds`, `test_cli_error_contract` | ✅ |
| RF05 | RN06, RN09 | US03 | UC01 / FA02 | `test_cli_parser_defaults`, `test_disabled_class_is_absent_from_password` | ✅ |
| RF06 | RN06 | US03 | UC01 | `test_..._contains_all_selected_classes` | ✅ |
| RF07 | RN06 | US03 | UC01 | `test_..._contains_all_selected_classes` | ✅ |
| RF08 | RN06 | US03 | UC01 | `test_..._contains_all_selected_classes`, `test_special_characters_belong_to_expected_set` | ✅ |
| RF09 | RN03 | US04 | UC01 / FE03 | `test_..._fails_when_no_class_is_active`, `test_cli_error_contract` | ✅ |
| ~~RF10~~ | ~~RN05~~ | — | — | — | **Removido** (ver 2.1) |
| RF11 | — | US01 | UC01 | `test_cli_installed_entrypoint_success` | ✅ |
| RF12 | RN10 | US01 | UC01 | `test_cli_success_contract` | ✅ |
| RF13 | — | — | — | a própria suíte (24 testes) | ⚠️ sem meta de cobertura |
| RF14 | RN04 | US03 | UC01 / passo 7 | `test_..._contains_all_selected_classes` | ✅ |
| RF15 | RN10 | US04 | UC01 | `test_cli_error_contract`, `test_cli_success_contract` | ✅ |
| RF16 | — | US05 | UC02 | `test_cli_help_lists_all_parameters`, `test_cli_help_documents_length_range` | ✅ |

### 2.1 O requisito órfão — e o que aconteceu com ele

**RF10 foi o único requisito sem história de usuário.** Não por omissão: ao tentar escrever a história,
não foi possível formular um "para que" com valor para o usuário — porque **não existia entrada capaz de
produzir aquele comportamento**.

A matriz funcionou como instrumento de detecção. Um requisito que não consegue virar história, e cujo
teste passa por um motivo diferente do declarado, é forte indício de requisito inválido. A verificação
confirmou (`analise-elicitacao.md`, seção 7.1) e **RF10 e RN05 foram removidos** do escopo e do código.

É o argumento mais concreto a favor de manter uma matriz de rastreabilidade: nenhum dos outros artefatos
teria exposto esse requisito, porque cada um olhava só para a sua própria parte.

## 3. Cobertura das regras de negócio

| Regra | Documentada antes? | Especificada agora | Testada |
|-------|--------------------|--------------------|---------|
| RN01 — padrão 16 | Sim | US01, UC01 | ✅ |
| RN02 — faixa 8..32 | Sim | US02, FE02 | ✅ (inclusive os limites) |
| RN03 — ≥ 1 classe ativa | Sim | US04, FE03 | ✅ (core e CLI) |
| RN04 — representatividade | **Não** | US03, UC01 passo 7 | ✅ |
| ~~RN05~~ — tamanho ≥ nº classes | Parcial | — | **Removida** |
| RN06 — alfabetos | **Não** | US03, protótipo §2 | ✅ |
| RN07 — CSPRNG | Sim | US06 | ✅ (fecha R01) |
| RN08 — não persistência | Parcial | US06, UC01 | ❌ dívida consciente |
| RN09 — composição padrão | **Não** | US01, FA01 | ✅ (quatro classes) |
| RN10 — contrato de saída | **Não** | US04, protótipo §7 | ✅ |

**Resultado:** as 5 regras que não estavam documentadas passaram a ter especificação **e teste**. Na
versão 1.0 deste documento, três delas (RN06, RN07, RN08) estavam sem verificação alguma; hoje resta
apenas **RN08**, cujo critério ("nenhum arquivo criado, nenhuma requisição de rede") exigiria instrumentar
o sistema de arquivos e a rede — custo desproporcional para o MVP, registrado como dívida consciente.

## 4. Convergência com a gestão de riscos

Os achados desta análise foram levantados a partir dos **requisitos**, sem consultar `riscos/`. A
sobreposição posterior é uma validação cruzada útil:

| Achado (requisitos) | Risco correspondente | Situação |
|---------------------|----------------------|----------|
| L02 / RN09 — composição padrão fraca | **R03** — baixa entropia padrão | ✅ **Causa eliminada**: padrão passou a ativar as quatro classes |
| RN07 sem teste | **R01** — regressão na fonte de aleatoriedade | ✅ **Mitigado**: dois testes garantem o uso de `secrets` e barram a volta de `random` |
| A03 / RF10 — código morto | **R08** — validação duplicada CLI/core | ✅ **Resolvido**: validação centralizada no core, requisito removido |
| US06 — cenário de não colisão | **R07** — cobertura de aleatoriedade | ✅ **Mitigado**: teste de 1000 amostras distintas |
| RN08/RNF12 — não retenção | **R02** — exposição no terminal | ⚠️ Em aberto. O requisito cobre a **aplicação**; R02 trata do **ambiente** (histórico de shell). Complementares, não duplicados |

O achado do RF10 foi o único **novo** em relação ao registro de riscos — surgiu porque a especificação
exigiu reproduzir cada fluxo de exceção, o que a análise de riscos não fazia.

## 5. Próximos passos recomendados

Concluídos nesta etapa:

- ✅ Composição padrão decidida e implementada (L02/RN09)
- ✅ RF10 removido e validação centralizada no core (A03/R08)
- ✅ `match=` em todos os `pytest.raises`, impedindo novos falsos-positivos
- ✅ Testes de US06 para CSPRNG e não colisão (R01, R07)
- ✅ RN06 e RN10 documentados no README e na ajuda da CLI

Pendentes, nenhum bloqueante para a v1.0.0:

1. Definir limiar de entropia e referência normativa (**L01**), o que permitiria transformar "senha
   forte" em critério numérico.
2. Avaliar o custo de verificar **RN08** (não persistência / ausência de rede).
3. Definir meta de cobertura para tornar **RF13** verificável (RNF09 propõe ≥ 90%).
4. Levar as decisões pendentes (análise, seção 9.2) ao solicitante antes da v1.1.
5. Backlog v1.1: **US07** (`--count`), **US08** (excluir ambíguos), **US09** (`--show-entropy`).
