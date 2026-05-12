# PRD: Módulo de Interação e Proximidade Unificado

## Problem Statement
Atualmente, a lógica de interação (diálogos e combate) está fragmentada dentro das cenas e depende de cálculos de distância absoluta (raio circular) espalhados pelo código. Isso dificulta a adição de novos tipos de objetos interagíveis (baús, portas, alavancas) e permite interações não intuitivas, como falar com um NPC que está de costas para o herói.

## Solution
Implementar um sistema de interação unificado baseado em Tiles e Direção. O mundo terá um registro central de "Interagíveis" e o herói poderá interagir com qualquer objeto que esteja exatamente no tile à sua frente.

## User Stories
1. Como herói, quero poder olhar para o Norte, Sul, Leste ou Oeste, para que minha intenção de interação seja clara.
2. Como herói, quero apertar um botão de interação (Espaço/E) e ativar o objeto que está na minha frente, para que o jogo responda às minhas ações.
3. Como desenvolvedor, quero adicionar um novo objeto ao mapa (ex: um baú) apenas registrando-o em uma coordenada, sem precisar mexer na lógica de colisão manual do herói.
4. Como jogador, quero que o combate ou o diálogo comecem apenas se eu estiver de frente para o inimigo ou NPC, para evitar interações acidentais por proximidade.
5. Como herói, quero que diferentes objetos tenham comportamentos diferentes (um abre diálogo, outro inicia luta), para que o mundo pareça rico e variado.

## Implementation Decisions
- **Unified Interactable Interface**: Criação de uma classe base ou interface `Interactable` com o método `on_interact(context)`.
- **Character Orientation**: Adição do atributo `facing_direction` (N, S, E, W) à classe `Character`.
- **Tile-based Discovery**: O módulo `World` passará a gerenciar um dicionário `interactables = {(x, y): object}`.
- **Directional Mapping**: A lógica de busca converterá a posição `(x, y)` do herói + `facing_direction` na coordenada alvo do tile.
- **Autonomous Resolution**: O `SceneManager` ou a `ExplorationScene` apenas invocará `target.on_interact(context)`, delegando a execução para o objeto.
- **Refactoring**: NPCs e Inimigos no mapa serão migrados para este novo sistema.

## Testing Decisions
- **Comportamento Externo**: Testar se, ao posicionar o herói de frente para um objeto e chamar a função de interação, o método `on_interact` do objeto é disparado.
- **Isolamento de Direção**: Testar se a interação falha se o herói estiver perto do objeto, mas olhando para a direção oposta.
- **Módulos Testados**: `Character` (pela direção), `World` (pela descoberta) e uma classe de teste `MockInteractable`.
- **Prior Art**: Seguir o padrão de testes unitários já estabelecidos em `tests/test_movement.py` e `tests/test_dialogue.py`.

## Out of Scope
- Animações de rotação de sprites (o foco é a lógica direcional).
- Interações complexas que ocupam múltiplos tiles (por enquanto, cada objeto ocupa 1 tile).
- Interações automáticas ao pisar (armadilhas de chão) — este PRD foca apenas em interação ativa via botão.

## Further Notes
Este sistema é fundamental para permitir a expansão futura para baús de tesouro e transições de mapa (portas).
