import pygame
import math
import random
from src.models.interaction import Interactable
from src.models.status import StatusManager

class EnemyInteractable(Interactable):
    def __init__(self, name, character_class, level, world_pos=None, gold_yield=50, xp_yield=100, loot_table=None, **kwargs):
        self.name = name
        # If character_class is a string, we need to map it (for LEGO engine)
        from src.models.classes import Warrior, Mage, Rogue
        class_map = {"Warrior": Warrior, "Mage": Mage, "Rogue": Rogue}
        if isinstance(character_class, str):
            self.character_class = class_map.get(character_class, Warrior)()
        else:
            self.character_class = character_class
            
        self.level = level
        self.world_pos = world_pos or kwargs.get("position")
        self.gold_yield = gold_yield
        self.xp_yield = xp_yield
        self.loot_table = loot_table or {}

    def on_interact(self, context):
        from src.ui.combat_scene import CombatScene
        from src.models.character import Character
        enemy = Character(self.name, self.character_class, level=self.level)
        enemy.hp = 30
        enemy.weakness = "Ice" 
        cm = CombatManager(context.party, [enemy], 
                           gold_reward=self.gold_yield, 
                           xp_reward=self.xp_yield, 
                           loot_table=self.loot_table,
                           signal_bus=context.signal_bus)
        return CombatScene(context.scene_manager, cm, self.world_pos)

    def draw(self, screen, context, pos):
        # Inimigos são quadrados vermelhos
        pygame.draw.rect(screen, (200, 50, 50), (pos[0], pos[1], 32, 32))
        # Detalhe para diferenciar (olhos pequenos)
        pygame.draw.rect(screen, (255, 255, 255), (pos[0] + 6, pos[1] + 10, 4, 4))
        pygame.draw.rect(screen, (255, 255, 255), (pos[0] + 22, pos[1] + 10, 4, 4))

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
    def __init__(self, party, enemies, gold_reward=0, xp_reward=0, loot_table=None, signal_bus=None):
        self.party = party  # List of Character objects
        self.enemies = enemies  # List of Character objects
        self.gold_reward = gold_reward
        self.xp_reward = xp_reward
        self.loot_table = loot_table or {} # {'ItemName': 0.5} (50% chance)
        self.signal_bus = signal_bus
        self.all_entities = party + enemies
        
        # Initialize ATB meters (0 to 100)
        self.atb_states = {entity: 0.0 for entity in self.all_entities}
        self.active_entity = None
        self.is_waiting_for_input = False
        self.battle_log = []
        self.is_over = False
        self.winner = None # "Party" or "Enemies"

    def generate_loot(self):
        """Generates a list of items based on the loot table."""
        loot = []
        for item_name, chance in self.loot_table.items():
            if random.random() < chance:
                loot.append(item_name)
        return loot

    def update(self, dt):
        """Update ATB meters. Returns the entity that reached 100 first, if any."""
        if self.is_over or self.active_entity or self.is_waiting_for_input:
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
                
                # Check if status tick killed the entity
                self.check_battle_status()
                if self.is_over:
                    return None
                    
                return entity
        return None

    def handle_enemy_turn(self, enemy):
        """Processes AI for the given enemy."""
        if self.is_over or enemy not in self.enemies:
            return

        if StatusManager.is_paralyzed(enemy):
            self.battle_log.append(f"{enemy.name} está paralisado e não pode agir!")
            self.atb_states[enemy] = 0.0
            self.active_entity = None
            return

        # Enemy AI: Uses a random skill if it has any, otherwise attacks
        available_skills = list(enemy.skills)
        if available_skills and random.random() < 0.7: # 70% chance to use a skill
            skill_name = random.choice(available_skills)
            # Targets the first party member for simplicity
            self.execute_action(enemy, "Skill", self.party[0], ability_name=skill_name)
        else:
            self.execute_action(enemy, "Attack", self.party[0])

    def check_battle_status(self):
        """Checks if the battle is over and sets winner."""
        if all(e.hp <= 0 for e in self.enemies):
            self.is_over = True
            self.winner = "Party"
        elif all(p.hp <= 0 for p in self.party):
            self.is_over = True
            self.winner = "Enemies"
        return self.is_over

    def resolve_rewards(self):
        """Distributes rewards and returns a summary message."""
        if not self.is_over or self.winner != "Party":
            return []

        messages = []
        summary = f"VITÓRIA! Ganhou {self.xp_reward} XP"
        if self.gold_reward > 0:
            summary += f" e {self.gold_reward} G"
        messages.append(summary)
        
        # Items
        loot = self.generate_loot()
        if loot:
            messages.append("Itens obtidos: " + ", ".join(loot))
            for item_name in loot:
                # Note: This assumes party[0] is the main player for inventory
                self.party[0].receive_item(item_name, self.signal_bus)
        
        # XP and Gold
        for hero in self.party:
            hero.gain_xp(self.xp_reward)
            hero.gold += self.gold_reward

        # Emit Kill signals
        if self.signal_bus:
            for enemy in self.enemies:
                self.signal_bus.emit("KILL_ENEMY", target=enemy.name)
            
        return messages

    def execute_action(self, attacker, action_type, target, ability_name=None):
        """Executes an action and resets ATB."""
        if self.is_over:
            return {"success": False, "msg": "Batalha já terminou."}

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
                self.is_over = True
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
        
        # Check if action ended the battle
        self.check_battle_status()
        
        return action_result

    def get_atb_percentage(self, entity):
        return self.atb_states.get(entity, 0.0)
