import math

class MapAPI:
    def __init__(self, context):
        self.context = context

    def set_flag(self, key, value):
        self.context.global_state.set_flag(key, value)

    def get_flag(self, key, default=False):
        return self.context.global_state.get_flag(key, default)

    def say(self, text):
        """Triggers a dialogue overlay."""
        return ("say", text)

    def give_item(self, item_name):
        self.context.player.receive_item(item_name, self.context.signal_bus)
        return ("give_item", item_name)

    def move_to(self, entity, target_pos, speed=2):
        """Triggers non-blocking movement for an entity."""
        return ("move_to", entity, target_pos, speed)

class DirectorEngine:
    def __init__(self, context, api):
        self.context = context
        self.api = api
        self.active_script = None
        self.current_action = None
        self.combat_manager = None

    def start_script(self, script_gen):
        self.active_script = script_gen
        self.advance()

    def run_script(self, script_name):
        """Runs a named script if registered (placeholder)."""
        print(f"DirectorEngine: Running script {script_name} (Not fully implemented)")
        # In the future, this will look up the script in a registry
        # For now, we can use it to trigger specific hardcoded behaviors or just log.
        pass

    def advance(self, signal=None):
        if not self.active_script:
            return
            
        try:
            self.current_action = self.active_script.send(signal)
        except StopIteration:
            self.active_script = None
            self.current_action = None

    def update(self, dt):
        """Processes time-based actions (like movement)."""
        # Auto-check combat hooks if in combat
        if self.combat_manager:
            self.check_combat_hooks()

        if not self.current_action:
            return

        action_type = self.current_action[0]
        if action_type == "move_to":
            _, entity, target_pos, speed = self.current_action
            
            dx = target_pos.x - entity.position.x
            dy = target_pos.y - entity.position.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist <= speed * dt:
                entity.position.x = target_pos.x
                entity.position.y = target_pos.y
                self.advance() # Action finished
            else:
                ratio = (speed * dt) / dist
                entity.position.x += dx * ratio
                entity.position.y += dy * ratio

    def attach_combat(self, combat_manager):
        self.combat_manager = combat_manager

    def check_combat_hooks(self):
        if not self.current_action or self.current_action[0] != "combat_hook":
            return
            
        _, hook_type, threshold = self.current_action
        
        if hook_type == "enemy_hp":
            # Check if any enemy is below threshold (pct or absolute?)
            # Let's assume absolute for now
            for enemy in self.combat_manager.enemies:
                if enemy.hp <= threshold:
                    self.advance("threshold_met")
                    break

    def is_busy(self):
        return self.active_script is not None
