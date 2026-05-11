# Product Requirements Document (PRD) - RPG Classic (Pygame)

## Problem Statement
The project lacks a centralized, formal definition of its features and requirements, which is essential for maintaining architectural consistency as development progresses. A modular and robust foundation for core RPG mechanics (Attributes, Classes, Combat, and Growth) is needed to ensure that future features like the Open World and Story can be built on a stable, testable, and scalable architecture.

## Solution
Implement a modular "Attribute Package" system and a class-based growth engine that powers a tactical ATB combat system, character progression, and world interactions. This solution focuses on separation of concerns, where mechanical logic is decoupled from state representation.

## User Stories
1. As a player, I want to see my character's core attributes (Health, Mana, Agility, Strength, Intelligence) so I can understand their strengths and weaknesses.
2. As a player, I want to choose between Warrior, Mage, and Rogue classes to experience different gameplay styles.
3. As a player, I want my character to grow automatically as they level up, with stats increasing based on my chosen class, so I feel a sense of progression.
4. As a player, I want to learn new skills and spells automatically when I reach certain Intelligence thresholds, rewarding my investment in that attribute.
5. As a player, I want to participate in Active Time Battle (ATB) combat where my Agility determines how often I can act, adding a layer of timing and strategy.
6. As a player, I want to use different combat actions (Attack, Skills, Spells, Items, Flee) to overcome various enemy types.
7. As a player, I want to experience tactical combat where defense is handled differently for physical (Absolute) vs magical (Relative) damage.
8. As a player, I want to see enemies on the world map so I can choose which encounters to engage in.
9. As a player, I want to interact with NPCs and make choices in dialogues that reflect my character's attributes or decisions.
10. As a player, I want to use my attributes to solve world puzzles, such as pushing heavy rocks if my Strength is high enough.
11. As a developer, I want a modular "Attribute Package" so I can easily reuse the stat logic for both players and enemies.
12. As a developer, I want a shared experience system so the entire party progresses together without the need for managing individual XP pools.
13. As a player, I want status effects (Poison, Paralysis, Sleep, Weakness, Dizziness, Silence, Stupidity) to behave predictably based on the Intelligence gap between the attacker and defender.
14. As a player, I want my equipment to have different effectiveness based on my class proficiency, encouraging role-specialization.

## Implementation Decisions
- **Modular 'Attribute Package'**: Logic for Health, Mana, Agility, Strength, and Intelligence is encapsulated in a composition-based system. It calculates final "Runtime Stats" by applying level gain rates, equipment modifiers, and status effect debuffs.
- **Class-Based Growth Engine**: A registry of class definitions (Warrior, Mage, Rogue) containing starting values and gain multipliers. Growth is automatic upon leveling.
- **Skill/Spell Acquisition**: A system that maps Intelligence thresholds to specific Skill or Spell objects. Acquisition is automatic upon reaching thresholds.
- **ATB Combat Core**: A circular meter-based Active Time Battle system. Agility determines the fill rate. Actions include Attack, Skills, Spells, Items, and Flee.
- **Dual-Defense Model**: 
  - **Absolute Defense**: Subtractive reduction (Damage - Defense) for physical attacks.
  - **Relative Defense**: Percentage-based reduction for magical/skill damage.
- **Status-Based AI**: Enemies use mixed behaviors (Random, Scripted, Reactive, Strategic) and analyze player attributes (Intelligence-based analysis) to choose actions.
- **Data Persistence**: Use JSON for save files, storing character state, party progress, and world flags.

## Testing Decisions
- **Unit Testing for Attribute Logic**: Verify that gain rates and multipliers are applied correctly across different levels and classes.
- **Integration Testing for Combat Flow**: Simulate ATB turns to verify turn ordering and correct application of both Absolute and Relative defense models.
- **Validation of Skill Gates**: Confirm that skills and spells are unlocked exactly when Intelligence thresholds are reached.
- **Behavioral Testing for Enemy AI**: Test that AI routines react correctly to player status and attributes.

## Out of Scope
- High-fidelity graphics (using primitives/simple sprites initially).
- Advanced world map features (minimaps, fog of war).
- Multiplayer or network functionality.
- Complex crafting or profession systems.

## Further Notes
The project follows a Socratic methodology for development, meaning technical implementation details (classes, methods) are derived from these requirements through logical deduction and architectural mapping.
