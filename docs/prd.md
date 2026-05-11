# Product Requirements Document (PRD) - RPG Classic (Final Fantasy Style)

## 1. Project Overview
A 2D top-down RPG built in Python with Pygame, focusing on classic mechanical progression, class-based growth, and a tactical ATB combat system.

## 2. Core Mechanics

### 2.1 Attribute System
Five fundamental attributes that define all entities:
- **Vida (HP):** Maximum hit points.
- **Mana (MP):** Resource for Spells.
- **Agilidade:** Governs ATB fill speed and Flee chance.
- **Força:** Base for physical damage and Absolute Defense calculations.
- **Inteligência:** Threshold for learning skills/spells, base for magical damage, Relative Defense, and status effect efficacy.

### 2.2 Classes & Growth
Three initial classes with distinct roles:
- **Guerreiro:** High HP and Strength gains.
- **Mago:** High Mana and Intelligence gains.
- **Ladino:** High Agility and balanced Intelligence gains.

**Growth Model:**
- **Initial Values:** Distinct per class at Level 1.
- **Gain Rate:** Automatic attribute increase per level based on class multipliers.
- **Experience:** Shared equally among the active party. No Level Cap.

### 2.3 Skill & Spell System
- **Skills:** Class-specific or common abilities. No cost to use. Gated by Intelligence requirements.
- **Spells:** Consume Mana. Also gated by Intelligence.
- **Acquisition:** Automatic discovery upon reaching the required Intelligence and Level thresholds.

### 2.4 Combat System (ATB)
- **Flow:** Active Time Battle. Time passes continuously; actions are taken when a circular meter fills.
- **Actions:** Attack, Skills, Spells, Items, Flee.
- **Defense Logic:** 
    - **Absolute Defense:** Subtractive reduction (Damage - Defense) for physical attacks.
    - **Relative Defense:** Percentage-based reduction for magical/skill damage.
- **Status Effects:** Poison, Paralysis, Sleep, Weakness, Dizziness, Silence, Stupidity (disables skills/spells).
    - Efficacy depends on the Intelligence difference between attacker and defender.
    - Resisted via equipment.

## 3. World & Exploration
- **Perspective:** 2D Top-down.
- **World Type:** Open World (aesthetic-only biomes).
- **Encounter Type:** Visible enemies on the map (no random encounters).
- **NPCs:** Classic dialogue windows with branching choices.
- **Items & Economy:** Loot from enemies, shop purchases, and world chests. Accessible costs for recovery.

## 4. Technical Architecture
- **Language:** Python 3.
- **Library:** Pygame.
- **Data Persistence:** JSON files for Save Points and progress.
- **Data Model:** Independent "Attribute Package" that calculates final values dynamically using Base Stats, Level, and Class Multipliers (Composition over Inheritance).

## 5. Success Criteria
- Functional ATB loop with visual circular meters.
- Accurate character scaling across levels based on class gain rates.
- Working inventory/equipment system with class-based proficiency.
- Save/Load functionality using Save Points.
