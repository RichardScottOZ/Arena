"""
Character class for player and non-player characters.

Based on Character.java by Daniel R. Collins (dcollins@superdan.net)
"""

from typing import Optional, Dict, List
from .monster import Monster, Attack
from .dice import Dice
from .enums import Ability, Alignment, ClassType
from .equipment import Armor, Weapon
import random


class Character(Monster):
    """
    One character (player or non-player personae).
    """
    
    # Constants
    BASE_AGE = 18
    BASE_ARMOR_CLASS = 9
    BASE_MOVEMENT = 12
    BASE_HD = Dice(1, 6)
    BASE_MAGIC_PER_LEVEL = 5
    
    # Ability dice options
    ABILITY_DICE = [
        Dice(3, 6),           # 3d6
        Dice(2, 6, 1, 6),     # 2d6+6
        Dice(2, 4, 1, 10),    # 2d4+10
        Dice(2, 3, 1, 12),    # 2d3+12
    ]
    
    def __init__(self, name: str = "", level: int = 1, 
                 class_type: ClassType = ClassType.FIGHTER):
        """
        Initialize a character.
        
        Args:
            name: Character name
            level: Starting level
            class_type: Character class
        """
        # Initialize as Monster first
        super().__init__(
            race=f"{class_type.value} {level}",
            armor_class=self.BASE_ARMOR_CLASS,
            move_inches=self.BASE_MOVEMENT,
            hit_dice=Dice(level, 6),
            attack=Attack(1, "1d8")
        )
        
        # Character-specific attributes
        self.name = name
        self.age = self.BASE_AGE
        self.class_type = class_type
        self.level = level
        
        # Ability scores
        self.ability_scores: Dict[Ability, int] = {}
        self.ability_score_damage: Dict[Ability, int] = {}
        self.roll_ability_scores()
        
        # Equipment
        self.armor_worn: Optional[Armor] = None
        self.shield_held: Optional[Armor] = None
        self.weapon_in_hand: Optional[Weapon] = None
        self.ring_worn = None
        self.wand_held = None
        self.equip_list: List = []
        
        # Class tracking
        self.experience_points = 0
        
        # Combat attributes
        self.sweep_rate = 0
        
        # Personality
        self.primary_personality = None
        self.secondary_personality = None
        
        # Roll hit points
        self.roll_hit_points()
    
    def roll_ability_scores(self, dice_option: int = 0):
        """
        Roll ability scores.
        
        Args:
            dice_option: Index into ABILITY_DICE (0-3), default is 3d6
        """
        dice = self.ABILITY_DICE[dice_option]
        for ability in Ability:
            self.ability_scores[ability] = dice.roll()
            self.ability_score_damage[ability] = 0
    
    def get_ability_score(self, ability: Ability) -> int:
        """Get an ability score."""
        base = self.ability_scores.get(ability, 10)
        damage = self.ability_score_damage.get(ability, 0)
        return max(0, base - damage)
    
    def get_ability_modifier(self, ability: Ability) -> int:
        """
        Get the modifier for an ability score.
        
        Uses standard OD&D modifiers:
        3-8: -1, 9-12: 0, 13-18: +1
        """
        score = self.get_ability_score(ability)
        if score <= 8:
            return -1
        elif score <= 12:
            return 0
        else:
            return 1
    
    def take_ability_damage(self, ability: Ability, damage: int):
        """Take ability score damage."""
        current = self.ability_score_damage.get(ability, 0)
        self.ability_score_damage[ability] = current + damage
    
    def zero_ability_damage(self):
        """Clear all ability damage."""
        for ability in Ability:
            self.ability_score_damage[ability] = 0
    
    def has_null_ability_score(self) -> bool:
        """Check if any ability score is 0."""
        for ability in Ability:
            if self.get_ability_score(ability) <= 0:
                return True
        return False
    
    # Equipment methods
    def get_armor(self) -> Optional[Armor]:
        """Get worn armor."""
        return self.armor_worn
    
    def get_shield(self) -> Optional[Armor]:
        """Get held shield."""
        return self.shield_held
    
    def get_weapon(self) -> Optional[Weapon]:
        """Get weapon in hand."""
        return self.weapon_in_hand
    
    def set_armor(self, armor: Optional[Armor]):
        """Set worn armor."""
        self.armor_worn = armor
        self.update_armor_class()
    
    def set_shield(self, shield: Optional[Armor]):
        """Set held shield."""
        self.shield_held = shield
        self.update_armor_class()
    
    def set_weapon(self, weapon: Optional[Weapon]):
        """Set weapon in hand."""
        self.weapon_in_hand = weapon
    
    def update_armor_class(self):
        """
        Update armor class based on equipment.
        
        Note: In D&D, lower AC is better. Base AC is 9, and armor/dexterity
        reduce the AC value (e.g., plate armor -6 gives AC 3).
        """
        ac = self.BASE_ARMOR_CLASS
        
        if self.armor_worn:
            ac -= self.armor_worn.get_armor_class()
        
        if self.shield_held:
            ac -= self.shield_held.get_armor_class()
        
        # Add dexterity bonus (positive modifier reduces AC)
        dex_mod = self.get_ability_modifier(Ability.DEXTERITY)
        ac -= dex_mod
        
        self.armor_class = ac
    
    def draw_best_weapon(self, opponent: Monster):
        """Draw the best weapon for the opponent (simple implementation)."""
        # For now, just ensure we have a weapon
        if not self.weapon_in_hand:
            self.weapon_in_hand = Weapon.create_sword()
    
    def sheathe_weapon(self):
        """Sheathe current weapon."""
        self.weapon_in_hand = None
    
    # Experience and leveling
    def add_xp(self, xp: int):
        """
        Add experience points.
        
        Args:
            xp: Experience points to add
        """
        self.experience_points += xp
    
    def get_xp(self) -> int:
        """Get total experience points."""
        return self.experience_points
    
    def get_level(self) -> int:
        """Get character level."""
        return self.level
    
    def level_up(self):
        """Increase character level."""
        self.level += 1
        self.hit_dice = Dice(self.level, 6)
        self.roll_hit_points()
    
    # Override Monster methods
    def get_sweep_rate(self) -> int:
        """Get sweep attack rate."""
        return self.sweep_rate
    
    def __str__(self) -> str:
        """String representation."""
        return (f"{self.name} ({self.class_type.value} {self.level}, "
                f"AC {self.armor_class}, HP {self.hit_points}/{self.max_hit_points})")
    
    def __repr__(self) -> str:
        return f"Character({self.name!r}, {self.level}, {self.class_type})"
