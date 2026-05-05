"""Core de geracao de senhas seguras."""

from __future__ import annotations

import secrets
import string


def generate_password(
    length: int = 16,
    upper: bool = False,
    lower: bool = True,
    number: bool = False,
    wildcards: bool = False,
) -> str:
    """Gera uma senha segura com base nos criterios selecionados.

    Args:
        length: Quantidade de caracteres da senha.
        upper: Indica se letras maiusculas devem ser consideradas.
        lower: Indica se letras minusculas devem ser consideradas.
        number: Indica se numeros devem ser considerados.
        wildcards: Indica se caracteres especiais devem ser considerados.

    Returns:
        Senha gerada aleatoriamente.

    Raises:
        TypeError: Se o tipo de length nao for inteiro.
        ValueError: Se o tamanho solicitado for menor que 8.
        ValueError: Se o tamanho solicitado for maior que 32.
        ValueError: Se nenhuma classe de caractere for selecionada.
        ValueError: Se o tamanho for menor que a quantidade de classes ativas.
    """
    if not isinstance(length, int):
        raise TypeError("O parametro length deve ser do tipo inteiro.")

    if length < 8:
        raise ValueError("O tamanho minimo recomendado e 8 caracteres.")
    if length > 32:
        raise ValueError("O tamanho maximo permitido e 32 caracteres.")

    selected_sets: list[str] = []
    if upper:
        selected_sets.append(string.ascii_uppercase)
    if lower:
        selected_sets.append(string.ascii_lowercase)
    if number:
        selected_sets.append(string.digits)
    if wildcards:
        selected_sets.append(string.punctuation)

    if not selected_sets:
        raise ValueError("Selecione ao menos uma classe de caractere.")

    if length < len(selected_sets):
        raise ValueError(
            "O tamanho da senha deve ser maior ou igual ao numero de classes ativas."
        )

    # Garante ao menos um caractere de cada classe selecionada.
    password_chars = [secrets.choice(chars) for chars in selected_sets]

    alphabet = "".join(selected_sets)
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(alphabet) for _ in range(remaining))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


