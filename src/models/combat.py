import math
import random
from src.models.interaction import Interactable
from src.models.status import StatusManager

class EnemyInteractable(Interactable):
    def __init__(self, name, character_class, level, world_pos, gold_yield=50, xp_yield=100, loot_table=None):
        self.name = name
        self.character_class = character_class
        self.level = level
        self.world_pos = world_pos 
        self.gold_yield = gold_yield
        self.xp_yield = xp_yield
        self.loot_table = loot_table or {}

    def on_interact(self, context):
        from src.ui.combat_scene import CombatScene
        from src.models.character import Character
        enemy = Character(self.name, self.character_class, level=self.level)
        enemy.hp = 30
        enemy.weakness = "Ice" 
        cm = CombatManager(context.party, [enemy], gold_reward=self.gold_yield, xp_reward=self.xp_yield, loot_table=self.loot_table)
        return CombatScene(context.scene_manager, cm, self.world_pos)

class DamageCalculator:
    ELEMENT_WEAKNESS = {
        "Fire": "Ice",    # Fire beats Ice
        "Ice": "Fire",    # Mutual for testing
        "Lightning": "Water"
    }

    def calculate_physical(self, attacker, defender):
        strength = attacker.get_attribute('forca')
        raw_damage = strength * 1.0
        defense = getattr(defender, 'defense_absolute', 0)
        damage = max(0, int(raw_damage - defense))
        return damage

    def calculate_magical(self, attacker, defender, skill=None):
        intelligence = attacker.get_attribute('inteligencia')
        power = skill.power if skill else 1.0
        raw_damage = intelligence * power
        
        # Elemental multiplier
        multiplier = 1.0
        if skill and skill.element:
            # Simplificação: O defensor pode ter uma fraqueza definida (ex: Slime é fraco contra Gelo)
            defender_weakness = getattr(defender, 'weakness', None)
            if defender_weakness == skill.element:
                multiplier = 1.5

        defense_rel = getattr(defender, 'defense_relative', 0.0)
        damage = max(0, int(raw_damage * (1.0 - defense_rel) * multiplier))
        return damage

    def calculate_status_chance(self, attacker, defender, base_chance=50):
        atk_int = attacker.get_attribute('inteligencia')
        def_int = defender.get_attribute('inteligencia')
        chance = base_chance + (atk_int - def_int)
        return max(0, min(100, int(chance)))

class CombatManager:
    def __init__(self, party, enemies, gold_reward=0, xp_reward=0, loot_table=None):
        self.party = party  # List of Character objects
        self.enemies = enemies  # List of Character objects
        self.gold_reward = gold_reward
        self.xp_reward = xp_reward
        self.loot_table = loot_table or {} # {'ItemName': 0.5} (50% chance)
        self.all_entities = party + enemies
        
        # Initialize ATB meters (0 to 100)
        self.atb_states = {entity: 0.0 for entity in self.all_entities}
        self.active_entity = None
        self.is_waiting_for_input = False
        self.battle_log = []

    def generate_loot(self):
        """Generates a list of items based on the loot table."""
        loot = []
        for item_name, chance in self.loot_table.items():
            if random.random() < chance:
                loot.append(item_name)
        return loot

    def update(self, dt):
        """Update ATB meters. Returns the entity that reached 100 first, if any."""
        if self.active_entity or self.is_waiting_for_input:
            return None

        # Sort by agility to handle simultaneous fills (though dt should be small)
        for entity in self.all_entities:
            # Formula: Increase based on Agility
            agility = entity.get_attribute('agilidade')
            # Adjust multiplier to control combat speed
            growth = (agility * 2.0) * dt
            self.atb_states[entity] = min(100.0, self.atb_states[entity] + growth)
            
            if self.atb_states[entity] >= 100.0:
                self.active_entity = entity
                
                # Process Status Ticks at turn start
                status_logs = StatusManager.process_tick(entity)
                self.battle_log.extend(status_logs)
                
                if entity in self.party:
                    self.is_waiting_for_input = True
                return entity
        return None

    def execute_action(self, attacker, action_type, target, ability_name=None):
        """Executes an action and resets ATB."""
        calc = DamageCalculator()
        damage = 0
        action_result = {"type": action_type, "success": True}
        
        if action_type == "Attack":
            damage = calc.calculate_physical(attacker, target)
            target.hp -= damage
            self.battle_log.append(f"{attacker.name} atacou {target.name} por {damage} de dano!")
        
        elif action_type == "Flee":
            # 50% chance to flee
            if random.random() > 0.5:
                self.battle_log.append(f"{attacker.name} fugiu da batalha!")
                action_result["fled"] = True
            else:
                self.battle_log.append(f"{attacker.name} tentou fugir, mas falhou!")
                action_result["success"] = False

        elif action_type in ["Skill", "Magic"]:
            from src.models.skills import ABILITY_DATA
            
            if not ability_name:
                self.battle_log.append(f"{attacker.name} não escolheu uma habilidade!")
                action_result["success"] = False
            else:
                ability = ABILITY_DATA.get(ability_name)
                current_int = attacker.get_attribute('inteligencia')
                
                if not ability or ability.int_req > current_int:
                    self.battle_log.append(f"{attacker.name} não tem INT para usar {ability_name}!")
                    action_result["success"] = False
                elif action_type == "Magic" and attacker.mana < ability.mana_cost:
                    self.battle_log.append(f"{attacker.name} não tem Mana para {ability_name}!")
                    action_result["success"] = False
                else:
                    # Executa a habilidade
                    if action_type == "Magic":
                        attacker.mana -= ability.mana_cost
                        damage = calc.calculate_magical(attacker, target, ability)
                        self.battle_log.append(f"{attacker.name} lançou {ability_name} em {target.name} por {damage} de dano!")
                    else:
                        damage = int(calc.calculate_physical(attacker, target) * ability.power)
                        self.battle_log.append(f"{attacker.name} usou {ability_name} em {target.name} por {damage} de dano!")
                    
                    target.hp -= damage

                    # Apply Status Effect if present
                    if ability.status_effect:
                        success, status_msg = StatusManager.apply_status(
                            attacker, target, 
                            ability.status_effect, 
                            ability.status_chance, 
                            ability.status_duration, 
                            ability.status_potency
                        )
                        self.battle_log.append(status_msg)
        
        elif action_type == "Item":
            self.battle_log.append(f"{attacker.name} usou um Item (Ainda não implementado)!")
        
        elif action_type == "Wait":
            self.battle_log.append(f"{attacker.name} esperou!")
        
        # Reset ATB
        self.atb_states[attacker] = 0.0
        self.active_entity = None
        self.is_waiting_for_input = False
        
        return action_result

    def get_atb_percentage(self, entity):
        return self.atb_states.get(entity, 0.0)
