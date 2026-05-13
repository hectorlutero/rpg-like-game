# Product Requirements Document (PRD) - Narrative & Quest Engine

## Problem Statement
The game currently lacks a formal way to track player progress beyond simple flags. There is no system to define complex objectives, provide player guidance (Quest Log), or react dynamically to world events (like picking up an item or defeating an enemy). This limits the depth of the narrative and the player's sense of purpose.

## Solution
Implement a centralized, event-driven Quest Engine. Quests will be defined in a structured JSON format, tracked via the `GlobalState`, and updated automatically through an Observer Pattern (signals). A detailed Quest Log will be added to the menu system to guide the player, and rewards will be orchestrated via the `DirectorEngine` to allow for cinematic completion sequences (dialogues, sounds, and items).

## User Stories
1. As a player, I want to receive quests from NPCs so I have clear goals in the world.
2. As a player, I want to see a notification when an objective is updated or completed, so I know I'm making progress.
3. As a player, I want a detailed Quest Log in the menu showing active quests and current objective descriptions.
4. As a player, I want the world to react to my quest status (e.g., a guard only lets me pass if I have a specific quest).
5. As a developer, I want to define quests in `quests.json` with multiple stages and objectives, keeping narrative logic separate from engine code.
6. As a developer, I want quest rewards to trigger via `DirectorEngine` scripts for maximum control over the "fanfare" and feedback.

## Implementation Decisions
- **Centralized Quest Registry**: A `data/quests.json` file defining:
    - Quest ID, Name, and Description.
    - Stages: A sequence of objectives.
    - Objectives: Specific criteria (e.g., `PICK_ITEM`, `KILL_ENEMY`, `REACH_TAG`).
- **Quest State (GlobalState)**: Quests will be tracked in the existing `GlobalState` using a consistent schema: `quests[quest_id] = {stage: 0, status: "IN_PROGRESS"}`.
- **Event Bus (Observer Pattern)**: A simple signal system where engine components (Inventory, Combat, Orchestrator) emit events. The `QuestManager` listens to these events to auto-complete objectives (Option A). 
- **Hybrid Validation**: While objectives update automatically via events, the final completion and reward hand-off often require a manual interaction with an NPC (Option B), which uses the `DirectorEngine` to check quest status and trigger final dialogues.
- **Detailed Quest Log**: A new `QuestLogScene` accessible via the main menu, rendering:
    - List of Active/Completed quests.
    - Current objective description for the selected quest.
- **Scripted Rewards**: When a quest reaches the 'Reward' stage, the `QuestManager` signals the `DirectorEngine` to run a completion script (e.g., João saying "Thanks!", playing a sound, and adding 100G).

## Testing Decisions
- **Quest Logic Unit Tests**: Verify that picking up a "Quest Item" correctly advances the stage in `GlobalState`.
- **JSON Validation**: Ensure the `QuestRegistry` correctly parses the `quests.json` schema.
- **UI Integration**: Test that the `QuestLogScene` correctly displays data from the `GlobalState`.
- **E2E Narrative Loop**: A test where an NPC gives a quest, the player picks up an item, and the NPC recognizes the completion.

## Out of Scope
- Branching quest paths (multiple choices leading to different endings for the same quest).
- Quest markers on the map (minimap icons).
- Time-limited quests.

## Further Notes
- Quest notifications should be non-blocking (small text at the top of the screen).
- The system must support "Hidden Quests" (flags that don't appear in the log until a certain stage).
