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
