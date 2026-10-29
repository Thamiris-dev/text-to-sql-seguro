
# Assistente de Dados com Text-to-SQL Seguro

## 1. Problema

Consultar bancos de dados exige conhecimento de SQL, o que pode
dificultar o acesso a informações por pessoas sem experiência técnica.

Este projeto propõe um assistente que recebe perguntas em linguagem
natural, gera consultas SQL com auxílio de inteligência artificial,
valida as consultas e apresenta os resultados de forma compreensível.

## 2. Objetivo

Desenvolver e avaliar um protótipo de Text-to-SQL que permita consultar
dados de forma acessível, com validação das consultas antes da execução.

## 3. Arquitetura proposta

O fluxo planejado é:

1. O usuário envia uma pergunta em linguagem natural.
2. O modelo de IA propõe uma consulta SQL.
3. O validador analisa a consulta e aplica regras de segurança.
4. Consultas aprovadas são executadas no banco de dados.
5. Os resultados são apresentados na interface.

A arquitetura será detalhada e atualizada conforme a implementação.

## 4. Tecnologias previstas

- Python
- Streamlit
- DuckDB
- SQLGlot
- Ollama para execução local do modelo de IA
- Pytest para testes automatizados
- Docker Compose
- GitHub Actions para integração contínua

## 5. Como executar

Instruções de instalação e execução serão adicionadas após a
configuração do ambiente e a implementação do protótipo.

## 6. Testes e avaliação experimental

A avaliação deverá incluir perguntas com consultas de referência,
métricas de acerto e testes de segurança para verificar se consultas
não permitidas são bloqueadas.

O protocolo, os dados e os resultados serão documentados em `eval/`.

## 7. Contribuições

Projeto desenvolvido individualmente por Thamiris de Oliveira e Silva.

## 8. Status

Fase inicial: preparação do ambiente, estruturação do repositório
e documentação do projeto.
