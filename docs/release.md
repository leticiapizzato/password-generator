# Checklist de Release v1.0.0

> **Situação em 2026-08-04:** release preparado e publicado no repositório (commits e tag anotada
> `v1.0.0` enviados). Restam apenas os itens que dependem da interface do GitHub e o registro do
> backlog — listados na seção "Pendências" ao final.

## Preparação do Código

- [x] Confirmar que a branch de release está atualizada com a branch principal.
- [x] Confirmar que não existem conflitos de merge pendentes.
- [x] Revisar mudanças finais de código (`git diff`) antes da tag.
- [x] Garantir que não há arquivos temporários ou segredos versionados.
      → 23 arquivos versionados, sem `.env`, chaves, `__pycache__` ou caches de teste.

## Ambiente e Build

- [x] Executar `make install` com sucesso no ambiente local.
- [x] Confirmar criação/uso correto do ambiente virtual `.venv`.
- [x] Validar instalação do pacote em modo editable (`pip install -e .[dev]`).
- [x] Validar entrypoint instalado (`password-gen-argparse`).

## Testes e Qualidade

- [x] Executar `make test` com sucesso.
- [x] Confirmar que todos os testes automatizados passam (`pytest -q`) → **24 passed**.
- [x] Validar manualmente geração de senha com cenário padrão.
- [x] Validar manualmente geração de senha com múltiplas classes ativas.
- [x] Validar cenário de erro para `--length` fora da faixa (8..32).
- [x] Validar cenário de erro com nenhuma classe ativa.
- [ ] **Confirmar o pipeline de CI verde no GitHub Actions.**
      → Não verificado localmente. A suíte mudou de 11 para 24 testes nesta versão e o pipeline roda em
      `ubuntu-latest`, enquanto o desenvolvimento é em Windows (risco **R06**).

## Consistência Funcional

- [x] Confirmar defaults da CLI: `length=16` e as **quatro** classes habilitadas.
- [x] Confirmar que `--length` aceita apenas valores entre 8 e 32 (limites inclusivos).
- [x] Confirmar que a senha respeita o tamanho solicitado.
- [x] Confirmar que classes ativas aparecem na senha gerada.
- [x] Confirmar o contrato de saída: sucesso `0`, erro `2` com `stdout` vazio.

## Documentação

- [x] Revisar `README.md` (setup, execução, testes e erros esperados).
- [x] Revisar `docs/escopo-mvp.md` e alinhar com implementação final.
- [x] Revisar `docs/release.md` antes da publicação.
- [x] Confirmar instruções de `make` para ambiente Windows.
      → `make.cmd install`, `test` e `run` executados com sucesso.

## Versionamento

- [x] Atualizar versão para `1.0.0` no `pyproject.toml`.
- [x] Criar commit exclusivo de version bump. → `21c56f3`
- [x] Criar tag anotada `v1.0.0`. → objeto `7f276d2`, aponta para `1087301`
- [x] Validar histórico de commits e mensagens no padrão Conventional Commits.

## Publicação no GitHub

- [x] Enviar commits finais para o remoto (`git push origin master`).
- [x] Enviar tags para o remoto (`git push origin v1.0.0`).
- [ ] Criar release `v1.0.0` no GitHub com notas de versão.
- [ ] Incluir no release notes: funcionalidades, validações e cobertura de testes.
- [ ] **Destacar a breaking change**: a composição padrão passou a ativar as quatro
      classes de caractere. Quem dependia da saída anterior (apenas minúsculas) deve
      usar `--no-upper --no-number --no-wildcards`.
- [ ] Registrar a remoção do RF10 (requisito inalcançável) nas notas de versão.

> Os quatro itens acima dependem da interface do GitHub. **A mensagem da tag anotada já contém todo esse
> conteúdo** — funcionalidades, validações, a breaking change e a remoção do RF10 — e pode ser aproveitada
> na descrição do release:
>
> ```powershell
> git tag -l -n99 v1.0.0
> ```

## Pós-Release

- [x] Confirmar que a tag `v1.0.0` está visível no repositório remoto.
      → `git ls-remote --tags origin` confirma a tag anotada.
- [x] Validar que o projeto pode ser instalado e executado a partir de clone limpo.
      → Clone em `v1.0.0`, `make install` e `make test` (**24 passed**), entrypoint validado.
- [ ] Registrar backlog de melhorias para `v1.1.0`.

## Pendências

| Item | Motivo |
|------|--------|
| Confirmar CI verde | Requer acesso à aba Actions do GitHub |
| Criar o release `v1.0.0` na interface | Requer acesso ao GitHub; conteúdo já pronto na tag |
| Registrar backlog `v1.1.0` | Candidatos já especificados como **US07** (`--count`), **US08** (excluir caracteres ambíguos) e **US09** (`--show-entropy`) em `requisitos/historias-usuario.md`, seção 3. Falta a decisão de escopo |
| Decisões de requisitos em aberto | `requisitos/analise-elicitacao.md`, seção 9.2 — entre elas o limiar mínimo de entropia (**L01**) |
