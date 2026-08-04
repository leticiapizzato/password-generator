# Checklist de Release v1.0.0

## Preparação do Código

- [ ] Confirmar que a branch de release está atualizada com a branch principal.
- [ ] Confirmar que não existem conflitos de merge pendentes.
- [ ] Revisar mudanças finais de código (`git diff`) antes da tag.
- [ ] Garantir que não há arquivos temporários ou segredos versionados.

## Ambiente e Build

- [ ] Executar `make install` com sucesso no ambiente local.
- [ ] Confirmar criação/uso correto do ambiente virtual `.venv`.
- [ ] Validar instalação do pacote em modo editable (`pip install -e .[dev]`).
- [ ] Validar entrypoint instalado (`password-gen-argparse`).

## Testes e Qualidade

- [ ] Executar `make test` com sucesso.
- [ ] Confirmar que todos os testes automatizados passam (`pytest -q`).
- [ ] Validar manualmente geração de senha com cenário padrão.
- [ ] Validar manualmente geração de senha com múltiplas classes ativas.
- [ ] Validar cenário de erro para `--length` fora da faixa (8..32).
- [ ] Validar cenário de erro com nenhuma classe ativa.

## Consistência Funcional

- [ ] Confirmar defaults da CLI: `length=16` e as **quatro** classes habilitadas.
- [ ] Confirmar que `--length` aceita apenas valores entre 8 e 32 (limites inclusivos).
- [ ] Confirmar que a senha respeita o tamanho solicitado.
- [ ] Confirmar que classes ativas aparecem na senha gerada.
- [ ] Confirmar o contrato de saída: sucesso `0`, erro `2` com `stdout` vazio.

## Documentação

- [ ] Revisar `README.md` (setup, execução, testes e erros esperados).
- [ ] Revisar `docs/escopo-mvp.md` e alinhar com implementação final.
- [ ] Revisar `docs/release.md` antes da publicação.
- [ ] Confirmar instruções de `make` para ambiente Windows.

## Versionamento

- [ ] Atualizar versão para `1.0.0` no `pyproject.toml`.
- [ ] Criar commit exclusivo de version bump.
- [ ] Criar tag anotada `v1.0.0`.
- [ ] Validar histórico de commits e mensagens no padrão Conventional Commits.

## Publicação no GitHub

- [ ] Enviar commits finais para o remoto (`git push origin master`).
- [ ] Enviar tags para o remoto (`git push origin v1.0.0`).
- [ ] Criar release `v1.0.0` no GitHub com notas de versão.
- [ ] Incluir no release notes: funcionalidades, validações e cobertura de testes.
- [ ] **Destacar a breaking change**: a composição padrão passou a ativar as quatro
      classes de caractere. Quem dependia da saída anterior (apenas minúsculas) deve
      usar `--no-upper --no-number --no-wildcards`.
- [ ] Registrar a remoção do RF10 (requisito inalcançável) nas notas de versão.

## Pós-Release

- [ ] Confirmar que a tag `v1.0.0` está visível no repositório remoto.
- [ ] Validar que o projeto pode ser instalado e executado a partir de clone limpo.
- [ ] Registrar backlog de melhorias para `v1.1.0`.
