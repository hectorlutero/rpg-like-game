class AttributePackage:
    @staticmethod
    def calculate_base(base_value, level, gain_rate, multiplier):
        """Calculates the base value before equipment bonuses."""
        return int((base_value + (level * gain_rate)) * multiplier)

class StatsCalculator:
    @staticmethod
    def get_proficiency_multiplier(equipment_item, char_class):
        """Calculates the highest proficiency multiplier for an item based on its tags."""
        if not equipment_item:
            return 1.0
        
        prof_mult = 1.0
        tags = getattr(equipment_item, 'tags', [])
        for tag in tags:
            if tag in char_class.proficiencies:
                prof_mult = max(prof_mult, char_class.proficiencies[tag])
        return prof_mult

    @staticmethod
    def calculate_final(name, base_stats, char_class, level, equipment):
        """Calculates the final attribute value including all bonuses and proficiencies."""
        base_value = base_stats.get(name, 0)
        multiplier = char_class.multipliers.get(name, 1.0)
        gain_rate = char_class.gain_rates.get(name, 0.0)
        
        final_base = AttributePackage.calculate_base(base_value, level, gain_rate, multiplier)
        
        total_flat_bonus = 0
        total_percent_bonus = 0.0
        
        for eq in equipment.values():
            if not eq: continue
            
            prof_mult = StatsCalculator.get_proficiency_multiplier(eq, char_class)
            
            # Flat Bonuses
            flat = eq.bonuses.get(name, 0)
            total_flat_bonus += int(flat * prof_mult)
            
            # Percentage Bonuses
            perc = getattr(eq, 'percent_bonuses', {}).get(name, 0.0)
            total_percent_bonus += (perc * prof_mult)

        return int((final_base + total_flat_bonus) * (1.0 + total_percent_bonus))

    @staticmethod
    def calculate_defense(equipment, char_class, mode='absolute'):
        """Calculates absolute or relative defense from equipment."""
        total = 0.0
        attr_key = 'defesa_absoluta' if mode == 'absolute' else 'defesa_relativa'
        
        for eq in equipment.values():
            if not eq: continue
            
            prof_mult = StatsCalculator.get_proficiency_multiplier(eq, char_class)
            val = eq.bonuses.get(attr_key, 0.0)
            total += (val * prof_mult)
            
        if mode == 'absolute':
            return int(total)
        return min(0.9, total) # Cap relative defense at 90%
