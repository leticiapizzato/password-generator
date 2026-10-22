"""Testes de integracao (happy path) do fluxo CLI -> parser -> core -> stdout.

Escopo: valida a comunicacao entre os componentes (``main.py``,
``cli_argparse.py`` e ``generator.py``) atraves da fronteira real do processo,
executando a CLI como subprocesso. Nao exercita os ramos de erro (ver
``test_cli_integration_edge.py``).

Convencoes herdadas da suite existente (sem novas libs):
- ``pytest`` como unico framework de teste;
- execucao por subprocesso via ``subprocess`` + ``sys.executable``;
- resolucao de caminhos com ``pathlib``;
- contrato de saida RF15 (codigo 0, senha em stdout, stderr vazio).
"""

from __future__ import annotations

import string
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
MAIN = SRC_DIR / "main.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Executa a CLI como subprocesso (integracao real entre camadas)."""
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        capture_output=True,
        text=True,
        check=False,
    )


# --- Fluxo feliz de ponta a ponta --------------------------------------------


def test_default_run_produces_sixteen_char_password() -> None:
    """Sem argumentos: fluxo completo deve devolver senha padrao de 16 chars."""
    result = run_cli()

    assert result.returncode == 0
    assert result.stderr == ""
    assert len(result.stdout.strip()) == 16
    assert result.stdout.count("\n") == 1


@pytest.mark.parametrize("length", [8, 16, 24, 32])
def test_length_flag_propagates_through_all_layers(length: int) -> None:
    """O --length informado deve chegar intacto ao core e definir o tamanho."""
    result = run_cli("--length", str(length))

    assert result.returncode == 0
    assert result.stderr == ""
    assert len(result.stdout.strip()) == length


def test_default_run_contains_all_four_classes() -> None:
    """A composicao padrao deve integrar as quatro classes na saida final."""
    password = run_cli("--length", "32").stdout.strip()

    assert any(c in string.ascii_uppercase for c in password)
    assert any(c in string.ascii_lowercase for c in password)
    assert any(c in string.digits for c in password)
    assert any(c in string.punctuation for c in password)


@pytest.mark.parametrize(
    "flag, forbidden_set",
    [
        ("--no-upper", string.ascii_uppercase),
        ("--no-lower", string.ascii_lowercase),
        ("--no-number", string.digits),
        ("--no-wildcards", string.punctuation),
    ],
)
def test_disabling_one_class_removes_it_end_to_end(
    flag: str, forbidden_set: str
) -> None:
    """Desligar uma classe pela CLI deve refleti-la ausente na senha final."""
    password = run_cli("--length", "32", flag).stdout.strip()

    assert len(password) == 32
    assert not any(c in forbidden_set for c in password)


def test_single_class_only_run() -> None:
    """Apenas uma classe ativa: a saida deve conter somente aquele conjunto."""
    password = run_cli(
        "--length", "20", "--no-upper", "--no-number", "--no-wildcards"
    ).stdout.strip()

    assert len(password) == 20
    assert all(c in string.ascii_lowercase for c in password)


def test_help_flag_lists_parameters_and_exits_zero() -> None:
    """--help deve integrar as descricoes dos parametros e sair com codigo 0."""
    result = run_cli("--help")

    assert result.returncode == 0
    for flag in ("--length", "--lower", "--upper", "--number", "--wildcards"):
        assert flag in result.stdout


def test_installed_entrypoint_matches_module_run() -> None:
    """O entrypoint instalado e a execucao por modulo devem ser equivalentes."""
    exe_name = (
        "password-gen-argparse.exe"
        if sys.platform.startswith("win")
        else "password-gen-argparse"
    )
    entrypoint = Path(sys.executable).with_name(exe_name)
    if not entrypoint.exists():
        pytest.skip("entrypoint instalado nao encontrado no ambiente")

    result = subprocess.run(
        [str(entrypoint), "--length", "16"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert len(result.stdout.strip()) == 16


def test_success_output_contract() -> None:
    """Sucesso: codigo 0, uma unica linha em stdout e stderr vazio (RF15)."""
    result = run_cli("--length", "24")

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout.count("\n") == 1
    assert len(result.stdout.strip()) == 24
