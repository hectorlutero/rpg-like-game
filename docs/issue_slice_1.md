## Parent
#37

## What to build
Implement a centralized `EntityRegistry` that loads entity "prefabs" from a `data/entities.json` file. Entities will be defined as a set of capabilities/components (LEGO-style). The system must allow spawning entities into the game world by referencing their IDs in the registry.

## Acceptance criteria
- [x] `data/entities.json` exists with a schema for at least Chests and NPCs.
- [x] `src/core/registry.py` can load the JSON and instantiate the correct `Interactable` subclasses.
- [x] Unit tests verify that an entity created from the registry has the correct initial state and components.

## Blocked by
None - can start immediately
