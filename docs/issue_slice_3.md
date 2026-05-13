## Parent
#37

## What to build
Implement a `GlobalState` system that tracks persistent changes to the world via "Deltas". When a map is loaded, the orchestrator must apply these deltas (e.g., if a chest was previously opened). Update the `SaveManager` to persist these deltas to JSON.

## Acceptance criteria
- [ ] `src/core/state.py` manages a dictionary of flags and entity state overrides.
- [ ] `WorldOrchestrator` applies deltas during map initialization.
- [ ] Save/Load cycle preserves the state of opened chests and NPC interactions.

## Blocked by
#39
