## Parent
[Milestone 6 - Game Flow & Final Polish](../prd_milestone_6.md)

## What to build
Extend the `SaveManager` to support multiple save slots (e.g., 3-5 slots) instead of a single `savegame.json`. Each save file must include metadata like character level, play time, and timestamp for display in the UI.

## Acceptance criteria
- [ ] `SaveManager` can list, save, and load from specific slots (e.g., `save_1.json`, `save_2.json`).
- [ ] Save files contain a `metadata` block with `hero_level`, `play_time`, `timestamp`, and `location`.
- [ ] Logic for calculating `play_time` (accumulated seconds) implemented in `GameContext`.
- [ ] Unit tests for multi-slot persistence and metadata integrity.

## Blocked by
None - can start immediately
