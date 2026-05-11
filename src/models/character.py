from src.models.attributes import AttributePackage

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

    def get_attribute(self, name):
        base_value = self.base_stats.get(name, 0)
        multiplier = self.character_class.multipliers.get(name, 1.0)
        gain_rate = self.character_class.gain_rates.get(name, 0.0)
        
        return self.attributes.calculate(base_value, self.level, gain_rate, multiplier)

    def use_spell(self, spell):
        if self.current_mana >= spell.mana_cost:
            self.current_mana -= spell.mana_cost
            return True
        return False

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1
        # Update current hp/mana on level up? 
        # (For now just maxing them out is a simple approach)
        self.current_hp = self.get_attribute('vida')
        self.current_mana = self.get_attribute('mana')
