# Status da Implementação - 12 de Maio de 2026

## Fluxo de Economia e Exploração (Issues #24 e #23)

### 1. Sistema de Loja (ShopScene)
- **Funcionalidade**: Implementada cena de transação comercial completa.
- **Modos**: Suporte para Compra (BUY) e Venda (SELL), alternáveis via tecla `TAB`.
- **Lógica de Preços**: Venda configurada para 50% do valor de compra.
- **Interface**: Lista dinâmica de itens (Equipamentos e Consumíveis) com feedback visual de ouro e mensagens de sucesso/erro.

### 2. Geração de Loot de Combate
- **LootTable**: Implementada lógica no `CombatManager` para suporte a tabelas de espólios.
- **Recompensas**: Inimigos agora podem derrubar itens (além de Ouro e XP) com probabilidades customizáveis.
- **Integração**: O `CombatScene` processa e exibe os itens ganhos no log de batalha ao final da vitória.

### 3. Sistema de Baús de Tesouro (Chest)
- **Multi-Item**: Suporte para múltiplos itens e ouro em um único baú.
- **Persistência Automática**: Baús verificam o `GameContext` (IDs de baús abertos) para sincronizar seu estado visual e lógico automaticamente após o carregamento do jogo.
- **Feedback**: Mensagens customizáveis e alteração visual no mapa (baú aberto/fechado).

### 4. Automação de Testes UI (E2E)
- **Técnica**: Implementada injeção de eventos no loop do Pygame para testes de interface.
- **Modo Headless**: Testes rodam sem necessidade de interface gráfica física (driver `dummy`), garantindo rapidez e confiabilidade.
- **Cobertura**: Fluxos de Combate, Inventário e Loja 100% automatizados.

## Sistemas de Equipamento e Proficiência (Issue #4)
- **Proficiência**: Implementada lógica de bônus baseados em `tags` de equipamento. Cada classe tem multiplicadores específicos para tipos de arma/armadura.
- **Bônus Dinâmicos**: Suporte para bônus fixos (Flat) e percentuais (%) em equipamentos, calculados em tempo real.
- **Requisitos**: Equipamentos agora verificam nível, classe e atributos mínimos antes de permitir o uso.

## Melhorias de Arquitetura (Issues #26, #27, #28, #29)
- **Combat Logic Centralization (#26)**: Toda a lógica de batalha, IA inimiga e recompensas foi movida para o `CombatManager`, tornando a `CombatScene` uma camada de visualização fina e testável.
- **Polymorphic Rendering (#27)**: A renderização de objetos no mapa (Interactables) foi movida para as próprias classes (`Chest`, `NPC`, `Shopkeeper`), limpando o loop de desenho da `ExplorationScene`.
- **Character Refactor (#28)**: Extração da lógica de cálculo de atributos para o `StatsCalculator`, reduzindo o acoplamento da classe `Character`.
- **Simplificação do ATB (#29)**: Remoção do `ATBEngine` redundante, consolidando o controle de tempo diretamente no `CombatManager`.

## Ferramentas de Teste
- **Watch Mode**: Adicionada a flag `--watch` à suíte `pytest`. Agora é possível assistir à automação dos robôs E2E rodando visualmente em tempo real.
