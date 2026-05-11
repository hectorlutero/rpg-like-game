from src.models.attributes import AttributePackage

class Character:
    def __init__(self, name, character_class, base_stats, level=1):
        self.name = name
        self.character_class = character_class
        self.base_stats = base_stats
        self.level = level
        self.attributes = AttributePackage()

    def get_attribute(self, name):
        base_value = self.base_stats.get(name, 0)
        multiplier = self.character_class.multipliers.get(name, 1.0)
        gain_rate = self.character_class.gain_rates.get(name, 0.0)
        
        return self.attributes.calculate(base_value, self.level, gain_rate, multiplier)
