from src.models.attributes import AttributePackage
from src.models.world import Position

class Character:
    def __init__(self, name, character_class, base_stats=None, level=1):
        self.name = name
        self.character_class = character_class
        self.base_stats = base_stats if base_stats is not None else character_class.initial_stats
        self.level = level
        self.xp = 0
        self.xp_to_next_level = 100
        self.attributes = AttributePackage()
        
        self.defense_absolute = 0
        self.defense_relative = 0.0
        
        # Current resources
        self.current_hp = self.get_attribute('vida')
        self.current_mana = self.get_attribute('mana')
        
        # Position and Orientation
        self.position = Position(0, 0)
        self.facing_direction = "S" # South (down) default
        self._energy = 3
        self.skills = set() # Set of skill names

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

    def get_attribute(self, name):
        base_value = self.base_stats.get(name, 0)
        multiplier = self.character_class.multipliers.get(name, 1.0)
        gain_rate = self.character_class.gain_rates.get(name, 0.0)
        
        return self.attributes.calculate(base_value, self.level, gain_rate, multiplier)

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
