# Respostas aos Riscos — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C4 |
| **Documento** | Plano de respostas aos riscos |
| **Data** | 2026-07-16 |
| **Versão do documento** | 1.1 (revisão crítica) |
| **Base** | `riscos/identificacao.md` e `riscos/analise.md` (mesmos IDs) |

## 1. Objetivo

Definir, para cada risco analisado, a **estratégia de resposta**, a **justificativa** da escolha e as
**ações propostas**. As estratégias adotadas seguem o vocabulário clássico de gestão de riscos para
ameaças: **Evitar**, **Mitigar** (reduzir), **Transferir** e **Aceitar**.

> **Revisão crítica (v1.1):** os riscos ~~R05~~ e ~~R10~~ foram **descartados** na identificação por
> premissa incorreta (ver `riscos/identificacao.md`, seção 5). Este plano trata os **9 riscos
> remanescentes**, com IDs preservados.

## 2. Respostas por risco

### R01 — Regressão na fonte de aleatoriedade criptográfica
- **Estratégia:** Mitigar
- **Justificativa:** O impacto é alto (segurança do produto), então convém uma barreira automatizada
  barata que impeça a regressão sem reescrever a solução, que já é correta.
- **Ações propostas:**
  1. Adicionar teste que garanta o uso de fonte segura (ex.: monkeypatch/spy em `secrets.choice` ou
     verificação de que `random` não é importado no core).
  2. Registrar no README/checklist de release a exigência de `secrets` como critério de revisão.
  3. Incluir revisão obrigatória de PRs que toquem em `src/generator.py`.

### R02 — Exposição da senha gerada na saída/terminal
- **Estratégia:** Mitigar
- **Justificativa:** A saída em `stdout` é adequada ao MVP e não deve ser removida, mas o usuário
  precisa ser orientado e ter opções para reduzir a retenção do segredo.
- **Ações propostas:**
  1. Documentar boas práticas no README (limpar histórico, evitar terminais compartilhados, não
     redirecionar para arquivos).
  2. Avaliar (backlog v1.1.0) uma opção de cópia para a área de transferência em vez de imprimir.
  3. Garantir que a senha nunca seja registrada em logs/telemetria.

### R03 — Configuração padrão de baixa entropia
- **Estratégia:** Mitigar
- **Justificativa:** Mudar radicalmente os defaults poderia quebrar a compatibilidade com o escopo
  atual; reduzir o risco com orientação e/ou padrões mais fortes preserva a usabilidade.
- **Ações propostas:**
  1. Avaliar tornar `--upper` e `--number` habilitados por padrão (decisão de escopo com stakeholders).
  2. Enquanto o default não muda, destacar no `--help` e no README a combinação recomendada de classes.
  3. Considerar um aviso quando apenas uma classe estiver ativa.

### R04 — Dependência de versão específica do Python
- **Estratégia:** Mitigar
- **Justificativa:** A dependência de versão é legítima, mas o atrito de ambiente pode ser reduzido com
  documentação clara e verificação antecipada.
- **Ações propostas:**
  1. Manter o passo de validação `python --version` no README como pré-requisito obrigatório.
  2. Avaliar ampliar `requires-python` se nenhum recurso exclusivo de 3.10.5 for essencial.
  3. Registrar a versão suportada nas notas de release.

### R06 — Divergência entre ambiente de desenvolvimento (Windows) e CI (Linux)
- **Estratégia:** Mitigar
- **Justificativa:** Não é viável eliminar a diferença de plataformas, mas dá para reduzir a chance de
  falhas exclusivas de SO validando em ambos.
- **Ações propostas:**
  1. Adicionar `windows-latest` à matriz do workflow de CI (além de `ubuntu-latest`).
  2. Manter/expandir testes que já isolam diferenças de plataforma (nome do entrypoint, paths).
  3. Documentar comandos equivalentes para Windows e Linux/macOS no README.

### R07 — Cobertura de testes insuficiente para o comportamento aleatório
- **Estratégia:** Mitigar
- **Justificativa:** A confiança na aleatoriedade é central para o produto; testes adicionais de
  propriedade elevam a garantia com baixo custo.
