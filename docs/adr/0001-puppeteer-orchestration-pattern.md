# ADR 0001: Puppeteer Orchestration Pattern

## Status
Accepted

## Context
O projeto "The Forge" requer uma integração profunda entre o Dashboard (Electron) e a Engine (Pygame). O desenvolvedor precisa de um ciclo de feedback rápido ao editar mapas, itens e áudio. Lançar manualmente ambos os processos e monitorar logs em terminais separados é ineficiente e propenso a erros.

## Decision
Adotaremos o **Puppeteer Pattern** para orquestração do ciclo de vida. O Dashboard (Electron) será o processo pai responsável por:
1. Iniciar o servidor de comunicação (WebSocket).
2. Lançar a Engine (Python) como um subprocesso.
3. Passar argumentos de inicialização (ex: `--forge-mode`, `--port`).
4. Capturar `stdout` e `stderr` da Engine para exibição em um console integrado.
5. Gerenciar o encerramento gracioso de ambos os processos.

## Consequences
- **Prós:** Experiência de uso unificada; depuração facilitada através de um console centralizado; garantia de que a Engine sempre roda com as flags corretas.
- **Contras:** O Dashboard se torna um ponto único de falha; complexidade adicional na gestão de processos e tratamento de sinais (SIGTERM/SIGINT) entre Node.js e Python.
