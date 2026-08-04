"""Interface de linha de comando usando argparse."""

from __future__ import annotations

import argparse

from generator import MAX_LENGTH, MIN_LENGTH


def parse_length(value: str) -> int:
    """Converte o argumento de tamanho da senha para inteiro.

    A validacao da faixa permitida NAO acontece aqui: ela e responsabilidade
    unica de ``generator.generate_password``, que e chamado em seguida por
    ``main``. Manter a regra em um so lugar evita mensagens divergentes entre
    a CLI e o core.

    Args:
        value: Valor recebido pela linha de comando.

    Returns:
        Tamanho convertido para inteiro.

    Raises:
        argparse.ArgumentTypeError: Se o valor nao for um inteiro valido.
    """
    try:
        return int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "O valor de --length deve ser um numero inteiro."
        ) from error


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
        type=parse_length,
        default=16,
        help=(
            f"Quantidade de caracteres da senha "
            f"(entre {MIN_LENGTH} e {MAX_LENGTH}, padrao: 16)."
        ),
    )
    return parser



