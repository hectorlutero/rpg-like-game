# Product Requirements Document (PRD) - RPG Classic (Pygame)

## Problem Statement
The project requires a consolidated roadmap for the final polish and feature-complete version of the RPG engine. While the core systems (Combat, Quest, AI, Audio, Juice) are implemented and functional, the focus now shifts to world-building, narrative depth, and visual polish to transform the engine into a cohesive game experience.

## Solution
Transition from "Feature Development" to "Content & Polish". This involves leveraging the existing deep modules (QuestManager, AIController, SoundManager) to build a compelling narrative loop, detailed maps, and a polished visual presentation using the established Juice system.

## Active Focus Areas (Remaining Work)

### 1. Visual Polish & Assets (Milestone 5)
- **Asset Management**: Implement an `AssetManager` with Eager Loading. Maps will pre-load SpriteSheets (Tilesets & Characters) during transitions.
- **Sprite Metadata**: Use JSON files to define sprite dimensions, animation frames, and hitboxes to allow flexible entity sizes.
- **Y-Sorting**: Implement dynamic rendering order where entities with higher Y-coordinates are drawn over those with lower Y.
- **Sub-tile Hitboxes**: Move away from grid-based collision to pixel-perfect or offset-based hitboxes defined in metadata.
- **Juice & Particles**: Implement a hybrid particle system (pre-baked animations for spells, dynamic particles for hits/dust).

### 2. Test Integrity & Regression (MANDATORY)
- **Graceful Degradation**: Ensure the engine remains functional (Headless/Debug mode) even if assets are missing, allowing existing logic tests to pass.
- **Test Refactoring**: Update movement and collision tests to account for sub-tile precision without breaking core logic validation.
- **Debug Room**: Create a dedicated test map to validate all new visual systems (Y-sorting, Hitboxes, Particles) in a controlled environment.

### 3. Narrative & Content Expansion (Milestone 6)
- **Main Quest**: Create a complete sequence from Village to Boss Cave.
- **Side Quests**: Utilize `CountableObjective` for gathering/hunting tasks.
- **Dialogue**: Implement branching dialogues that impact global state.

## Implementation Standards (Already Met)
- [x] **Modular 'Attribute Package'**: Multi-tier attribute calculation.
- [x] **ATB Combat Core**: Circular meter logic with physical/magical defense split.
- [x] **Quest Engine (Deep)**: Strategy-based objectives and rewards.
- [x] **AI & Navigation**: A* pathfinding and behavior-based controllers.
- [x] **Audio & Juice**: Global SoundManager and Trauma-based screen shake.
- [x] **Persistence**: Delta-based global state and JSON save system.

## User Stories (Remaining)
1. As a player, I want to explore a world that feels "alive" with consistent visuals and sounds.
2. As a player, I want meaningful choices in dialogues that impact quest rewards.
3. As a player, I want combat to feel "heavy" and impactful through visual feedback.

## Testing Strategy
- **Content Validation**: Automated tests for map portals and spawn tags.
- **Regression Testing**: Maintain 100% pass rate on existing core logic tests by using asset mocking/fallbacks.
- **Visual Validation**: Manual and automated checks in the `Debug Room`.

## Out of Scope
- Multiplayer or networking.
- Procedural generation.
- Full 3D rendering.
