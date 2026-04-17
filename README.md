# Analisador Léxico

Um analisador léxico construído em Python baseado na teoria de Autômatos Finitos. Projeto desenvolvido para a disciplina de Construção de Compiladores da Universidade Federal da Fronteira Sul (UFFS).

## Objetivo
Este projeto recebe uma especificação de linguagem formal (palavras reservadas e Gramáticas Regulares), constrói um Autômato Finito Não-Determinístico (AFND), aplica a determinização para um Autômato Finito Determinístico (AFD) e utiliza essa estrutura matemática para reconhecer e classificar tokens em um arquivo de texto.

Como saída, o sistema gera:
1. **Tabela de Símbolos (TS):** Relatório tabular contendo o token lido, a linha de ocorrência, o status de reconhecimento (ACEITO ou ERRO) e a sequência de estados percorrida.
2. **Fita de Saída:** Uma representação linear dos estados de aceitação/erro em que o autômato parou após processar cada token.

## Estrutura dos Arquivos
* **`tokens.txt`**: Arquivo de configuração. Aqui você define as palavras reservadas estáticas e as produções da Gramática Regular (GR).
* **`afd.py`**: O motor matemático. Lê a configuração, mapeia as transições do AFND dinamicamente e aplica o algoritmo de construção de subconjuntos para gerar o AFD final na memória.
* **`al.py`**: O script principal do analisador léxico. Carrega o AFD e realiza a leitura sequencial dos caracteres do arquivo de entrada, alimentando a Tabela de Símbolos e a Fita.
* **`entrada.txt`**: O arquivo de texto com o código/palavras que você deseja testar no analisador.
