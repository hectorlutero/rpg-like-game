# RPG Project Tracking

## Concepts Learned & Defined
- **Attribute System:** Five core stats (Health, Mana, Agility, Strength, Intelligence).
- **Class-Based Growth:** Three classes (Warrior, Mage, Rogue) with distinct starting values and automatic "gain rates" per level.
- **Skill/Spell System:** Hybrid skills (common + class-specific) gated by Intelligence; Spells consume Mana. Automatic acquisition.
- **Combat Flow (ATB):** Active Time Battle with circular progress meters. Agility dictates frequency.
- **Combat Actions:** Attack, Skills, Spells, Items, Flee. No "Defend" action.
- **Damage & Defense Logic:** Dual model (Absolute for Physical, Relative for Magic). Defense from Armor.
- **Equipment:** Fixed + Percentage bonuses. Class proficiency multipliers.
- **Enemy AI:** Status-based entities with mixed behaviors (Random, Scripted, Reactive, Strategic). Intelligence-based analysis of player.
- **Exploration & World:** 2D Top-down, Open World (aesthetic biomes), Visible enemies (no random encounters).
- **NPC Interactions:** Classic dialogue with choices.
- **Party & Save:** Team-based (no reserve), shared EXP. Save Points (JSON).
- **Technical Stack:** Python + Pygame.

## Roadmap
1. [x] Mechanical Concept Definition
2. [x] Detailed Design Refinement (Grill-Me)
3. [x] Product Requirements Document (PRD)
4. [x] Core Data Structure Architecture (Implementation)
5. [x] Character Initialization System
6. [x] ATB Engine Prototype
7. [x] Skill & Damage Calculation System
8. [x] World & Exploration Module
9. [x] NPC & Dialogue System
10. [ ] Interface de Combate e Medidores Circulares
