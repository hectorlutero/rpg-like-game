class Item:
    def __init__(self, name, description, price=0, category="Consumable"):
        self.name = name
        self.description = description
        self.price = price
        self.category = category

class Equipment(Item):
    def __init__(self, name, description, slot, bonuses=None, req_stats=None, req_class=None, price=0, percent_bonuses=None, tags=None):
        super().__init__(name, description, price, category="Equipment")
        self.slot = slot # "weapon", "shield", "armor", "accessory"
        self.bonuses = bonuses or {} # {'forca': 5, 'defesa_absoluta': 2}
        self.percent_bonuses = percent_bonuses or {} # {'vida': 0.10}
        self.tags = tags or [] # ["sword", "heavy_armor"]
        self.req_stats = req_stats or {} # {'forca': 10}
        self.req_class = req_class # "Warrior"

# Equipment Registry
class Consumable(Item):
    def __init__(self, name, description, effect, price=0):
        super().__init__(name, description, price, category="Consumable")
        self.effect = effect # {'hp': 50, 'mana': 20}

# Registries
CONSUMABLE_DATA = {
    "Poção de Vida": Consumable("Poção de Vida", "Restaura 50 de HP.", {'hp': 50}, price=20),
    "Poção de Mana": Consumable("Poção de Mana", "Restaura 30 de Mana.", {'mana': 30}, price=30),
    "Antídoto": Consumable("Antídoto", "Cura o efeito de Veneno.", {'cure': 'poison'}, price=40),
    "Remédio Estimulante": Consumable("Remédio Estimulante", "Cura o efeito de Paralisia.", {'cure': 'paralysis'}, price=50)
}

EQUIPMENT_DATA = {
    "Espada de Ferro": Equipment(
        "Espada de Ferro", "Uma espada robusta de ferro.", 
        slot="weapon", bonuses={'forca': 5}, req_stats={'forca': 8}, price=50, tags=["sword"]
    ),
    "Escudo de Madeira": Equipment(
        "Escudo de Madeira", "Proteção básica contra ataques.", 
        slot="shield", bonuses={'defesa_absoluta': 3}, req_stats={'forca': 5}, price=30, tags=["shield"]
    ),
    "Armadura de Couro": Equipment(
        "Armadura de Couro", "Leve e resistente.", 
        slot="armor", bonuses={'vida': 20, 'defesa_absoluta': 1}, price=40, tags=["leather_armor"]
    ),
    "Armadura de Placas": Equipment(
        "Armadura de Placas", "Pesada e impenetrável.",
        slot="armor", bonuses={'vida': 50, 'defesa_absoluta': 5}, price=150, tags=["heavy_armor"], req_stats={'forca': 15}
    ),
    "Cajado de Aprendiz": Equipment(
        "Cajado de Aprendiz", "Foca energia mágica.",
        slot="weapon", bonuses={'inteligencia': 8}, price=60, tags=["staff"]
    ),
    "Anel de Inteligência": Equipment(
        "Anel de Inteligência", "Aumenta a compreensão mágica.", 
        slot="accessory", bonuses={'inteligencia': 5}, price=100
    ),
    "Anel Anti-Veneno": Equipment(
        "Anel Anti-Veneno", "Protege 100% contra veneno.",
        slot="accessory", bonuses={}, price=150
    ),
    "Anel de Resistência": Equipment(
        "Anel de Resistência", "Aumenta 50% de resistência a tudo.",
        slot="accessory", bonuses={}, price=200
    )
}

# Update items with resistances
EQUIPMENT_DATA["Anel Anti-Veneno"].resistances = {'poison': 1.0}
EQUIPMENT_DATA["Anel de Resistência"].resistances = {'poison': 0.5, 'paralysis': 0.5}
