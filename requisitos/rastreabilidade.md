# Rastreabilidade e Justificativa dos Artefatos — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C10 (Engenharia de Requisitos com GenAI) |
| **Documento** | Justificativa da seleção de artefatos e matriz de rastreabilidade |
| **Data** | 2026-08-04 |
| **Versão do documento** | 1.0 |

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
| **Caso de uso expandido** | Fluxos de exceção invisíveis (L05) | Nesta CLI, **a maior parte do comportamento é desvio**: 4 fluxos de exceção para 1 fluxo principal. Histórias descrevem valor; caso de uso é o formato que dá estrutura a pré-condições, pós-condições e exceções |
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

Legenda: ✅ coberto por teste automatizado · ⚠️ implementado sem teste · ❌ sem implementação ou sem teste

| Requisito | Regra | História | Caso de uso | Teste automatizado | Status |
|-----------|-------|----------|-------------|--------------------|--------|
| RF01 | RN07 | US01, US06 | UC01 | — | ⚠️ uso de `secrets` não é verificado |
| RF02 | RN02 | US02 | UC01 | `test_generate_password_has_expected_length` | ✅ |
| RF03 | RN01 | US01 | UC01 / FA01 | `test_cli_parser_defaults` | ✅ |
| RF04 | RN02 | US02 | UC01 / FE01, FE02 | `test_..._below_minimum`, `test_..._above_maximum`, `test_cli_integration_error_for_invalid_length` | ✅ |
| RF05 | RN06, RN09 | US03 | UC01 / FA02 | `test_cli_parser_defaults` | ⚠️ desligamento não testado |
| RF06 | RN06 | US03 | UC01 | `test_..._contains_all_selected_classes` | ✅ |
| RF07 | RN06 | US03 | UC01 | `test_..._contains_all_selected_classes` | ✅ |
| RF08 | RN06 | US03 | UC01 | `test_..._contains_all_selected_classes` | ✅ |
| RF09 | RN03 | US04 | UC01 / FE03 | `test_..._fails_when_no_class_is_active` | ⚠️ só no core, não na CLI |
| **RF10** | **RN05** | **—** | **UC01 / FE04** | `test_..._incompatible_length_and_classes` | ❌ **código morto; teste falso-positivo** |
| RF11 | — | US01 | UC01 | `test_cli_installed_entrypoint_success` | ✅ |
| RF12 | RN10 | US01 | UC01 | `test_cli_integration_success` | ⚠️ formato exato não verificado |
| RF13 | — | — | — | a própria suíte (11 testes) | ⚠️ sem meta de cobertura |
| RF14 | RN04 | US03 | UC01 / passo 7 | `test_..._contains_all_selected_classes` | ✅ |
| RF15 | RN10 | US04 | UC01 | parcial (`returncode != 0`) | ⚠️ código 2 não fixado |
| RF16 | — | US05 | UC02 | — | ❌ `--help` sem teste |

### 2.1 O requisito órfão

**RF10 é o único requisito sem história de usuário.** Isso não foi omissão: ao tentar escrever a
história, não foi possível formular um "para que" com valor para o usuário — porque **não existe entrada
capaz de produzir esse comportamento** (`analise-elicitacao.md`, seção 7.1). A matriz funcionou como
instrumento de detecção: um requisito que não consegue virar história e cujo teste passa por outro
motivo é um forte indício de requisito inválido.

## 3. Cobertura das regras de negócio

| Regra | Documentada antes? | Especificada agora | Testada |
|-------|--------------------|--------------------|---------|
| RN01 — padrão 16 | Sim | US01, UC01 | ✅ |
| RN02 — faixa 8..32 | Sim | US02, FE01/FE02 | ✅ (limites inclusivos ⚠️) |
| RN03 — ≥ 1 classe ativa | Sim | US04, FE03 | ⚠️ só no core |
| RN04 — representatividade | **Não** | US03, UC01 passo 7 | ✅ |
| RN05 — tamanho ≥ nº classes | Parcial | FE04 (não realizável) | ❌ |
| RN06 — alfabetos | **Não** | US03, protótipo §2 | ❌ |
| RN07 — CSPRNG | Sim | US06 | ❌ (risco R01) |
| RN08 — não persistência | Parcial | US06, UC01 | ❌ |
| RN09 — composição padrão | **Não** | US01, FA01 | ✅ (mas **pendente de decisão**) |
| RN10 — contrato de saída | **Não** | US04, protótipo §6 | ⚠️ parcial |

**Resultado:** as 5 regras que não estavam documentadas passaram a ter especificação. Três delas
(RN06, RN07, RN08) seguem **sem teste** — é a dívida técnica prioritária desta etapa.

## 4. Convergência com a gestão de riscos

Os achados desta análise foram levantados a partir dos **requisitos**, sem consultar `riscos/`. A
sobreposição posterior é uma validação cruzada útil:

| Achado (requisitos) | Risco correspondente | Leitura |
|---------------------|----------------------|---------|
| L02 / RN09 — composição padrão fraca | **R03** — baixa entropia padrão | Mesmo problema por dois caminhos. Confirma prioridade **alta** |
| RN07 sem teste | **R01** — regressão na fonte de aleatoriedade | A especificação de US06 fornece o critério que faltava para escrever o teste |
| A03 / RF10 — código morto | **R08** — validação duplicada CLI/core | A análise de requisitos **aprofundou** o risco: não era só duplicação, é regra inalcançável |
| US06 — cenário de não colisão | **R07** — cobertura de aleatoriedade | Critério em Gherkin já pronto para virar teste |
| RN08/RNF12 — não retenção | **R02** — exposição no terminal | Requisito cobre a **aplicação**; R02 trata do **ambiente** (histórico de shell). Complementares, não duplicados |

O achado do RF10 é o único **novo** em relação ao registro de riscos — surgiu porque a especificação
exigiu reproduzir cada fluxo de exceção, o que a análise de riscos não fazia.

## 5. Próximos passos recomendados

Em ordem de prioridade:

1. **Decidir a composição padrão** (L02/RN09) — é a única pendência que muda o comportamento do caminho
   mais usado do produto. Bloqueia a aceitação de US01.
2. **Resolver o RF10** — remover a regra e corrigir o teste, ou promover o core a biblioteca com
   validação única. Enquanto não decidido, a suíte tem um teste que não testa o que diz testar.
3. **Adicionar `match=` em todos os `pytest.raises`** — impede novos falsos-positivos.
4. **Escrever os testes de US06** (CSPRNG, não persistência, não colisão) — maior lacuna de verificação
   no atributo central do produto.
5. **Documentar RN06 e RN10** no README e na ajuda da CLI.
6. Levar as decisões pendentes (análise, seção 9) para validação com o solicitante antes da v1.1.
