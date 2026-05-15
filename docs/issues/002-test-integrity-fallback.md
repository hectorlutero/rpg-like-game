## What to build

Implement a "Graceful Degradation" strategy to ensure the game engine remains fully functional even when visual assets are missing. This is critical for maintaining the integrity of existing logic tests.

- Implement a fallback rendering system (Headless/Debug mode) that uses colored rectangles (as current) when a sprite is missing or when running in a test environment.
- Modify `ExplorationScene` and `CombatScene` to use the `AssetManager` with this fallback logic.
- Ensure all existing tests in `tests/` pass 100% after integrating the new asset infrastructure.

## Acceptance criteria

- [ ] Existing logic tests (`pytest tests/`) pass with zero regressions.
- [ ] If a SpriteSheet is missing, the game renders a placeholder rectangle instead of crashing.
- [ ] A new test case verifies that the engine can initialize and run logic in a "Headless" state (no display/no assets).

## Blocked by

- docs/issues/001-asset-manager-infrastructure.md
