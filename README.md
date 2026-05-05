# Password Generator

Gerador de senhas seguras em **Python 3.10.5**, com interface de linha de
comando baseada em `argparse`.

## Objetivo

Entregar um MVP para geração de senhas seguras no terminal, priorizando:

- simplicidade de uso em CLI
- geração com aleatoriedade criptograficamente segura (`secrets`)
- validação explícita dos parâmetros de entrada
- base evolutiva para regras de composição configuráveis

## Stack

- Python 3.10.5
- `argparse` (CLI)
- `secrets` e `string` (geração de senha)
- `pytest` (testes)
- `setuptools` + `pyproject.toml` (empacotamento)

## Estrutura do Projeto

- `src/main.py`: ponto de entrada da aplicação.
- `src/cli_argparse.py`: configuração e validação dos argumentos CLI.
- `src/generator.py`: core de geração de senha.
- `tests/test_generator.py`: testes automatizados iniciais.
- `docs/escopo-mvp.md`: escopo funcional e critérios de aceite do MVP.

## Como Rodar o Projeto

### 1. Criar e ativar ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar o projeto em modo de desenvolvimento

```powershell
pip install -e .
```

Para instalar também as dependências de desenvolvimento (testes):

```powershell
pip install -e .[dev]
```

### 3. Executar a CLI

```powershell
password-gen-argparse --length 16
```

Parâmetros disponíveis:

- `--length`: tamanho da senha (entre `8` e `32`, padrão: `16`)
- `--lower` / `--no-lower`: letras minúsculas (padrão: habilitado)
- `--upper` / `--no-upper`: letras maiúsculas (padrão: desabilitado)
- `--number` / `--no-number`: números (padrão: desabilitado)
- `--wildcards` / `--no-wildcards`: caracteres especiais (padrão: desabilitado)

Exemplo com múltiplos critérios:

```powershell
password-gen-argparse --length 20 --upper --number --wildcards
```

## Como Rodar os Testes

Com o ambiente virtual ativo:

```powershell
pytest -q
```

## Roadmap de Releases

Roadmap baseado nos requisitos definidos em `docs/escopo-mvp.md`.

### v0.1.0 - Base do MVP

- geração de senha segura com `secrets`
- parâmetro `--length` com valor padrão 16 e faixa de 8 a 32
- estrutura inicial de testes

### v0.2.0 - Critérios de Composição na CLI

- opções para habilitar/desabilitar minúsculas, maiúsculas, números e especiais
- validação para impedir execução sem classes de caractere ativas

### v0.3.0 - Regras de Consistência e Qualidade

- validação de compatibilidade entre tamanho e critérios ativos
- ampliação da suíte de testes para cobrir combinações de critérios
- melhoria de mensagens de erro e ajuda da CLI