- **Ações propostas:**
  1. Adicionar teste de unicidade (várias gerações sem colisão) e de cobertura de classes.
  2. Incluir teste de propriedade para diferentes tamanhos e combinações de classes.
  3. Medir e acompanhar a cobertura de testes ao longo da evolução.

### R08 — Inconsistência entre validações da CLI e do core
- **Estratégia:** Mitigar
- **Justificativa:** A duplicação é uma dívida técnica de baixo impacto atual; centralizar as regras
  previne divergências futuras sem alterar o comportamento.
- **Ações propostas:**
  1. Extrair limites (mín. 8 / máx. 32) para constantes compartilhadas usadas por CLI e core.
  2. Padronizar as mensagens de erro entre as camadas.
  3. Adicionar teste que compare os limites usados pela CLI e pelo core.

### R09 — Versionamento desalinhado com o processo de release
- **Estratégia:** Mitigar
- **Justificativa:** O `docs/release.md` já prevê o alinhamento; o risco é de execução, tratável com
  disciplina de processo e verificação.
- **Ações propostas:**
  1. Atualizar `pyproject.toml` para `1.0.0` em commit dedicado de version bump antes da tag.
  2. Seguir o checklist de `docs/release.md` (tag anotada `v1.0.0` e notas de versão).
  3. Validar a versão do pacote/entrypoint como parte do "Definition of Done" do release.

### R11 — Baixo fator de continuidade (bus factor)
- **Estratégia:** Mitigar
- **Justificativa:** A concentração de conhecimento não pode ser eliminada em equipe reduzida, mas pode
  ser reduzida com documentação e compartilhamento de contexto.
- **Ações propostas:**
  1. Manter README/escopo/release atualizados como base de onboarding.
  2. Registrar decisões e comandos essenciais (já apoiado por `prompts/prompts.md`).
  3. Definir um responsável reserva e compartilhar acesso ao repositório e ao ambiente.

## 3. Resumo

| ID | Risco | Estratégia | Ação-chave |
|----|-------|-----------|------------|
| R02 | Exposição da senha na saída/terminal | Mitigar | Orientar boas práticas; avaliar cópia p/ área de transferência |
| R03 | Configuração padrão de baixa entropia | Mitigar | Rever defaults/aviso; destacar combinação recomendada |
| R09 | Versionamento desalinhado com o release | Mitigar | Version bump dedicado antes da tag `v1.0.0` |
| R11 | Baixo fator de continuidade (bus factor) | Mitigar | Documentação de onboarding e responsável reserva |
| R01 | Regressão na fonte de aleatoriedade | Mitigar | Teste que fixa uso de `secrets` + revisão de PR |
| R04 | Dependência de versão do Python | Mitigar | Validar versão; avaliar ampliar `requires-python` |
| R06 | Divergência dev (Windows) vs CI (Linux) | Mitigar | Adicionar `windows-latest` à matriz de CI |
| R07 | Cobertura de testes de aleatoriedade | Mitigar | Testes de unicidade e de propriedade |
| R08 | Inconsistência de validações CLI vs core | Mitigar | Centralizar limites e mensagens |

**Distribuição de estratégias:** Evitar (0), **Mitigar (9)**, Transferir (0), Aceitar (0).

**Prioridade de execução:** com o descarte do antigo R05, **não há mais um item bloqueante**. As ações
prioritárias passam a ser as dos riscos de nível Alto — **R02, R03, R09 e R11**. As demais mitigações
podem ser planejadas junto ao release v1.0.0 e ao backlog de melhorias v1.1.0. As respostas serão
reavaliadas a cada mudança relevante de escopo, código ou ambiente.

## 4. Observação sobre riscos descartados

Os riscos ~~R05~~ (pin `pytest>=9.0.0`) e ~~R10~~ (branch `master` vs `main`) foram **removidos** por
premissa incorreta, confirmada por verificação no ambiente (pytest 9.0.3 instalado e testes passando) e
no repositório (branch principal `master`, tornando `docs/release.md` correto). Não há, portanto, ação
de resposta associada a eles.
