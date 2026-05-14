# Issue: Ambient Loops & Animation Sync

## Parent
PRD: docs/prd_audio_immersion.md

## What to build
Add support for looping environmental sounds and frame-perfect audio triggers for animations.

- Implement an `Ambient` layer in `SoundManager` for sounds like rain or fire.
- Allow entities or map JSONs to define ambient sound sources.
- Introduce an `ANIM_TRIGGER` signal that `SoundManager` listens to for playing sounds exactly when a specific frame is reached in an animation.

## Acceptance criteria
- [ ] Looping ambient sounds play correctly and can be started/stopped.
- [ ] `ANIM_TRIGGER` allows playing a sound synced with a visual action (e.g., footstep or sword swing).
- [ ] Ambient sounds stop correctly when switching maps.

## Blocked by
- docs/issue_slice_2_audio.md
