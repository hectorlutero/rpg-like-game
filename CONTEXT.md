# Project Context: RPG Classic (Pygame)

## Domain Language

- **Atributos**: Core stats (Vida, Mana, Agilidade, Força, Inteligência).
- **Classes**: Warrior (Guerreiro), Mage (Mago), Rogue (Ladino).
- **ATB (Active Time Battle)**: Combat system where agility determines turn frequency.
- **Proficiência**: Class-based effectiveness bonuses for equipment.
- **Defesa Absoluta**: Subtractive reduction for physical damage.
- **Defesa Relativa**: Percentage-based reduction for magic/skills.
- **Y-Sorting**: Dynamic rendering order where entities with higher Y-coordinate are drawn over those with lower Y.
- **Eager Asset Loading**: Maps pre-load all required sprites (Tilesets & Character Sheets) during scene transitions.
- **Sprite Metadata**: JSON-based definition for sprite dimensions and animation frames to allow flexible entity sizes.

## System Overview

A 2D top-down RPG built with Python and Pygame. It features an open world, team-based combat, and a modular attribute system where logic is separated from state.
