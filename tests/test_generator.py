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

import generator
from cli_argparse import build_parser
from generator import MAX_LENGTH, MIN_LENGTH, generate_password


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Executa a CLI como subprocesso e devolve o resultado."""
    return subprocess.run(
        [sys.executable, str(SRC_DIR / "main.py"), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_generate_password_fails_for_length_below_minimum() -> None:
    """Deve falhar quando o tamanho for menor que MIN_LENGTH."""
    with pytest.raises(ValueError, match="entre 8 e 32"):
        generate_password(length=MIN_LENGTH - 1)


def test_generate_password_fails_for_length_above_maximum() -> None:
    """Deve falhar quando o tamanho for maior que MAX_LENGTH."""
    with pytest.raises(ValueError, match="entre 8 e 32"):
        generate_password(length=MAX_LENGTH + 1)


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


def test_generate_password_fails_for_invalid_length_type() -> None:
    """Deve falhar quando o tipo de length nao for inteiro."""
    with pytest.raises(TypeError, match="tipo inteiro"):
        generate_password(length="16")  # type: ignore[arg-type]


def test_cli_parser_defaults() -> None:
    """Valida os valores padrao definidos para a CLI."""
    parser = build_parser()
    args = parser.parse_args([])

    assert args.length == 16
    assert args.lower is True
    assert args.upper is True
    assert args.number is True
    assert args.wildcards is True


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


def test_cli_installed_entrypoint_success() -> None:
    """Valida execucao do entrypoint instalado no ambiente."""
    exe_name = "password-gen-argparse.exe" if sys.platform.startswith("win") else "password-gen-argparse"
    entrypoint = Path(sys.executable).with_name(exe_name)

    result = subprocess.run(
        [str(entrypoint), "--length", "16", "--lower"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert len(result.stdout.strip()) == 16


# --- RN07: fonte criptografica de aleatoriedade (risco R01) -------------------


def test_generate_password_uses_secrets_module(monkeypatch: pytest.MonkeyPatch) -> None:
    """A geracao deve obter cada caractere via secrets.choice."""
    calls: list[str] = []
    real_choice = generator.secrets.choice

    def spy(sequence: str) -> str:
        calls.append(sequence)
        return real_choice(sequence)

    monkeypatch.setattr(generator.secrets, "choice", spy)
    password = generate_password(length=16)

    assert len(calls) == 16
    assert len(password) == 16


def test_generator_does_not_import_insecure_random() -> None:
    """Guarda contra regressao do CSPRNG para o modulo random.

    O modulo ``random`` e adequado para simulacao, nao para segredos. Este
    teste falha se uma refatoracao futura reintroduzi-lo no core.
    """
    source = Path(generator.__file__).read_text(encoding="utf-8")

    assert "import random" not in source


def test_generated_passwords_do_not_collide() -> None:
    """Mil senhas geradas devem ser todas distintas (risco R07)."""
    passwords = {generate_password(length=16) for _ in range(1000)}

    assert len(passwords) == 1000


# --- RN02: limites inclusivos da faixa de tamanho -----------------------------


@pytest.mark.parametrize("length", [MIN_LENGTH, MAX_LENGTH])
def test_generate_password_accepts_inclusive_bounds(length: int) -> None:
    """Os limites 8 e 32 devem ser aceitos, nao rejeitados."""
    assert len(generate_password(length=length)) == length


# --- RN06: classes desligadas nao aparecem na senha ---------------------------


def test_disabled_class_is_absent_from_password() -> None:
    """Uma classe desligada nao deve aparecer na senha gerada."""
    password = generate_password(
        length=32,
        lower=False,
        upper=True,
        number=True,
        wildcards=False,
    )

    assert not any(char in string.ascii_lowercase for char in password)
    assert not any(char in string.punctuation for char in password)
    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.digits for char in password)


def test_special_characters_belong_to_expected_set() -> None:
    """Os especiais usados devem ser exatamente os de string.punctuation."""
    password = generate_password(
        length=32,
        lower=False,
        upper=False,
        number=False,
        wildcards=True,
    )

    assert all(char in string.punctuation for char in password)


# --- RN10/RF15: contrato de saida da CLI --------------------------------------


@pytest.mark.parametrize(
    "args",
    [
        ["--length", "33"],
        ["--length", "7"],
        ["--length", "abc"],
        ["--no-lower", "--no-upper", "--no-number", "--no-wildcards"],
    ],
)
def test_cli_error_contract(args: list[str]) -> None:
    """Erros devem sair com codigo 2, stdout vazio e mensagem em stderr."""
    result = run_cli(*args)

    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""


def test_cli_success_contract() -> None:
    """Sucesso deve sair com codigo 0, senha em stdout e stderr vazio."""
    result = run_cli("--length", "24")

    assert result.returncode == 0
    assert result.stderr == ""
    assert len(result.stdout.strip()) == 24
    assert result.stdout.count("\n") == 1


# --- RF16: ajuda de uso -------------------------------------------------------


def test_cli_help_lists_all_parameters() -> None:
    """A ajuda deve listar todos os parametros e sair com codigo 0."""
    result = run_cli("--help")

    assert result.returncode == 0
    for flag in ("--length", "--lower", "--upper", "--number", "--wildcards"):
        assert flag in result.stdout


def test_cli_help_documents_length_range() -> None:
    """A ajuda deve informar a faixa valida e o padrao de --length.

    O texto e normalizado antes da verificacao porque o argparse quebra as
    linhas conforme a largura do terminal: em COLUMNS=70, por exemplo, a faixa
    sai como "entre 8 e\\n32". Sem normalizar, o teste passaria localmente e
    falharia na CI apenas por diferenca de largura.
    """
    result = run_cli("--help")
    help_text = " ".join(result.stdout.split())

    assert f"entre {MIN_LENGTH} e {MAX_LENGTH}" in help_text
    assert "padrao: 16" in help_text
