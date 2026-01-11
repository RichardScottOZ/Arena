"""
Basic tests for the Arena package.
"""

import pytest
from arena import Dice, Character, Monster, Party, Arena
from arena.enums import Alignment, ArmorType, ClassType
from arena.equipment import Armor, Weapon


class TestDice:
    """Test dice rolling functionality."""
    
    def test_simple_dice(self):
        """Test simple dice creation and rolling."""
        d6 = Dice(1, 6)
        assert d6.get_sides() == 6
        assert d6.get_num() == 1
        
        roll = d6.roll()
        assert 1 <= roll <= 6
    
    def test_from_string(self):
        """Test parsing dice notation."""
        d = Dice.from_string("3d6")
        assert d.get_num() == 3
        assert d.get_sides() == 6
        
        d = Dice.from_string("2d8+3")
        assert d.get_num() == 2
        assert d.get_sides() == 8
        assert d.get_addition() == 3
    
    def test_max_min_roll(self):
        """Test max and min roll calculations."""
        d = Dice(3, 6, 1, 2)  # 3d6+2
        assert d.max_roll() == 20  # 18 + 2
        assert d.min_roll() == 5   # 3 + 2


class TestAlignment:
    """Test alignment enumeration."""
    
    def test_from_char(self):
        """Test alignment from character."""
        assert Alignment.from_char('L') == Alignment.LAWFUL
        assert Alignment.from_char('N') == Alignment.NEUTRAL
        assert Alignment.from_char('C') == Alignment.CHAOTIC
    
    def test_random_normal(self):
        """Test random alignment generation."""
        # Just ensure it doesn't crash
        align = Alignment.random_normal()
        assert align in [Alignment.LAWFUL, Alignment.NEUTRAL, Alignment.CHAOTIC]


class TestArmor:
    """Test armor equipment."""
    
    def test_create_armor(self):
        """Test armor creation."""
        armor = Armor.make_type(ArmorType.PLATE)
        assert armor.get_base_armor() == 6
        assert armor.is_metal()
    
    def test_armor_with_magic(self):
        """Test magical armor."""
        armor = Armor.make_type(ArmorType.CHAIN, magic_bonus=2)
        assert armor.get_armor_class() == 6  # 4 base + 2 bonus


class TestMonster:
    """Test monster class."""
    
    def test_create_monster(self):
        """Test basic monster creation."""
        monster = Monster("Orc", 6, 12)
        assert monster.get_race() == "Orc"
        assert monster.get_ac() == 6
        assert monster.is_alive()
    
    def test_take_damage(self):
        """Test damage and death."""
        monster = Monster("Goblin", 6, 12)
        initial_hp = monster.get_hp()
        
        still_alive = monster.take_damage(5)
        assert monster.get_hp() == initial_hp - 5
        
        # Kill it
        monster.take_damage(100)
        assert monster.is_dead()


class TestCharacter:
    """Test character class."""
    
    def test_create_character(self):
        """Test character creation."""
        char = Character("Bob", 1, ClassType.FIGHTER)
        assert char.name == "Bob"
        assert char.get_level() == 1
        assert char.is_alive()
    
    def test_ability_scores(self):
        """Test ability scores."""
        char = Character("Alice", 1, ClassType.FIGHTER)
        
        # Should have all abilities
        from arena.enums import Ability
        for ability in Ability:
            score = char.get_ability_score(ability)
            assert 3 <= score <= 18  # Normal range
    
    def test_equipment(self):
        """Test equipment management."""
        char = Character("Charlie", 1, ClassType.FIGHTER)
        
        armor = Armor.make_type(ArmorType.PLATE)
        char.set_armor(armor)
        assert char.get_armor() == armor


class TestParty:
    """Test party management."""
    
    def test_create_party(self):
        """Test party creation."""
        party = Party()
        assert party.is_empty()
        assert party.get_size() == 0
    
    def test_add_members(self):
        """Test adding members."""
        party = Party()
        
        char1 = Character("Fighter1", 1, ClassType.FIGHTER)
        char2 = Character("Fighter2", 2, ClassType.FIGHTER)
        
        party.add_member(char1)
        party.add_member(char2)
        
        assert party.get_size() == 2
        assert not party.is_empty()
    
    def test_living_and_dead(self):
        """Test tracking living and dead members."""
        party = Party()
        
        char1 = Character("Fighter1", 1, ClassType.FIGHTER)
        char2 = Character("Fighter2", 1, ClassType.FIGHTER)
        
        party.add_member(char1)
        party.add_member(char2)
        
        # Kill one
        char1.take_damage(100)
        
        assert party.num_living() == 1
        assert party.num_dead() == 1


class TestArena:
    """Test arena simulation."""
    
    def test_create_arena(self):
        """Test arena creation."""
        arena = Arena()
        assert arena.num_years == Arena.DEFAULT_NUM_YEARS
        assert arena.num_fighters == Arena.DEFAULT_NUM_FIGHTERS
    
    def test_parse_args(self):
        """Test argument parsing."""
        arena = Arena()
        arena.parse_args(['-n=50', '-y=10'])
        
        assert arena.num_fighters == 50
        assert arena.num_years == 10
    
    def test_recruit_fighters(self):
        """Test fighter recruitment."""
        arena = Arena()
        arena.num_fighters = 10
        
        arena.recruit_new_fighters()
        
        assert arena.fighter_list.get_size() == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
