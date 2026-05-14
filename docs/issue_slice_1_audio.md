# Issue: SoundManager & BGM System

## Parent
PRD: docs/prd_audio_immersion.md

## What to build
Implement the core `SoundManager` service and integrate it into `GameContext`. This system will handle background music (BGM) with support for map-specific tracks defined in map JSONs.

- Create `src/core/audio.py` with a `SoundManager` class.
- Support `Music`, `SFX`, and `Ambient` channel groups using `pygame.mixer`.
- Implement a "Graceful Degradation" strategy: if an audio file is missing, log a warning but do not crash.
- Implement automatic BGM switching when entering a map, including a cross-fade effect.
- Map JSONs (e.g., `starting_village.json`) should support a `"bgm"` property.

## Acceptance criteria
- [ ] `SoundManager` is accessible via `context.sound_manager`.
- [ ] Entering a map with a defined `"bgm"` starts playing the track.
- [ ] Switching maps with different BGMs triggers a fade-out/fade-in.
- [ ] Switching maps with the same BGM does not restart the track.
- [ ] Game starts and runs even if the specified audio files are missing from the disk.
- [ ] Unit tests verify `SoundManager` interaction with `pygame.mixer`.

## Blocked by
None - can start immediately.
