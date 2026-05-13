## Parent
#37

## What to build
Implement the `WorldOrchestrator` which loads hierarchical map data from JSON files. The orchestrator will use the `EntityRegistry` to populate the map with the correct entities at their defined coordinates.

## Acceptance criteria
- [ ] `data/maps/vila_inicial.json` exists with a layout of tiles and entity placements.
- [ ] `src/core/orchestrator.py` can parse map JSONs and populate a `World` object.
- [ ] Integration test verifies that a map loaded from JSON contains the expected entities at the correct tile positions.

## Blocked by
#38
