"""
Arena simulation of battling fighters.

Based on Arena.java by Daniel R. Collins (dcollins@superdan.net)
"""

from typing import Optional
from .character import Character
from .party import Party
from .enums import Alignment, ArmorType, ClassType
from .equipment import Armor, Weapon
from .dice import set_random_seed
import sys


class Arena:
    """
    Arena of battling fighters (as gladiators).
    
    Simulates a population of fighters battling for experience and treasure
    over time. Can simulate man vs. man or man vs. monster combat.
    """
    
    # Default constants
    DEFAULT_NUM_YEARS = 50
    DEFAULT_FIGHTS_PER_YEAR = 12
    DEFAULT_NUM_FIGHTERS = 100
    DEFAULT_PARTY_SIZE = 1
    DEFAULT_PCT_MAGIC_PER_LEVEL = 15
    DEFAULT_ARMOR = ArmorType.PLATE
    
    def __init__(self):
        """Initialize arena simulation."""
        # Core parameters
        self.num_years = self.DEFAULT_NUM_YEARS
        self.fights_per_year = self.DEFAULT_FIGHTS_PER_YEAR
        self.num_fighters = self.DEFAULT_NUM_FIGHTERS
        self.start_level = 1
        self.fighter_party_size = self.DEFAULT_PARTY_SIZE
        
        # Simulation modes
        self.fight_man_vs_monster = False
        self.use_monster_treasure_type = False
        self.use_revised_xp_awards = False
        
        # Reporting options
        self.report_fighter_stats = True
        self.report_fighter_data = False
        self.report_monster_kills = False
        self.report_total_monster_kills = False
        self.report_year_end = False
        self.report_xp_awards = False
        self.report_all_xp_awards = False
        self.report_every_encounter = False
        
        # Other settings
        self.base_armor_type: Optional[ArmorType] = self.DEFAULT_ARMOR
        self.typical_alignment = Alignment.NEUTRAL
        self.make_win_percent_matrix = False
        
        # State tracking
        self.fighter_list = Party()
        self.sup_max_age = 120
        self.total_monster_xp = 0
        self.total_treasure_xp = 0
        self.exit_after_args = False
    
    def parse_args(self, args: list):
        """
        Parse command-line arguments.
        
        Args:
            args: List of command-line arguments
        """
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg.startswith('-'):
                if arg == '-?':
                    self.print_usage()
                    self.exit_after_args = True
                elif arg.startswith('-y='):
                    self.num_years = self._get_param_int(arg)
                elif arg.startswith('-f='):
                    self.fights_per_year = self._get_param_int(arg)
                elif arg.startswith('-n='):
                    self.num_fighters = self._get_param_int(arg)
                elif arg.startswith('-l='):
                    self.start_level = self._get_param_int(arg)
                elif arg.startswith('-p='):
                    self.fighter_party_size = self._get_param_int(arg)
                elif arg.startswith('-a='):
                    self._set_base_armor_from_int(self._get_param_int(arg))
                elif arg == '-m':
                    self.fight_man_vs_monster = True
                elif arg == '-t':
                    self.use_monster_treasure_type = True
                elif arg.startswith('-r'):
                    self._set_reporting_from_param_code(arg)
                else:
                    print(f"Unknown option: {arg}")
                    self.exit_after_args = True
            i += 1
    
    def _get_param_int(self, s: str) -> int:
        """Get integer following equals sign in parameter."""
        try:
            if len(s) > 3 and s[2] == '=':
                return int(s[3:])
        except ValueError:
            pass
        self.exit_after_args = True
        return -1
    
    def _set_base_armor_from_int(self, code: int):
        """Set base armor type from integer code."""
        armor_map = {
            0: None,
            1: ArmorType.LEATHER,
            2: ArmorType.CHAIN,
            3: ArmorType.PLATE,
        }
        if code in armor_map:
            self.base_armor_type = armor_map[code]
        else:
            self.exit_after_args = True
    
    def _set_reporting_from_param_code(self, s: str):
        """Set reporting flags from parameter code."""
        self.report_fighter_stats = False  # Shut off default
        for char in s[2:]:
            if char == 's':
                self.report_fighter_stats = True
            elif char == 'd':
                self.report_fighter_data = True
            elif char == 'k':
                self.report_monster_kills = True
            elif char == 't':
                self.report_total_monster_kills = True
            elif char == 'x':
                self.report_xp_awards = True
            elif char == 'y':
                self.report_year_end = True
            else:
                self.exit_after_args = True
    
    def print_banner(self):
        """Print program banner."""
        print("OED Arena - Battle Simulator")
        print("-----------------------------")
    
    def print_usage(self):
        """Print usage information."""
        print("Usage: arena [options]")
        print("Options:")
        print("  -? : Show this help")
        print("  -y=N : Set number of years (default: 50)")
        print("  -f=N : Set fights per year (default: 12)")
        print("  -n=N : Set number of fighters (default: 100)")
        print("  -l=N : Set starting level (default: 1)")
        print("  -p=N : Set party size (default: 1)")
        print("  -a=N : Set armor type (0=none, 1=leather, 2=chain, 3=plate)")
        print("  -m : Fight man vs. monster")
        print("  -t : Use monster treasure types")
        print("  -r[sdktxy] : Set reporting options")
        print("    s: Fighter statistics")
        print("    d: Fighter details")
        print("    k: Monster kills")
        print("    t: Total monster kills")
        print("    x: XP awards")
        print("    y: Year-end status")
    
    def report_start(self):
        """Report simulation start parameters."""
        print("\nSimulation Settings:")
        print(f"  Fight mode: {'Man vs Monster' if self.fight_man_vs_monster else 'Man vs Man'}")
        print(f"  Number of fighters: {self.num_fighters}")
        print(f"  Years: {self.num_years}")
        print(f"  Fights per year: {self.fights_per_year}")
        print(f"  Party size: {self.fighter_party_size}")
        print(f"  Starting level: {self.start_level}")
        if self.base_armor_type:
            print(f"  Base armor: {self.base_armor_type.name}")
        print()
    
    def run_sim(self):
        """Run the arena's top-level simulation."""
        for year in range(1, self.num_years + 1):
            for _ in range(self.fights_per_year):
                self.run_one_cycle()
            self.year_end(year)
    
    def run_one_cycle(self):
        """Run one cycle of fights for the whole list."""
        self.recruit_new_fighters()
        self.fighter_list.shuffle_members()
        self.fight_duels()
        self.fighter_list.bring_out_your_dead()
        self.fighter_list.clear_fallen()
        self.fighter_list.heal_all()
    
    def recruit_new_fighters(self):
        """Fill out the fighter list to the target size."""
        while self.fighter_list.get_size() < self.num_fighters:
            fighter = self.new_fighter(self.start_level)
            self.fighter_list.add_member(fighter)
    
    def new_fighter(self, level: int) -> Character:
        """
        Create a new fighter of the indicated level.
        
        Args:
            level: Starting level for the fighter
            
        Returns:
            New Character instance
        """
        fighter = Character(
            name=f"Fighter_{id(self)}",
            level=level,
            class_type=ClassType.FIGHTER
        )
        
        # Set alignment
        fighter.set_alignment(Alignment.random_normal())
        
        # Set equipment
        if self.base_armor_type:
            fighter.set_armor(Armor.make_type(self.base_armor_type))
        
        fighter.set_weapon(Weapon.create_sword())
        
        return fighter
    
    def fight_duels(self):
        """Fight duels for all fighters in list."""
        if self.fight_man_vs_monster:
            self.fight_duels_man_vs_monster()
        else:
            self.fight_duels_man_vs_man()
    
    def fight_duels_man_vs_man(self):
        """Duel each pair of fighters."""
        members = self.fighter_list.get_members()
        for i in range(0, len(members) - 1, 2):
            fighter1 = members[i]
            fighter2 = members[i + 1]
            
            if self.report_every_encounter:
                print(f"Arena event: {fighter1} vs {fighter2}")
            
            # Simple combat simulation (placeholder)
            self._simple_combat(fighter1, fighter2)
    
    def fight_duels_man_vs_monster(self):
        """Duel each fighter against random monsters."""
        # Placeholder for monster combat
        print("Man vs Monster combat not yet fully implemented")
    
    def _simple_combat(self, fighter1: Character, fighter2: Character):
        """
        Simple combat between two fighters (placeholder).
        
        Args:
            fighter1: First fighter
            fighter2: Second fighter
        """
        # Very simple: each does damage until one dies
        from .dice import Dice
        
        damage_dice = Dice(1, 8)
        
        while fighter1.is_alive() and fighter2.is_alive():
            # Fighter 1 attacks
            damage = damage_dice.roll()
            fighter2.take_damage(damage)
            
            if not fighter2.is_alive():
                break
            
            # Fighter 2 attacks
            damage = damage_dice.roll()
            fighter1.take_damage(damage)
    
    def year_end(self, year: int):
        """
        Process year-end events.
        
        Args:
            year: Current year number
        """
        if self.report_year_end:
            print(f"\nYear {year} complete:")
            print(f"  Living fighters: {self.fighter_list.num_living()}")
            print(f"  Average level: {self.fighter_list.get_average_level():.1f}")
    
    def report_final_stats(self):
        """Report final simulation statistics."""
        if self.report_fighter_stats:
            print("\n=== Final Statistics ===")
            print(f"Total fighters: {self.fighter_list.get_size()}")
            print(f"Living fighters: {self.fighter_list.num_living()}")
            print(f"Dead fighters: {self.fighter_list.num_dead()}")
            print(f"Average level: {self.fighter_list.get_average_level():.1f}")
            
            if self.fighter_list.get_size() > 0:
                highest = self.fighter_list.get_highest_level_member()
                print(f"Highest level: {highest.get_level()} ({highest})")
    
    def run(self, args: list = None):
        """
        Main entry point for running the simulation.
        
        Args:
            args: Command-line arguments (optional)
        """
        if args:
            self.parse_args(args)
        
        if self.exit_after_args:
            return
        
        self.print_banner()
        self.report_start()
        
        print("Running simulation...")
        self.run_sim()
        
        print("\nSimulation complete!")
        self.report_final_stats()


def main():
    """Main entry point for command-line execution."""
    arena = Arena()
    arena.run(sys.argv[1:])


if __name__ == "__main__":
    main()
