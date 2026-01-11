"""
Monster and related classes for the Arena package.

Based on Monster.java by Daniel R. Collins (dcollins@superdan.net)
"""

from typing import Optional, Set, Dict, List
from .dice import Dice
from .enums import Alignment, SpecialType
import copy


class Attack:
    """
    Attack routine for a monster or character.
    """
    
    def __init__(self, num_attacks: int, damage_dice: str, attack_bonus: int = 0):
        """
        Initialize attack routine.
        
        Args:
            num_attacks: Number of attacks per round
            damage_dice: Dice notation for damage per attack
            attack_bonus: Bonus to hit
        """
        self.num_attacks = num_attacks
        self.damage_dice = damage_dice
        self.attack_bonus = attack_bonus
    
    def get_num_attacks(self) -> int:
        """Get number of attacks."""
        return self.num_attacks
    
    def get_damage_dice(self) -> str:
        """Get damage dice notation."""
        return self.damage_dice
    
    def get_attack_bonus(self) -> int:
        """Get attack bonus."""
        return self.attack_bonus
    
    def __str__(self) -> str:
        return f"{self.num_attacks} attacks, {self.damage_dice}"


class Monster:
    """
    Monster (hostile or benign creature).
    """
    
    # Constants
    BASE_HIT_DIE = 6
    MAX_MELEERS = 6
    UNDEFINED_EHD = -1
    
    def __init__(self, race: str = "", armor_class: int = 10, 
                 move_inches: int = 12, hit_dice: Optional[Dice] = None,
                 attack: Optional[Attack] = None):
        """
        Initialize a monster.
        
        Args:
            race: Name/type of the monster
            armor_class: Armor class (lower is better)
            move_inches: Movement rate in inches
            hit_dice: Hit dice for the monster
            attack: Attack routine
        """
        # Basic attributes
        self.race = race
        self.source_book = ""
        self.mon_type = ""
        self.environment = ""
        self.number_appearing = ""
        self.armor_class = armor_class
        self.move_inches = move_inches
        self.hit_dice = hit_dice or Dice(1, self.BASE_HIT_DIE)
        self.in_lair_pct = 0
        self.treasure_type = ""
        self.attack = attack or Attack(1, "1d6")
        self.alignment = Alignment.NEUTRAL
        
        # Derived attributes
        self.hit_dice_as_float = 0.0
        self.equivalent_hit_dice = self.hit_dice.get_num()
        self.hit_points = 0
        self.max_hit_points = 0
        self.dragon_age = 0
        self.breath_charges = 0
        
        # Combat tracking
        self.kill_tally = 0
        self.times_meleed = 0
        self.host: Optional[Monster] = None
        
        # Special abilities
        self.special_list: Set[SpecialType] = set()
        self.condition_list: Set[SpecialType] = set()
        self.special_values: Dict[SpecialType, int] = {}
        self.spell_memory = None
        
        # Roll initial hit points
        self.roll_hit_points()
    
    def roll_hit_points(self):
        """Roll hit points for this monster."""
        self.hit_points = self.hit_dice.roll()
        self.max_hit_points = self.hit_points
    
    def heal_fully(self):
        """Restore to maximum hit points."""
        self.hit_points = self.max_hit_points
    
    def take_damage(self, damage: int) -> bool:
        """
        Take damage.
        
        Args:
            damage: Amount of damage to take
            
        Returns:
            True if still alive, False if dead
        """
        self.hit_points -= damage
        return self.hit_points > 0
    
    def is_alive(self) -> bool:
        """Check if the monster is alive."""
        return self.hit_points > 0
    
    def is_dead(self) -> bool:
        """Check if the monster is dead."""
        return self.hit_points <= 0
    
    # Accessors
    def get_race(self) -> str:
        return self.race
    
    def get_armor_class(self) -> int:
        return self.armor_class
    
    def get_ac(self) -> int:
        """Shortcut for armor class."""
        return self.armor_class
    
    def get_hit_points(self) -> int:
        return self.hit_points
    
    def get_hp(self) -> int:
        """Shortcut for hit points."""
        return self.hit_points
    
    def get_max_hit_points(self) -> int:
        return self.max_hit_points
    
    def get_hit_dice(self) -> Dice:
        return self.hit_dice
    
    def get_hit_dice_num(self) -> int:
        return self.hit_dice.get_num()
    
    def get_hd(self) -> int:
        """Shortcut for hit dice number."""
        return self.get_hit_dice_num()
    
    def get_level(self) -> int:
        """Get the effective level (same as HD for monsters)."""
        return self.get_hit_dice_num()
    
    def get_move_inches(self) -> int:
        return self.move_inches
    
    def get_mv(self) -> int:
        """Shortcut for movement."""
        return self.move_inches
    
    def get_alignment(self) -> Alignment:
        return self.alignment
    
    def get_attack(self) -> Attack:
        return self.attack
    
    def get_equivalent_hit_dice(self) -> int:
        return self.equivalent_hit_dice
    
    def get_ehd(self) -> int:
        """Shortcut for equivalent hit dice."""
        return self.equivalent_hit_dice
    
    def get_treasure_type(self) -> str:
        return self.treasure_type
    
    def get_kill_tally(self) -> int:
        return self.kill_tally
    
    def get_times_meleed(self) -> int:
        return self.times_meleed
    
    def get_host(self) -> Optional['Monster']:
        return self.host
    
    # Mutators
    def set_alignment(self, alignment: Alignment):
        self.alignment = alignment
    
    def inc_kill_tally(self):
        """Increment kill count."""
        self.kill_tally += 1
    
    def clear_times_meleed(self):
        """Reset times meleed counter."""
        self.times_meleed = 0
    
    def inc_times_meleed(self):
        """Increment times meleed counter."""
        self.times_meleed += 1
    
    # Special abilities
    def has_special(self, special: SpecialType) -> bool:
        """Check if monster has a special ability."""
        return special in self.special_list
    
    def add_special(self, special: SpecialType, value: Optional[int] = None):
        """Add a special ability."""
        self.special_list.add(special)
        if value is not None:
            self.special_values[special] = value
    
    def get_special_value(self, special: SpecialType) -> int:
        """Get the value associated with a special ability."""
        return self.special_values.get(special, 0)
    
    # Null methods for Character inheritance
    def get_armor(self):
        """Get armor (for Character compatibility)."""
        return None
    
    def get_shield(self):
        """Get shield (for Character compatibility)."""
        return None
    
    def get_weapon(self):
        """Get weapon (for Character compatibility)."""
        return None
    
    def set_armor(self, armor):
        """Set armor (no-op for Monster)."""
        pass
    
    def draw_best_weapon(self, opponent):
        """Draw best weapon (no-op for Monster)."""
        pass
    
    def sheathe_weapon(self):
        """Sheathe weapon (no-op for Monster)."""
        pass
    
    def boost_magic_items_one_level(self):
        """Boost magic items (no-op for Monster)."""
        pass
    
    def has_null_ability_score(self) -> bool:
        """Check for null ability score (always False for Monster)."""
        return False
    
    def has_feat(self, feat) -> bool:
        """Check for feat (always False for Monster)."""
        return False
    
    def get_spell_list(self):
        """Get spell list (None for Monster)."""
        return None
    
    def add_xp(self, xp: int):
        """Add experience (no-op for Monster)."""
        pass
    
    def get_sweep_rate(self) -> int:
        """Get sweep attack rate (0 for Monster)."""
        return 0
    
    def copy(self) -> 'Monster':
        """Create a deep copy of this monster."""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.race} (HD {self.get_hd()}, AC {self.armor_class}, HP {self.hit_points})"
    
    def __repr__(self) -> str:
        return f"Monster({self.race!r}, {self.armor_class}, {self.move_inches}, {self.hit_dice!r})"
