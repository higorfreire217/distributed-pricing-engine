# Estrutura do Projeto

Este repositório está organizado em diretórios, cada um correspondente a um desafio específico. Cada diretório de desafio possui seu próprio arquivo `README.md`, onde você encontrará uma descrição detalhada das soluções implementadas.

## Desafios

- **Desafios 1 ao 3**:  
    Nestes diretórios, além da descrição das soluções, estão disponíveis diagramas que ilustram a arquitetura proposta.  
    Você pode visualizar os diagramas de duas formas:
    1. Abrindo diretamente o arquivo `Diagram.png` presente no diretório do desafio.
    2. Executando o comando abaixo no terminal (Linux ou Mac OS), dentro do diretório de cada desafio:
     ```bash
     make run-structurizr
     # ou caso esteja usando windows, execute o comando docker diretamente
    docker run --rm -p 8080:8080 -v %cd%:/usr/local/structurizr structurizr/lite
     ```

     Este comando irá gerar e abrir o diagrama utilizando o Structurizr com Docker (importante que o mesmo esteja instalado na sua maquina).

Consulte os arquivos `README.md` de cada diretório para informações detalhadas sobre cada solução.