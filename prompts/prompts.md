#  Especialização em Eng. de Software: Automação e Inovação com Inteligência Artifical Generativa

## Módulo 1: Introdução prática - Curso 4: Lab Introdutório - Construindo um mini-projeto com GenAI

### MVP de geração de senhas seguras para conclusão do Módulo 1

#### Prompt 1 - criação do ambiente
```powershell
Contexto: Estou iniciando um projeto de gerador de senhas seguras, em Python usando os frameworks Click/Argparse para integração com linha de comando.
Objetivo: Gere um arquivo .gitignore considerando Python, ambiente virtual, cache de testes e configurações locais do editor.
Estilo: O código deve ser escrito em Python 3.10.5, seguinto a proposta PEP8 e incluir docstrings.
Resposta: Crie ambiente incluindo o arquivo .gitignore do projeto.
```

#### Prompt 2 - Escopo MVP
```powershell
Contexto: MVP para geração de senhas seguras, utilizando click e argparse.
Objetivo: Gerar documento de escopo incluindo objetivo, requisitos funcionais, não funcionais e fora de escopo.
Estilo: Linguagem técnica, direta com markdown.
Tonalidade: A linguagem deve ser técnica, porém amigável.
Resposta: Gere o arquivo completo de docs/escopo-mvp.md.
```

#### Prompt 3 - Reduzir escopo para uso apenas do Argparse 
Vamos reduzir o escopo e utilizar só o argparse, ok?
Ajuste os arquivos para remover o uso do framework "click"


#### Prompt 4 - Ajustes nos requisitos funcionais
```powershell
Contexto: Melhorar os requisitos funcionais do projeto de geração de senhas seguras.
Objetivo: Atualizar documentação dos requisitos funcionais, permitidno que o usuário escolha os critérios para definição da senha: o uso de caracteres especiais, uso de letras maiúsculas/minúsculas, números, além do tamanho.
Estilo: Linguagem técnica, direta com markdown.
Tonalidade: A linguagem deve ser técnica, porém amigável.
Resposta: Atualização do arquivo docs/escopo-mvp.md.
```

#### Prompt 5 - README
```powershell
Contexto: MVP para geração de senhas seguras utilizando argparse.
Objetivo: Melhorar o README inicial, incluindo objetivo detalhado, stack, informações de como rodar o projeto e os testes e um roadmap de releases, baseado nos requisitos definidos.
Estilo: Incluir markdown simples, direto e profissional.
Resposta: Atualização do arquivo README.
```

#### Prompt 6 - Primeiro commit
```powershell
Contexto: Adicionei estrutura inicial de código e testes, README, .gitignore. Veja também outras alterações que não estão listadas.
Objetivo: criar mensagem adequada de commit.
Estilo: Utilize o padrão Conventional Commits para a mensagem.
Resposta: Faça o commit para mim, com apenas uma linha de mensagem no commit.
```

#### Prompt 7 - Adicionar parametros do argparse
```powershell
Contexto: Argumentos de entrada para a CLI.
Objetivo: Adicionar os argumentos que serão configurados pelo usuário: upper (para letras maiusculas), lower (para letras minusculas), number (para números), wildcards (para caracteres especiais) e length (para tamanho)
Estilo: Código simples e legível, comentários relevantes em docstrings
Resposta: Alteração do arquivo src/password_generator/cli_argparse.py.
```
#### Prompt 8 - Definir opções default
```powershell
Contexto: Argumentos de entrada para a CLI.
Objetivo: Definir que a configuração padrão (default) de entrada seja apenas minusculas, de tamanho 16. Outras opções serão desabilitadas por padrão.
Estilo: Código simples e legível, comentários relevantes em docstrings
Resposta: Alteração do arquivo src/password_generator/cli_argparse.py.
```

#### Prompt 9 - Adicionar parametros no gerador de senhas 
```powershell
Contexto: Criação do core de geração de senhas, a partir da entrada do usuário
Objetivo: Função core do projeto, responsável pela geração de senhas, considerando os inputs do usuário.
Estilo: Código simples e legível, comentários relevantes em docstrings
Resposta: Alteração do arquivo src/password_generator/generator.py.
```

