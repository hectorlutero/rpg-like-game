# ADR 0003: Thread-Safe Inter-Engine Communication

## Status
Accepted

## Context
A comunicação bidirecional entre o Dashboard (Node.js/Electron) e a Engine (Python/Pygame) via WebSockets ocorre de forma assíncrona. Se a Engine processar mudanças de estado ou assets no exato momento em que são recebidas, há um alto risco de "Race Conditions" (ex: um item ser deletado enquanto o sistema de combate calcula seu efeito), resultando em crashes ou comportamentos imprevisíveis.

## Decision
Adotaremos o padrão de **Frame-Synchronized Message Processing**:
1. A Engine Python manterá uma thread secundária dedicada exclusivamente a escutar o socket.
2. Mensagens recebidas serão colocadas em uma `thread-safe Queue`.
3. O Loop Principal da Engine (Main Loop), no início de cada frame (antes de `update` e `draw`), consumirá todas as mensagens pendentes na fila e aplicará as mudanças.

## Consequences
- **Prós:** Integridade total dos dados durante o frame; eliminação de conflitos de concorrência; comportamento determinístico da Engine.
- **Contras:** Introduz uma latência mínima (no máximo 1 frame, ~16ms a 60 FPS) entre o envio da mensagem e seu processamento; requer gestão cuidadosa da thread secundária para evitar processos zumbis.
