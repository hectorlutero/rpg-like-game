## What to build

Implement a hybrid particle system to enhance visual feedback during combat and exploration.

- **MANDATORY**: Start with a `grill-me` session to define the particle engine architecture (dynamic vs pre-baked).
- Create a `ParticleManager` to handle short-lived visual effects.
- Implement "Hit Sparks" for combat and "Dust Particles" for movement.
- Integrate with the existing `JuiceService`.

## Acceptance criteria

- [ ] Successful completion of the "Particle System Grill".
- [ ] Particles are correctly layered and sorted (Y-Sorting).
- [ ] No significant performance drop when spawning multiple particles simultaneously.

## Blocked by

- docs/issues/001-asset-manager-infrastructure.md
- docs/issues/005-sprite-animation-system.md
