"""
CSV file reading utilities for the Arena package.

Based on CSVReader.java by Daniel R. Collins (dcollins@superdan.net)
"""

import csv
import os
from typing import List, Dict, Any


class CSVReader:
    """
    Utility class for reading CSV data files.
    """
    
    @staticmethod
    def read_csv(filename: str, data_dir: str = None) -> List[List[str]]:
        """
        Read a CSV file and return rows as a list of lists.
        
        Args:
            filename: Name of the CSV file
            data_dir: Directory containing data files (defaults to repo root)
            
        Returns:
            List of rows, where each row is a list of strings
        """
        if data_dir is None:
            # Try to find data files relative to package
            import arena
            pkg_dir = os.path.dirname(os.path.abspath(arena.__file__))
            data_dir = os.path.join(os.path.dirname(pkg_dir), '..')
        
        filepath = os.path.join(data_dir, filename)
        
        rows = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            print(f"Warning: Could not find data file: {filepath}")
        
        return rows
    
    @staticmethod
    def read_csv_as_dicts(filename: str, data_dir: str = None) -> List[Dict[str, str]]:
        """
        Read a CSV file with headers and return as list of dictionaries.
        
        Args:
            filename: Name of the CSV file
            data_dir: Directory containing data files
            
        Returns:
            List of dictionaries, where keys are column headers
        """
        if data_dir is None:
            import arena
            pkg_dir = os.path.dirname(os.path.abspath(arena.__file__))
            data_dir = os.path.join(os.path.dirname(pkg_dir), '..')
        
        filepath = os.path.join(data_dir, filename)
        
        rows = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            print(f"Warning: Could not find data file: {filepath}")
        
        return rows
    
    @staticmethod
    def parse_int(s: str, default: int = 0) -> int:
        """
        Parse an integer from a string, with a default value.
        
        Args:
            s: String to parse
            default: Default value if parsing fails
            
        Returns:
            Parsed integer or default value
        """
        try:
            return int(s.strip())
        except (ValueError, AttributeError):
            return default
    
    @staticmethod
    def parse_float(s: str, default: float = 0.0) -> float:
        """
        Parse a float from a string, with a default value.
        
        Args:
            s: String to parse
            default: Default value if parsing fails
            
        Returns:
            Parsed float or default value
        """
        try:
            return float(s.strip())
        except (ValueError, AttributeError):
            return default


class MonsterDatabase:
    """
    Database of monsters loaded from CSV files.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize monster database.
        
        Args:
            data_dir: Directory containing CSV files
        """
        self.monsters: List[Dict[str, Any]] = []
        self.data_dir = data_dir
        self._load_monsters()
    
    def _load_monsters(self):
        """Load monsters from CSV files."""
        # This is a placeholder - full implementation would parse
        # MonsterDatabase.csv and related files
        files = [
            'MonsterDatabase.csv',
            'MonsterDatabase-Dragons.csv',
            'MonsterDatabase-Hydras.csv',
        ]
        
        for filename in files:
            try:
                rows = CSVReader.read_csv(filename, self.data_dir)
                # Skip header row if present
                if rows and not rows[0][0].isdigit():
                    rows = rows[1:]
                
                for row in rows:
                    if len(row) > 0 and row[0]:
                        self.monsters.append({
                            'race': row[0] if len(row) > 0 else '',
                            'number_appearing': row[1] if len(row) > 1 else '',
                            'armor_class': CSVReader.parse_int(row[2]) if len(row) > 2 else 10,
                            'move': CSVReader.parse_int(row[3]) if len(row) > 3 else 12,
                            'hit_dice': row[4] if len(row) > 4 else '1',
                            # Add more fields as needed
                        })
            except Exception as e:
                print(f"Warning: Could not load {filename}: {e}")
    
    def get_monster_count(self) -> int:
        """Get the number of monsters in the database."""
        return len(self.monsters)
    
    def get_monster_by_name(self, name: str) -> Dict[str, Any]:
        """
        Get a monster by name.
        
        Args:
            name: Name of the monster
            
        Returns:
            Monster data dictionary, or None if not found
        """
        for monster in self.monsters:
            if monster['race'].lower() == name.lower():
                return monster
        return None
    
    def get_all_monsters(self) -> List[Dict[str, Any]]:
        """Get all monsters."""
        return self.monsters
