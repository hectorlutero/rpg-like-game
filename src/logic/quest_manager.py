import json
import os

class QuestManager:
    def __init__(self, global_state, signal_bus):
        self.global_state = global_state
        self.signal_bus = signal_bus
        self.quests = {}
        self.director = None # Injected later

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
            objectives = current_stage.get("objectives", [])
            
            # Check if event matches any objective
            match = False
            for obj in objectives:
                if obj["type"] == event_data.get("type") and obj["target"] == event_data.get("target"):
                    match = True
                    break
            
            if match:
                self._advance_quest(qid, quest_def)

    def _advance_quest(self, qid, quest_def):
        state = self.global_state.quests[qid]
        current_stage_idx = state["stage"]
        stages = quest_def.get("stages", [])
        
        # Trigger reward script if exists for this stage
        current_stage = stages[current_stage_idx]
        reward_script = current_stage.get("reward_script")
        if reward_script and self.director:
            self.director.run_script(reward_script)
            
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
