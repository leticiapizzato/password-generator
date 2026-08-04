# Identificação de Riscos — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C4 |
| **Documento** | Identificação de riscos |
| **Data** | 2026-07-16 (atualizado em 2026-08-04) |
| **Versão do documento** | 1.2 (situação dos riscos após a etapa de engenharia de requisitos) |
| **Fonte de análise** | Código-fonte (`src/`), testes (`tests/`), documentação (`docs/`, `README.md`), CI (`.github/workflows/ci.yml`), empacotamento (`pyproject.toml`) e verificação do repositório/ambiente (`git`, `.venv`) |

## 1. Objetivo

Este documento identifica os riscos do projeto **Password Generator**, um MVP de linha de comando
em Python 3.10.5 para geração de senhas seguras (interface `argparse`, aleatoriedade via `secrets`).
Cada risco é registrado com **ID**, **nome do risco**, **descrição** e **contexto** (a origem/evidência
que fundamenta o risco no projeto). A análise (probabilidade/impacto) e as respostas são tratadas em
documentos complementares (`riscos/analise.md` e `riscos/respostas.md`).

> **Revisão crítica (v1.1):** após validação das evidências no repositório e no ambiente, dois riscos
> inicialmente levantados foram **descartados** por terem premissa incorreta (ver seção 5). Os IDs dos
> riscos remanescentes foram **preservados** para manter a rastreabilidade entre os documentos; por isso
> a numeração salta os IDs retirados (R05 e R10).

## 2. Método de identificação

Os riscos foram levantados por inspeção dos artefatos do projeto e agrupados por categoria:

- **Segurança (SEG)** — força criptográfica e exposição da senha gerada.
- **Técnico/Ambiente (TEC)** — dependências, versões e diferenças de plataforma.
- **Qualidade (QUA)** — testes e consistência de validações.
- **Processo/Gestão (PRO)** — versionamento e continuidade.

## 3. Riscos identificados

### R01 — Regressão na fonte de aleatoriedade criptográfica
- **Categoria:** Segurança (SEG)
- **Descrição:** Alterações futuras podem substituir o módulo `secrets` por um gerador
  pseudoaleatório inadequado à segurança (ex.: `random`), enfraquecendo a força das senhas geradas
  sem que isso seja percebido.
- **Contexto:** Os requisitos RF01 e RNF06 exigem fonte criptograficamente segura. Hoje
  `src/generator.py` usa `secrets.choice` e `secrets.SystemRandom().shuffle`, porém **não há teste
  que garanta o uso de `secrets`**; uma refatoração descuidada passaria despercebida na CI.

### R02 — Exposição da senha gerada na saída/terminal
- **Categoria:** Segurança (SEG)
- **Descrição:** A senha é impressa em `stdout` e pode permanecer em histórico de shell, buffer do
  terminal, logs de execução ou ser observada em ambientes compartilhados.
- **Contexto:** O RF12 define saída de uma linha em `stdout` e `src/main.py` executa `print(password)`.
  Em uso real (PowerShell/bash), a senha pode ser retida no histórico de comandos ou capturada por
  redirecionamento/observação de tela.

### R03 — Configuração padrão de baixa entropia
- **Categoria:** Segurança (SEG)
- **Descrição:** Com os padrões atuais, o usuário que executar a CLI sem flags obtém uma senha
  composta apenas por letras minúsculas, com entropia inferior à esperada para uma "senha forte".
- **Contexto:** Em `src/cli_argparse.py`, `--lower` tem `default=True` e `--upper`, `--number` e
  `--wildcards` têm `default=False`. Assim, `password-gen-argparse` sem argumentos gera 16 caracteres
  somente minúsculos, contrastando com a proposta de "senhas fortes" do escopo.

### R04 — Dependência de versão específica do Python
- **Categoria:** Técnico/Ambiente (TEC)
- **Descrição:** O projeto exige Python 3.10.5+ e usa recursos dessa faixa; ambientes com versões
  anteriores não executam a aplicação nem os testes.
