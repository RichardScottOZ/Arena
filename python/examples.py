#!/usr/bin/env python
"""
Example script demonstrating Arena Python API usage.
"""

from arena import Arena, Character, Party, Dice
from arena.enums import ClassType, Alignment, ArmorType
from arena.equipment import Armor, Weapon


def example_dice_rolling():
    """Demonstrate dice rolling."""
    print("=== Dice Rolling Examples ===")
    
    # Simple dice
    d6 = Dice(1, 6)
    print(f"1d6: {d6.roll()}")
    
    # Multiple dice
    d3d6 = Dice(3, 6)
    print(f"3d6: {d3d6.roll()}")
    
    # Dice from string
    damage = Dice.from_string("2d8+3")
    print(f"2d8+3: {damage.roll()}")
    
    print()


def example_character_creation():
    """Demonstrate character creation."""
    print("=== Character Creation ===")
    
    # Create a fighter
    fighter = Character("Conan", 5, ClassType.FIGHTER)
    print(f"Created: {fighter}")
    
    # Equip the fighter
    fighter.set_armor(Armor.make_type(ArmorType.PLATE, magic_bonus=1))
    fighter.set_weapon(Weapon.create_sword(magic_bonus=2))
    
    print(f"After equipment:")
    print(f"  AC: {fighter.get_ac()}")
    print(f"  Armor: {fighter.get_armor()}")
    print(f"  Weapon: {fighter.get_weapon()}")
    
    # Show ability scores
    from arena.enums import Ability
    print(f"  STR: {fighter.get_ability_score(Ability.STRENGTH)}")
    print(f"  DEX: {fighter.get_ability_score(Ability.DEXTERITY)}")
    
    print()


def example_party_management():
    """Demonstrate party management."""
    print("=== Party Management ===")
    
    # Create a party
    party = Party()
    
    # Add members
    for i in range(4):
        char = Character(f"Fighter{i+1}", level=i+1, class_type=ClassType.FIGHTER)
        party.add_member(char)
    
    print(f"Party: {party}")
    print(f"Members: {party.get_size()}")
    print(f"Average level: {party.get_average_level():.1f}")
    
    # Simulate some damage
    members = party.get_members()
    members[0].take_damage(100)  # Kill first member
    
    print(f"After combat:")
    print(f"  Living: {party.num_living()}")
    print(f"  Dead: {party.num_dead()}")
    
    print()


def example_simple_simulation():
    """Run a simple arena simulation."""
    print("=== Simple Arena Simulation ===")
    
    arena = Arena()
    
    # Configure for a quick test
    arena.num_years = 2
    arena.fights_per_year = 3
    arena.num_fighters = 10
    arena.start_level = 1
    arena.report_year_end = True
    
    # Run simulation
    arena.run()
    
    print()


def example_custom_simulation():
    """Create a custom simulation with manual control."""
    print("=== Custom Simulation ===")
    
    # Create two fighters
    fighter1 = Character("Alice", 3, ClassType.FIGHTER)
    fighter1.set_armor(Armor.make_type(ArmorType.CHAIN))
    fighter1.set_weapon(Weapon.create_sword())
    
    fighter2 = Character("Bob", 3, ClassType.FIGHTER)
    fighter2.set_armor(Armor.make_type(ArmorType.PLATE))
    fighter2.set_weapon(Weapon.create_axe())
    
    print(f"{fighter1}")
    print(f"{fighter2}")
    print()
    
    # Simple combat
    print("Beginning combat...")
    damage_dice = Dice(1, 8)
    
    rounds = 0
    while fighter1.is_alive() and fighter2.is_alive():
        rounds += 1
        
        # Fighter 1 attacks
        dmg = damage_dice.roll()
        fighter2.take_damage(dmg)
        print(f"Round {rounds}: {fighter1.name} deals {dmg} damage to {fighter2.name} (HP: {fighter2.get_hp()})")
        
        if not fighter2.is_alive():
            print(f"{fighter2.name} is defeated!")
            break
        
        # Fighter 2 attacks
        dmg = damage_dice.roll()
        fighter1.take_damage(dmg)
        print(f"Round {rounds}: {fighter2.name} deals {dmg} damage to {fighter1.name} (HP: {fighter1.get_hp()})")
        
        if not fighter1.is_alive():
            print(f"{fighter1.name} is defeated!")
            break
    
    winner = fighter1 if fighter1.is_alive() else fighter2
    print(f"\nWinner: {winner.name} with {winner.get_hp()} HP remaining")
    
    print()


def main():
    """Run all examples."""
    print("Arena Python Package - Examples")
    print("=" * 50)
    print()
    
    example_dice_rolling()
    example_character_creation()
    example_party_management()
    example_simple_simulation()
    example_custom_simulation()
    
    print("=" * 50)
    print("Examples complete!")


if __name__ == "__main__":
    main()
