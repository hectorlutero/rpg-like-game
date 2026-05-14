# Issue: Visual Juice: Screen Shake & Flash

## Parent
PRD: docs/prd_audio_immersion.md

## What to build
Add visual feedback mechanisms to the `ExplorationScene` (and potentially others) to give actions more impact.

- Implement a `Camera` offset logic in the renderer.
- Add a "Trauma" system: events add trauma (0.0 to 1.0), which generates random screen shake and decays over time.
- Implement a "Screen Flash" overlay that can be triggered in different colors (red for damage, white for healing).
- Listen to signals like `ENTITY_DAMAGED` to trigger these effects.

## Acceptance criteria
- [ ] Screen shakes randomly when a high-trauma signal is received.
- [ ] Screen flashes red when the player takes damage.
- [ ] Visual effects do not interfere with UI or collision logic (they are purely cosmetic).
- [ ] Effects decay smoothly and don't persist indefinitely.

## Blocked by
None - can start immediately.