- **Contexto:** `pyproject.toml` define `requires-python = ">=3.10.5"` e o README exige a versão no
  `PATH`. O código usa `argparse.BooleanOptionalAction` (3.9+) e anotações `list[str]`. Máquinas de
  colegas/laboratório podem ter versões divergentes.

### R06 — Divergência entre ambiente de desenvolvimento (Windows) e CI (Linux)
- **Categoria:** Técnico/Ambiente (TEC)
- **Descrição:** O desenvolvimento ocorre em Windows enquanto o CI roda em Linux; diferenças de path,
  shell e nome do entrypoint podem causar falhas que não aparecem localmente (ou vice-versa).
- **Contexto:** O README foca em PowerShell/`make.cmd`, mas `.github/workflows/ci.yml` usa
  `ubuntu-latest` (sem matriz de SO). O teste `test_cli_installed_entrypoint_success` já precisa
  diferenciar `password-gen-argparse.exe` (Windows) do binário Linux.

### R07 — Cobertura de testes insuficiente para o comportamento aleatório
- **Categoria:** Qualidade (QUA)
- **Descrição:** Os testes validam tamanho e presença de classes, mas não avaliam a
  distribuição/aleatoriedade nem a unicidade das senhas, permitindo que defeitos sutis passem.
- **Contexto:** `tests/test_generator.py` (11 testes) cobre validações e integração via CLI, porém não
  há verificação estatística, de repetibilidade ou de não-colisão das senhas geradas.

### R08 — Inconsistência entre validações da CLI e do core
- **Categoria:** Qualidade (QUA)
- **Descrição:** As regras de faixa (8..32) e as mensagens de erro estão duplicadas entre a CLI e o
  core; alterar uma sem a outra produz comportamento e mensagens divergentes.
- **Contexto:** `src/cli_argparse.py` valida e emite "deve estar entre 8 e 32", enquanto
  `src/generator.py` valida novamente com textos distintos ("tamanho minimo/maximo"). O uso do core
  como biblioteca (fora da CLI) não passa pela validação de `validate_length`.

### R09 — Versionamento desalinhado com o processo de release
- **Categoria:** Processo/Gestão (PRO)
- **Descrição:** A versão declarada no empacotamento está defasada em relação ao release planejado;
  publicar sem alinhar versão e tag gera inconsistência de entrega.
- **Contexto:** `pyproject.toml` está em `version = "0.1.0"`, enquanto `docs/release.md` prevê bump para
  `1.0.0`, criação de tag anotada `v1.0.0` e publicação no GitHub.

### R11 — Baixo fator de continuidade (bus factor) do projeto
- **Categoria:** Processo/Gestão (PRO)
- **Descrição:** Por ser um trabalho de curso com equipe reduzida, o conhecimento fica concentrado; a
  indisponibilidade do responsável compromete manutenção, correções e a entrega no prazo.
- **Contexto:** Projeto acadêmico (UFG — C4) com estrutura enxuta e histórico de commits individuais,
  sujeito a prazo fixo de curso, o que amplia o impacto de qualquer ausência.

## 4. Resumo

Após a revisão crítica, permanecem **9 riscos** distribuídos em quatro categorias:

| ID | Risco | Categoria |
|----|-------|-----------|
| R01 | Regressão na fonte de aleatoriedade criptográfica | Segurança |
| R02 | Exposição da senha gerada na saída/terminal | Segurança |
| R03 | Configuração padrão de baixa entropia | Segurança |
| R04 | Dependência de versão específica do Python | Técnico/Ambiente |
| R06 | Divergência entre ambiente de dev (Windows) e CI (Linux) | Técnico/Ambiente |
| R07 | Cobertura de testes insuficiente para aleatoriedade | Qualidade |
| R08 | Inconsistência entre validações da CLI e do core | Qualidade |
| R09 | Versionamento desalinhado com o processo de release | Processo/Gestão |
| R11 | Baixo fator de continuidade (bus factor) | Processo/Gestão |

**Distribuição por categoria:** Segurança (3), Técnico/Ambiente (2), Qualidade (2), Processo/Gestão (2).

