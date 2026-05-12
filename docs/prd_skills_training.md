# PRD: Sistema Avançado de Skills, Magias e Treinamento

## Problem Statement
O sistema de combate atual é limitado a ataques físicos básicos e o progresso dos atributos é puramente automático via Level Up. Não há uma forma de o jogador influenciar o crescimento do herói através de atividades no mundo, e o Mana existente não possui utilidade prática.

## Solution
Implementar um ecossistema de aprendizado e treino. Atributos poderão ser aumentados através de atividades (Leitura para Inteligência, Exercício para Força/Vitalidade), consumindo um recurso diário de "Energia". Magias serão aprendidas através de Livros que servem como "guias de aprendizado" escalonados pela Inteligência.

## User Stories
1. Como jogador, quero ler um livro para aumentar minha Inteligência se meu nível atual for menor que o requisito da magia contida nele.
2. Como jogador, quero aprender uma magia automaticamente ao atingir a Inteligência e o Nível necessários através do estudo.
3. Como jogador, quero usar objetos no mapa (como bonecos de treino) para aumentar minha Força ou Vitalidade.
4. Como jogador, quero ter um limite de 3 atividades por dia (ciclo de sono/save), para que eu precise planejar meu desenvolvimento.
5. Como herói, quero usar magias no combate que consomem Mana e causam dano baseado no meu atributo de Inteligência e no elemento da magia (Fogo, Gelo, etc).
6. Como herói, quero que meus ataques mágicos sejam mais eficazes contra inimigos com fraquezas elementais específicas.

## Implementation Decisions
- **Energy System**: Adição do atributo `energy` ao `GameContext` (ou `Character`), resetado ao usar um Save Point (Dormir).
- **Study Logic**: 
    - Se `char.int < book.threshold`: ganha +1 de INT e consome 1 Energia.
    - Se `char.int >= book.threshold` e `char.level >= book.min_level`: aprende a `Skill` e consome 1 Energia.
    - Se a magia já foi aprendida: o livro não concede mais bônus.
- **Training Interactables**: Criação de classes `TrainingObject` que herdam de `Interactable` para Força e Agilidade.
- **Elemental System**: Adição de `element_type` (Fire, Ice, Lightning, Earth) à classe `Skill` e `DamageCalculator`.
- **UI Update**: Exibição da energia atual na HUD de exploração.

## Testing Decisions
- **Unit Tests**: Validar o ganho de +1 INT por leitura e o bloqueio de ganho acima do threshold.
- **Integration Tests**: Verificar se a Energia é decrementada corretamente após cada atividade.
- **Combat Tests**: Validar o multiplicador de dano elemental (ex: Fogo contra inimigo de Gelo causa 1.5x dano).

## Out of Scope
- Animações complexas de partículas para as magias (foco na lógica e números).
- Árvores de habilidades (talent trees) complexas.
- Sistema de fadiga ou fome.

## Further Notes
Este sistema torna a exploração muito mais recompensadora, pois encontrar uma biblioteca ou um ginásio torna-se um evento estratégico importante.
