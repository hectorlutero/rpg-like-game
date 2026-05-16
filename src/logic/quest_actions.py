class QuestAction:
    """Base interface for all quest actions/rewards."""
    def execute(self, context):
        raise NotImplementedError()

class RunScriptAction(QuestAction):
    """Executes a script via the DirectorEngine."""
    def __init__(self, script_name):
        self.script_name = script_name

    def execute(self, context):
        director = context.get("director")
        if director:
            director.run_script(self.script_name)

class GiveItemAction(QuestAction):
    """Gives an item directly to the player."""
    def __init__(self, item_name):
        self.item_name = item_name

    def execute(self, context):
        game_context = context.get("game_context")
        signal_bus = context.get("signal_bus")
        if game_context and game_context.player:
            game_context.player.receive_item(self.item_name, signal_bus)

class GiveXPAction(QuestAction):
    """Grants XP directly to the player."""
    def __init__(self, amount):
        self.amount = amount

    def execute(self, context):
        game_context = context.get("game_context")
        if game_context and game_context.player:
            game_context.player.gain_xp(self.amount)

class RollCreditsAction(QuestAction):
    """Triggers the credits scene."""
    def execute(self, context):
        sm = context.get("scene_manager")
        if sm:
            from src.ui.credits_scene import CreditsScene
            sm.push(CreditsScene(sm))

class GameOverAction(QuestAction):
    """Triggers the game over scene."""
    def execute(self, context):
        sm = context.get("scene_manager")
        if sm:
            from src.ui.game_over_scene import GameOverScene
            sm.push(GameOverScene(sm))

