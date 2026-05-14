# Issue: Volume Controls & Persistence

## Parent
PRD: docs/prd_audio_immersion.md

## What to build
Allow the player to control audio settings and ensure these settings persist between game sessions.

- Add `master_volume`, `music_volume`, and `sfx_volume` to `GlobalState`.
- Update `SoundManager` to respect these volume levels across all channels.
- Ensure volume settings are saved/loaded via `SaveManager`.
- (Optional) Provide a simple command or UI hook to toggle/adjust volume.

## Acceptance criteria
- [ ] Adjusting `music_volume` affects only background music.
- [ ] Adjusting `sfx_volume` affects all effects.
- [ ] Settings persist after restarting the game and loading a save.
- [ ] Default volumes are sensible (e.g., 0.7).

## Blocked by
- docs/issue_slice_1_audio.md
