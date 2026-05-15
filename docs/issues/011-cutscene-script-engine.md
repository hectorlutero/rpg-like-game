## Parent
[Milestone 6 - Game Flow & Final Polish](../prd_milestone_6.md)

## What to build
Develop a script-based engine to execute narrative sequences (cutscenes). The engine will read JSON files defining a timeline of events like entity movement, camera pans, and dialogue.

## Acceptance criteria
- [ ] Parser for Cutscene JSON format supporting: `move`, `wait`, `dialogue`, `animate`, `sound`, `camera`.
- [ ] Integration with `ExplorationScene` to trigger sequences based on triggers or map entry.
- [ ] Automated locking of player input during cutscene execution via `GameContext`.
- [ ] Integration test verifying a simple 3-step sequence completes and returns control to the player.

## Blocked by
- [008-input-centralization-presets.md](008-input-centralization-presets.md)
