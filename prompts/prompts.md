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

#### Prompt 4 - README
```powershell
Contexto: MVP para geração de senhas seguras utilizando argparse.
Objetivo: Melhorar o README inicial, incluindo objetivo detalhado, stack, informações de como rodar o projeto e os testes e um roadmap de releases, baseado nos requisitos definidos.
Estilo: Incluir markdown simples, direto e profissional.
Resposta: Atualização do arquivo README.
```

#### Prompt 5 - Primeiro commit
```powershell
Contexto: Adicionei estrutura inicial de código e testes, README, .gitignore. Veja também outras alterações que não estão listadas.
Objetivo: criar mensagem adequada de commit.
Estilo: Utilize o padrão Conventional Commits para a mensagem.
Resposta: Faça o commit para mim, com apenas uma linha de mensagem no commit.
```