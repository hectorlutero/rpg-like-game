import random

class StatusManager:
    @staticmethod
    def calculate_chance(attacker, defender, base_chance, status_type):
        """Calculates final chance considering INT and equipment resistance."""
        atk_int = attacker.get_attribute('inteligencia')
        def_int = defender.get_attribute('inteligencia')
        
        # Base logic: base_chance + INT difference
        chance = base_chance + (atk_int - def_int)
        
        # Equipment Resistance
        resistance = 0.0
        for eq in defender.equipment.values():
            if eq and hasattr(eq, 'resistances'):
                resistance += eq.resistances.get(status_type, 0.0)
        
        final_chance = chance * (1.0 - resistance)
        return max(0, min(100, int(final_chance)))

    @staticmethod
    def apply_status(attacker, defender, status_type, base_chance, duration, potency=0):
        """Attempts to apply a status effect to the defender."""
        chance = StatusManager.calculate_chance(attacker, defender, base_chance, status_type)
        
        if random.randint(1, 100) <= chance:
            defender.status_effects[status_type] = {
                'duration': duration,
                'potency': potency
            }
            return True, f"{defender.name} foi afetado por {status_type.capitalize()}!"
        return False, f"{defender.name} resistiu a {status_type.capitalize()}."

    @staticmethod
    def process_tick(entity):
        """Processes status effect ticks at the start of a turn. Returns a list of logs."""
        logs = []
        expired = []
        
        for status, data in entity.status_effects.items():
            if status == 'poison':
                damage = data['potency']
                entity.hp -= damage
                logs.append(f"{entity.name} sofreu {damage} de dano por Veneno!")
            
            # Reduce duration
            data['duration'] -= 1
            if data['duration'] <= 0:
                expired.append(status)
        
        for status in expired:
            del entity.status_effects[status]
            logs.append(f"O efeito de {status.capitalize()} em {entity.name} acabou.")
            
        return logs

    @staticmethod
    def is_paralyzed(entity):
        return 'paralysis' in entity.status_effects
