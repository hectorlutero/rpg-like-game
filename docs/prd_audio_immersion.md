# Product Requirements Document (PRD) - Audio & Immersion

## Problem Statement
The game currently feels like a "silent simulation." While the logic (combat, movement, quests) is functional, there is no emotional layer (music), no visceral feedback for actions (SFX), and no visual "juice" (screen shake, fades) that makes the experience feel polished and professional. This lack of sensory feedback reduces player engagement and makes the game feel "stiff."

## Solution
Implement a comprehensive **Audio & Immersion System** (Milestone 4) that adds:
1.  **SoundManager**: A centralized service for Music, SFX, and Ambient sounds.
2.  **Juice System**: Visual feedback mechanisms (Screen Shake, Flash, Hit Stop) integrated into the core loop.
3.  **Visual Polish**: Smooth scene transitions (Fades) and Map-specific BGMs.
4.  **Event-Driven Audio**: Decoupled sound triggering using the existing `SignalBus`.

## User Stories
1.  As a player, I want to hear background music that matches the atmosphere of the map (e.g., peaceful in town, tense in a dungeon).
2.  As a player, I want the music to transition smoothly (fade out/in) when I change maps or enter a cutscene.
3.  As a player, I want to hear a sound effect when I interact with a chest, pick up an item, or enter combat.
4.  As a player, I want to feel the impact of a critical hit through a brief screen shake and a slight pause in action (hit stop).
5.  As a player, I want my screen to flash red when I take damage or white when I am healed.
6.  As a player, I want to hear looping environmental sounds (like a fireplace or wind) that add to the world's ambiance.
7.  As a player, I want to be able to adjust the volume of Music and SFX independently in the settings.
8.  As a developer, I want to map sound effects to game events (signals) via a simple JSON file without touching Python code.
9.  As a developer, I want the engine to handle missing audio files gracefully without crashing the game.
10. As a developer, I want precise control over when a sound plays during an animation (frame-perfect triggers).

## Implementation Decisions

### 1. SoundManager Service
-   **Centralization**: Added to `GameContext`.
-   **Mixer Channels**: Uses `pygame.mixer` with separate groups:
    -   `Music Channel`: Single track, supports looping and cross-fading.
    -   `SFX Channels`: A pool of channels for overlapping effects.
    -   `Ambient Channel`: For looping environmental sounds.
-   **Audio Stack**: Supports priorities. A high-priority music track (e.g., boss theme) can override and later restore the map's default BGM.

### 2. Event-Driven Audio Mapping (`audio_config.json`)
-   The `SoundManager` subscribes to the global `SignalBus`.
-   A JSON configuration maps `signal_name` -> `audio_file`.
-   Supports "Payload-Aware Mapping": Different sounds for the same signal based on data (e.g., `PICK_ITEM` with `"gold"` vs `"sword"`).

### 3. Visual Juice (Screen Shake & Flash)
-   **Camera Offset**: Renderers (like `ExplorationScene`) will use a dynamic `offset` to draw the world.
-   **Trauma Model**: "Trauma" is added on events (damage, explosion) and decays over time, causing random jitter in the offset.
-   **Flash Overlay**: A semi-transparent surface drawn over the scene for a few frames.

### 4. Hit Stop Logic
-   When a high-impact event (e.g., `CRITICAL_HIT`) occurs, the `Orchestrator` briefly pauses the logic update (dt = 0) while keeping the rendering and audio active.

### 5. DirectorEngine Integration
-   New commands: `PLAY_MUSIC`, `STOP_MUSIC`, `PLAY_SFX`, `SET_VOLUME`.
-   Allows cutscenes to orchestrate the audio experience perfectly.

### 6. Configuration & Persistence
-   `Master`, `Music`, and `SFX` volume levels are stored in the `GlobalState` and persisted via `SaveManager`.

## Testing Decisions
-   **Mock Mixer**: Unit tests will use a mock `pygame.mixer` to verify that the `SoundManager` attempts to play the correct files at the correct volumes.
-   **Signal-to-Audio Integration Tests**: Verify that emitting a `PICK_ITEM` signal results in a call to `mixer.Sound.play()`.
-   **Volume Persistence Tests**: Ensure that changing volume settings persists through a save/load cycle.
-   **Graceful Degradation**: A test that attempts to play a non-existent sound file and verifies no exception is raised.

## Out of Scope
-   **Positional Audio (Panning)**: Sounds will not vary based on left/right screen position.
-   **3D Reverb/Echo**: No complex environmental audio filters.
-   **Voice Acting**: Only text-based dialogue with simple "blip" sounds.

## Further Notes
-   Audio files should ideally be `.ogg` for music (better compression) and `.wav` for SFX (lower latency).
-   Default `fade_speed` for scene transitions will be standardized across all map portals.
