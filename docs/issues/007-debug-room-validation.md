## What to build

Create a dedicated "Debug Room" map that utilizes all the newly implemented visual systems for final validation.

- Create a `debug_room.json` map with a specific tileset.
- Populate the room with NPCs, Obstacles (with sub-tile hitboxes), and a combat trigger.
- Use this room to verify Y-sorting, Animations, and Particles in a single scene.

## Acceptance criteria

- [ ] Visual verification of Y-sorting with multiple entities.
- [ ] Verification of sub-tile collision against diverse obstacles.
- [ ] Verification of combat-to-exploration transition with active particles.

## Blocked by

- All Milestone 5 issues (001 to 006).