#### Prompt 10 - Remover um nível de diretório
```powershell
vamos mover tudo que está em src/password_generator para src/. estou achando desnecessária o nível "password_genarator".
Faça os ajustes necessários para manter a coerencia dos códigos já criados.
```

#### Prompt 11 - Criação da função principal
```powershell
Contexto: Projeto MVP de gerador de senhas, em Ptyhon com argparse
Objetivo: Criar um arquivo src/main.py que chame as funções responsáveis pelo parse dos comandos e da função de geração de senha.
Estilo: Respeitar PEP8, código limpo simples e claro.
Resposta: Arquivo src/main.py coerente e executando sem erros.
```

#### Prompt 11 - Criação da função principal
```powershell
Me parece que existe duplicata de main(). Você pode revisar os arquivos src/main.py e src/cli_argparse.py, mantendo a main apenas no main.py
```

#### Prompt 12 - Commits
```powershell
Existem várias alterações no meu repositório.
Faça commits separados por  módulos, considerando o padrão Conventional commits para cada um.
Pode deixar de fora o diretório tests.
Lembre-se que houve mudança no path de alguns arquivos, utilize o git mv ao invés de remover os arquivos excluidos e os adicionar novamente.
```

#### Prompt 13 - Revisão crítica
```powershell
Revise os arquivos do projeto e responda:
1 - Onde faltam validações?
2 - Quais 5 testes que devo priorizar?
Resposta em checklist.
```

#### Prompt 14 - Ajustes de validação main.
```powershell
Contexto: Ajustes de validações em main.py.
Objetivo: Ajustar tratamento de erro ValueParse em src/main.py.
Estilo: Respeitar PEP8, código limpo simples e claro.
Resposta: Ajustes no arquivo src/main.py deixando coerente e executando sem erros.
```

#### Prompt 15 - Ajustes de validação do length
```powershell
Contexto: Ajustes de validações do argumento --length
Objetivo: Para o parametro length: Ajustar validação explicita em src/generator.py e validar limite máximo de caracteres para 32 em src/cli_argparse.py
Estilo: Respeitar PEP8, código limpo simples e claro.
Resposta: Ajustes nos arquivos src/generator.py e src/cli_argparse.py, deixando coerentes e executando sem erros.
```

#### Prompt 16 - Revisão de documentações
```powershell
Contexto: Revisão das documentações
Objetivo: Revisão dos documentos criados, para manter coerencia com o implmentado.
Estilo: Respeitar PEP8, código limpo simples e claro.
Resposta: Ajustar documentos README, pyproject.toml, .gitignore, docs/escopo-mvp.md
```

#### Prompt 17 - Commits
```powershell
Existem várias alterações no meu repositório.
Faça commits separados por  módulos, considerando o padrão Conventional commits para cada um.
Pode deixar de fora o diretório tests.
Lembre-se de enviar para o servidor (push).
```

#### Prompt 18 - Testes e validações
```powershell
Contexto: Testes e validações do projeto
Objetivo: Gerar suite de testes, utilizando Pytest considerando: 1 - regras mínimas (exemplo length < 8), 2 - regras máximas (exemplo length > 32), 3 - nenhuma classe ativa (no-upper, no-lower, no-wildcards, no-number), 4 - validação do tamanho coerente com o lenght passado, 5 - se as classes obrigátorias tem ao menos 1 caracter cada na senha gerada, 6 - testes de integração com a cli;
Estilo: Código limpo, simples e claro
Resposta: Ajustar arquivo de testes em tests/test_generator.py
```

#### Prompt 18 - Testes e validações
```powershell
Contexto: Testes e validações do projeto
Objetivo: Gerar suite de testes, utilizando Pytest considerando: 1 - regras mínimas (exemplo length < 8), 2 - regras máximas (exemplo length > 32), 3 - nenhuma classe ativa (no-upper, no-lower, no-wildcards, no-number), 4 - validação do tamanho coerente com o lenght passado, 5 - se as classes obrigátorias tem ao menos 1 caracter cada na senha gerada, 6 - testes de integração com a cli;
Estilo: Código limpo, simples e claro
Resposta: Ajustar arquivo de testes em tests/test_generator.py
```

