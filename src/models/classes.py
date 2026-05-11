class BaseClass:
    def __init__(self):
        self.multipliers = {}
        self.gain_rates = {}

class Warrior(BaseClass):
    def __init__(self):
        super().__init__()
        self.multipliers = {
            'vida': 1.2, 'mana': 0.8, 'agilidade': 1.0, 'forca': 1.5, 'inteligencia': 0.9
        }
        self.gain_rates = {
            'vida': 10.0, 'mana': 2.0, 'agilidade': 1.0, 'forca': 2.0, 'inteligencia': 0.5
        }

class Mage(BaseClass):
    def __init__(self):
        super().__init__()
        self.multipliers = {
            'vida': 0.8, 'mana': 1.5, 'agilidade': 1.0, 'forca': 0.6, 'inteligencia': 1.8
        }
        self.gain_rates = {
            'vida': 5.0, 'mana': 10.0, 'agilidade': 1.0, 'forca': 0.5, 'inteligencia': 5.0
        }

class Rogue(BaseClass):
    def __init__(self):
        super().__init__()
        self.multipliers = {
            'vida': 1.0, 'mana': 1.0, 'agilidade': 1.6, 'forca': 1.1, 'inteligencia': 1.2
        }
        self.gain_rates = {
            'vida': 7.0, 'mana': 4.0, 'agilidade': 4.0, 'forca': 1.5, 'inteligencia': 2.0
        }
