## Parent
[Milestone 6 - Game Flow & Final Polish](../prd_milestone_6.md)

## What to build
Implement the `TitleScene` as the game's entry point. It should allow players to start a New Game, select a slot to Load, or enter the Options menu.

## Acceptance criteria
- [ ] `TitleScene` with interactive buttons/options: "Novo Jogo", "Carregar Jogo", "Opções", "Sair".
- [ ] Integration with `SaveManager` to display a "Load Menu" showing available slots with metadata (Level, Time).
- [ ] Proper scene transition from Title -> Exploration (New Game) or Title -> Specific Map (Load).
- [ ] Full keyboard navigation using `InputManager` actions.

## Blocked by
- [008-input-centralization-presets.md](008-input-centralization-presets.md)
- [009-multi-slot-save-system.md](009-multi-slot-save-system.md)
