from src.models.world import Position
from src.models.persistence import Inventory

class Character:
    def __init__(self, name, character_class, base_stats=None, level=1):
        self.name = name
        self.character_class = character_class
        self.base_stats = base_stats if base_stats is not None else character_class.initial_stats
        self.level = level
        self.xp = 0
        self.xp_to_next_level = 100
        
        # Equipment Slots
        self.equipment = {
            "weapon": None,
            "shield": None,
            "armor": None,
            "accessory": None
        }
        
        # Current resources
        self.current_hp = self.get_attribute('vida')
        self.current_mana = self.get_attribute('mana')
        
        # Position and Orientation
        self.position = Position(0, 0)
        self.facing_direction = "S" # South (down) default
        self._energy = 3
        self.skills = set() # Set of skill names
        self._gold = 0
        self.inventory = Inventory()
        self.status_effects = {} # {status_type: {'duration': X, 'potency': Y}}

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = max(0, value)

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = max(0, min(value, 3))

    def rest(self):
        """Replenishes energy, HP, and Mana to max."""
        self.energy = 3
        self.hp = self.max_hp
        self.mana = self.max_mana

    def update_orientation(self, dx, dy):
        """Updates facing direction based on movement vector."""
        if dx > 0: self.facing_direction = "E"
        elif dx < 0: self.facing_direction = "W"
        elif dy > 0: self.facing_direction = "S"
        elif dy < 0: self.facing_direction = "N"

    def _get_proficiency_multiplier(self, equipment_item):
        """Calculates the highest proficiency multiplier for an item based on its tags."""
        if not equipment_item:
            return 1.0
        
        prof_mult = 1.0
        tags = getattr(equipment_item, 'tags', [])
        for tag in tags:
            if tag in self.character_class.proficiencies:
                prof_mult = max(prof_mult, self.character_class.proficiencies[tag])
        return prof_mult

    def get_attribute(self, name):
        """Calculates final attribute considering base, level, class and equipment."""
        base_value = self.base_stats.get(name, 0)
        multiplier = self.character_class.multipliers.get(name, 1.0)
        gain_rate = self.character_class.gain_rates.get(name, 0.0)
        
        # Base calculation
        final_base = int((base_value + (self.level * gain_rate)) * multiplier)
        
        total_flat_bonus = 0
        total_percent_bonus = 0.0
        
        for eq in self.equipment.values():
            if not eq: continue
            
            prof_mult = self._get_proficiency_multiplier(eq)
            
            # Flat Bonuses
            flat = eq.bonuses.get(name, 0)
            total_flat_bonus += int(flat * prof_mult)
            
            # Percentage Bonuses
            perc = getattr(eq, 'percent_bonuses', {}).get(name, 0.0)
            total_percent_bonus += (perc * prof_mult)

        return int((final_base + total_flat_bonus) * (1.0 + total_percent_bonus))

    @property
    def defense_absolute(self):
        total = 0.0
        for eq in self.equipment.values():
            if not eq: continue
            prof_mult = self._get_proficiency_multiplier(eq)
            val = eq.bonuses.get('defesa_absoluta', 0.0)
            total += (val * prof_mult)
        return int(total)

    @property
    def defense_relative(self):
        total = 0.0
        for eq in self.equipment.values():
            if not eq: continue
            prof_mult = self._get_proficiency_multiplier(eq)
            val = eq.bonuses.get('defesa_relativa', 0.0)
            total += (val * prof_mult)
        return min(0.9, total) # Cap relative defense at 90%

    def equip_item(self, item):
        """Checks requirements and equips an item."""
        # Check class
        if item.req_class and item.req_class != self.character_class.__class__.__name__:
            return False, f"Classe {self.character_class.__class__.__name__} não pode usar este item."
        
        # Check stats
        for stat, req in item.req_stats.items():
            if self.get_attribute(stat) < req:
                return False, f"{stat.capitalize()} insuficiente (Requer {req})."

        # Equip
        old_item = self.equipment.get(item.slot)
        self.equipment[item.slot] = item
        return True, old_item

    def use_item(self, item_name):
        """Uses or equips an item from the inventory."""
        from src.models.items import CONSUMABLE_DATA, EQUIPMENT_DATA
        
        # Check if it's a consumable
        if item_name in CONSUMABLE_DATA:
            item = CONSUMABLE_DATA[item_name]
            # Apply Effects
            for effect, value in item.effect.items():
                if effect == 'hp':
                    self.hp += value
                elif effect == 'mana':
                    self.mana += value
                elif effect == 'cure':
                    if value in self.status_effects:
                        del self.status_effects[value]
            
            self.inventory.remove_item(item_name)
            return True, f"Usou {item_name}!"

        # Check if it's equipment
        if item_name in EQUIPMENT_DATA:
            item = EQUIPMENT_DATA[item_name]
            success, result = self.equip_item(item)
            if success:
                self.inventory.remove_item(item_name)
                if result: # old_item
                    self.inventory.add_item(result.name)
                return True, f"Equipou {item_name}!"
            return False, result

        return False, "Item não encontrado."

    def unequip_item(self, slot):
        if slot in self.equipment:
            item = self.equipment[slot]
            self.equipment[slot] = None
            return item
        return None

    @property
    def hp(self):
        return self.current_hp

    @hp.setter
    def hp(self, value):
        self.current_hp = max(0, min(value, self.max_hp))

    @property
    def max_hp(self):
        return self.get_attribute('vida')

    @property
    def mana(self):
        return self.current_mana

    @mana.setter
    def mana(self, value):
        self.current_mana = max(0, min(value, self.max_mana))

    @property
    def max_mana(self):
        return self.get_attribute('mana')

    def use_spell(self, spell):
        if self.mana >= spell.mana_cost:
            self.mana -= spell.mana_cost
            return True
        return False

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1
        self.current_hp = self.get_attribute('vida')
        self.current_mana = self.get_attribute('mana')
