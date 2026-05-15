## Parent
[Milestone 6 - Game Flow & Final Polish](../prd_milestone_6.md)

## What to build
Implement a centralized `InputManager` to decouple physical key presses (e.g., `pygame.K_w`, `pygame.K_UP`) from logical game actions (e.g., `move_up`, `interact`, `menu`). This includes supporting "Presets" (Standard, WASD) and refactoring existing scenes to use this manager.

## Acceptance criteria
- [ ] `InputManager` class created with a configurable mapping dictionary.
- [ ] Support for at least two presets: Standard (Arrows) and WASD.
- [ ] `ExplorationScene`, `CombatScene`, and `MenuScene` refactored to use `InputManager.is_action_pressed(action)`.
- [ ] Unit tests for mapping translation and preset switching.
- [ ] Logic for "Custom" remapping is ready for UI integration.

## Blocked by
None - can start immediately
