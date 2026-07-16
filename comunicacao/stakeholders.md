# Comunicação aos Stakeholders — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C4 |
| **Documento** | Atualização de projeto e riscos |
| **Data** | 2026-07-16 |
| **Versão do documento** | 1.1 (após revisão crítica dos riscos) |
| **Período de referência** | Fase de preparação do release v1.0.0 |
| **Destinatários** | Stakeholders do projeto (orientação do curso, equipe e demais interessados) |

## 1. Atualização do projeto

O **Password Generator** é uma aplicação de linha de comando (CLI) em **Python 3.10.5** para geração de
senhas seguras, com interface em `argparse` e aleatoriedade criptográfica via `secrets`. O MVP está
**funcional e alinhado ao escopo** (`docs/escopo-mvp.md`):

- Geração de senha com fonte segura (`secrets`), tamanho configurável de **8 a 32** caracteres (padrão 16).
- Seleção de classes de caracteres (minúsculas, maiúsculas, números e especiais) com validações de entrada.
- **Suíte de testes automatizados** (pytest) e **pipeline de CI** no GitHub Actions em cada push/PR.
- Documentação de apoio: `README.md`, escopo do MVP e **checklist de release v1.0.0** (`docs/release.md`).

O projeto encontra-se na **fase de preparação para o release v1.0.0**. Como parte da governança, foi
conduzido um ciclo de **gestão de riscos** (identificação, análise e plano de respostas), seguido de uma
**revisão crítica** que validou cada risco contra as evidências reais do repositório e do ambiente. Toda
a documentação está em `riscos/`.

## 2. Riscos identificados (resumo)

A revisão crítica reduziu o quadro de **11 para 9 riscos**, ao descartar dois itens cujas premissas se
mostraram **incorretas** após verificação (ver seção 5). **Não há atualmente risco de nível crítico ou
bloqueante.** Os riscos de maior atenção são de nível **Alto**:

| Prioridade | ID | Risco | Nível |
|-----------|----|-------|-------|
| 1 | R02 | Exposição da senha gerada no terminal/histórico | Alto |
| 2 | R03 | Configuração padrão de baixa entropia (apenas minúsculas por padrão) | Alto |
| 3 | R09 | Versionamento desalinhado (`0.1.0` no pacote vs `1.0.0` planejado) | Alto |
| 4 | R11 | Baixo fator de continuidade (bus factor) do projeto | Alto |

Demais riscos, de nível **Médio/Baixo**: regressão na fonte de aleatoriedade (R01), dependência de
versão do Python (R04), divergência entre Windows e CI Linux (R06), cobertura de testes de aleatoriedade
(R07) e inconsistência de validações CLI/core (R08). O detalhamento completo está em
`riscos/identificacao.md` e `riscos/analise.md`.

## 3. Ações em andamento

- **Governança de riscos revisada:** identificação, análise e plano de respostas atualizados após a
  revisão crítica, com dois riscos descartados por premissa incorreta.
- **R09:** alinhamento de versionamento (bump para `1.0.0` em commit dedicado) conforme o checklist de
  release.
- **R03:** avaliação dos padrões de composição da senha e reforço da orientação de uso no README/`--help`.
- **R02:** documentação de boas práticas de uso para reduzir a retenção do segredo no terminal.

## 4. Próximos passos

1. Executar o **checklist de release v1.0.0** (`docs/release.md`): version bump (R09), tag anotada
   `v1.0.0`, validação manual dos cenários e notas de versão.
2. Implementar mitigações de **segurança** priorizadas (R01, R02, R03).
3. Reforçar **qualidade e portabilidade** (R06: incluir `windows-latest` na matriz de CI; R07: testes de
   unicidade/propriedade; R08: centralizar validações).
4. Reduzir o **bus factor** (R11) com documentação de onboarding e definição de responsável reserva.
5. Reavaliar o quadro de riscos após o release e registrar o **backlog v1.1.0**.

## 5. Conclusões

O MVP está funcional e aderente ao escopo. A **revisão crítica dos riscos** trouxe uma boa notícia: o
item anteriormente sinalizado como **crítico/bloqueante** (pin de dependência de teste) era um **falso
alarme** — verificou-se que o `pytest 9.0.3` está instalado e os testes passam — e outro item foi
descartado por a documentação de release já estar **correta** quanto à branch (`master`). Com isso,
**não resta risco crítico ou bloqueante**, e o projeto está **apto a seguir para o release v1.0.0**.

Os riscos remanescentes de nível Alto (R02, R03, R09, R11) são gerenciáveis por mitigação planejada e não
comprometem prazo ou escopo do MVP. Recomenda-se **aprovar a continuidade para o release v1.0.0**,
condicionada apenas ao alinhamento de versionamento (R09) e à confirmação do CI verde. Novas atualizações
serão comunicadas a cada marco relevante.
