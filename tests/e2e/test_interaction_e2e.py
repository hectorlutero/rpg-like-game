import pygame
import pytest
from src.ui.exploration_scene import ExplorationScene
from src.models.interaction import Chest
from src.models.world import Position
from tests.e2e.ui_tester import UITester

def test_exploration_interaction_flow_e2e():
    """Testa o fluxo completo de interação na cena de exploração (Baú)."""
    tester = UITester()
    
    # 1. Setup: Coloca um baú no mapa
    # Tile (2, 2) terá o baú
    chest = Chest(gold=100, chest_id="e2e_chest")
    tester.world.add_interactable(2, 2, chest)
    
    # Posiciona o jogador em (2, 3) olhando para o Norte (para o baú)
    tester.player.position = Position(2 * 32 + 16, 3 * 32 + 16)
    tester.player.facing_direction = "N"
    
    scene = ExplorationScene(tester.manager, None, None)
    tester.manager.push(scene)
    
    # Inicialmente não há diálogo ativo
    assert not scene.interaction_manager.is_active
    
    # 2. Interage (Simula pressionar ESPAÇO)
    tester.post_key(pygame.K_SPACE, delay=0.1)
    
    # 3. Verifica se o InteractionManager ativou o diálogo do baú
    assert scene.interaction_manager.is_active
    vm = scene.interaction_manager.get_view_model()
    assert "Você abriu o baú" in vm['text']
    assert vm['speaker'] == "Mundo"
    
    # 4. Avança/Fecha o diálogo (Simula pressionar ESPAÇO novamente)
    tester.post_key(pygame.K_SPACE, delay=0.1)
    
    # 5. Verifica se o diálogo fechou e a recompensa foi concedida
    assert not scene.interaction_manager.is_active
    assert tester.player.gold == 100
    
    pygame.quit()

def test_exploration_dialogue_with_choices_e2e():
    """Testa o fluxo de diálogo com escolhas (NPC)."""
    from src.models.dialogue import NPC
    tester = UITester()
    
    data = {
        "start": {"text": "Tudo bem?", "choices": {"Sim": "yes", "Não": "no"}},
        "yes": {"text": "Que bom!"},
        "no": {"text": "Poxa..."}
    }
    npc = NPC("Guarda", Position(0, 0), dialogue_data=data)
    tester.world.add_interactable(2, 2, npc)
    
    # Posiciona jogador olhando para o NPC
    tester.player.position = Position(2 * 32 + 16, 3 * 32 + 16)
    tester.player.facing_direction = "N"
    
    scene = ExplorationScene(tester.manager, None, None)
    tester.manager.push(scene)
    
    # 1. Inicia conversa
    tester.post_key(pygame.K_SPACE, delay=0.1)
    assert scene.interaction_manager.is_active
    vm = scene.interaction_manager.get_view_model()
    assert len(vm['choices']) == 2
    assert vm['selected_index'] == 0 # "Sim"
    
    # 2. Muda para "Não" (Down)
    tester.post_key(pygame.K_DOWN, delay=0.1)
    vm = scene.interaction_manager.get_view_model()
    assert vm['selected_index'] == 1 # "Não"
    
    # 3. Confirma "Não"
    tester.post_key(pygame.K_SPACE, delay=0.1)
    vm = scene.interaction_manager.get_view_model()
    assert vm['text'] == "Poxa..."
    assert len(vm['choices']) == 0
    
    # 4. Fecha
    tester.post_key(pygame.K_SPACE, delay=0.1)
    assert not scene.interaction_manager.is_active
    
    pygame.quit()
