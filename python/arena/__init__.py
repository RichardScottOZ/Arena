"""
Arena - Python Package for Simulating Original D&D Combat

This package provides routines for simulating combat in a tabletop 
Fantasy Role-Playing Game (FRPG) similar to Original D&D or 
closely-related games.

Based on the Java implementation by Daniel R. Collins (dcollins@superdan.net)
"""

__version__ = "0.1.0"
__author__ = "Daniel R. Collins"

# Import main classes for easy access
from .dice import Dice, set_random_seed
from .enums import Alignment, ArmorType, SpecialType, Ability, ClassType
from .equipment import Equipment, Armor, Weapon
from .monster import Monster, Attack
from .character import Character
from .party import Party
from .arena import Arena
from .athena import Athena

__all__ = [
    'Dice', 'set_random_seed',
    'Alignment', 'ArmorType', 'SpecialType', 'Ability', 'ClassType',
    'Equipment', 'Armor', 'Weapon',
    'Monster', 'Attack',
    'Character',
    'Party',
    'Arena',
    'Athena',
]
