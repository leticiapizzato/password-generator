# Password Generator

Gerador de senhas seguras em **Python 3.10.5** com interface CLI em `argparse`.

## Objetivo

Fornecer uma CLI simples para gerar senhas fortes com validações de entrada,
permitindo configurar tamanho e classes de caracteres.

## Stack

- Python 3.10.5
- argparse
- secrets + string
- pytest
- setuptools + pyproject.toml

## Estrutura

- `src/main.py`: ponto de entrada.
- `src/cli_argparse.py`: parser e validações da CLI.
- `src/generator.py`: lógica de geração de senha.
- `tests/test_generator.py`: testes automatizados.
- `docs/escopo-mvp.md`: escopo funcional.

## Pré-requisitos

- Python 3.10.5 no `PATH`
- `pip` habilitado

Validação rápida:

```powershell
python --version
python -m pip --version
```

## Instalação e Execução

### Windows (recomendado neste projeto)

```powershell
.\make install
.\make run
.\make test
.\make uninstall
```

### Linux/macOS

```bash
make install
make run
make test
make uninstall
```

### Instalação manual (sem make)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

## Comandos Disponíveis

### CLI instalada

```powershell
password-gen-argparse --length 16
```

### Execução direta por módulo

```powershell
python src/main.py --length 16
```

### Parâmetros da CLI

- `--length`: tamanho da senha (8 a 32, padrão 16)
- `--lower` / `--no-lower`: minúsculas (padrão habilitado)
- `--upper` / `--no-upper`: maiúsculas (padrão desabilitado)
- `--number` / `--no-number`: números (padrão desabilitado)
- `--wildcards` / `--no-wildcards`: especiais (padrão desabilitado)

Exemplo:

```powershell
password-gen-argparse --length 20 --upper --number --wildcards
```

Exemplo de saída:

```text
bkaGsjZVX8Ft9VOFt9QL
```

## Targets do Makefile

- `install`: cria/atualiza `.venv` e instala `.[dev]`
- `run`: executa `src/main.py --length 16`
- `test`: executa `pytest -q`
- `uninstall`: remove o pacote `password-generator` do `.venv`

## Erros Esperados

- `--length` fora da faixa (ex.: 7 ou 33):
  - `O valor de --length deve estar entre 8 e 32.`
- nenhuma classe ativa (`--no-lower --no-upper --no-number --no-wildcards`):
  - `Selecione ao menos uma classe de caractere.`
- tipo inválido em `--length` (ex.: `abc`):
  - `O valor de --length deve ser um numero inteiro.`

## Validação Rápida do Projeto

```powershell
.\make install
.\make test
.\make run
```

Resultado esperado dos testes:

```text
11 passed
```
