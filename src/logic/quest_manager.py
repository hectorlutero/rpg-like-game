import json
import os

class QuestManager:
    def __init__(self, global_state, signal_bus):
        self.global_state = global_state
        self.signal_bus = signal_bus
        self.quests = {}
        self.director = None # Injected later
        self.game_context = None # Injected later

    def load_quests(self, path):
        if not os.path.exists(path):
            return
        with open(path, 'r', encoding='utf-8') as f:
            self.quests = json.load(f)

    def accept_quest(self, quest_id):
        if quest_id not in self.quests:
            return
        
        if self.global_state:
            self.global_state.quests[quest_id] = {
                "stage": 0,
                "status": "IN_PROGRESS"
            }

    def on_event(self, event_data):
        if not self.global_state:
            return
            
        for qid, state in self.global_state.quests.items():
            if state["status"] != "IN_PROGRESS":
                continue
                
            quest_def = self.quests.get(qid)
            if not quest_def:
                continue
                
            current_stage_idx = state["stage"]
            stages = quest_def.get("stages", [])
            
            if current_stage_idx >= len(stages):
                continue
                
            current_stage = stages[current_stage_idx]
            objectives_data = current_stage.get("objectives", [])
            
            from src.logic.quest_objectives import EventObjective
            
            # Instantiate objectives
            objectives = []
            for obj_data in objectives_data:
                # In the future, we could have an ObjectiveFactory based on obj_data
                objectives.append(EventObjective(obj_data.get("type"), obj_data.get("target")))
            
            # Check if event matches any objective
            match = False
            for obj in objectives:
                if obj.is_fulfilled(event_data, state):
                    match = True
                    break
            
            if match:
                self._advance_quest(qid, quest_def)

    def _advance_quest(self, qid, quest_def):
        state = self.global_state.quests[qid]
        current_stage_idx = state["stage"]
        stages = quest_def.get("stages", [])
        
        current_stage = stages[current_stage_idx]
        
        # Build execution context for actions
        action_context = {
            "director": self.director,
            "global_state": self.global_state,
            "signal_bus": self.signal_bus,
            "game_context": self.game_context
        }
        
        # New action system
        actions_data = current_stage.get("actions", [])
        
        # Backward compatibility for old JSON format
        reward_script = current_stage.get("reward_script")
        if reward_script:
            actions_data.append({"type": "RUN_SCRIPT", "script": reward_script})

        from src.logic.quest_actions import RunScriptAction, GiveItemAction, GiveXPAction
        for act_data in actions_data:
            action = None
            if act_data.get("type") == "RUN_SCRIPT":
                action = RunScriptAction(act_data.get("script"))
            elif act_data.get("type") == "GIVE_ITEM":
                action = GiveItemAction(act_data.get("item"))
            elif act_data.get("type") == "GIVE_XP":
                action = GiveXPAction(act_data.get("amount"))
                
            if action:
                action.execute(action_context)
            
        # Advance to next stage or complete
        if current_stage_idx + 1 < len(stages):
            state["stage"] += 1
            if self.signal_bus:
                next_stage = stages[state["stage"]]
                self.signal_bus.emit("QUEST_UPDATED", 
                                    name=quest_def.get("name"), 
                                    description=next_stage.get("description"))
        else:
            state["status"] = "COMPLETED"
            if self.signal_bus:
                self.signal_bus.emit("QUEST_COMPLETED", name=quest_def.get("name"))

    def get_active_quests(self):
        if not self.global_state:
            return []
        return [qid for qid, s in self.global_state.quests.items() if s["status"] == "IN_PROGRESS"]

    def get_quest_stage(self, quest_id):
        if not self.global_state or quest_id not in self.global_state.quests:
            return -1
        return self.global_state.quests[quest_id].get("stage", -1)

    def is_completed(self, quest_id):
        if not self.global_state or quest_id not in self.global_state.quests:
            return False
        return self.global_state.quests[quest_id].get("status") == "COMPLETED"
