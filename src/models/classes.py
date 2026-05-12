import json
import os

class BaseClass:
    _data = None

    def __init__(self, class_name):
        if BaseClass._data is None:
            self._load_data()
        
        data = BaseClass._data.get(class_name, {})
        self.multipliers = data.get("multipliers", {})
        self.gain_rates = data.get("gain_rates", {})
        self.initial_stats = data.get("initial_stats", {})
        self.proficiencies = data.get("proficiencies", {})

    def _load_data(self):
        # Determine path relative to this file or root
        # For simplicity, assuming running from root
        path = "data/classes.json"
        if not os.path.exists(path):
            # Fallback for tests if needed, but path should be root
            pass
        
        with open(path, 'r') as f:
            BaseClass._data = json.load(f)

class Warrior(BaseClass):
    def __init__(self):
        super().__init__("Warrior")

class Mage(BaseClass):
    def __init__(self):
        super().__init__("Mage")

class Rogue(BaseClass):
    def __init__(self):
        super().__init__("Rogue")
