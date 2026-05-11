class Skill:
    def __init__(self, name, int_threshold, mana_cost=0, power=1.0, skill_type="physical"):
        self.name = name
        self.int_threshold = int_threshold
        self.mana_cost = mana_cost
        self.power = power
        self.skill_type = skill_type

class SkillRegistry:
    def __init__(self):
        self.skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def get_available_skills(self, character):
        char_int = character.get_attribute('inteligencia')
        return [s for s in self.skills if char_int >= s.int_threshold]
        # In the future, add class-specific checks here
