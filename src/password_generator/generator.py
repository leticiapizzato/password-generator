"""Funcoes para geracao de senhas seguras."""

from __future__ import annotations

import secrets
import string


def generate_password(length: int = 16) -> str:
    """Gera uma senha segura com letras, numeros e simbolos.

    Args:
        length: Quantidade de caracteres da senha.

    Returns:
        Senha gerada aleatoriamente.

    Raises:
        ValueError: Se o tamanho solicitado for menor que 8.
    """
    if length < 8:
        raise ValueError("O tamanho minimo recomendado e 8 caracteres.")

    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))
