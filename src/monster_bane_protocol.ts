# src/monsters.py
"""Repository Core Module: Monster Definition Management."""

import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MonsterDefinition:
    """A single monster definition string."""
    name: str  # e.g., "The Obsidian Monk", "Burning Flame Dragon"
    category: str = ""      # Type, such as "Demon", "Beast", "Monster"
    lore_text: Optional[str] = None  # Description of the entity's nature

def is_monster(self) -> bool:
    """Check if this definition represents a valid monster."""
    return self.name != "" and re.match(r'^[A-Z][^a-zA-Z]*$', self.name.lower())


@dataclass(frozen=True)
class MonsterType(Enum):
    MONSTER = "monster"  # The base category
    
    DEMON = "demon"      # Demonatic entity (often associated with exclamation marks or question marks in lore)
    
    BEAST = "beast"     # Wild animal-like creature


@dataclass(frozen=True)
class MonsterRegistry(ABC):
    """Abstract base class for monster registry."""

    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def check(self) -> bool:
        """Check if this entity satisfies logical consistency requirements.
        
        Returns True if the definition is valid (e.g., a demon must be named 
        after an animal or have specific lore). False otherwise."""

@dataclass(frozen=True)
class MonsterTypeRegistry(MonsterRegistry):
    """A registry of known monster types with their associated rules."""

    def __init__(self, name: str = "types"):
        super().__init__()
        self.types: Dict[str, MonsterDefinition] = {}  # Name -> Definition object
    
    @property
    def type_name(self) -> str:
        return self.name


class MonarchDB(MonsterRegistry):
    """A specialized database for monster definitions from the repository."""

    def __init__(self, name: str = "db"):
        super().__init__()
        
        # Load existing monsters (if any exist in this repo)
        if os.path.exists(os.path.join("src", f"monsters.py")) and not os.access(
            os.path.join("src", "monsters.py"), os.R_OK | os.W_OK
        ):
            with open(os.path.join("src", "monsters.py"), 'r', encoding='utf-8') as f:
                self.load_from_file(f.read())

    def load_from_file(self, content: str):
        """Load monsters from a Python file."""
        lines = [line for line in content.split('\n') if not line.startswith('#')]
        
        # Split by newlines to handle multi-line definitions safely
        monster_lines = []
        current_line = ""
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip comments and empty lines (except for the first one)
            if not re.match(r'^[A-Z][^a-zA-Z]*$', line.lower()) or \
               (i == 0 and current_line != ""):
                i += 1
                continue
            
            monster_lines.append(line.strip() + '\n')

        # Parse lines into a list of definitions
        self.monsters = []
        
        for line in monster_lines[1:]:  # Skip empty first entry (if any) and comments
            if not re.match(r'^[A-Z][^a-zA-Z]*$', line.lower()):
                continue
            
            current_line = ""
            
            while i < len(lines):
                next_line = lines[i]
                
                # Check for comment or continuation
                is_comment = (next_line.startswith('#') and not re.match(r'^[A-Z][^a-zA-Z]*$', next_line.lower()))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        with open(f"src/monsters.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Loaded monsters from file")
    
    else:
        # Load test data for demonstration
        import random
        
        def create_test_monster(name, category="monster"):
            return MonsterDefinition(
                name=name, 
                category=category if not category.lower().startswith('demon') else "demon",
                lore_text=f"Entity {name} is a wild creature from the forest."
            )

        # Generate 5 test monsters for
