"""Monta o prompt de diagnostico de falha de pipeline para uma GenAI.

Le o log do pytest, extrai os testes que falharam e o trecho relevante do
traceback, anexa o codigo-fonte suspeito e grava um prompt pronto para ser
enviado a um LLM. Usa apenas a biblioteca padrao.

Seguranca: o log e filtrado para mascarar valores que parecam credenciais
antes de entrar no prompt.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = PROJECT_ROOT / "src" / "generator.py"
MAX_LOG_CHARS = 6000

SECRET_PATTERN = re.compile(
    r"(?i)(token|secret|password|api[_-]?key)\s*[=:]\s*\S+"
)

PROMPT_TEMPLATE = """\
Atue como engenheiro DevOps/QA especialista em Python e CI/CD.

Contexto: o job de testes de um pipeline falhou. Projeto: CLI de geracao de
senhas (main.py -> cli_argparse.py -> generator.py), testada com pytest.
Regra documentada (RF04): --length aceita 8..32, limites INCLUSIVOS.

Testes que falharam:
{failed}

Trecho relevante do log:
```
{log}
```

Codigo-fonte suspeito (src/generator.py):
```python
{source}
```

Tarefa (nao altere nada, apenas diagnostique):
1. Identifique a causa raiz e a linha responsavel.
2. Classifique como defeito, erro ou falha.
3. Sugira a correcao minima.
4. Aponte o que precisa ser validado por um humano antes de aplicar.
"""


def mask_secrets(text: str) -> str:
    """Mascara pares chave=valor que lembrem credenciais."""
    return SECRET_PATTERN.sub(lambda m: f"{m.group(1)}=***", text)


def extract_failed(log: str) -> str:
    """Devolve as linhas FAILED do resumo do pytest."""
    failed = [line for line in log.splitlines() if line.startswith("FAILED")]
    return "\n".join(failed) if failed else "(nenhum teste FAILED encontrado)"


def main() -> None:
    """Gera o arquivo de prompt a partir do log informado."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    log = args.log.read_text(encoding="utf-8", errors="replace")
    prompt = PROMPT_TEMPLATE.format(
        failed=extract_failed(log),
        log=mask_secrets(log)[-MAX_LOG_CHARS:],
        source=SOURCE_FILE.read_text(encoding="utf-8"),
    )
    args.out.write_text(prompt, encoding="utf-8")
    print(f"Prompt gravado em {args.out}")


if __name__ == "__main__":
    main()
