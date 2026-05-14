# Issue: Event-Driven SFX & Mapping

## Parent
PRD: docs/prd_audio_immersion.md

## What to build
Implement a decoupled sound triggering system using the `SignalBus`. Sounds will be mapped to game events via a JSON configuration file.

- Create `data/audio_config.json` to map signals (e.g., `PICK_ITEM`, `INTERACT`, `START_COMBAT`) to sound files.
- `SoundManager` must subscribe to the `SignalBus` and check the config for matches on every emitted signal.
- Support "Payload-Aware Mapping" for signals like `PICK_ITEM` (different sounds for gold vs items).
- Ensure SFX play on separate channels to allow overlapping sounds.

## Acceptance criteria
- [ ] `SoundManager` automatically plays the correct SFX when a mapped signal is emitted.
- [ ] Emitting `PICK_ITEM` with `"gold"` in the payload plays a coin sound, while other items play a generic sound.
- [ ] Multiple SFX can play simultaneously without cutting each other off.
- [ ] Config file is easy to edit without touching Python code.

## Blocked by
- docs/issue_slice_1_audio.md
