"""
Athena - Master wrapper around all Arena applications.

Based on Athena.java by Daniel R. Collins (dcollins@superdan.net)
"""

import sys


class Athena:
    """
    Master wrapper around all other applications in the Arena package.
    """
    
    # Available applications
    APP_NAMES = ["arena", "marshal", "monster_metrics", "npc_generator"]
    
    def __init__(self):
        """Initialize Athena."""
        self.app_select = None
        self.app_args = []
        self.exit_after_args = False
    
    def print_banner(self):
        """Print program banner."""
        print("OED Athena Master")
        print("-----------------")
    
    def print_usage(self):
        """Print usage information."""
        print("Usage: athena [command] [options]")
        print("  where commands include:")
        for app in self.APP_NAMES:
            print(f"    {app}")
        print("For options in individual programs, run with -?")
        print()
    
    def parse_args(self, args: list):
        """
        Parse command-line arguments.
        
        Args:
            args: Command-line arguments
        """
        if len(args) == 0:
            self.exit_after_args = True
            return
        
        self.app_select = args[0].lower()
        
        if self.app_select not in self.APP_NAMES:
            self.exit_after_args = True
            return
        
        self.app_args = args[1:] if len(args) > 1 else []
    
    def run_app(self):
        """Run the chosen application with modified arguments."""
        if self.app_select == "arena":
            from .arena import Arena
            app = Arena()
            app.run(self.app_args)
        elif self.app_select == "marshal":
            print("Marshal application not yet implemented")
        elif self.app_select == "monster_metrics":
            print("MonsterMetrics application not yet implemented")
        elif self.app_select == "npc_generator":
            print("NPCGenerator application not yet implemented")
    
    def run(self, args: list):
        """
        Main entry point.
        
        Args:
            args: Command-line arguments
        """
        self.parse_args(args)
        
        if self.exit_after_args:
            self.print_banner()
            self.print_usage()
            return
        
        self.run_app()


def main():
    """Command-line entry point."""
    athena = Athena()
    athena.run(sys.argv[1:])


if __name__ == "__main__":
    main()
