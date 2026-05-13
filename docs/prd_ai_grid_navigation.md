# Product Requirements Document (PRD) - Milestone 3: AI & Grid Navigation

## Problem Statement

Currently, the RPG world is static. NPCs and enemies exist in the world as interactables, but they cannot move or navigate the grid on their own. To create a living, breathing classic RPG experience (Milestone 3), entities must be able to move intelligently across the grid without overlapping, pursue the player when spotted, and navigate around obstacles, all while adhering to the strict tile-based movement system and maintaining high performance. Furthermore, gameplay rules regarding enemy encounters on the map, aggro management, and respawn mechanics must be defined.

## Solution

Implement a robust Grid Navigation and AI system. This will be built upon an A* pathfinding algorithm that is tightly integrated with the existing `GameContext` and `World` state. To ensure performance, pathfinding will be dynamic but constrained: enemies will only recalculate their routes when the player is within Line-of-Sight (LoS) and will cache their paths. 

To maintain grid integrity and prevent entities from overlapping or getting stuck, the system will use an "Immediate Tile Claiming" strategy, where an entity reserves its destination tile in the `world.interactables` registry before its visual movement animation finishes.

Gameplay mechanics will be strictly classical: simple contact initiates combat without positional advantage, enemies use a "Leash Distance" to drop aggro and return to spawn, and enemies respawn upon map reloading.

## User Stories

1. As a player, I want NPCs in towns to wander around randomly or on set paths, so that the world feels alive.
2. As a player, I want enemy encounters on the map to start moving towards me if I get too close (Line-of-Sight), so that I have to think tactically about positioning and avoidance.
3. As a player, I want enemies pursuing me to navigate around rocks, trees, and other obstacles instead of just getting stuck on them, so that they feel like a genuine threat.
4. As a player, I want to see enemies occasionally pause or hesitate while pursuing me, so that I have a chance to outmaneuver them (A* cooldown/cache).
5. As a player, I want to ensure that if an enemy and an NPC try to walk into the same space, they don't clip into each other or merge together, so that the game's physical rules remain consistent.
6. As a developer, I want the pathfinding algorithm to only run when necessary (LoS triggered), so that the game doesn't drop frames even if there are dozens of entities on a large map.
7. As a developer, I want the tile reservation system to instantly update the map's state the moment an entity commits to moving, so that no two pathfinders can claim the same tile simultaneously.
8. As a developer, I want a deep, decoupled pathfinding module that can be unit-tested purely mathematically, without needing Pygame's rendering loop.
9. As a player, I want combat to initiate immediately and fairly when I collide with an enemy on the map.
10. As a player, I want enemies to stop chasing me if I run far enough away (Leashing), returning to their original posts so I can escape danger.
11. As a player, I want defeated enemies to disappear from the map, but respawn if I leave the area and come back, allowing me to grind for XP.

## Implementation Decisions

- **Deep Module - PathfindingEngine:** A purely mathematical A* implementation decoupled from Pygame. It will take a grid state, start, and end coordinates, and return a list of steps. It will respect impassable tiles and currently claimed interactable tiles.
- **Deep Module - AIController:** A strategy pattern for entity behaviors. Includes:
  - `StaticBehavior`: Stands still or turns.
  - `RandomWanderBehavior`: Picks an adjacent valid tile occasionally.
  - `PursuitBehavior`: Uses the `PathfindingEngine` to track the player. Implements the Line-of-Sight distance check and the path recalculation cooldown (e.g., walk 3 steps of the cached path before running A* again).
- **Gameplay AI Rules:**
  - **Engagement:** Simple contact. If player moves into enemy tile, or enemy moves into player tile, trigger `CombatScene`. No positional advantages (Back-attack).
  - **Leashing:** `PursuitBehavior` tracks a distance from the enemy's original spawn point or player distance. If the player exceeds the "Leash Radius" (e.g., 8 tiles), the enemy transitions back to a `ReturnToSpawnBehavior` until it reaches home.
  - **Respawn:** Defeated enemies are popped from the `world.interactables` dictionary upon combat victory. They are NOT saved in persistent state, so reloading the map from JSON restores them naturally.
- **Immediate Tile Claiming Logic:**
  - Modified movement execution within `entities/interactables`. When an entity decides to move from `(x, y)` to `(x+1, y)`, it immediately updates its key in the `world.interactables` dictionary to `(x+1, y)`, even while its `visual_offset` is animating.
  - If a collision occurs (tile already claimed or impassable map tile), the movement is rejected and the entity stays at `(x,y)`.
- **Line-of-Sight (LoS):** A simple Manhattan or Euclidean distance check combined with a raycast (Bresenham's line algorithm) to ensure no walls are blocking the view before triggering the `PursuitBehavior`.
- **Integration:** The `WorldOrchestrator` (or `DirectorEngine`) will have an `update_ai(dt)` phase that ticks all active AI controllers.

## Testing Decisions

- **Pathfinding Unit Tests:** 
  - Provide 2D arrays representing maps with walls.
  - Test straight paths, paths around U-shaped walls, and unreachable destinations (should fail gracefully).
- **Line-of-Sight Unit Tests:**
  - Test clear LoS, LoS blocked by a wall, and distance limits.
- **Tile Claiming Integration Tests:**
  - Two mock NPCs instructed to move to the exact same tile at the same time. The test must assert that one succeeds and the other fails, and the dictionary only has one occupant at that tile.
- **Pursuit AI & Leashing Integration Tests:**
  - Assert that an AI does not move if the player is far away.
  - Assert that it begins moving when the player enters range.
  - Assert it returns to spawn point when the player runs out of leash range.
- **Engagement Integration Test:**
  - Assert that colliding with an enemy interactable fires the correct combat event.
- **Prior Art:** We will use `pytest` with simple dictionaries/arrays to simulate the grid, similar to how `test_interaction_manager.py` mocks the world state.

## Out of Scope

- Diagonal movement (game remains strictly 4-directional).
- Flocking behaviors or group tactics (enemies act independently).
- Enemies opening doors or interacting with complex objects to reach the player.
- Positional Combat Advantages (Back-attacks).

## Further Notes
This architecture ensures that the computational weight of A* is heavily mitigated by LoS gating and caching, while the Immediate Tile Claiming preserves the structural integrity of the `GameContext` which everything else relies upon.
