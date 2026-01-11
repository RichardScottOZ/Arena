"""
Party management for groups of characters or monsters.

Based on Party.java by Daniel R. Collins (dcollins@superdan.net)
"""

from typing import List, Optional
from .monster import Monster
from .character import Character
import random


class Party:
    """
    Party of characters or monsters.
    """
    
    def __init__(self):
        """Initialize an empty party."""
        self.members: List[Monster] = []
    
    def add_member(self, member: Monster):
        """
        Add a member to the party.
        
        Args:
            member: Character or Monster to add
        """
        self.members.append(member)
    
    def remove_member(self, member: Monster):
        """
        Remove a member from the party.
        
        Args:
            member: Member to remove
        """
        if member in self.members:
            self.members.remove(member)
    
    def get_members(self) -> List[Monster]:
        """Get all party members."""
        return self.members
    
    def get_size(self) -> int:
        """Get the number of members in the party."""
        return len(self.members)
    
    def is_empty(self) -> bool:
        """Check if the party is empty."""
        return len(self.members) == 0
    
    def get_living_members(self) -> List[Monster]:
        """Get all living party members."""
        return [m for m in self.members if m.is_alive()]
    
    def get_dead_members(self) -> List[Monster]:
        """Get all dead party members."""
        return [m for m in self.members if m.is_dead()]
    
    def num_living(self) -> int:
        """Get count of living members."""
        return len(self.get_living_members())
    
    def num_dead(self) -> int:
        """Get count of dead members."""
        return len(self.get_dead_members())
    
    def all_dead(self) -> bool:
        """Check if all members are dead."""
        return self.num_living() == 0
    
    def any_alive(self) -> bool:
        """Check if any members are alive."""
        return self.num_living() > 0
    
    def shuffle_members(self):
        """Randomly shuffle the order of party members."""
        random.shuffle(self.members)
    
    def bring_out_your_dead(self) -> List[Monster]:
        """
        Remove and return dead members.
        
        Returns:
            List of dead members that were removed
        """
        dead = self.get_dead_members()
        self.members = self.get_living_members()
        return dead
    
    def clear_fallen(self):
        """Remove all dead members from the party."""
        self.bring_out_your_dead()
    
    def heal_all(self):
        """Heal all party members to full health."""
        for member in self.members:
            member.heal_fully()
    
    def clear_all_times_meleed(self):
        """Clear the times meleed counter for all members."""
        for member in self.members:
            member.clear_times_meleed()
    
    def get_random_member(self) -> Optional[Monster]:
        """
        Get a random living member.
        
        Returns:
            Random living member, or None if party is empty
        """
        living = self.get_living_members()
        if not living:
            return None
        return random.choice(living)
    
    def get_average_level(self) -> float:
        """
        Get the average level of all party members.
        
        Returns:
            Average level, or 0 if party is empty
        """
        if not self.members:
            return 0.0
        return sum(m.get_level() for m in self.members) / len(self.members)
    
    def get_total_hit_points(self) -> int:
        """Get total current hit points of all living members."""
        return sum(m.get_hit_points() for m in self.get_living_members())
    
    def get_total_max_hit_points(self) -> int:
        """Get total maximum hit points of all members."""
        return sum(m.get_max_hit_points() for m in self.members)
    
    def get_highest_level_member(self) -> Optional[Monster]:
        """
        Get the highest level member.
        
        Returns:
            Highest level member, or None if party is empty
        """
        if not self.members:
            return None
        return max(self.members, key=lambda m: m.get_level())
    
    def sort_by_level(self, reverse: bool = True):
        """
        Sort party members by level.
        
        Args:
            reverse: If True, sort highest to lowest (default)
        """
        self.members.sort(key=lambda m: m.get_level(), reverse=reverse)
    
    def __len__(self) -> int:
        """Get number of members."""
        return len(self.members)
    
    def __iter__(self):
        """Iterate over party members."""
        return iter(self.members)
    
    def __str__(self) -> str:
        """String representation."""
        if not self.members:
            return "Empty party"
        
        living = self.num_living()
        total = len(self.members)
        avg_level = self.get_average_level()
        
        return f"Party of {total} ({living} alive, avg level {avg_level:.1f})"
    
    def __repr__(self) -> str:
        return f"Party({len(self.members)} members)"
