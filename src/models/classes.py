class BaseClass:
    def __init__(self):
        self.multipliers = {}
        self.gain_rates = {}
        self.initial_stats = {}
        self.proficiencies = {} # {'sword': 1.2}

class Warrior(BaseClass):
    def __init__(self):
        super().__init__()
        self.initial_stats = {
            'vida': 100, 'mana': 20, 'agilidade': 8, 'forca': 10, 'inteligencia': 5
        }
        self.multipliers = {
            'vida': 1.2, 'mana': 0.8, 'agilidade': 1.0, 'forca': 1.5, 'inteligencia': 0.9
        }
        self.gain_rates = {
            'vida': 10.0, 'mana': 2.0, 'agilidade': 1.0, 'forca': 2.0, 'inteligencia': 0.5
        }
        self.proficiencies = {
            'sword': 1.2, 'shield': 1.2, 'heavy_armor': 1.1
        }

class Mage(BaseClass):
    def __init__(self):
        super().__init__()
        self.initial_stats = {
            'vida': 60, 'mana': 100, 'agilidade': 10, 'forca': 5, 'inteligencia': 10
        }
        self.multipliers = {
            'vida': 0.8, 'mana': 1.5, 'agilidade': 1.0, 'forca': 0.6, 'inteligencia': 1.8
        }
        self.gain_rates = {
            'vida': 5.0, 'mana': 10.0, 'agilidade': 1.0, 'forca': 0.5, 'inteligencia': 5.0
        }
        self.proficiencies = {
            'staff': 1.3, 'robe': 1.1
        }

class Rogue(BaseClass):
    def __init__(self):
        super().__init__()
        self.initial_stats = {
            'vida': 80, 'mana': 40, 'agilidade': 12, 'forca': 8, 'inteligencia': 8
        }
        self.multipliers = {
            'vida': 1.0, 'mana': 1.0, 'agilidade': 1.6, 'forca': 1.1, 'inteligencia': 1.2
        }
        self.gain_rates = {
            'vida': 7.0, 'mana': 4.0, 'agilidade': 4.0, 'forca': 1.5, 'inteligencia': 2.0
        }
        self.proficiencies = {
            'dagger': 1.4, 'leather_armor': 1.2
        }
