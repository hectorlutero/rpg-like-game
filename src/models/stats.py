from enum import Enum

class ModifierType(Enum):
    FLAT = "flat"
    PERCENT = "percent"

class Modifier:
    def __init__(self, value, mod_type=ModifierType.FLAT, source=None):
        self.value = value
        self.type = mod_type
        self.source = source

    def __repr__(self):
        return f"Modifier({self.value}, {self.type.value}, source={self.source})"

class Stat:
    """Represents a single character attribute with modifier stacking logic."""
    def __init__(self, name, base_value=0):
        self.name = name
        self.base_value = base_value
        self.modifiers = []

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

    def remove_modifiers_from_source(self, source):
        self.modifiers = [m for m in self.modifiers if m.source != source]

    def clear_modifiers(self):
        self.modifiers = []

    def calculate(self):
        """
        Calculates the final value. 
        Formula: (Base + Sum of Flats) * (1 + Sum of Percents)
        """
        total_flat = 0
        total_percent = 0.0
        
        for mod in self.modifiers:
            if mod.type == ModifierType.FLAT:
                total_flat += mod.value
            elif mod.type == ModifierType.PERCENT:
                total_percent += mod.value
        
        return int((self.base_value + total_flat) * (1.0 + total_percent))

    def get_details(self):
        """Returns a string breakdown of the stat calculation for debugging."""
        flats = [m for m in self.modifiers if m.type == ModifierType.FLAT]
        percs = [m for m in self.modifiers if m.type == ModifierType.PERCENT]
        
        detail = f"{self.name.upper()}: Base({self.base_value})"
        if flats:
            detail += " + Flats(" + " + ".join([f"{m.value}[{m.source}]" for m in flats]) + ")"
        if percs:
            detail += " * Percents(1 + " + " + ".join([f"{m.value}[{m.source}]" for m in percs]) + ")"
        
        detail += f" = {self.calculate()}"
        return detail
