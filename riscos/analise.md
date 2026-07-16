# Análise de Riscos — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C4 |
| **Documento** | Análise de riscos |
| **Data** | 2026-07-16 |
| **Versão do documento** | 1.1 (revisão crítica) |
| **Base** | `riscos/identificacao.md` (mesmos IDs) |

## 1. Objetivo

Analisar qualitativamente os riscos identificados em `riscos/identificacao.md`, atribuindo a cada um
**probabilidade**, **impacto**, uma **análise** do efeito no projeto e os **fatores condicionantes**
(gatilhos que aumentam ou reduzem a exposição). O resultado orienta a priorização das respostas em
`riscos/respostas.md`.

> **Revisão crítica (v1.1):** os riscos ~~R05~~ (pin `pytest>=9.0.0`) e ~~R10~~ (branch `master` vs
> `main`) foram **descartados** por premissa incorreta — ver seção 5 de `riscos/identificacao.md`. Esta
> análise cobre os **9 riscos remanescentes**, com os IDs preservados.

## 2. Escalas adotadas

- **Probabilidade:** Baixa · Média · Alta
- **Impacto:** Baixo · Médio · Alto
- **Nível de exposição** (severidade), derivado da combinação Probabilidade × Impacto:

| Prob. \ Impacto | Baixo | Médio | Alto |
|-----------------|-------|-------|------|
| **Alta** | Médio | Alto | Crítico |
| **Média** | Baixo | Médio | Alto |
| **Baixa** | Baixo | Baixo | Médio |

## 3. Análise por risco

### R01 — Regressão na fonte de aleatoriedade criptográfica
- **Probabilidade:** Baixa
- **Impacto:** Alto
- **Nível de exposição:** Médio
- **Análise:** O código atual está correto (`secrets`), então a probabilidade de introduzir uma
  regressão é baixa em um MVP estável. Contudo, se ocorrer, o impacto é severo: senhas previsíveis
  descaracterizam completamente o produto e violam RF01/RNF06, sem sinal visível de falha.
- **Fatores condicionantes:** refatorações no `generator.py`; ausência de teste que fixe o uso de
  `secrets`; contribuições de terceiros sem revisão focada em segurança.

### R02 — Exposição da senha gerada na saída/terminal
- **Probabilidade:** Média
- **Impacto:** Alto
- **Nível de exposição:** Alto
- **Análise:** Impressão em `stdout` é adequada para um MVP CLI, mas o dado é sensível. Em uso rotineiro
  a senha tende a ficar em histórico de shell/buffer, elevando a chance de vazamento local. O impacto é
  alto porque compromete diretamente o segredo que o produto deveria proteger.
- **Fatores condicionantes:** uso em terminais compartilhados; histórico de comandos habilitado;
  redirecionamento para arquivos/logs; captura de tela em apresentações/aulas.

### R03 — Configuração padrão de baixa entropia
- **Probabilidade:** Alta
- **Impacto:** Médio
- **Nível de exposição:** Alto
- **Análise:** É muito provável que usuários executem a CLI sem flags (comportamento padrão), obtendo
  senhas só de minúsculas. O impacto é médio: continua sendo uma senha aleatória de tamanho razoável,
  mas com entropia bem abaixo do potencial e do esperado para "senha forte".
- **Fatores condicionantes:** desconhecimento das flags; ausência de aviso/recomendação na saída;
  documentação que não destaca a combinação recomendada de classes.

### R04 — Dependência de versão específica do Python
- **Probabilidade:** Média
- **Impacto:** Médio
- **Nível de exposição:** Médio
- **Análise:** Ambientes acadêmicos costumam ter versões heterogêneas de Python. A incompatibilidade
  impede execução/testes, mas é diagnosticável e contornável com instalação da versão adequada, o que
  limita o impacto.
- **Fatores condicionantes:** máquinas de laboratório/colegas com Python antigo; `PATH` apontando para
  versão diferente; uso de recursos exclusivos de versões recentes.

### R06 — Divergência entre ambiente de desenvolvimento (Windows) e CI (Linux)
- **Probabilidade:** Média
- **Impacto:** Médio
- **Nível de exposição:** Médio
- **Análise:** Diferenças de plataforma podem produzir falhas específicas (paths, nome do entrypoint,
  shell). Como o código já trata o sufixo `.exe` e não há dependências nativas, o impacto é moderado,
  mas defeitos podem passar despercebidos até rodarem no ambiente oposto.
