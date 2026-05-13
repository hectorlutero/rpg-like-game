## Problem Statement

The current Quest Engine implementation is shallow and inflexible. The `QuestManager` directly evaluates objective completion through simplistic dictionary key matching (`type` and `target`), which makes it impossible to support complex quest mechanics such as quantity tracking (e.g., "Collect 5 Apples"), time limits, or composite conditions without cluttering the core manager with conditional logic. Additionally, quest rewards are tightly coupled to invoking scripts via the `DirectorEngine`, limiting the system's ability to easily grant items, experience, or trigger other game events upon quest completion.

## Solution

Deepen the Quest Engine architecture by introducing two primary seams: the Objective Evaluation Seam and the Quest Action/Reward Seam. By extracting objective evaluation into dedicated Strategy classes (e.g., `CollectItemObjective`, `DefeatEnemyObjective`) and standardizing quest outcomes through a `QuestAction` interface, the system becomes highly extensible. The `QuestManager` will delegate evaluation and reward logic to these deep modules, ensuring that new quest types or reward mechanisms can be added without modifying the core progression loop.

## User Stories

1. As a quest designer, I want to define quests that require collecting multiple items, so that players have sustained goals.
2. As a quest designer, I want to create objectives based on defeating specific enemies, so that combat contributes to narrative progression.
3. As a quest designer, I want to specify rewards such as items or experience points directly in the quest data, so that I don't have to write a custom script for every simple reward.
4. As a game developer, I want objective logic encapsulated in dedicated classes, so that I can easily test objective completion rules in isolation.
5. As a game developer, I want the `QuestManager` to be ignorant of specific objective types, so that the core engine remains clean and closed for modification but open for extension.
6. As a player, I want accurate tracking of my progress on multi-step quests (e.g., 3/5 apples collected), so that I know how close I am to completion.

## Implementation Decisions

- **Objective Strategy Pattern:** Introduce a base `QuestObjective` interface. Concrete implementations (e.g., `CountableObjective`, `EventObjective`) will handle the logic of `is_fulfilled(event, state)` and tracking progress (like item counts).
- **Quest Action Interface:** Introduce a `QuestAction` (or `QuestReward`) interface with an `execute(context)` method. Concrete classes like `GiveItemAction`, `GiveXPAction`, or `RunScriptAction` will handle the consequences of completing a quest stage.
- **QuestManager Refactor:** The `QuestManager` will be updated to instantiate these strategy objects when loading from JSON. Its `on_event` method will delegate the matching logic to the active stage's objective objects.
- **State Persistence:** The `GlobalState` will need to track the internal progress of complex objectives (e.g., `current_count`) alongside the quest's overall stage.

## Testing Decisions

- A good test will verify that specific events correctly increment or fulfill an objective independently of the entire game loop.
- **Modules Tested:** The new `QuestObjective` and `QuestAction` implementations will be tested in strict isolation using unit tests.
- **Integration Testing:** Existing E2E tests (like `test_quest_e2e.py`) will be updated to ensure the refactored `QuestManager` still correctly advances quests through the new strategy objects without regressions.

## Out of Scope

- Implementing a visual UI for tracking multi-step objectives on the screen (only the underlying logic and state tracking are in scope).
- Creating new complex quest scripts for the Director; this PRD focuses strictly on the architectural decoupling of the engine itself.

## Further Notes

- This refactor aligns with the "Deep Modules" principle by pushing complex conditional logic down into specialized adapters, increasing both locality and leverage within the codebase.