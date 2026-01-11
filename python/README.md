# Arena Python Package

This is a Python implementation of the Arena D&D combat simulator, based on the original Java implementation by Daniel R. Collins.

## Overview

Arena provides routines for simulating combat in a tabletop Fantasy Role-Playing Game (FRPG) similar to Original D&D or closely-related games. Combat is done as per "theater of the mind" without tracking exact spatial locations.

## Installation

```bash
cd python
pip install -e .
```

For development with testing:
```bash
pip install -e ".[dev]"
```

For notebook support:
```bash
pip install -e ".[notebooks]"
```

## Usage

### Command Line

Run the Arena simulation:
```bash
arena
```

Or use the Athena master program:
```bash
athena arena
```

### Options

```
arena [options]
  -? : Show help
  -y=N : Set number of years (default: 50)
  -f=N : Set fights per year (default: 12)
  -n=N : Set number of fighters (default: 100)
  -l=N : Set starting level (default: 1)
  -p=N : Set party size (default: 1)
  -a=N : Set armor type (0=none, 1=leather, 2=chain, 3=plate)
  -m : Fight man vs. monster
  -t : Use monster treasure types
  -r[sdktxy] : Set reporting options
```

### Python API

```python
from arena import Arena

# Create and configure simulation
sim = Arena()
sim.num_years = 10
sim.num_fighters = 50
sim.fight_man_vs_monster = True

# Run simulation
sim.run()
```

## Project Structure

```
python/
├── arena/              # Main package
│   ├── __init__.py
│   ├── dice.py        # Dice rolling mechanics
│   ├── enums.py       # Enumerations (Alignment, SpecialType, etc.)
│   ├── equipment.py   # Equipment, Armor, Weapon classes
│   ├── monster.py     # Monster base class
│   ├── character.py   # Character class (extends Monster)
│   ├── party.py       # Party management
│   ├── arena.py       # Main Arena simulation
│   └── athena.py      # Master wrapper program
├── notebooks/         # Jupyter notebooks
│   └── Arena.ipynb   # Original prototype notebook
├── tests/            # Test suite
├── setup.py          # Package setup
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## Features

### Implemented
- Dice rolling with standard notation (3d6, 2d8+3, etc.)
- Character and monster classes
- Basic equipment system (armor, weapons)
- Party management
- Basic arena simulation framework
- Command-line interface

### Planned
- Full combat system
- Monster database loading from CSV
- Treasure generation
- XP awards and leveling
- Spell system
- Marshal (random band generator)
- Monster Metrics (balance calculator)
- NPC Generator

## Development

The Python version is based on the Java implementation, with the following design principles:
- Maintain compatibility with original CSV data files
- Use Pythonic idioms where appropriate
- Keep the simulation logic consistent with the Java version
- Provide both CLI and programmatic API

## Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=arena
```

## License

GNU General Public License v3.0 - see LICENSE file

## Credits

Original Java implementation by Daniel R. Collins (dcollins@superdan.net)
Python port maintaining compatibility with original design

For more information, visit: http://www.oedgames.com
