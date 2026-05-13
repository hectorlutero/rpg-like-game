## Problem Statement
The current project structure relies on manual configuration in `main.py` for world setup, entity placement, and interaction logic. This creates a high configuration burden, makes the code hard to scale, and complicates the creation of complex narrative sequences and multi-map exploration.

## Solution
Implement a data-driven Engine and Scripting System. This involves a centralized Entity Registry for defining "prefabs", a World Orchestrator for loading hierarchical maps from JSON, a Director Engine for executing Python-based area scripts with non-blocking logic (`yield`), and a Global State system that tracks changes via "Deltas".

## User Stories
1. As a player, I want to explore different maps (World, Cities, Houses) so that the game feels like a vast adventure.
2. As a player, I want the world to remember my actions (opened chests, talked NPCs) so that my progress is consistent.
3. As a player, I want NPCs and world objects to react to my progress in the story, so that the narrative feels alive.
4. As a player, I want to experience scripted events (cutscenes, boss transitions) without the game freezing or crashing.
5. As a player, I want my game to save safely, ensuring that I don't lose progress or end up in a broken state during a scene.
6. As a designer, I want to define maps and entities in JSON files, so that I can build the world without writing Python code for every placement.
7. As a designer, I want to write complex logic in Python scripts for specific areas, so that I have full power over the game's narrative.

## Implementation Decisions
- **Entity Registry**: Centralized catalog of entity definitions (prefabs) in JSON.
- **World Orchestrator**: Loads maps from JSON and applies "Deltas" from the Global State.
- **Director Engine**: Executes Python scripts with `yield` for asynchronous-like behavior.
- **Global State**: Manages persistent flags and entity state changes (Deltas).
- **Save Protection**: Disables saving while the Director Engine is executing a script.
- **Area Scripts**: Separate Python modules for each map/area to maintain locality.
- **MapAPI**: A simplified interface for scripts to interact with the engine safely.
- **Entry Points**: Tag-based teleportation system for reliable map transitions.

## Testing Decisions
- **Unit Tests**: Test the Registry loading, State Delta application, and MapAPI commands.
- **Integration Tests**: Verify map loading and entity spawning.
- **E2E Tests**: Use `UITester` to verify complete scripted sequences and save-blocking behavior.

## Out of Scope
- Database-backed persistence (keeping it as JSON for now).
- Visual scripting editor (scripts are hand-written).
- Complex multi-entity pathfinding (beyond basic move-to).
