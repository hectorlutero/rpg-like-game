import pytest
from src.models.combat import CombatManager, EnemyInteractable
from src.models.character import Character
from src.models.classes import Warrior
from src.ui.scenes import GameContext
from src.models.world import World, Position

def test_loot_generation_logic():
    # Setup
    player = Character("Hero", Warrior())
    dummy_grid = [[0 for _ in range(10)] for _ in range(10)]
    world = World(dummy_grid)
    context = GameContext(player, world)
    
    enemy = Character("Slime", Warrior())
    enemy.hp = 10
    
    # Test CombatManager with loot table
    loot_table = {"Poção de Vida": 1.0} # 100% chance for test
    cm = CombatManager([player], [enemy], gold_reward=50, xp_reward=100, loot_table=loot_table)
    
    # Generate loot
    loot = cm.generate_loot()
    assert "Poção de Vida" in loot
    
    # Simulate victory and reward distribution (as done in CombatScene)
    initial_gold = player.gold
    player.gold += cm.gold_reward
    for item_name in loot:
        player.inventory.add_item(item_name)
        
    assert player.gold == initial_gold + 50
    assert "Poção de Vida" in player.inventory.items

def test_shop_buy_sell_logic():
    # Setup
    player = Character("Hero", Warrior())
    player.gold = 100
    
    # Test buying
    item_name = "Poção de Vida"
    price = 20
    
    if player.gold >= price:
        player.gold -= price
        player.inventory.add_item(item_name)
    
    assert player.gold == 80
    assert item_name in player.inventory.items
    
    # Test selling (usually 50% price)
    sell_price = price // 2
    if item_name in player.inventory.items:
        player.inventory.remove_item(item_name)
        player.gold += sell_price
        
    assert player.gold == 90
    assert item_name not in player.inventory.items