Os riscos de **segurança** (R01–R03) são os mais sensíveis por afetarem o propósito central do produto
(gerar senhas fortes). Os riscos **técnicos** (R04, R06) concentram-se em impedir a execução/validação
em diferentes ambientes. Os riscos de **qualidade e processo** (R07, R08, R09, R11) afetam a
confiabilidade da entrega e a manutenção futura. A priorização quantitativa é feita em
`riscos/analise.md`.

## 5. Revisão crítica (riscos descartados)

Durante a revisão, dois riscos inicialmente identificados foram **verificados no repositório/ambiente e
descartados** por não se sustentarem:

| ID retirado | Risco original | Motivo do descarte |
|-------------|----------------|--------------------|
| ~~R05~~ | Dependência de teste indisponível (`pytest>=9.0.0`) | **Premissa falsa.** O ambiente possui **pytest 9.0.3** instalado e a suíte passa; `pytest>=9.0.0` é uma restrição válida e satisfeita — não há bloqueio de instalação/CI. O único resíduo (ausência de limite superior no pin) é uma dívida menor de manutenção, insuficiente para caracterizar um risco relevante. |
| ~~R10~~ | Documentação divergente da implementação (branch `master` vs `main`) | **Premissa falsa.** A branch principal do repositório é **`master`** (local e `origin/master`); portanto `docs/release.md` está **correto** ao usar `git push origin master`. O resíduo (número "11 passed" fixo no README) é trivial e não caracteriza risco de projeto. |

## 6. Situação após a etapa de engenharia de requisitos (v1.2)

A especificação dos requisitos (`requisitos/`) e os ajustes de código dela decorrentes alteraram o quadro
de riscos. Atualização por item:

| ID | Risco | Situação | Evidência |
|----|-------|----------|-----------|
| R01 | Regressão na fonte de aleatoriedade | ✅ **Mitigado** | `test_generate_password_uses_secrets_module` verifica o uso de `secrets.choice`; `test_generator_does_not_import_insecure_random` barra a reintrodução de `random` |
| R02 | Exposição da senha no terminal/histórico | ⚠️ **Em aberto** | Risco do **ambiente**, não da aplicação. Segue válido |
| R03 | Configuração padrão de baixa entropia | ✅ **Eliminado** | A composição padrão passou a ativar as quatro classes (≈105 bits). A causa deixou de existir |
| R04 | Dependência de versão do Python | ⚠️ **Em aberto** | Sem mudança |
| R06 | Divergência entre dev (Windows) e CI (Linux) | ⚠️ **Em aberto** | A matriz de CI segue apenas com `ubuntu-latest` |
| R07 | Cobertura insuficiente do comportamento aleatório | ✅ **Mitigado** | `test_generated_passwords_do_not_collide` valida 1000 senhas distintas |
| R08 | Inconsistência entre validações da CLI e do core | ✅ **Resolvido** | Faixa 8..32 centralizada em `MIN_LENGTH`/`MAX_LENGTH` no core; a CLI importa as constantes. Mensagem de erro passou a ser única |
| R09 | Versionamento desalinhado com o release | 🔄 **Em andamento** | Version bump para `1.0.0` executado; resta a tag anotada |
| R11 | Baixo fator de continuidade (bus factor) | ⚠️ **Em aberto** | Sem mudança |

**Resumo:** de 9 riscos, **4 foram resolvidos ou mitigados** (R01, R03, R07, R08) e 1 está em andamento
(R09). Os 4 remanescentes (R02, R04, R06, R11) não têm relação com o produto em si — dizem respeito ao
ambiente de uso, ao ambiente de execução e à estrutura da equipe.

> **Observação metodológica.** R08 foi **aprofundado** pela análise de requisitos: o registro original
> falava em "validação duplicada", mas a especificação revelou que uma das validações era **inalcançável
> por qualquer entrada** e que o teste que a cobria passava capturando outra exceção. A gestão de riscos
> apontou a região certa; a engenharia de requisitos encontrou o defeito concreto.
