class QuestObjective:
    """Base interface for all quest objectives."""
    def is_fulfilled(self, event_data, state):
        raise NotImplementedError()

class EventObjective(QuestObjective):
    """Objective fulfilled by a matching event type and target."""
    def __init__(self, obj_type, target):
        self.obj_type = obj_type
        self.target = target

    def is_fulfilled(self, event_data, state):
        return self.obj_type == event_data.get("type") and self.target == event_data.get("target")
