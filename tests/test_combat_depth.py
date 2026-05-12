import pytest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.combat import CombatManager

def test_combat_manager_victory_and_rewards_depth():
    # Setup
    player = Character("Hero", Warrior())
    enemy = Character("Slime", Warrior())
    enemy.hp = 10
    
    loot_table = {"Poção de Vida": 1.0}
    cm = CombatManager([player], [enemy], gold_reward=50, xp_reward=100, loot_table=loot_table)
    
    # 1. Simulate Player Turn (Manual execution)
    # Warrior has 10 STR, Slime has 0 DEF -> 10 damage
    cm.execute_action(player, "Attack", enemy)
    
    # 2. Check if battle is over
    assert enemy.hp == 0
    assert cm.is_over is True
    assert cm.winner == "Party"
    
    # 3. Resolve Rewards
    messages = cm.resolve_rewards()
    
    assert any("VITÓRIA" in m for m in messages)
    assert any("Poção de Vida" in m for m in messages)
    assert player.gold == 50
    assert player.level == 2 # 100 XP gained
    assert "Poção de Vida" in player.inventory.items

def test_combat_manager_defeat_depth():
    # Setup
    player = Character("Hero", Warrior())
    player.hp = 10
    enemy = Character("Boss", Warrior())
    
    cm = CombatManager([player], [enemy])
    
    # 1. Simulate Enemy Turn
    # Boss has 10 STR, Player has 0 DEF -> 10 damage
    cm.handle_enemy_turn(enemy)
    
    # 2. Check if battle is over
    assert player.hp == 0
    assert cm.is_over is True
    assert cm.winner == "Enemies"
    
    # 3. Rewards should be empty
    messages = cm.resolve_rewards()
    assert len(messages) == 0

def test_combat_manager_atb_status_kill():
    # Setup
    player = Character("Hero", Warrior())
    player.hp = 5
    # Apply poison that deals 5 damage
    player.status_effects['poison'] = {'duration': 1, 'potency': 5}
    
    enemy = Character("Slime", Warrior())
    
    cm = CombatManager([player], [enemy])
    
    # Update until player turn starts (Agility 8 * 2.0 = 16 per sec)
    # At dt=10, ATB reaches 160 (>= 100)
    cm.update(10.0)
    
    # Status should have ticked and killed the player before they could act
    assert player.hp == 0
    assert cm.is_over is True
    assert cm.winner == "Enemies"
    assert cm.active_entity == player # It was their turn but they died
