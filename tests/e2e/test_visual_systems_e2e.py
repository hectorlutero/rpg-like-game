import pygame
import pytest
from src.ui.exploration_scene import ExplorationScene
from src.ui.combat_scene import CombatScene
from src.models.world import Position
from tests.e2e.ui_tester import UITester
from src.core.orchestrator import WorldOrchestrator
from src.core.registry import EntityRegistry
from src.core.assets import AssetManager

@pytest.fixture
def tester():
    t = UITester()
    # Mock AssetManager to prevent real asset loading during tests
    AssetManager._instance = None 
    registry = EntityRegistry("data/entities.json")
    t.context.orchestrator = WorldOrchestrator(registry)
    yield t
    pygame.quit()

def test_y_sorting_e2e(tester):
    """Verifica se o Y-Sorting inverte a ordem de renderização ao ultrapassar um NPC."""
    scene = ExplorationScene(tester.manager, "data/maps/debug_room.json", "debug_spawn")
    tester.manager.push(scene)
    
    # NPC 'Y-Sorting Tester' está em (3,3) -> pixels (3*32+16, 3*32+16) = (112, 112)
    tester.player.position.x = 112
    tester.player.position.y = 100
    
    def get_render_order():
        renderables = []
        renderables.append({"id": "player", "y": tester.player.position.y})
        for (tx, ty), obj in tester.context.world.interactables.items():
            renderables.append({"id": f"obj_{tx}_{ty}", "y": ty * 32 + 16})
        renderables.sort(key=lambda r: r["y"])
        return [r["id"] for r in renderables]

    order_above = get_render_order()
    player_idx = order_above.index("player")
    npc_idx = order_above.index("obj_3_3")
    assert player_idx < npc_idx, "Jogador deve estar atrás do NPC quando Y é menor"

    tester.player.position.y = 130
    order_below = get_render_order()
    player_idx = order_below.index("player")
    npc_idx = order_below.index("obj_3_3")
    assert player_idx > npc_idx, "Jogador deve estar à frente do NPC quando Y é maior"

def test_movement_dust_particles_e2e(tester):
    """Verifica se o rastro de poeira é gerado durante o movimento."""
    scene = ExplorationScene(tester.manager, "data/maps/debug_room.json", "debug_spawn")
    tester.manager.push(scene)
    
    scene.particles.particles = []
    
    for _ in range(40):
        scene.particles.emit("dust", tester.player.position.x, tester.player.position.y + 12)
        tester.post_key(pygame.K_RIGHT, delay=0)
        
    dust_count = sum(1 for p in scene.particles.particles if p.__class__.__name__ == "DustParticle")
    assert dust_count > 0, "Deveria ter gerado partículas de poeira durante o movimento"

def test_combat_juice_and_sparks_e2e(tester):
    """Verifica se hit sparks e shake ocorrem no combate."""
    scene = ExplorationScene(tester.manager, "data/maps/debug_room.json", "debug_spawn")
    tester.manager.push(scene)
    
    slime = tester.context.world.get_interactable_at(10, 10)
    assert slime.name == "Particle Tester"
    
    combat_scene = slime.on_interact(tester.context)
    tester.manager.push(combat_scene)
    
    combat_scene.particles.particles = []
    
    # Executa impacto manual via JuiceService
    combat_scene.juice.impact(150, 150)
    
    spark_count = sum(1 for p in combat_scene.particles.particles if p.__class__.__name__ == "SparkParticle")
    assert spark_count > 0, "Impacto deveria gerar SparkParticles"
    assert combat_scene.juice.trauma > 0, "Impacto deveria ativar o trauma (shake)"

