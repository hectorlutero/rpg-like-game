# PRD: Sistema de Equipamento, Inventário e Economia

## Problem Statement
O herói atualmente não possui forma de aumentar seu poder através de itens ou tesouros. Não há um sistema de inventário para gerenciar consumíveis ou equipamentos, e a economia do jogo é inexistente, impedindo a criação de mecânicas de recompensa por vitória ou exploração.

## Solution
Implementar um sistema completo de Equipamentos (Arma, Escudo, Armadura, Acessório) com bônus híbridos, um Inventário categorizado e um Sistema Monetário (Ouro). Itens serão adquiridos via Baús, Drops de Combate e Lojas.

## User Stories
1. [X] Como herói, quero equipar uma arma para aumentar meu dano físico e força.
2. [X] Como herói, quero equipar uma armadura para reduzir o dano recebido.
3. [X] Como jogador, quero abrir baús no mapa para encontrar itens raros ou ouro.
4. [X] Como jogador, quero que inimigos deixem cair espólios após a batalha.
5. [X] Como herói, quero acumular ouro para comprar equipamentos melhores em uma loja.
6. [X] Como jogador, quero visualizar meu inventário organizado por categorias (Equipamentos e Consumíveis).
7. [X] Como herói, quero usar poções do meu inventário durante a exploração ou combate para recuperar HP.
8. [X] Como desenvolvedor, quero que itens tenham requisitos de classe ou atributos mínimos para serem equipados, com bônus de proficiência.

## Implementation Decisions
- **Inventory Module**: Criação da classe `Inventory` que gerencia listas de `Item` e `Equipment`.
- **Item Data**: Estrutura base para itens com preço de compra/venda, raridade e efeitos.
- **Equipment Logic**: 4 slots (Weapon, Shield, Armor, Accessory). Bônus são aplicados dinamicamente no `Character.get_attribute`.
- **Monetary System**: Adição do atributo `gold` ao `Character`.
- **Acquisition Systems**:
    - `Chest`: Um `Interactable` que adiciona itens ao inventário e se auto-destrói/muda de estado.
    - `LootTable`: Lógica no `CombatManager` para gerar prêmios ao final da batalha.
    - `ShopScene`: Uma nova cena de menu para transações comerciais.
- **Restrictions**: Itens terão atributos `req_class` e `req_stats` verificados no momento de equipar.

## Testing Decisions
- **Unit Tests**: Validar se equipar um item altera corretamente os atributos finais do herói.
- **Unit Tests**: Garantir que itens não podem ser equipados se os requisitos não forem atendidos.
- **Integration Tests**: Simular compra em loja verificando subtração de ouro e adição de item.
- **Persistence Tests**: Garantir que o ouro e o inventário são salvos e carregados do JSON.

## Out of Scope
- Visual de troca de equipamento no sprite do personagem (permanecerá o quadrado azul com indicador).
- Durabilidade de itens (quebra de arma).
- Sistema de crafting (ferreiro).

## Further Notes
Este sistema completa a tríade de progressão: Nível (Automático), Treino (Manual) e Equipamento (Tesouros/Economia).
