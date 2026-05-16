# ADR 0004: Managed Python Virtual Environment

## Status
Accepted

## Context
A Engine Python depende de bibliotecas específicas (Pygame, Watchdog, Websockets) e de versões compatíveis do interpretador Python. Depender do ambiente global do sistema é arriscado e inconsistente entre diferentes máquinas. O Dashboard precisa de uma forma confiável de executar a Engine com todas as dependências garantidas.

## Decision
O Dashboard implementará um sistema de **Managed Venv**:
1. O Dashboard verificará a existência de um venv dedicado (ex: `.forge_venv`) na raiz do projeto.
2. Se o venv não existir ou estiver desatualizado, o Dashboard o criará e executará automaticamente `pip install -r requirements.txt`.
3. O Dashboard armazenará um hash do arquivo `requirements.txt`. Se o arquivo mudar, o Dashboard solicitará ou executará automaticamente uma atualização das dependências antes de lançar a Engine.
4. O caminho absoluto deste venv será a referência única para todas as execuções de sub-processos da Engine.

## Consequences
- **Prós:** Ambiente de execução determinístico e isolado; atualizações de dependências automatizadas; facilita o onboarding de novos desenvolvedores.
- **Contras:** Aumento do uso de disco (cada projeto tem seu venv); overhead inicial de criação/instalação; necessidade de o Dashboard lidar com diferentes versões de Python instaladas no sistema para a criação do venv.
