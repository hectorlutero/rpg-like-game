## Parent
#37

## What to build
Implement safety features for the engine, including a save-block mechanism while scripts are active. Add a "Tag-based" entry point system for robust teleportation between maps.

## Acceptance criteria
- [ ] `SaveManager` denies saving if `DirectorEngine.is_busy` is True.
- [ ] Map transitions use string tags (e.g., "village_entrance") instead of raw coordinates.
- [ ] Final integration refactor cleans up `main.py`, leaving it as a thin entry point.

## Blocked by
#42
