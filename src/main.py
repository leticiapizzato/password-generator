"""Ponto de entrada principal do gerador de senhas."""

from __future__ import annotations

from cli_argparse import build_parser
from generator import generate_password


def main() -> None:
    """Executa o fluxo principal da aplicacao.

    Este fluxo interpreta os argumentos de linha de comando e chama
    o core de geracao de senha com os criterios informados pelo usuario.
    """
    parser = build_parser()
    args = parser.parse_args()

    password = generate_password(
        length=args.length,
        upper=args.upper,
        lower=args.lower,
        number=args.number,
        wildcards=args.wildcards,
    )
    print(password)


if __name__ == "__main__":
    main()