#### Prompt 19 - Coerência do ambiente
```powershell
Faça os ajustes necessários no projeto e no ambiente para garantir que tanto o projeto quanto os testes possam ser executados com sucesso.
```

#### Prompt 20 - Verificação crítica
```powershell
Com base no código e testes atuais, gere um checklist:
1 - Os requisitos funcionais estão sendo atendidos?
2 - Tem algum GAP na corbertura dos testes?
3 - Sugira melhorias prioritárias para a próxima release.
Resposta em bullets curtos.
```

#### Prompt 21 - Revisão de documentações - v2
```powershell
Contexto: Revisão das documentações
Objetivo: Revisão dos documentos criados, para manter coerencia com o ambiente atual e o código implmentado.
Estilo: Respeitar PEP8, código limpo simples e claro.
Resposta: Ajustar documentos README, pyproject.toml, .gitignore, docs/escopo-mvp.md
```

#### Prompt 22 - Commits
```powershell
Existem várias alterações no meu repositório.
Faça commits separados por módulos, considerando o padrão Conventional commits para cada um.
```

#### Prompt 22 - Commits
```powershell
Posso acreditar que você fez o push dessa vez? se não fez, faça.
```

#### Prompt 23 - Ampliação da cobertura de testes e validações
```powershell
Contexto: Ampliação dos testes e validações do projeto
Objetivo: Aumentar a cobertura dos testes, implementando testes que validem: length com tipo inválido, regra de compatibilidade de length < que classes ativas, testes que validem o default e entrypoint intalado no ambiente de pacotes.
Estilo: Código limpo, simples e claro.
Resposta: Ajustar arquivo de testes em tests/test_generator.py
```

#### Prompt 24 - Makefile
```powershell
Contexto: Projeto de gerador de senhas seguras com argparse, com instalação de depencias, que possibilite executar o projeto e rodar os testes de validação.
Objetivo: Gerar Makefile com targets install, run e test.
Estilo: Simples e portável.
Resposta: Crie o arquivo completo de Makefile.
```

#### Prompt 25 - Revisão de README
```powershell
Analise meu README e faça:
1 - O que falta para ser reproduzível em máquina local
2 - seção com erros esperados
3 - Exemplos de execução
Ajuste o arquivo README.
```

#### Prompt 26 - Execução do Makefile
```powershell
Valide as possiveis execuções do makefile: make, make install, make run, make test
```

#### Prompt 27 - Execução do Makefile - ajustes
```powershell
Faça os ajustes necessários para executar o make.
Faça tabém as alterações no ambiente virtual e arquivos necessários para que ele esteja apto a rodar tudo (testes, make e entrypoint/execuções) sem erros.
```

#### Prompt 28 - Execução do projeto
```powershell
Eu queria ver o projeto rodando. Execute ele para mim, mostrando os comandos de entrada e as senhas seguras de saída.
```

#### Prompt 29 - Execução dos testes
```powershell
Agora também temos os testes, podemos executa-lo e verificar se está tudo correto. Faça essa avaliação para mim.
```

#### Prompt 30 - Checklist de release
```powershell
Contexto: Vou publicar a versão v1.0.0 no GitHub.
Objetivo: Gerar checklist final com itens técnicos e de documentos para release.
Estilo: Checkbox com markdown.
Resposta: Lista completa no arquivo docs/release.md
```

#### Prompt 31 - Commits
```powershell
Inclua o target de uninstall no arquivo Makefile. E valide que está funcionando com .\make uninstall.
```

#### Prompt 32 - Validação do ambiente virtual
```powershell
Valide que o ambiente virtual está atualizado. Caso não esteja, atualize-o.
```

#### Prompt 33 - Validação do pyproject.toml
```powershell
Valide que o arquivo pyproject.toml está atualizado. Caso não esteja, atualize-o.
```

