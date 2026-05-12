import pytest
from src.models.character import Character
from src.models.classes import Warrior, Mage
from src.models.items import Equipment

def test_equipment_percentage_bonuses():
    player = Character("Hero", Warrior())
    # Warrior base life at level 1: (100 + (1 * 10)) * 1.2 = 132
    base_hp = player.get_attribute('vida')
    assert base_hp == 132
    
    # Create item with percentage bonus
    # We need to update the Equipment class to support this
    armor = Equipment("Escama de Dragão", "Bônus de 10% de Vida", slot="armor", price=500)
    armor.percent_bonuses = {'vida': 0.10} # 10%
    
    player.equipment['armor'] = armor
    
    # Final HP should be base_hp * 1.10 = 145.2 -> 145
    # Let's decide if flat bonuses come before or after percentage. 
    # Usually: (Base + Flat) * (1 + Multiplier)
    assert player.get_attribute('vida') == int(base_hp * 1.10)

def test_class_proficiency_bonus():
    warrior = Character("Grog", Warrior())
    mage = Character("Zand", Mage())
    
    # Sword with tag "sword" and 10 Strength bonus
    sword = Equipment("Espada Mágica", "Forte para guerreiros", slot="weapon", price=300)
    sword.bonuses = {'forca': 10}
    sword.tags = ["sword"]
    
    # Warrior Proficiency for 'sword' is 1.2
    # Mage has no proficiency for 'sword' (default 1.0)
    
    base_str_warrior = warrior.get_attribute('forca')
    base_str_mage = mage.get_attribute('forca')
    
    warrior.equipment['weapon'] = sword
    mage.equipment['weapon'] = sword
    
    # Warrior should get 10 * 1.2 = 12 bonus
    assert warrior.get_attribute('forca') == base_str_warrior + 12
    # Mage should get 10 * 1.0 = 10 bonus
    assert mage.get_attribute('forca') == base_str_mage + 10
