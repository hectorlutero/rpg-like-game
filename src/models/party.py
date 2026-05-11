class Party:
    MAX_SIZE = 4

    def __init__(self):
        self.members = []

    def add_member(self, character):
        if len(self.members) < self.MAX_SIZE:
            self.members.append(character)
            return True
        return False

    def gain_xp(self, total_amount):
        if not self.members:
            return
        
        amount_per_member = total_amount // len(self.members)
        for member in self.members:
            member.gain_xp(amount_per_member)
