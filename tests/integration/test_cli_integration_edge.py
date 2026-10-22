"""Testes de integracao de borda (edge cases) do fluxo CLI completo.

Escopo: exercita os limites e os contratos de erro definidos na documentacao
(``docs/escopo-mvp.md`` e ``README.md``), verificando a integracao entre
``main.py`` -> ``cli_argparse.py`` -> ``generator.py`` na fronteira do processo.

Referencias documentais respeitadas:
- RF04 / Criterio de aceite 2: faixa valida 8..32 com limites **inclusivos**;
- RF09: ao menos uma classe de caractere deve estar ativa;
- RF15: erro -> stdout vazio, mensagem em stderr, codigo de saida **2**;
- RF16: --help documenta faixa, padrao e classes.

Sem novas libs: apenas ``pytest`` + ``subprocess`` + ``pathlib`` + ``string``,
exatamente como a suite unitaria ja existente.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
MAIN = SRC_DIR / "main.py"

# Limites documentados (RF04). Fixados aqui de proposito: um teste de borda
# tambem protege contra alteracao silenciosa da faixa publicada.
MIN_LENGTH = 8
MAX_LENGTH = 32
ERROR_EXIT_CODE = 2


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Executa a CLI como subprocesso (integracao real entre camadas)."""
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        capture_output=True,
        text=True,
        check=False,
    )


# --- Bordas inclusivas aceitas (dentro do dominio) ----------------------------


@pytest.mark.parametrize("length", [MIN_LENGTH, MAX_LENGTH])
def test_inclusive_bounds_are_accepted(length: int) -> None:
    """Os limites 8 e 32 sao validos e devem gerar senha (RF04, aceite 2)."""
    result = run_cli("--length", str(length))

    assert result.returncode == 0
    assert result.stderr == ""
    assert len(result.stdout.strip()) == length


# --- Bordas imediatamente fora do dominio (rejeitadas) ------------------------


@pytest.mark.parametrize("length", [MIN_LENGTH - 1, MAX_LENGTH + 1])
def test_just_outside_bounds_are_rejected(length: int) -> None:
    """7 e 33 (vizinhos dos limites) devem violar o contrato e sair com 2."""
    result = run_cli("--length", str(length))

    assert result.returncode == ERROR_EXIT_CODE
    assert result.stdout == ""
    assert f"entre {MIN_LENGTH} e {MAX_LENGTH}" in result.stderr


@pytest.mark.parametrize("length", ["0", "-1", "1", "100"])
def test_far_out_of_range_values_are_rejected(length: str) -> None:
    """Valores bem acima/abaixo da faixa tambem devem ser recusados."""
    result = run_cli("--length", length)

    assert result.returncode == ERROR_EXIT_CODE
    assert result.stdout == ""
    assert result.stderr.strip() != ""


# --- Bordas de tipo / formato de entrada --------------------------------------


@pytest.mark.parametrize("value", ["abc", "8.5", "16a", "", " "])
def test_non_integer_length_is_rejected(value: str) -> None:
    """--length nao inteiro deve falhar na conversao com codigo 2."""
    result = run_cli("--length", value)

    assert result.returncode == ERROR_EXIT_CODE
    assert result.stdout == ""
    assert result.stderr.strip() != ""


# --- Borda de composicao: nenhuma classe ativa (RF09) -------------------------


def test_all_classes_disabled_is_rejected() -> None:
    """Desligar as quatro classes viola o minimo de composicao (RF09)."""
    result = run_cli(
        "--no-lower", "--no-upper", "--no-number", "--no-wildcards"
    )

    assert result.returncode == ERROR_EXIT_CODE
    assert result.stdout == ""
    assert "ao menos uma classe" in result.stderr


def test_three_classes_disabled_one_active_is_accepted() -> None:
    """Borda minima de composicao: exatamente uma classe ativa deve passar."""
    result = run_cli(
        "--length", str(MIN_LENGTH), "--no-upper", "--no-number", "--no-wildcards"
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert len(result.stdout.strip()) == MIN_LENGTH


# --- Contrato de erro agregado (RF15) -----------------------------------------


@pytest.mark.parametrize(
    "args",
    [
        ["--length", str(MAX_LENGTH + 1)],
        ["--length", str(MIN_LENGTH - 1)],
        ["--length", "abc"],
        ["--no-lower", "--no-upper", "--no-number", "--no-wildcards"],
    ],
)
def test_error_contract_is_uniform(args: list[str]) -> None:
    """Todo erro de validacao: codigo 2, stdout vazio, mensagem em stderr."""
    result = run_cli(*args)

    assert result.returncode == ERROR_EXIT_CODE
    assert result.stdout == ""
    assert result.stderr.strip() != ""


# --- Borda documental: --help expoe faixa e padrao (RF16) ---------------------


def test_help_documents_range_and_default() -> None:
    """--help deve publicar a faixa inclusiva e o valor padrao (RF16)."""
    result = run_cli("--help")
    help_text = " ".join(result.stdout.split())

    assert result.returncode == 0
    assert f"entre {MIN_LENGTH} e {MAX_LENGTH}" in help_text
    assert "padrao: 16" in help_text
