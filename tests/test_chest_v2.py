import pytest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.ui.scenes import GameContext
from src.models.interaction import Chest
from src.models.items import CONSUMABLE_DATA

def test_chest_interaction_grant_items_and_gold():
    # Setup
    player = Character("Hero", Warrior())
    world = World([[0]*5 for _ in range(5)])
    context = GameContext(player, world)
    
    item = CONSUMABLE_DATA["Poção de Vida"]
    chest = Chest(items=[item], gold=100, chest_id="chest_01")
    
    # 1. Interact first time
    msg = chest.on_interact(context)
    
    assert "Você abriu o baú!" in msg
    assert "Ganhou 100 G!" in msg
    assert "Encontrou Poção de Vida!" in msg
    assert player.gold == 100
    assert "Poção de Vida" in player.inventory.items
    assert chest.is_open is True
    assert "chest_01" in context.opened_chests
    
    # 2. Interact second time
    msg2 = chest.on_interact(context)
    assert msg2 == "O baú está vazio."
    assert player.gold == 100 # No additional gold

def test_chest_persistence_sync():
    # Setup
    player = Character("Hero", Warrior())
    world = World([[0]*5 for _ in range(5)])
    context = GameContext(player, world)
    
    # Simulate loading a game where chest is already open
    context.opened_chests.add("chest_99")
    
    chest = Chest(gold=50, chest_id="chest_99")
    
    # We need a way to sync chest state with context.opened_chests
    # Let's improve the Chest class to check context in on_interact
    
    msg = chest.on_interact(context)
    # If it's already in context.opened_chests, it should be considered empty
    # This test will fail with current implementation if chest.is_open is False by default
    assert msg == "O baú está vazio."
