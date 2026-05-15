## What to build

Implement a dynamic rendering order system where entities with a higher Y-coordinate are drawn on top of those with a lower Y-coordinate. This creates a 2.5D depth illusion.

- Update `ExplorationScene` and `CombatScene` to collect all renderable entities (Player, NPCs, Interactables) into a single list.
- Sort this list by the `y` coordinate (specifically the base/feet of the entity) before drawing.
- Ensure the floor tiles are always drawn first (at the bottom layer).

## Acceptance criteria

- [ ] Entities correctly overlap each other based on their vertical position.
- [ ] Moving the Player from behind to in front of an NPC results in a correct visual swap.
- [ ] Sorting logic is optimized to avoid performance hits with large numbers of entities.

## Blocked by

- docs/issues/001-asset-manager-infrastructure.md
- docs/issues/002-test-integrity-fallback.md
