# PRD: Milestone 6 - Game Flow & Final Polish

## Problem Statement
The game currently possesses core mechanics (combat, exploration, inventory) but lacks a cohesive "Game Flow". There is no main menu, the saving system is limited to a single file, inputs are hardcoded across multiple scenes, and there is no narrative delivery system (cutscenes) or final wrap-up (credits). This makes the project feel like a collection of systems rather than a finished game experience.

## Solution
Implement a complete game loop from title screen to credits. This includes a centralized input management system for remapping, a robust multi-slot save system, accessibility options for text, and a script-based cutscene engine. Visual and functional polish will be applied to shops and transitions to ensure a high-quality "classic RPG" feel.

## User Stories
1. As a player, I want a Title Screen so I can choose between starting a new journey, continuing a previous one, or adjusting settings.
2. As a player, I want multiple Save Slots so I can maintain different playthroughs or save at different points in the story.
3. As a player, I want to see the date, time, and character level in the Load menu so I can easily identify my progress.
4. As a player, I want a Pause Menu during exploration to manage my equipment, status, and view active quests.
5. As a player, I want to remap my keys using presets so I can play with the control scheme I'm most comfortable with (e.g., WASD vs Arrows).
6. As a player, I want to adjust the text size to a "Readable" mode so I can follow the story without eye strain.
7. As a player, I want to adjust Audio volumes (Music/SFX) so I can balance the game's sound to my liking.
8. As a player, I want to choose a Difficulty Level that affects enemy stats, allowing me to tailor the challenge.
9. As a player, I want to experience narrative moments through Cutscenes where characters move and talk automatically.
10. As a player, I want to see a preview of stat changes when buying equipment in shops so I can make informed purchases.
11. As a player, I want to see a scrolling Credits sequence after finishing the game to acknowledge the journey.
12. As a player, I want smooth Fades and Screen Shakes during transitions and impactful moments to feel more immersed.

## Implementation Decisions

### 1. Centralized Input Management
- Create an `InputManager` that maps logical actions (move_up, interact, menu) to physical keys.
- Implement "Presets" (Standard, WASD, Custom).
- Refactor existing scenes to use the `InputManager` instead of direct `pygame.KEYDOWN` checks for game logic.

### 2. Multi-Slot Save System
- Extend `SaveManager` to handle multiple files (e.g., `save_1.json`, `save_2.json`).
- Include metadata in save files: `timestamp`, `play_time`, `hero_level`, `location_name`.
- Create a dedicated "Save/Load Scene" with slot selection.

### 3. Cutscene Engine (Script-based)
- Parser for JSON-based cutscene files.
- Commands supported: `move_entity`, `play_animation`, `show_dialogue`, `wait`, `play_sound`, `camera_pan`.
- Integration with `GameContext` to lock/unlock player control.

### 4. UI/UX Polishment & Accessibility
- **Options Scene**: Sliders for audio, toggles for fullscreen, and font size pre-sets.
- **Shop Enhancements**: Comparison UI showing "Current Stat -> New Stat" (green/red indicators).
- **Credits Scene**: Vertical scroll renderer with background image support.
- **Difficulty Scaling**: Implement a `DifficultyManager` that applies multipliers to `EnemyInteractable` stats during combat initialization.

## Testing Decisions
- **Unit Tests**: 
    - `InputManager` mapping and preset switching.
    - `SaveManager` metadata extraction and slot integrity.
    - `DifficultyManager` multiplier calculations.
- **Integration/E2E Tests**:
    - Full flow from Title Screen -> New Game -> Exploration.
    - Cutscene trigger and completion.
    - Saving in one scene and loading in another to verify `GameContext` persistence.
- **Visual Validation**: Use existing `ui_tester.py` to capture screenshots of the new menus and compare against expected layouts.

## Out of Scope
- Visual Cutscene Editor (Tooling).
- Online Leaderboards or Achievements.
- Advanced Graphic Settings (Shaders, Resolution scaling beyond fullscreen toggle).
- Game Localization (Translations).

## Further Notes
- Adhere to the `Scene-based` architecture.
- All new UIs must respect the `Y-Sorting` and `Eager Asset Loading` mandates defined in `CONTEXT.md`.
