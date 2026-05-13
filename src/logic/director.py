class MapAPI:
    def __init__(self, context):
        self.context = context

    def set_flag(self, key, value):
        self.context.global_state.set_flag(key, value)

    def get_flag(self, key, default=False):
        return self.context.global_state.get_flag(key, default)

    def say(self, text):
        """Triggers a dialogue overlay."""
        # This will be integrated with the InteractionManager/Renderer later
        # For now it's a yield point
        return ("say", text)

    def give_item(self, item_name):
        self.context.player.inventory.add_item(item_name)
        return ("give_item", item_name)

class DirectorEngine:
    def __init__(self, context, api):
        self.context = context
        self.api = api
        self.active_script = None

    def start_script(self, script_gen):
        self.active_script = script_gen
        self.advance()

    def advance(self, signal=None):
        if not self.active_script:
            return
            
        try:
            # Advance the generator
            result = self.active_script.send(signal)
            # result can be used for more complex wait logic (timers, etc.)
        except StopIteration:
            self.active_script = None

    def is_busy(self):
        return self.active_script is not None
