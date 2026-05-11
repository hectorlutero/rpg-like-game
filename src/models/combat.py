class DamageCalculator:
    def calculate_physical(self, attacker, defender):
        strength = attacker.get_attribute('forca')
        # Using a default power of 1.0 for basic attacks
        raw_damage = strength * 1.0
        defense = getattr(defender, 'defense_absolute', 0)
        
        damage = max(0, int(raw_damage - defense))
        return damage

    def calculate_magical(self, attacker, defender):
        intelligence = attacker.get_attribute('inteligencia')
        # Using a default power of 1.0 for basic magic
        raw_damage = intelligence * 1.0
        defense_rel = getattr(defender, 'defense_relative', 0.0)
        
        damage = max(0, int(raw_damage * (1.0 - defense_rel)))
        return damage

    def calculate_status_chance(self, attacker, defender, base_chance=50):
        atk_int = attacker.get_attribute('inteligencia')
        def_int = defender.get_attribute('inteligencia')
        
        # Simple formula: base + difference
        chance = base_chance + (atk_int - def_int)
        return max(0, min(100, int(chance)))
