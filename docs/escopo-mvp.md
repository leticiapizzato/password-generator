# Escopo do MVP - Gerador de Senhas Seguras

## 1. Objetivo

Definir e implementar um **MVP (Minimum Viable Product)** de linha de comando para geração de senhas seguras em Python, com interface baseada em `argparse`.

O MVP deve permitir ao usuário gerar senhas aleatórias fortes, com parâmetros de composição configuráveis, validações explícitas de entrada e comportamento previsível para uso local em terminal.

## 2. Requisitos Funcionais

### RF01 - Geração de senha segura
O sistema deve gerar senhas aleatórias utilizando fonte criptograficamente segura (`secrets`), evitando geradores pseudoaleatórios inadequados para segurança.

### RF02 - Definição de tamanho da senha
O usuário deve poder informar o tamanho da senha via argumento de linha de comando (`--length`).

### RF03 - Valor padrão
Quando o tamanho não for informado, o sistema deve gerar senha com tamanho padrão de **16 caracteres**.

### RF04 - Faixa válida de tamanho
O sistema deve validar o tamanho informado e aceitar apenas valores entre **8** e **32** caracteres, retornando erro amigável para valores fora dessa faixa.

### RF05 - Seleção de uso de letras minúsculas
O usuário deve poder habilitar ou desabilitar o uso de letras minúsculas na composição da senha por meio de opção de linha de comando.

### RF06 - Seleção de uso de letras maiúsculas
O usuário deve poder habilitar ou desabilitar o uso de letras maiúsculas na composição da senha por meio de opção de linha de comando.

### RF07 - Seleção de uso de números
O usuário deve poder habilitar ou desabilitar o uso de dígitos numéricos na composição da senha por meio de opção de linha de comando.

### RF08 - Seleção de uso de caracteres especiais
O usuário deve poder habilitar ou desabilitar o uso de caracteres especiais na composição da senha por meio de opção de linha de comando.

### RF09 - Validação de critérios mínimos de composição
O sistema deve validar que ao menos uma classe de caractere esteja habilitada (minúsculas, maiúsculas, números ou especiais), retornando erro claro caso nenhuma classe seja selecionada.

### RF10 - Compatibilidade entre tamanho e critérios
O sistema deve validar a compatibilidade entre o tamanho solicitado e os critérios ativos, retornando erro amigável em caso de inviabilidade.

### RF11 - Interface CLI com argparse
O projeto deve expor uma forma de execução via módulo/entrypoint com `argparse`, utilizando `src/main.py` como ponto de entrada.

### RF12 - Saída simples no terminal
A senha gerada deve ser exibida no `stdout`, em uma única linha, sem informações sensíveis adicionais.

### RF13 - Estrutura mínima de testes
O projeto deve incluir testes automatizados cobrindo geração, tamanho e critérios de composição selecionáveis.

## 3. Requisitos Não Funcionais

### RNF01 - Linguagem e versão
O projeto deve ser desenvolvido em **Python 3.10.5**.

### RNF02 - Qualidade de código
O código deve seguir boas práticas de legibilidade e manutenção, incluindo:

- aderência à PEP 8
- uso de `docstrings` em módulos e funções principais
- organização por responsabilidade (core, parser e ponto de entrada)

### RNF03 - Usabilidade em terminal
A experiência de uso CLI deve ser direta, com mensagens de ajuda (`--help`) e erros compreensíveis.

### RNF04 - Portabilidade
O MVP deve executar em ambiente local padrão de desenvolvimento Python, sem dependências complexas de infraestrutura externa.

### RNF05 - Reprodutibilidade do ambiente
O projeto deve possuir configuração mínima de empacotamento/dependências e arquivo `.gitignore` adequado para Python, ambiente virtual e caches de teste.

### RNF06 - Segurança básica
A solução deve evitar práticas inseguras conhecidas para geração de senha, priorizando APIs da biblioteca padrão voltadas à segurança.

## 4. Fora de Escopo (MVP)

Os itens abaixo **não** fazem parte da primeira entrega:

- interface gráfica (desktop, web ou mobile)
- persistência de senhas em arquivo, banco de dados ou cofre
- criptografia/armazenamento de histórico de senhas
- integração com serviços externos (APIs, gerenciadores de senha, cloud)
- geração de passphrases com dicionário
- internacionalização (i18n)
- pipeline completo de CI/CD
- empacotamento distribuível em múltiplos formatos (exe, installer, container)

## 5. Critérios de Aceite do MVP

O MVP será considerado concluído quando:

1. A geração de senha funcionar via `argparse`.
2. O parâmetro `--length` for aceito na faixa de 8 a 32.
3. O usuário conseguir definir critérios de composição para minúsculas, maiúsculas, números e caracteres especiais.
4. O valor padrão de 16 caracteres for aplicado quando não houver parâmetro.
5. Configurações sem nenhuma classe de caractere ativa gerarem erro de validação claro.
6. Houver ao menos um conjunto inicial de testes automatizados passando localmente.
7. A documentação básica do projeto estiver disponível (`README` + este escopo).

## 6. Entregáveis

- Código-fonte do MVP em Python 3.10.5
- CLI funcional com `argparse` (entrypoint em `src/main.py`)
- Testes iniciais
- Documento de escopo do MVP (`docs/escopo-mvp.md`)
