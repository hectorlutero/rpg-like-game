# ADR 0002: Hot-Loading and Asset Consistency

## Status
Accepted

## Context
O desenvolvimento ágil no "The Forge" exige que mudanças em assets (gráficos, metadados) sejam refletidas na Engine sem reinicialização. Em um projeto escalável, recarregar todo o estado global a cada mudança é ineficiente, mas recarregar apenas partes isoladas pode causar inconsistências visuais (ex: paletas de cores divergentes entre tilesets).

## Decision
Adotaremos uma estratégia híbrida de **Lazy Refresh with Hard-Reload Fallback**:
1. O `AssetManager` na Engine monitorará mudanças individuais em arquivos via mensagens WebSocket.
2. Apenas os recursos modificados terão seu cache invalidado e serão recarregados no próximo acesso (Lazy).
3. O Dashboard fornecerá um comando global de "Hard Reload" que limpa integralmente o cache da Engine, forçando o re-carregamento de todos os assets da cena atual para garantir a consistência visual absoluta quando necessário.

## Consequences
- **Prós:** Feedback quase instantâneo para edições atômicas; baixo consumo de recursos durante a iteração; escalabilidade para grandes volumes de assets.
- **Contras:** Risco temporário de inconsistência visual durante edições complexas de múltiplos arquivos; necessidade de lógica de invalidação de cache granular no `AssetManager`.
