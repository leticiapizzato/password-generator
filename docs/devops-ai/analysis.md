# Analise da GenAI (entrada: `ai-prompt.md`)

## Resultado do pipeline

`10 failed, 48 passed` no job `tests` (INJECT_BUG=true).

## Diagnostico da IA

- Causa raiz: `src/generator.py`, linha 41. A validacao esta como
  `MIN_LENGTH <= length < MAX_LENGTH`, tornando o limite superior (32)
  **exclusivo**. A especificacao (RF04) define 8..32 **inclusivo**.
- Classificacao: **defeito** (instrucao incorreta no codigo). As **falhas**
  observadas sao a rejeicao de `--length 32` (exit code 2) e os testes vermelhos.
- Agrupamento: as 10 falhas tem o mesmo padrao - todas usam `length=32`
  (`--length 32`, `[32]`, ou testes de classe com senha de 32 caracteres). Ou seja,
  **um unico defeito** explica os 10 testes; nao sao 10 problemas.
- Correcao minima sugerida: voltar para `MIN_LENGTH <= length <= MAX_LENGTH`.

## Validacao humana

- Conferido contra `docs/escopo-mvp.md` (RF04 e criterio de aceite 2): limites inclusivos. Confirmado.
- Conferido que os testes que passam (7 e 33 rejeitados, 8 aceito) continuam
  coerentes com a correcao. Confirmado.
- Correcao nao aplicada ao repositorio: o defeito existe apenas no job de CI.
