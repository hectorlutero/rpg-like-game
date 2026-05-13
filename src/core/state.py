class GlobalState:
    def __init__(self, flags=None, deltas=None):
        self.flags = flags or {}
        self.deltas = deltas or {} # {entity_id: {attr: value}}

    def set_flag(self, key, value):
        self.flags[key] = value

    def get_flag(self, key, default=False):
        return self.flags.get(key, default)

    def set_entity_delta(self, entity_id, data):
        if entity_id not in self.deltas:
            self.deltas[entity_id] = {}
        self.deltas[entity_id].update(data)

    def get_entity_delta(self, entity_id):
        return self.deltas.get(entity_id, {})

    def to_dict(self):
        return {
            "flags": self.flags,
            "deltas": self.deltas
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            flags=data.get("flags", {}),
            deltas=data.get("deltas", {})
        )
