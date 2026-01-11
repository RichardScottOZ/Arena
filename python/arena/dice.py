"""
Dice rolling mechanics for the Arena package.

Based on Dice.java by Daniel R. Collins (dcollins@superdan.net)
"""

import random
import re
from typing import Optional


class Dice:
    """
    Dice group for random rolls.
    
    Supports standard dice notation parsing: e.g., "3d6", "2d8+3", "1d20*2"
    """
    
    def __init__(self, number: int = 1, sides: int = 6, 
                 multiplier: int = 1, addition: int = 0):
        """
        Initialize a dice group.
        
        Args:
            number: Number of dice to roll
            sides: Number of sides on each die
            multiplier: Multiplier to apply to roll (negative = divisor)
            addition: Addition to the roll (negative = subtraction)
        """
        self.number = number
        self.sides = sides
        self.multiplier = multiplier
        self.addition = addition
        
    @classmethod
    def from_string(cls, dice_str: str) -> 'Dice':
        """
        Parse a dice string and create a Dice object.
        
        Supports formats like: "d6", "3d6", "2d8+3", "1d20*2", "4d6/2"
        
        Args:
            dice_str: String descriptor of dice roll
            
        Returns:
            Dice object parsed from string
        """
        # Pattern to match dice notation
        # Group 1: number of dice (optional)
        # Group 2: sides
        # Group 3: multiplier symbol (* or /)
        # Group 4: multiplier value
        # Group 5: addition symbol (+ or -)
        # Group 6: addition value
        pattern = r'(\d*)d(\d+)(?:([*/])(\d+))?(?:([+\-])(\d+))?'
        match = re.match(pattern, dice_str.strip(), re.IGNORECASE)
        
        if not match:
            raise ValueError(f"Invalid dice notation: {dice_str}")
            
        groups = match.groups()
        
        # Parse number of dice (default to 1)
        number = int(groups[0]) if groups[0] else 1
        
        # Parse sides
        sides = int(groups[1])
        
        # Parse multiplier
        multiplier = 1
        if groups[2] and groups[3]:
            mul_value = int(groups[3])
            if groups[2] == '*':
                multiplier = mul_value
            elif groups[2] == '/':
                multiplier = -mul_value  # Negative indicates division
        
        # Parse addition
        addition = 0
        if groups[4] and groups[5]:
            add_value = int(groups[5])
            if groups[4] == '+':
                addition = add_value
            elif groups[4] == '-':
                addition = -add_value
                
        return cls(number, sides, multiplier, addition)
    
    def roll(self) -> int:
        """
        Roll the dice and return the result.
        
        Returns:
            Integer result of the dice roll
        """
        result = sum(random.randint(1, self.sides) for _ in range(self.number))
        
        # Apply multiplier
        if self.multiplier > 0:
            result *= self.multiplier
        elif self.multiplier < 0:
            result //= abs(self.multiplier)  # Integer division
            
        # Apply addition
        result += self.addition
        
        return max(result, 0)  # Ensure non-negative
    
    def get_num(self) -> int:
        """Get the number of dice."""
        return self.number
    
    def get_sides(self) -> int:
        """Get the number of sides."""
        return self.sides
    
    def get_multiplier(self) -> int:
        """Get the multiplier."""
        return self.multiplier
    
    def get_addition(self) -> int:
        """Get the addition."""
        return self.addition
    
    def max_roll(self) -> int:
        """
        Calculate the maximum possible roll.
        
        Returns:
            Maximum possible value
        """
        result = self.number * self.sides
        
        if self.multiplier > 0:
            result *= self.multiplier
        elif self.multiplier < 0:
            result //= abs(self.multiplier)
            
        result += self.addition
        
        return max(result, 0)
    
    def min_roll(self) -> int:
        """
        Calculate the minimum possible roll.
        
        Returns:
            Minimum possible value
        """
        result = self.number  # Minimum is 1 per die
        
        if self.multiplier > 0:
            result *= self.multiplier
        elif self.multiplier < 0:
            result //= abs(self.multiplier)
            
        result += self.addition
        
        return max(result, 0)
    
    def __str__(self) -> str:
        """String representation of the dice."""
        s = f"{self.number}d{self.sides}"
        
        if self.multiplier != 1:
            if self.multiplier > 0:
                s += f"*{self.multiplier}"
            else:
                s += f"/{abs(self.multiplier)}"
        
        if self.addition != 0:
            if self.addition > 0:
                s += f"+{self.addition}"
            else:
                s += f"{self.addition}"  # Negative already has sign
                
        return s
    
    def __repr__(self) -> str:
        return f"Dice({self.number}, {self.sides}, {self.multiplier}, {self.addition})"


def set_random_seed(seed: Optional[int] = None):
    """Set the random seed for reproducible dice rolls."""
    random.seed(seed)
