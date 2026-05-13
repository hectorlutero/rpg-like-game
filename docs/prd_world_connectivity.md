# Product Requirements Document (PRD) - Portal & World Connectivity

## Problem Statement
The game currently only supports a single map (`starting_village.json`). There is no mechanism to transition between different geographical areas, which prevents the expansion of the game world. Players cannot explore new regions, and the sense of a continuous world is missing.

## Solution
Implement a robust Map Transition System. This includes a new `Portal` entity that can trigger transitions either automatically (stepping on it) or manually (interacting with a door). The system will use a "Fade-to-Black" effect to hide the loading process, manage the handoff between maps via `WorldOrchestrator`, ensure the player appears at the correct location using `Tags`, and automatically save the game to prevent progress loss during transitions.

## User Stories
1. As a player, I want to walk to the edge of a map and seamlessly enter a new area, so the world feels large and connected.
2. As a player, I want to interact with doors or cave entrances to enter buildings or dungeons, so I can explore interior spaces.
3. As a player, I want to see the screen fade to black when changing areas, so the transition feels polished and professional.
4. As a player, I want the game to auto-save when I change maps, so I don't lose progress if something goes wrong.
5. As a player, I want to appear at the logical entrance of the new map (e.g., coming from the east, I should appear on the east side of the next map), maintaining spatial orientation.
6. As a developer, I want to define portals in JSON, specifying the target map, target tag, and whether interaction is required, so I can easily build complex worlds without writing code for every door.

## Implementation Decisions
- **Portal Entity**: A specialized `Interactable` entity with properties: `target_map` (filename), `target_tag` (ID of the destination tag), and `require_interaction` (boolean).
- **Trigger Logic**: 
    - If `require_interaction` is `false`, the transition triggers when the player's grid position matches the portal's position (On Step).
    - If `require_interaction` is `true`, the transition triggers only when the player interacts with the portal while adjacent (Interaction).
- **Fade Transition System**: A visual overlay in `ExplorationScene` with an `alpha` value.
    - **Phase 1 (Fade Out)**: Alpha goes from 0 to 255. Input is blocked.
    - **Phase 2 (Swap)**: At Alpha 255, `WorldOrchestrator` loads the new map data and triggers `Persistence.save()`.
    - **Phase 3 (Fade In)**: Alpha goes from 255 to 0. Input remains blocked until complete.
- **Tag-Based Positioning**: The `WorldOrchestrator` will look for an entity/tag in the new map with an ID matching the `target_tag` to determine the player's spawn coordinates.
- **Auto-save Point**: The save occurs at the "peak" of the fade (Alpha 255) to ensure all state is captured before the old map is discarded.

## Testing Decisions
- **Integration Test (Village to Forest)**: Verify that stepping on a portal in `starting_village.json` correctly loads `forest.json`.
- **Tag Verification**: Test that the player's `(x, y)` in the new map matches the coordinates of the `target_tag`.
- **Input Blocking**: Ensure no player movement or interaction is possible during the fade phases.
- **Auto-save Validation**: Check that `savegame.json` is updated during a transition and contains the data for the new map location.

## Out of Scope
- Animated portals (visual effects on the portal itself).
- "Peeking" into the next map before entering.
- Transitioning with followers or multiple party members (handled by `PartyManager` logic, not the portal itself).

## Further Notes
- All maps and tags must follow English naming conventions.
- Transition speed should be fast (under 1 second total) to maintain game flow.
