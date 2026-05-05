"""Interface de linha de comando usando argparse."""

from __future__ import annotations

import argparse


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
        type=int,
        default=16,
        help="Quantidade de caracteres da senha (padrao: 16).",
    )
    return parser



