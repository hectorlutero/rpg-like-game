## What to build

Design and implement a flexible animation system for sprites, supporting multiple states (idle, walking, attacking).

- **MANDATORY**: Start with a `grill-me` session to define the animation state machine and metadata structure.
- Implement an `AnimationController` that updates the current frame based on time and entity state.
- Support frame-based animation defined in the Sprite Metadata JSON.

## Acceptance criteria

- [ ] Successful completion of the "Animation System Grill".
- [ ] Entities transition smoothly between animation states (e.g., Idle -> Walk).
- [ ] Animation speed is independent of the game's frame rate (uses `dt`).

## Blocked by

- docs/issues/001-asset-manager-infrastructure.md
- docs/issues/002-test-integrity-fallback.md