#### Prompt 34 - Validação do README
```powershell
Valide que o arquivo README está atualizado. Caso não esteja, atualize-o.
Favor incluir informações relevantes do Makefile caso não exista. E atualizar as formas de executar o projeto.
```

#### Prompt 35 - Atualização do README
```powershell
Poxa vida, o README está bem confuso e com informações repetidas. Faça os ajustes necessários para que ele seja claro, direto e simpes de ler. tendo informações relevantes e não repetidas.
```

#### Prompt 36 - Atualização do README
```powershell
Contexto: Arquivo README com informações relevantes do projeto
Objetivo: atualizar o readme para que contenha apenas informações relevantes do projeto e não repetidas
Estilo: simples e direto
Resposta: arquivo readme atualizado, com informações detalhadas sobre o projeto, formas de uso - exemplo dos parametros, erros possíveis, como configurar o ambiente, instalar e testar. Além disso, mostrar o uso do makefile e seus targets disponíveis install//uninstall/run/test. Avalie possíveis informações faltaantes e adicione de forma coerente.
```

#### Prompt 37 - CI simples para teste
```powershell
Contexto: CI para execução dos testes no commit.
Objetivo: Criar um CI (GitHub Actions) simples que rode os testes a cada PUSH/PR.
Estilo: Simples e legível.
Resposta: Arquivo de ci válido.
```

#### Prompt 38 - Commits
```powershell
Faça os ajustes necessários no repositorio para garantir que o arquivo ci.yml seja executado com commit/pr.
```

#### Prompt 39 - Commits
```powershell
Existem várias modifiçãoes. Faça commit por módulo, utilizando conventional commits.
Lembre-se de executar o push.
```

---

## Curso 10: Engenharia de Requisitos com IA Generativa

#### Prompt 40 - Análise do documento de elicitação
```powershell
Contexto: O arquivo docs/escopo-mvp.md é o documento produzido na etapa de elicitação de requisitos.
Objetivo: Analisar criticamente esse documento e identificar requisitos funcionais, regras de negócio,
requisitos não funcionais, lacunas e ambiguidades.
Importante: não confie apenas no texto. Compare o documento com o código real em src/ e tests/, e
execute a CLI para verificar o comportamento efetivo. Aponte onde documento e produto divergem.
Estilo: Linguagem técnica, direta, com markdown e tabelas.
Resposta: Arquivo requisitos/analise-elicitacao.md.
```

#### Prompt 41 - Seleção e elaboração dos artefatos de especificação
```powershell
Contexto: Análise da elicitação concluída em requisitos/analise-elicitacao.md.
Objetivo: Selecionar os artefatos de especificação mais adequados a este projeto e elaborá-los.
Justifique a escolha a partir dos defeitos encontrados na análise, e justifique também os artefatos
que você decidiu NÃO produzir.
Estilo: Critérios de aceite em Gherkin; casos de uso com fluxos alternativos e de exceção.
Resposta: requisitos/historias-usuario.md, requisitos/casos-de-uso.md e requisitos/rastreabilidade.md.
```

#### Prompt 42 - Protótipo de interface para CLI
```powershell
Contexto: O projeto é uma CLI, não tem interface gráfica.
Objetivo: Produzir o equivalente a um protótipo para uma aplicação de terminal.
Importante: capture as saídas REAIS executando o projeto, não escreva exemplos fictícios.
Se o comportamento observado divergir do documentado, sinalize.
Resposta: Arquivo requisitos/prototipo-cli.md.
```

> **Nota:** foi o Prompt 42 que expôs o achado mais relevante desta etapa. Ao tentar **reproduzir** o
> fluxo de exceção do RF10 para o protótipo, constatou-se que ele é inatingível por qualquer entrada
> (código morto) e que o teste que o cobria passava pelo motivo errado. A instrução de "capturar saída
> real em vez de escrever exemplo" foi o que transformou uma revisão documental em verificação.

#### Prompt 43 - Commits
```powershell
Faça commit por documento, utilizando conventional commits.
```




