"""
Equipment classes for the Arena package.

Based on Equipment.java, Armor.java, and Weapon.java
"""

from typing import Optional
from .enums import ArmorType
import copy


class Equipment:
    """
    Base class for equipment items.
    """
    
    MAX_MAGIC_BONUS = 5
    
    def __init__(self, name: str, magic_bonus: int = 0, weight: int = 0):
        """
        Initialize equipment.
        
        Args:
            name: Name of the equipment
            magic_bonus: Magic bonus (0 for non-magical)
            weight: Weight of the equipment
        """
        self.name = name
        self.magic_bonus = min(magic_bonus, self.MAX_MAGIC_BONUS)
        self.weight = weight
    
    def set_magic_bonus(self, bonus: int):
        """Set the magic bonus, capped at MAX_MAGIC_BONUS."""
        self.magic_bonus = min(bonus, self.MAX_MAGIC_BONUS)
    
    def inc_magic_bonus(self):
        """Increment the magic bonus by 1."""
        self.set_magic_bonus(self.magic_bonus + 1)
    
    def get_magic_bonus(self) -> int:
        """Get the magic bonus."""
        return self.magic_bonus
    
    def get_weight(self) -> int:
        """Get the weight."""
        return self.weight
    
    def __str__(self) -> str:
        """String representation."""
        if self.magic_bonus > 0:
            return f"{self.name} +{self.magic_bonus}"
        elif self.magic_bonus < 0:
            return f"{self.name} {self.magic_bonus}"
        return self.name
    
    def copy(self):
        """Create a deep copy of this equipment."""
        return copy.deepcopy(self)


class Armor(Equipment):
    """
    Armor equipment.
    """
    
    def __init__(self, armor_type: ArmorType, base_armor: int, 
                 weight: int = 0, magic_bonus: int = 0):
        """
        Initialize armor.
        
        Args:
            armor_type: Type of armor
            base_armor: Base armor class value
            weight: Weight of the armor
            magic_bonus: Magic bonus
        """
        self.armor_type = armor_type
        self.base_armor = base_armor
        super().__init__(armor_type.name.title(), magic_bonus, weight)
    
    def get_armor_type(self) -> ArmorType:
        """Get the armor type."""
        return self.armor_type
    
    def get_base_armor(self) -> int:
        """Get the base armor value."""
        return self.base_armor
    
    def get_armor_class(self) -> int:
        """
        Get the total armor class.
        
        Returns:
            Base armor plus magic bonus
        """
        return self.base_armor + self.magic_bonus
    
    def is_metal(self) -> bool:
        """Check if this armor is made of metal."""
        return self.armor_type in (ArmorType.PLATE, ArmorType.CHAIN)
    
    def is_shield(self) -> bool:
        """Check if this is a shield."""
        return self.armor_type == ArmorType.SHIELD
    
    @classmethod
    def make_type(cls, armor_type: ArmorType, magic_bonus: int = 0) -> 'Armor':
        """
        Factory method to create standard armor of a given type.
        
        Args:
            armor_type: Type of armor to create
            magic_bonus: Magic bonus to apply
            
        Returns:
            New Armor instance
        """
        if armor_type == ArmorType.PLATE:
            return cls(armor_type, 6, 4, magic_bonus)
        elif armor_type == ArmorType.CHAIN:
            return cls(armor_type, 4, 2, magic_bonus)
        elif armor_type == ArmorType.LEATHER:
            return cls(armor_type, 2, 1, magic_bonus)
        elif armor_type == ArmorType.SHIELD:
            return cls(armor_type, 1, 1, magic_bonus)
        else:
            raise ValueError(f"Unknown armor type: {armor_type}")


class Weapon(Equipment):
    """
    Weapon equipment.
    """
    
    def __init__(self, name: str, damage_dice: str, weight: int = 0, 
                 magic_bonus: int = 0, is_magic: bool = False):
        """
        Initialize weapon.
        
        Args:
            name: Name of the weapon
            damage_dice: Dice notation for damage (e.g., "1d8")
            weight: Weight of the weapon
            magic_bonus: Magic bonus to hit and damage
            is_magic: Whether this is a magical weapon
        """
        super().__init__(name, magic_bonus, weight)
        self.damage_dice = damage_dice
        self.is_magic = is_magic or (magic_bonus > 0)
    
    def get_damage_dice(self) -> str:
        """Get the damage dice notation."""
        return self.damage_dice
    
    def is_magical(self) -> bool:
        """Check if this weapon is magical."""
        return self.is_magic
    
    def get_to_hit_bonus(self) -> int:
        """Get the to-hit bonus."""
        return self.magic_bonus
    
    def get_damage_bonus(self) -> int:
        """Get the damage bonus."""
        return self.magic_bonus
    
    @classmethod
    def create_sword(cls, magic_bonus: int = 0) -> 'Weapon':
        """Create a standard sword."""
        return cls("Sword", "1d8", 1, magic_bonus)
    
    @classmethod
    def create_axe(cls, magic_bonus: int = 0) -> 'Weapon':
        """Create a standard axe."""
        return cls("Axe", "1d8", 1, magic_bonus)
    
    @classmethod
    def create_spear(cls, magic_bonus: int = 0) -> 'Weapon':
        """Create a standard spear."""
        return cls("Spear", "1d6", 1, magic_bonus)
    
    @classmethod
    def create_dagger(cls, magic_bonus: int = 0) -> 'Weapon':
        """Create a standard dagger."""
        return cls("Dagger", "1d4", 0, magic_bonus)
