import subprocess
import re

def create_issue(title, body, label="ready-for-agent"):
    result = subprocess.run(
        ["gh", "issue", "create", "--title", title, "--body", body, "--label", label],
        capture_output=True, text=True, check=True
    )
    # the output is a URL like https://github.com/hectorlutero/rpg-like-game/issues/64
    url = result.stdout.strip()
    issue_number = url.split("/")[-1]
    return issue_number

# Issues definitions
issues = [
    {
        "title": "A* Pathfinding Deep Module",
        "body": """## Parent
#63

## What to build
Implementar a classe `PathfindingEngine` isolada e puramente matemática (sem dependência do loop visual do Pygame). A engine deve receber um estado de grid (ex: matriz 2D), coordenadas de origem e destino, e retornar uma lista de passos (tuplas) para alcançar o objetivo. Deve contornar obstáculos e falhar graciosamente se o destino for inalcançável.

## Acceptance criteria
- [ ] Implementar algoritmo A* (ou similar) em um módulo profundo.
- [ ] Ignorar tiles bloqueados/impassáveis.
- [ ] Retornar o caminho mais curto.
- [ ] Unit tests garantindo evasão de obstáculos em U.
- [ ] Unit tests garantindo retorno vazio/graceful failure para áreas inacessíveis.

## Blocked by
None - can start immediately"""
    },
    {
        "title": "Integração de Reivindicação de Tile Imediata (Immediate Tile Claiming)",
        "body": """## Parent
#63

## What to build
Atualizar a física do Grid no sistema de movimentação. Quando uma entidade decide mover-se de `(x, y)` para `(x+1, y)`, a chave dessa entidade no dicionário `world.interactables` deve ser atualizada instantaneamente para `(x+1, y)`, mesmo que a animação visual (`visual_offset`) ainda esteja ocorrendo. Movimentos para tiles já ocupados no dicionário devem ser abortados.

## Acceptance criteria
- [ ] Movimento de entidades atualiza chave no dicionário imediatamente.
- [ ] Movimento rejeitado (colisão) se o tile destino já existir no dicionário.
- [ ] Testes de integração (unit/mock) provando que duas entidades indo pro mesmo tile no mesmo frame não causam sobreposição de chaves ou fusão de entidades.

## Blocked by
None - can start immediately"""
    },
    {
        "title": "IA Controller e Random Wander Behavior",
        "body": """## Parent
#63

## What to build
Criar o padrão Strategy `AIController` para entidades do mapa, contendo inicialmente `StaticBehavior` e `RandomWanderBehavior`. Integrar uma fase `update_ai(dt)` no `WorldOrchestrator` ou `GameContext` para invocar o método de raciocínio de todos os NPCs do mapa a cada frame. NPCs configurados para 'RandomWander' devem ocasionalmente escolher andar para um tile adjacente válido.

## Acceptance criteria
- [ ] Estrutura base de `AIController` criada e anexada a interactables/NPCs.
- [ ] `RandomWanderBehavior` implementado, escolhendo direções cardeais validas periodicamente.
- [ ] Tick global de IA sendo acionado no loop principal (Exploration/World).
- [ ] Testes provando que a IA toma decisões e respeita as colisões da mecânica de Reivindicação de Tile.

## Blocked by
#{issue_2}"""
    },
    {
        "title": "Line-of-Sight (LoS) Raycasting",
        "body": """## Parent
#63

## What to build
Implementar um módulo puramente matemático para verificação de Linha de Visão (Line-of-Sight). A engine de LoS deve traçar uma linha (ex: Bresenham) entre a entidade e o alvo. Se qualquer tile bloqueado cruzar essa linha, retornar falso. Caso contrário, verdadeiro. Deve suportar limitação de distância (Raio de visão).

## Acceptance criteria
- [ ] Função para verificar LoS entre dois pontos no grid.
- [ ] Funcionalidade de distância máxima de visão.
- [ ] Unit tests comprovando que paredes interrompem a visão (LoS = False).
- [ ] Unit tests comprovando visão limpa em corredores e campo aberto (LoS = True).

## Blocked by
None - can start immediately"""
    },
    {
        "title": "Pursuit & Leashing Behavior (A Caçada)",
        "body": """## Parent
#63

## What to build
Criar a inteligência hostil: `PursuitBehavior`. Este comportamento deve utilizar o LoS para "acordar" quando vir o jogador. Uma vez acordado, utiliza o `PathfindingEngine` para gerar uma rota até o jogador, andando até o jogador utilizando a física do grid. O comportamento deve ter `Leashing`: se o jogador fugir além de uma distância X da posição de "spawn" do inimigo, o inimigo abandona a perseguição e volta caminhando para seu ponto original. Adicionalmente, implementar cache no A* (recalcular apenas a cada N passos) para evitar gargalos de performance.

## Acceptance criteria
- [ ] `PursuitBehavior` acionado via LoS contra o jogador.
- [ ] Inimigo segue a rota usando A* (`PathfindingEngine`).
- [ ] Cache de pathfinding implementado (não roda o A* todo frame).
- [ ] `Leashing` implementado: retorna ao spawn se o jogador correr além de X tiles de distância.
- [ ] Testes de integração comprovando a transição de estados (Idle -> Pursuit -> Leashing/Return).

## Blocked by
#{issue_1}, #{issue_3}, #{issue_4}"""
    },
    {
        "title": "Map Combat Engagement & Ciclo de Respawn",
        "body": """## Parent
#63

## What to build
Integrar inimigos com a mecânica de contato e combate. Se o jogador caminhar para o tile do inimigo, ou o inimigo caminhar para o tile do jogador, acionar o evento de início de batalha neutra (sem vantagem posicional), transicionando para `CombatScene`. Após vitória, o inimigo deve ser destruído/removido do `world.interactables` do mapa atual. O inimigo não deve ser persistido em savegame; recarregar o mapa deve naturalmente dar respawn no inimigo.

## Acceptance criteria
- [ ] Colisão (movimento do jogador ou da IA hostil) em tile ocupado pela outra parte aciona combate neutro.
- [ ] Vitória no combate remove a instância do inimigo ativo da memória temporária do mapa.
- [ ] Derrotar o inimigo e recarregar a sala (usar um portal de ida e volta) respawna o inimigo no lugar original (via JSON).
- [ ] Teste E2E ou de integração garantindo que esbarrar aciona combate e remove o inimigo.

## Blocked by
#{issue_5}"""
    }
]

# Track created issues to replace template tags
created_issues = {}

for index, issue_def in enumerate(issues):
    title = issue_def["title"]
    # Replace dependency placeholders
    body = issue_def["body"].format(**created_issues)
    
    print(f"Creating issue: {title}")
    issue_id = create_issue(title, body)
    
    key = f"issue_{index + 1}"
    created_issues[key] = issue_id
    print(f"-> Created Issue #{issue_id}")

print("All issues created successfully.")