- **Fatores condicionantes:** CI validado só em Linux (`ubuntu-latest`, sem matriz de SO); suposições de
  path/shell; entrypoint instalado com nome diferente entre SOs.

### R07 — Cobertura de testes insuficiente para o comportamento aleatório
- **Probabilidade:** Média
- **Impacto:** Médio
- **Nível de exposição:** Médio
- **Análise:** A suíte cobre validações e integração, mas não a qualidade da aleatoriedade nem a
  unicidade. Defeitos sutis (viés de distribuição, colisões) poderiam passar sem detecção, afetando a
  confiança no produto sem quebrar os testes existentes.
- **Fatores condicionantes:** foco dos testes em validação de entrada; natureza não determinística da
  saída; ausência de testes estatísticos/de propriedade.

### R08 — Inconsistência entre validações da CLI e do core
- **Probabilidade:** Média
- **Impacto:** Baixo
- **Nível de exposição:** Baixo
- **Análise:** A duplicação de regras/mensagens (CLI e core) cria manutenção divergente. O impacto é
  baixo no MVP porque ambas as camadas hoje concordam, mas cresce se o core for reutilizado como
  biblioteca ou se apenas um lado for alterado.
- **Fatores condicionantes:** alteração de limites em um único módulo; reutilização do `generator` fora
  da CLI; ausência de constantes/validação compartilhadas.

### R09 — Versionamento desalinhado com o processo de release
- **Probabilidade:** Alta
- **Impacto:** Médio
- **Nível de exposição:** Alto
- **Análise:** A defasagem já existe (`0.1.0` vs `1.0.0` planejado), então a probabilidade de publicar
  desalinhado é alta se o checklist não for seguido. O impacto é médio: gera inconsistência entre
  pacote, tag e notas de release, exigindo retrabalho e correção de histórico.
- **Fatores condicionantes:** execução do release sem o passo de version bump; tag criada antes do
  ajuste do `pyproject.toml`; pressão de prazo levando a atalhos.

### R11 — Baixo fator de continuidade (bus factor)
- **Probabilidade:** Média
- **Impacto:** Alto
- **Nível de exposição:** Alto
- **Análise:** Em projeto de curso com poucos responsáveis, a concentração de conhecimento é comum.
  Uma ausência próxima da entrega tem impacto alto sobre o prazo e a qualidade, pois há pouca
  redundância de pessoas e de contexto.
- **Fatores condicionantes:** equipe reduzida/individual; prazo acadêmico fixo; documentação de
  onboarding limitada; ausência de responsável reserva.

## 4. Resumo

| ID | Risco | Probabilidade | Impacto | Nível de exposição |
|----|-------|---------------|---------|--------------------|
| R02 | Exposição da senha gerada na saída/terminal | Média | Alto | **Alto** |
| R03 | Configuração padrão de baixa entropia | Alta | Médio | **Alto** |
| R09 | Versionamento desalinhado com o release | Alta | Médio | **Alto** |
| R11 | Baixo fator de continuidade (bus factor) | Média | Alto | **Alto** |
| R01 | Regressão na fonte de aleatoriedade | Baixa | Alto | Médio |
| R04 | Dependência de versão específica do Python | Média | Médio | Médio |
| R06 | Divergência dev (Windows) vs CI (Linux) | Média | Médio | Médio |
| R07 | Cobertura de testes de aleatoriedade insuficiente | Média | Médio | Médio |
| R08 | Inconsistência de validações CLI vs core | Média | Baixo | Baixo |

**Priorização:** após a revisão crítica **não há risco de nível Crítico** no projeto (o antigo R05, que
recebia essa classificação, foi descartado por premissa falsa). Os riscos de maior atenção são os de
nível **Alto** — **R02, R03, R09 e R11** —, que combinam alta probabilidade e/ou alto impacto sobre
segurança, entrega e continuidade. Os riscos de nível **Médio/Baixo** (R01, R04, R06, R07, R08) são
relevantes para a robustez e a manutenção, mas comportam tratamento planejado. As estratégias e ações
estão em `riscos/respostas.md`.

## 5. Observação sobre riscos descartados

Os riscos ~~R05~~ e ~~R10~~ não constam desta análise por terem sido **removidos na etapa de
identificação** após verificação de que suas premissas eram incorretas (pytest 9.0.3 instalado e
funcional; branch principal é `master`, tornando o `docs/release.md` correto). O detalhamento está na
seção 5 de `riscos/identificacao.md`.
