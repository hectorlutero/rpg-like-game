## What to build

Transition from rigid, grid-based collision to a more organic sub-tile system using custom hitboxes defined in sprite metadata.

- Update the movement logic in `World` and `Character` to check for collisions using Rectangles (hitboxes) instead of integer grid coordinates.
- Integrate hitbox data (offsets and dimensions) from the Sprite Metadata JSON.
- Refactor existing movement and collision tests to use these new precision checks.

## Acceptance criteria

- [ ] Player can walk "behind" a tall sprite (like a tree) and only collide with its base (trunk).
- [ ] Collision is checked against entity hitboxes, not just tile boundaries.
- [ ] Existing movement tests are updated and pass with the new hitbox logic.

## Blocked by

- docs/issues/001-asset-manager-infrastructure.md
- docs/issues/002-test-integrity-fallback.md
