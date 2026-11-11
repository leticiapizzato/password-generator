# Miniprojeto DevOps + GenAI - diagnostico de falha em pipeline

## Arquivos

- `.github/workflows/devops-ai.yml`: workflow manual com os jobs `tests` e `ai-diagnosis`.
- `scripts/ai_diagnose.py`: monta o prompt de diagnostico a partir do log (stdlib, mascara credenciais).
- `docs/devops-ai/pytest-failure.log`: log do job `tests` com o erro intencional.
- `docs/devops-ai/ai-prompt.md`: prompt gerado automaticamente a partir desse log.
- `docs/devops-ai/analysis.md`: diagnostico produzido pela GenAI e validacao humana.

## Como reproduzir

1. Pipeline verde: `Actions > DevOps AI Diagnosis > Run workflow` com `inject_bug` desmarcado.
2. Pipeline com falha: rode o mesmo workflow com `inject_bug` marcado.
   O job `tests` aplica um `sed` que troca `<= length <= MAX_LENGTH` por
   `<= length < MAX_LENGTH` (off-by-one no limite superior). Ele publica
   `pytest.log` e o `generator.py` testado; o job `ai-diagnosis` gera o prompt,
   exibe no resumo da execucao e o publica como artefato `ai-prompt`.
3. Envie o `ai-prompt.md` a um LLM e compare com `analysis.md`.

O codigo de producao em `src/` nao e alterado no repositorio: o erro so existe
dentro do job de CI.
