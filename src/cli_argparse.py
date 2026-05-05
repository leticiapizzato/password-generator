"""Interface de linha de comando usando argparse."""

from __future__ import annotations

import argparse


def validate_length(value: str) -> int:
    """Valida o argumento de tamanho da senha para a CLI.

    Args:
        value: Valor recebido pela linha de comando.

    Returns:
        Tamanho convertido para inteiro.

    Raises:
        argparse.ArgumentTypeError: Se o valor estiver fora do intervalo 8..32.
    """
    try:
        length = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "O valor de --length deve ser um numero inteiro."
        ) from error

    if length < 8 or length > 32:
        raise argparse.ArgumentTypeError(
            "O valor de --length deve estar entre 8 e 32."
        )

    return length


def build_parser() -> argparse.ArgumentParser:
    """Cria e retorna o parser da CLI com argparse.

    Returns:
        Parser configurado com os argumentos da linha de comando.
    """
    parser = argparse.ArgumentParser(
        description="Gerador de senhas seguras (argparse)."
    )
    parser.add_argument(
        "--upper",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Habilita ou desabilita letras maiusculas (padrao: desabilitado).",
    )
    parser.add_argument(
        "--lower",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Habilita ou desabilita letras minusculas (padrao: habilitado).",
    )
    parser.add_argument(
        "--number",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Habilita ou desabilita numeros (padrao: desabilitado).",
    )
    parser.add_argument(
        "--wildcards",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Habilita ou desabilita caracteres especiais (padrao: desabilitado).",
    )
    parser.add_argument(
        "--length",
        type=validate_length,
        default=16,
        help="Quantidade de caracteres da senha (entre 8 e 32, padrao: 16).",
    )
    return parser



