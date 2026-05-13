## Parent
#37

## What to build
Implement the `DirectorEngine` and a foundational `MapAPI`. The director will execute map-specific Python scripts using `yield` for non-blocking interaction sequences (dialogues, item giving).

## Acceptance criteria
- [ ] `src/logic/director.py` can execute a generator-based script.
- [ ] `MapAPI` provides methods for `say`, `give_item`, and `set_flag`.
- [ ] A script `scripts/vila_inicial.py` successfully handles an interaction with a branching dialogue.

## Blocked by
#40
