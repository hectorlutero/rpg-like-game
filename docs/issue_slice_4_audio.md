# Issue: Hit Stop & Critical Impact

## Parent
PRD: docs/prd_audio_immersion.md

## What to build
Enhance the visceral feel of combat by introducing a brief pause in the game's logic during high-impact moments.

- Modify the `Orchestrator` to support a `hit_stop(duration)` method.
- When `hit_stop` is active, `dt` passed to logic updates is 0, but rendering and audio continue.
- Trigger `hit_stop` on signals like `CRITICAL_HIT` or when an enemy is defeated.
- Combine this with a strong Screen Shake from Slice 3.

## Acceptance criteria
- [ ] Game logic briefly "freezes" on critical hits for ~0.1s.
- [ ] Animations/Logic pause but the screen remains responsive (no OS hang).
- [ ] Combined effect of Screen Shake + Hit Stop feels "heavy" and impactful.

## Blocked by
- docs/issue_slice_3_audio.md
