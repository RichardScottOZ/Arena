# Arena Python Package - User Guide

## Introduction

The Arena Python package is a port of the original Java implementation for simulating Original D&D combat scenarios. It provides both a command-line interface and a programmatic API for running combat simulations.

## Installation

### From Source

```bash
cd python
pip install -e .
```

### Dependencies

- Python 3.7+
- numpy (optional, for advanced features)
- pandas (optional, for data analysis)

## Quick Start

### Command Line

Run a basic simulation:
```bash
# Using the arena command directly
arena

# Using python module
python -m arena arena

# With custom parameters
arena -n=20 -y=10 -f=12
```

### Python API

```python
from arena import Arena

# Create and configure simulation
sim = Arena()
sim.num_years = 10
sim.num_fighters = 50

# Run simulation
sim.run()
```

## Command-Line Options

### Arena Options

- `-?` : Show help message
- `-y=N` : Set number of years to simulate (default: 50)
- `-f=N` : Set number of fights per year (default: 12)
- `-n=N` : Set number of fighters (default: 100)
- `-l=N` : Set starting level for fighters (default: 1)
- `-p=N` : Set party size (default: 1)
- `-a=N` : Set base armor type
  - 0: No armor
  - 1: Leather
  - 2: Chain
  - 3: Plate (default)
- `-m` : Enable man vs. monster mode
- `-t` : Use monster treasure types
- `-r[sdktxy]` : Set reporting options
  - `s`: Fighter statistics
  - `d`: Fighter details
  - `k`: Monster kills
  - `t`: Total monster kills
  - `x`: XP awards
  - `y`: Year-end status

### Examples

```bash
# Small test run
arena -n=10 -y=5 -f=6

# Longer simulation with reporting
arena -n=100 -y=50 -ry

# Man vs Monster mode
arena -m -n=20 -y=10
```

## Python API Guide

### Core Classes

#### Dice

Handles dice rolling with standard notation:

```python
from arena import Dice

# Create dice
d6 = Dice(1, 6)          # 1d6
d3d6 = Dice(3, 6)        # 3d6
damage = Dice(2, 8, 1, 3) # 2d8+3

# From string
d = Dice.from_string("3d6+2")

# Roll
result = d.roll()
```

#### Character

Represents player characters:

```python
from arena import Character
from arena.enums import ClassType, Alignment

# Create character
fighter = Character("Conan", level=5, class_type=ClassType.FIGHTER)

# Set equipment
from arena.equipment import Armor, Weapon
from arena.enums import ArmorType

fighter.set_armor(Armor.make_type(ArmorType.PLATE))
fighter.set_weapon(Weapon.create_sword(magic_bonus=1))

# Access properties
print(f"AC: {fighter.get_ac()}")
print(f"HP: {fighter.get_hp()}")
print(f"Level: {fighter.get_level()}")
```

#### Monster

Base class for creatures:

```python
from arena import Monster, Attack
from arena.dice import Dice

# Create monster
orc = Monster("Orc", armor_class=6, move_inches=12)
orc.hit_dice = Dice(1, 6)
orc.attack = Attack(1, "1d8")

# Combat
orc.take_damage(5)
if orc.is_alive():
    print(f"Orc has {orc.get_hp()} HP remaining")
```

#### Party

Manages groups:

```python
from arena import Party, Character
from arena.enums import ClassType

# Create party
party = Party()

# Add members
for i in range(4):
    char = Character(f"Fighter{i}", level=i+1, class_type=ClassType.FIGHTER)
    party.add_member(char)

# Query party
print(f"Party size: {party.get_size()}")
print(f"Living members: {party.num_living()}")
print(f"Average level: {party.get_average_level()}")

# Manage party
party.heal_all()
dead = party.bring_out_your_dead()
```

#### Arena

Main simulation class:

```python
from arena import Arena

# Create arena
arena = Arena()

# Configure
arena.num_years = 20
arena.fights_per_year = 12
arena.num_fighters = 100
arena.start_level = 1
arena.fight_man_vs_monster = False
arena.report_year_end = True

# Run
arena.run()

# Or parse command-line args
arena.parse_args(['-n=50', '-y=10'])
arena.run()
```

### Enumerations

```python
from arena.enums import (
    Alignment,      # LAWFUL, NEUTRAL, CHAOTIC
    ArmorType,      # PLATE, CHAIN, LEATHER, SHIELD
    ClassType,      # FIGHTER, WIZARD, THIEF, ELF
    Ability,        # STRENGTH, DEXTERITY, etc.
    SpecialType,    # Special abilities
)

# Random alignments
align = Alignment.random_normal()    # Normal distribution
align = Alignment.random_uniform()   # Uniform distribution
align = Alignment.from_char('L')     # From character
```

### Equipment

```python
from arena.equipment import Armor, Weapon
from arena.enums import ArmorType

# Create armor
plate = Armor.make_type(ArmorType.PLATE)
magic_chain = Armor.make_type(ArmorType.CHAIN, magic_bonus=2)

# Create weapons
sword = Weapon.create_sword()
magic_axe = Weapon.create_axe(magic_bonus=1)

# Custom equipment
from arena.equipment import Equipment
ring = Equipment("Ring of Protection", magic_bonus=1)
```

## Advanced Usage

### Custom Combat Simulation

```python
from arena import Character, Dice
from arena.enums import ClassType

# Create fighters
fighter1 = Character("Alice", 3, ClassType.FIGHTER)
fighter2 = Character("Bob", 3, ClassType.FIGHTER)

# Set up equipment
from arena.equipment import Armor, Weapon
from arena.enums import ArmorType

fighter1.set_armor(Armor.make_type(ArmorType.CHAIN))
fighter1.set_weapon(Weapon.create_sword())

fighter2.set_armor(Armor.make_type(ArmorType.PLATE))
fighter2.set_weapon(Weapon.create_axe())

# Run combat
damage_dice = Dice(1, 8)

while fighter1.is_alive() and fighter2.is_alive():
    # Fighter 1 attacks
    dmg = damage_dice.roll()
    fighter2.take_damage(dmg)
    
    if not fighter2.is_alive():
        break
    
    # Fighter 2 attacks
    dmg = damage_dice.roll()
    fighter1.take_damage(dmg)

winner = fighter1 if fighter1.is_alive() else fighter2
print(f"Winner: {winner.name}")
```

### Seeded Random Rolls

For reproducible results:

```python
from arena.dice import set_random_seed

# Set seed for reproducibility
set_random_seed(42)

# Now all random operations will be deterministic
```

## Testing

Run the test suite:

```bash
cd python
pytest tests/
```

Run with coverage:

```bash
pytest tests/ --cov=arena --cov-report=html
```

## Examples

See `examples.py` for comprehensive usage examples:

```bash
cd python
python examples.py
```

## Jupyter Notebooks

Interactive notebooks are available in `notebooks/`:

```bash
cd python
jupyter notebook notebooks/
```

## Contributing

When contributing to the Python package:

1. Maintain consistency with the Java implementation
2. Use type hints where appropriate
3. Follow PEP 8 style guidelines
4. Add tests for new features
5. Update documentation

## Troubleshooting

### Import Errors

If you get import errors, ensure the package is installed:
```bash
cd python
pip install -e .
```

### Missing Data Files

Some features require CSV data files from the repository root. Ensure you're running from the correct directory or set the data path appropriately.

## References

- Original Java implementation: http://www.oedgames.com
- Repository: https://github.com/RichardScottOZ/Arena
- OED House Rules: http://www.oedgames.com
