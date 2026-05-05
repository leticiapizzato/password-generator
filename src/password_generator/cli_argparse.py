"""Interface de linha de comando usando argparse."""

from __future__ import annotations

import argparse

from password_generator.generator import generate_password


def build_parser() -> argparse.ArgumentParser:
    """Cria e retorna o parser da CLI com argparse."""
    parser = argparse.ArgumentParser(
        description="Gerador de senhas seguras (argparse)."
    )
    parser.add_argument(
        "--length",
        type=int,
        default=16,
        help="Quantidade de caracteres da senha (padrao: 16).",
    )
    return parser


def main() -> None:
    """Executa a CLI baseada em argparse."""
    parser = build_parser()
    args = parser.parse_args()
    print(generate_password(args.length))


if __name__ == "__main__":
    main()
