class DifficultyManager:
    EASY = "Fácil"
    NORMAL = "Normal"
    HARD = "Difícil"

    MULTIPLIERS = {
        EASY: {
            "hp": 0.8,
            "attack": 0.8,
            "agility": 0.8,
            "rewards": 1.2
        },
        NORMAL: {
            "hp": 1.0,
            "attack": 1.0,
            "agility": 1.0,
            "rewards": 1.0
        },
        HARD: {
            "hp": 1.5,
            "attack": 1.3,
            "agility": 1.2,
            "rewards": 0.8
        }
    }

    def __init__(self, difficulty=NORMAL):
        self.difficulty = difficulty

    def get_multiplier(self, stat):
        return self.MULTIPLIERS.get(self.difficulty, self.MULTIPLIERS[self.NORMAL]).get(stat, 1.0)

    def apply_scaling(self, enemy):
        """Applies stat scaling to an enemy Character using temporary modifiers."""
        from src.models.stats import Modifier, ModifierType
        
        hp_mult = self.get_multiplier("hp")
        if hp_mult != 1.0:
            enemy.add_temporary_modifier("vida", Modifier(hp_mult, ModifierType.PERCENT, source="Difficulty"))
            # Recalculate current HP if it's already set to max
            enemy.hp = enemy.max_hp

        atk_mult = self.get_multiplier("attack")
        if atk_mult != 1.0:
            enemy.add_temporary_modifier("forca", Modifier(atk_mult, ModifierType.PERCENT, source="Difficulty"))

        agi_mult = self.get_multiplier("agility")
        if agi_mult != 1.0:
            enemy.add_temporary_modifier("agilidade", Modifier(agi_mult, ModifierType.PERCENT, source="Difficulty"))

    def scale_rewards(self, amount):
        """Scales gold or XP rewards."""
        return int(amount * self.get_multiplier("rewards"))
