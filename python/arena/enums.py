"""
Enumerations used throughout the Arena package.

Based on Java enums from the original implementation.
"""

from enum import Enum
import random


class Alignment(Enum):
    """Character and monster alignment."""
    LAWFUL = "L"
    NEUTRAL = "N"
    CHAOTIC = "C"
    
    @classmethod
    def from_char(cls, c: str) -> 'Alignment':
        """
        Convert a letter to alignment.
        
        Args:
            c: Character code ('L', 'N', or 'C')
            
        Returns:
            Corresponding Alignment
        """
        c = c.upper()
        if c in ('L', 'LAWFUL'):
            return cls.LAWFUL
        elif c in ('N', 'NEUTRAL'):
            return cls.NEUTRAL
        elif c in ('C', 'CHAOTIC'):
            return cls.CHAOTIC
        else:
            raise ValueError(f"Invalid alignment character: {c}")
    
    @classmethod
    def random_normal(cls) -> 'Alignment':
        """
        Randomize a normally-distributed alignment.
        
        Distribution: Lawful 1/6, Neutral 4/6, Chaotic 1/6
        
        Returns:
            Random Alignment
        """
        roll = random.randint(1, 6)
        if 2 <= roll <= 5:
            return cls.NEUTRAL
        elif roll == 1:
            return cls.LAWFUL
        else:  # roll == 6
            return cls.CHAOTIC
    
    @classmethod
    def random_uniform(cls) -> 'Alignment':
        """
        Randomize a uniformly-distributed alignment.
        
        Returns:
            Random Alignment with equal probability
        """
        roll = random.randint(1, 6)
        if 1 <= roll <= 2:
            return cls.LAWFUL
        elif 3 <= roll <= 4:
            return cls.NEUTRAL
        else:  # 5-6
            return cls.CHAOTIC
    
    @classmethod
    def random_lawful(cls) -> 'Alignment':
        """
        Randomize a Lawful-biased alignment.
        
        Distribution: Lawful 4/6, Neutral 2/6
        
        Returns:
            Random Alignment biased toward Lawful
        """
        roll = random.randint(1, 6)
        if 1 <= roll <= 4:
            return cls.LAWFUL
        else:
            return cls.NEUTRAL
    
    @classmethod
    def random_chaotic(cls) -> 'Alignment':
        """
        Randomize a Chaotic-biased alignment.
        
        Distribution: Neutral 2/6, Chaotic 4/6
        
        Returns:
            Random Alignment biased toward Chaotic
        """
        roll = random.randint(1, 6)
        if 1 <= roll <= 2:
            return cls.NEUTRAL
        else:
            return cls.CHAOTIC


class ArmorType(Enum):
    """Types of armor."""
    PLATE = 1
    CHAIN = 2
    LEATHER = 3
    SHIELD = 4


class EnergyType(Enum):
    """Types of energy for breath weapons and resistances."""
    FIRE = 1
    COLD = 2
    LIGHTNING = 3
    ACID = 4
    POISON = 5


class SpecialType(Enum):
    """Special abilities for monsters and characters."""
    NPC = 1
    POISON = 2
    PARALYSIS = 3
    PETRIFICATION = 4
    BLOOD_DRAIN = 5
    ENERGY_DRAIN = 6
    CONSTRICTION = 7
    CORROSION = 8
    IMMOLATION = 9
    ROTTING = 10
    SWALLOWING = 11
    SILVER_TO_HIT = 12
    MAGIC_TO_HIT = 13
    CHOP_IMMUNITY = 14
    DAMAGE_REDUCTION = 15
    MULTIHEADS = 16
    BERSERKING = 17
    HIT_BONUS = 18
    INVISIBILITY = 19
    DETECTION = 20
    GRABBING = 21
    SPORE_CLOUD = 22
    ROCK_HURLING = 23
    TAIL_SPIKES = 24
    CHARM = 25
    FEAR = 26
    SAVE_BONUS = 27
    DODGE_GIANTS = 28
    REGENERATION = 29
    STRENGTH_DRAIN = 30
    ABSORPTION = 31
    WHIRLWIND = 32
    WALL_OF_FIRE = 33
    CONE_OF_COLD = 34
    ACID_SPITTING = 35
    CONFUSION = 36
    DISPLACEMENT = 37
    BLINKING = 38
    PHASING = 39
    CHARM_TOUCH = 40
    DRAGON = 41
    FIRE_BREATH = 42
    COLD_BREATH = 43
    VOLT_BREATH = 44
    ACID_BREATH = 45
    POISON_BREATH = 46
    PETRIFYING_BREATH = 47
    PETRIFYING_GAZE = 48
    SUMMON_VERMIN = 49
    SUMMON_TREES = 50
    MIND_BLAST = 51
    BRAIN_CONSUMPTION = 52
    SAPPING_STRANDS = 53
    SLOWING = 54
    FIRE_IMMUNITY = 55
    COLD_IMMUNITY = 56
    ACID_IMMUNITY = 57
    VOLT_IMMUNITY = 58
    STEAM_BREATH = 59
    STENCH = 60
    RESIST_STENCH = 61
    WEBS = 62
    WEB_MOVE = 63
    SLEEP = 64
    HOLD = 65
    BLINDNESS = 66
    POLYMORPHISM = 67
    UNDEAD = 68
    GOLEM = 69
    DEATH = 70
    SPELLS = 71
    MANY_EYE_FUNCTIONS = 72
    MAGIC_RESISTANCE = 73
    MAGIC_IMMUNITY = 74
    UNDEAD_IMMUNITY = 75
    FEARLESSNESS = 76
    PROTECTION_FROM_EVIL = 77
    
    @classmethod
    def find_by_name(cls, name: str) -> 'SpecialType':
        """
        Find a SpecialType by name.
        
        Args:
            name: Name of the special type (case-insensitive)
            
        Returns:
            Corresponding SpecialType
            
        Raises:
            ValueError: If name not found
        """
        name_upper = name.upper().replace(' ', '_')
        for special_type in cls:
            if special_type.name == name_upper:
                return special_type
        raise ValueError(f"Unknown special type: {name}")


class Ability(Enum):
    """Character ability scores."""
    STRENGTH = "STR"
    INTELLIGENCE = "INT"
    WISDOM = "WIS"
    DEXTERITY = "DEX"
    CONSTITUTION = "CON"
    CHARISMA = "CHA"


class ClassType(Enum):
    """Character class types."""
    FIGHTER = "Fighter"
    WIZARD = "Wizard"
    THIEF = "Thief"
    ELF = "Elf"
    DWARF = "Dwarf"
    HALFLING = "Halfling"
