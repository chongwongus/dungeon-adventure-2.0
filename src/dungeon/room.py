import random
from typing import Optional, List
from src.characters.monsters.ogre import Ogre
from src.characters.monsters.gremlin import Gremlin
from src.characters.monsters.skeleton import Skeleton
from src.characters.base.monster import Monster


class Room:
    """
    Represents a single location within the dungeon environment.

    The Room class is a comprehensive state container that manages
    all possible room configurations, contents, and interactions.

    Key Design Characteristics:
    - Flexible content management
    - Randomized monster and item generation
    - ASCII art representation
    - Detailed state tracking for game mechanics

    Class-Level Constants:
    Provide visual representations for different room states:
    - EMPTY: Represents an unoccupied room
    - PIT: Indicates a trap room
    - ENTRANCE/EXIT: Special location markers
    - VISION/HEALTH POT: Item presence indicators
    - MONSTER: Enemy presence marker

    Core Attributes Track:
    - Room contents (monsters, items, pillars)
    - Directional doors
    - Visited status
    - Special room types
    """

    # Room display characters
    EMPTY = ' '
    PIT = 'X'
    ENTRANCE = 'i'
    EXIT = 'o'
    VISION_POT = 'V'
    HEALTH_POT = 'H'
    MULTIPLE_ITEMS = 'M'
    MONSTER = 'E'  # E for Enemy

    # Add Pillars list
    PILLARS = ['A', 'E', 'I', 'P']  # The four Pillars of OO

    def __init__(self):
        """
        Initialize a new room with default state.

        Sets up the initial configuration for a room, including:
        - No items or monsters by default
        - Closed doors in all directions
        - Unvisited status
        - Placeholder for potential special contents

        The constructor prepares a blank room state that can be
        dynamically populated during dungeon generation.
        """
        self.hasPit = False
        self.hasHealthPot = False
        self.hasVisionPot = False
        self.hasPillar = False
        self.isEntrance = False
        self.isExit = False
        self.pillarType = None
        self.doors = {
            'N': False, 'S': False,
            'E': False, 'W': False
        }
        self.visited = False

        # Monster and loot attributes
        self.monster: Optional[Monster] = None
        self.loot_drops = {
            'health_potion': 0.3,  # 30% chance
            'vision_potion': 0.2  # 20% chance
        }

    def spawn_monster(self, force: bool = False) -> None:
        """
        Attempt to spawn a monster in the room.

        This method manages monster generation with sophisticated rules:
        - 30% chance of monster spawn (or 100% if forced)
        - Prevents spawning in entrance/exit rooms
        - Randomly selects from different monster types
        - Configures monster with type-specific attributes

        Spawning Process:
        1. Check room eligibility for monster
        2. Determine spawn probability
        3. Randomly select monster type
        4. Create monster with predefined characteristics

        Args:
            force (bool, optional):
                Guarantees monster spawn if True.
                Defaults to False.
        """
        # Don't spawn in entrance/exit or if already has monster
        if (self.isEntrance or self.isExit or self.monster) and not force:
            return

        # 30% chance to spawn monster (or 100% if forced)
        if force or random.random() < 0.3:
            monster_types = [Ogre, Gremlin, Skeleton]
            monster_class = random.choice(monster_types)

            # Create monster with appropriate default values based on type
            # PLACEHOLDER HARD CODED VALUES FOR NOW
            if monster_class == Ogre:
                self.monster = Ogre(
                    hp=200,
                    min_damage=30,
                    max_damage=60,
                    attack_speed=2,
                    hit_chance=0.6,
                    heal_chance=0.1,
                    min_heal=30,
                    max_heal=60
                )
            elif monster_class == Skeleton:
                self.monster = Skeleton(
                    hp=100,
                    min_damage=30,
                    max_damage=50,
                    attack_speed=3,
                    hit_chance=0.8,
                    heal_chance=0.3,
                    min_heal=30,
                    max_heal=50
                )
            elif monster_class == Gremlin:
                self.monster = Gremlin(
                    hp=70,
                    min_damage=15,
                    max_damage=30,
                    attack_speed=5,
                    hit_chance=0.8,
                    heal_chance=0.4,
                    min_heal=20,
                    max_heal=40
                )

    def get_drops(self) -> List[str]:
        """
        Determine potential item drops when a monster is defeated.

        Implements a probabilistic loot system:
        - Health potion: 30% drop chance
        - Vision potion: 20% drop chance
        - Supports multiple potential drops

        Randomization ensures varied player experiences
        and adds an element of surprise to monster defeats.

        Returns:
            List[str]: Items that were successfully dropped
        """
        drops = []
        for item, chance in self.loot_drops.items():
            if random.random() < chance:
                drops.append(item)
        return drops

    def clear_monster(self) -> List[str]:
        """
        Remove a defeated monster and collect its drops.

        This method handles the end-of-combat room state:
        - Checks if monster is defeated
        - Collects potential item drops
        - Removes monster from the room

        Returns:
            List[str]: Items dropped by the defeated monster
        """
        if self.monster and not self.monster.is_alive:
            drops = self.get_drops()
            self.monster = None
            return drops
        return []

    def get_room_display(self) -> str:
        """
        Generate a single-character representation of room contents.

        Creates a visual shorthand that quickly communicates
        the room's current state, including:
        - Special room types (entrance, exit)
        - Monster presence
        - Multiple item indicators
        - Specific item types

        Prioritization Logic:
        1. Special location markers (entrance/exit)
        2. Monster presence
        3. Multiple item indicator
        4. Specific item types
        5. Default empty state

        Returns:
            str: Single-character room state representation
        """
        if self.isEntrance:
            return self.ENTRANCE
        if self.isExit:
            return self.EXIT
        if self.monster and self.visited:
            return self.MONSTER

        # Count visible items
        items = sum([self.hasPit, self.hasHealthPot,
                     self.hasVisionPot, self.hasPillar])

        if items > 1:
            return self.MULTIPLE_ITEMS
        elif self.hasPit:
            return self.PIT
        elif self.hasHealthPot:
            return self.HEALTH_POT
        elif self.hasVisionPot:
            return self.VISION_POT
        elif self.hasPillar:
            return self.pillarType
        else:
            return self.EMPTY

    def __str__(self) -> str:
        """
        Create an ASCII art representation of the room.

        Generates a visual ASCII representation that shows:
        - Directional doors
        - Room contents
        - Exploration state

        The representation includes:
        - Top border with door status
        - Middle section with room contents
        - Bottom border with door status

        Returns:
            str: Multi-line ASCII art room representation
        """
        top = ' * ' + ('-' if self.doors['N'] else ' * ') + ' * '
        mid = (' | ' if self.doors['W'] else ' * ') + \
              (self.get_room_display() + ' ' if self.visited else ' ? ') + \
              (' | ' if self.doors['E'] else ' * ')
        bot = ' * ' + (' - ' if self.doors['S'] else ' * ') + ' * '
        return top + '\n' + mid + '\n' + bot