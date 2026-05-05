"""Testes iniciais para o gerador de senhas."""

from password_generator.generator import generate_password


def test_generate_password_has_expected_length() -> None:
    """Valida se a senha possui o tamanho solicitado."""
    password = generate_password(12)
    assert len(password) == 12
