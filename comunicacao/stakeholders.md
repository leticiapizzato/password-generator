# Comunicação aos Stakeholders — Password Generator

| Campo | Valor |
|-------|-------|
| **Projeto** | Password Generator (MVP — CLI de geração de senhas seguras) |
| **Contexto acadêmico** | UFG — C4 |
| **Documento** | Atualização de projeto, requisitos e riscos |
| **Data** | 2026-07-16 (atualizado em 2026-08-04) |
| **Versão do documento** | 2.0 (após a etapa de engenharia de requisitos) |
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

Após a etapa de engenharia de requisitos, **4 dos 9 riscos foram resolvidos ou mitigados** e 1 está em
andamento. **Não há risco crítico ou bloqueante.**

| ID | Risco | Situação |
|----|-------|----------|
| R01 | Regressão na fonte de aleatoriedade | ✅ Mitigado — dois testes garantem o uso de `secrets` |
| R03 | Configuração padrão de baixa entropia | ✅ **Eliminado** — padrão passou a usar as quatro classes |
| R07 | Cobertura da aleatoriedade | ✅ Mitigado — teste de 1000 senhas distintas |
| R08 | Inconsistência entre validações CLI/core | ✅ Resolvido — validação centralizada no core |
| R09 | Versionamento desalinhado | 🔄 Em andamento — versão elevada para `1.0.0`; resta a tag |
| R02 | Exposição da senha no terminal | ⚠️ Em aberto — risco do ambiente, não da aplicação |
| R04 | Dependência de versão do Python | ⚠️ Em aberto |
| R06 | Divergência entre dev (Windows) e CI (Linux) | ⚠️ Em aberto |
| R11 | Baixo fator de continuidade (bus factor) | ⚠️ Em aberto |

Os quatro riscos remanescentes **não dizem respeito ao produto em si**: tratam do ambiente de uso, do
ambiente de execução e da estrutura da equipe. Detalhamento em `riscos/identificacao.md`, seção 6.

## 3. Trabalho realizado na etapa

A especificação dos requisitos (`requisitos/`) revelou que **metade das regras que governam o produto não
estava documentada**, e que um requisito era inválido. As correções decorrentes:

- **Composição padrão (R03).** O comando sem argumentos gerava senha apenas com minúsculas (≈75 bits),
  contradizendo o objetivo de "senhas fortes". Passou a ativar as quatro classes (≈105 bits). É uma
  **mudança de comportamento** e será destacada nas notas da v1.0.0.
- **Requisito RF10 removido.** A especificação demonstrou que a validação de "tamanho menor que o número
  de classes" era **inalcançável por qualquer entrada** e que o teste que a cobria passava capturando
  outra exceção. Requisito, regra e código foram removidos.
- **Validação centralizada (R08).** A faixa 8..32 vivia duplicada na CLI e no core, com mensagens
  diferentes. Passou a ter fonte única.
- **Cobertura de testes.** De 11 para **24 testes**, cobrindo agora o uso de CSPRNG, a unicidade das
  senhas, o contrato de saída e a ajuda de uso.

## 4. Próximos passos

1. Concluir o **checklist de release v1.0.0** (`docs/release.md`): tag anotada `v1.0.0`, validação manual
   e notas de versão **destacando a mudança de comportamento**.
2. Reforçar **portabilidade** (R06: incluir `windows-latest` na matriz de CI).
3. Reduzir o **bus factor** (R11) com documentação de onboarding e responsável reserva.
4. Avaliar as decisões de requisitos ainda pendentes (`requisitos/analise-elicitacao.md`, seção 9.2),
   entre elas o limiar mínimo de entropia.
5. Registrar o **backlog v1.1.0**: geração em lote, exclusão de caracteres ambíguos e exibição de
   entropia estimada.

## 5. Conclusões

O MVP está funcional e, agora, **aderente ao que promete**. A etapa de engenharia de requisitos trouxe um
resultado que a gestão de riscos sozinha não havia alcançado: ao exigir que cada fluxo especificado fosse
**reproduzido na prática**, expôs um requisito que parecia implementado e testado, mas não fazia nada — e
um padrão de uso que contrariava o objetivo central do produto.

Vale registrar o contraste: o quadro de riscos apontava R08 apenas como "validação duplicada", enquanto a
especificação encontrou o defeito concreto por trás dele. As duas abordagens se complementaram.

Com R03 eliminado e R01, R07 e R08 endereçados, **recomenda-se aprovar a continuidade para o release
v1.0.0**, condicionada apenas à criação da tag e à confirmação do CI verde. Novas atualizações serão
comunicadas a cada marco relevante.
