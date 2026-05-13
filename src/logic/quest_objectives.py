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

class CountableObjective(QuestObjective):
    """Objective fulfilled after a matching event happens a certain number of times."""
    def __init__(self, obj_type, target, count, progress_key):
        self.obj_type = obj_type
        self.target = target
        self.count = count
        self.progress_key = progress_key

    def is_fulfilled(self, event_data, state):
        if self.obj_type == event_data.get("type") and self.target == event_data.get("target"):
            if "progress" not in state:
                state["progress"] = {}
            current = state["progress"].get(self.progress_key, 0)
            current += 1
            state["progress"][self.progress_key] = current
            return current >= self.count
        return False
