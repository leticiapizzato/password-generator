"""Core de geracao de senhas seguras."""

from __future__ import annotations

import secrets
import string

#: Limites de tamanho da senha. Fonte unica de verdade: a CLI importa estas
#: constantes em vez de repetir os valores (evita divergencia entre camadas).
MIN_LENGTH = 8
MAX_LENGTH = 32


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
        ValueError: Se o tamanho estiver fora da faixa permitida.
        ValueError: Se nenhuma classe de caractere for selecionada.
    """
    if not isinstance(length, int):
        raise TypeError("O parametro length deve ser do tipo inteiro.")

    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise ValueError(
            f"O tamanho da senha deve estar entre {MIN_LENGTH} e {MAX_LENGTH}."
        )

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

    # Nao ha checagem de "tamanho < numero de classes": com MIN_LENGTH = 8 e no
    # maximo 4 classes, a condicao e sempre falsa. A validacao existia e era
    # codigo morto (RF10). Ver requisitos/analise-elicitacao.md secao 7.1.

    # Garante ao menos um caractere de cada classe selecionada.
    password_chars = [secrets.choice(chars) for chars in selected_sets]

    alphabet = "".join(selected_sets)
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(alphabet) for _ in range(remaining))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


