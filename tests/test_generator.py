"""Suite de testes para o gerador de senhas e CLI."""

from __future__ import annotations

import string
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from generator import generate_password


def test_generate_password_fails_for_length_below_minimum() -> None:
    """Deve falhar quando o tamanho for menor que 8."""
    with pytest.raises(ValueError, match="minimo"):
        generate_password(length=7)


def test_generate_password_fails_for_length_above_maximum() -> None:
    """Deve falhar quando o tamanho for maior que 32."""
    with pytest.raises(ValueError, match="maximo"):
        generate_password(length=33)


def test_generate_password_fails_when_no_class_is_active() -> None:
    """Deve falhar quando nenhuma classe de caractere estiver ativa."""
    with pytest.raises(ValueError, match="ao menos uma classe"):
        generate_password(
            length=16,
            upper=False,
            lower=False,
            number=False,
            wildcards=False,
        )


def test_generate_password_has_expected_length() -> None:
    """Valida se a senha possui o tamanho solicitado."""
    password = generate_password(length=12, lower=True)
    assert len(password) == 12


def test_generate_password_contains_all_selected_classes() -> None:
    """Valida se a senha contem ao menos um caractere de cada classe ativa."""
    password = generate_password(
        length=20,
        upper=True,
        lower=True,
        number=True,
        wildcards=True,
    )

    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.ascii_lowercase for char in password)
    assert any(char in string.digits for char in password)
    assert any(char in string.punctuation for char in password)


def test_cli_integration_success() -> None:
    """Deve gerar senha com sucesso via CLI."""
    result = subprocess.run(
        [sys.executable, str(SRC_DIR / "main.py"), "--length", "16", "--lower"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    password = result.stdout.strip()
    assert len(password) == 16


def test_cli_integration_error_for_invalid_length() -> None:
    """Deve retornar erro via CLI para tamanho fora da faixa permitida."""
    result = subprocess.run(
        [sys.executable, str(SRC_DIR / "main.py"), "--length", "33"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "entre 8 e 32" in result.stderr
