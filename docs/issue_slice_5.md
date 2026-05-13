## Parent
#37

## What to build
Extend the `MapAPI` and `DirectorEngine` to support entity movement (`move_to`) and combat hooks. This allows scripts to orchestrate cutscenes where NPCs move and trigger specific narrative events during combat.

## Acceptance criteria
- [ ] `MapAPI.move_to` handles non-blocking entity movement across frames.
- [ ] Combat hooks allow a script to intervene in a `CombatManager` session based on HP thresholds.
- [ ] E2E test shows an NPC moving to a point and starting a dialogue.

## Blocked by
#41
