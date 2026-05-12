class Ability:
    """Base class for Skills and Spells."""
    def __init__(self, name, power, category="Skill", element=None, int_req=0, level_req=1, mana_cost=0):
        self.name = name
        self.power = power
        self.category = category # "Skill" or "Spell"
        self.element = element
        self.int_req = int_req
        self.level_req = level_req
        self.mana_cost = mana_cost

# Registry
ABILITY_DATA = {
    # Habilidades Físicas (Skills) - Sem custo de Mana
    "Corte Rápido": Ability("Corte Rápido", power=1.5, category="Skill", int_req=5),
    "Impacto Pesado": Ability("Impacto Pesado", power=2.2, category="Skill", int_req=12),
    
    # Feitiços (Spells) - Com custo de Mana
    "Bola de Fogo": Ability("Bola de Fogo", power=2.0, category="Spell", element="Fire", int_req=10, mana_cost=10),
    "Lança de Gelo": Ability("Lança de Gelo", power=1.8, category="Spell", element="Ice", int_req=15, mana_cost=8),
    "Trovão": Ability("Trovão", power=2.5, category="Spell", element="Lightning", int_req=20, mana_cost=15)
}
