class ATBEngine:
    def __init__(self):
        self.combatants = {} # {combatant_object: current_meter_value}

    def add_combatant(self, combatant):
        self.combatants[combatant] = 0.0

    def get_meter(self, combatant):
        return self.combatants.get(combatant, 0.0)

    def tick(self, delta_time):
        for combatant in self.combatants:
            agility = combatant.get_attribute('agilidade')
            # Formula: speed = agility * multiplier. 
            # If agility is 10, and delta_time is 1, maybe it gains 10 points.
            # At 100 points, it's ready.
            growth = agility * delta_time
            self.combatants[combatant] = min(100.0, self.combatants[combatant] + growth)

    def is_ready(self, combatant):
        return self.combatants.get(combatant, 0.0) >= 100.0

    def get_ready_combatants(self):
        return [c for c, m in self.combatants.items() if m >= 100.0]

    def reset_meter(self, combatant):
        if combatant in self.combatants:
            self.combatants[combatant] = 0.0
