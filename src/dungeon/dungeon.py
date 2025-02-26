# src/dungeon/dungeon.py
from typing import Tuple, Optional, List, Dict
from .room import Room
import random
from src.combat.combat_system import CombatSystem

class Dungeon:
    """
    Represents the game's dungeon as a complex, interconnected grid of rooms.

    The Dungeon class is the central spatial representation of the game world,
    managing room layouts, connections, and intricate interactions between
    different dungeon elements.

    Key Responsibilities:
    - Maintain dungeon grid structure
    - Validate and process hero movement
    - Handle room-specific interactions
    - Manage visibility and exploration
    """

    def __init__(self, size: Tuple[int, int] = (8, 8)):
        """
        Initialize a new dungeon with specified dimensions.

        This constructor sets up the fundamental structure of the dungeon:
        - Creates an empty maze grid
        - Defines dungeon size
        - Prepares placeholders for entrance and exit points

        Args:
            size (Tuple[int, int], optional):
                Dimensions of the dungeon grid.
                Defaults to an 8x8 grid.
        """
        self.size = size
        self.maze: List[List[Room]] = [[]]
        self.entrance: Optional[Tuple[int, int]] = None
        self.exit: Optional[Tuple[int, int]] = None

    def reveal_adjacent_rooms(self, center_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reveal rooms adjacent to a given position, simulating a vision potion effect.

        This method:
        - Identifies all rooms surrounding the given position
        - Marks these rooms as visited
        - Supports exploration mechanics

        Args:
            center_pos (Tuple[int, int]):
                Coordinates of the central room

        Returns:
            List[Tuple[int, int]]:
                Coordinates of rooms that were revealed
        """
        revealed = []
        x, y = center_pos

        # Check all adjacent positions (including diagonals)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size[0] and 0 <= new_y < self.size[1]:
                self.maze[new_y][new_x].visited = True
                revealed.append((new_x, new_y))

        return revealed

    def is_room_reachable(self, start: Tuple[int, int], target: Tuple[int, int]) -> bool:
        """
        Determine if a path exists between two rooms using depth-first search.

        This method:
        - Checks room connectivity
        - Validates potential navigation routes
        - Ensures dungeon exploration is possible

        Args:
            start (Tuple[int, int]): Starting room coordinates
            target (Tuple[int, int]): Destination room coordinates

        Returns:
            bool: True if a path exists, False otherwise
        """
        visited = set()
        stack = [start]

        while stack:
            current = stack.pop()
            if current == target:
                return True

            if current not in visited:
                visited.add(current)
                x, y = current

                # Check all possible moves from current position
                if self.maze[y][x].doors['N'] and y > 0:
                    stack.append((x, y - 1))
                if self.maze[y][x].doors['S'] and y < self.size[1] - 1:
                    stack.append((x, y + 1))
                if self.maze[y][x].doors['E'] and x < self.size[0] - 1:
                    stack.append((x + 1, y))
                if self.maze[y][x].doors['W'] and x > 0:
                    stack.append((x - 1, y))

        return False

    def get_room(self, x: int, y: int) -> Optional[Room]:
        """
        Retrieve the room at specific coordinates.

        This method:
        - Validates room coordinates
        - Returns the Room instance at those coordinates
        - Handles boundary checking

        Args:
            x (int): X-coordinate in the dungeon grid
            y (int): Y-coordinate in the dungeon grid

        Returns:
            Optional[Room]: Room at the specified coordinates, or None
        """
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            return self.maze[y][x]
        return None

    def get_room_in_direction(self, current_pos: Tuple[int, int], direction: str) -> Optional[Tuple[int, int]]:
        """
        Calculate room coordinates when moving in a specific direction.

        This method:
        - Determines new room coordinates based on movement direction
        - Performs boundary checking
        - Supports navigation logic

        Args:
            current_pos (Tuple[int, int]): Current room coordinates
            direction (str): Movement direction ('N', 'S', 'E', 'W')

        Returns:
            Optional[Tuple[int, int]]: Coordinates of the room in the specified direction
        """
        x, y = current_pos
        new_x, new_y = x, y

        if direction == 'N':
            new_y -= 1
        elif direction == 'S':
            new_y += 1
        elif direction == 'E':
            new_x += 1
        elif direction == 'W':
            new_x -= 1

        # Check if new position would be in bounds
        if 0 <= new_x < self.size[0] and 0 <= new_y < self.size[1]:
            return (new_x, new_y)
        return None

    def move_hero(self, hero, direction: str) -> Tuple[bool, List[str], Optional[CombatSystem]]:
        """
        Process hero movement through the dungeon.

        This comprehensive method handles:
        - Movement validation
        - Room connectivity checking
        - Room effect processing
        - Potential combat encounter initiation

        Detailed steps:
        1. Validate current hero location
        2. Check movement direction availability
        3. Verify room-to-room connectivity
        4. Update hero's location
        5. Process room-specific interactions
        6. Handle potential combat encounters

        Args:
            hero: The hero character attempting to move
            direction (str): Movement direction

        Returns:
            Tuple containing:
            - Movement success (bool)
            - Interaction messages (List[str])
            - Potential combat system (Optional[CombatSystem])
        """
        if not hero.location:
            return False, ["No current location!"], None

        current_room = self.get_room(*hero.location)
        if not current_room or not current_room.doors[direction]:
            return False, ["You cannot move in that direction."], None

        # Calculate new position
        new_pos = self.get_room_in_direction(hero.location, direction)
        if not new_pos:
            return False, ["You cannot move in that direction."], None

        # Check connecting door
        new_room = self.get_room(*new_pos)
        opposite_directions = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        if not new_room.doors[opposite_directions[direction]]:
            return False, ["You cannot move in that direction."], None

        # Move is valid - update position
        hero.location = new_pos
        new_room.visited = True

        # Apply room effects and get messages
        messages = self.apply_room_effects(hero)

        # Check for combat
        combat_system = None
        if new_room.monster and new_room.monster.is_alive:
            combat_system = CombatSystem(hero, new_room.monster)
            messages.append(f"You encounter a {new_room.monster.name}!")

        return True, messages, combat_system

    def apply_room_effects(self, hero) -> List[str]:
        """
        Process all interactions and effects when entering a room.

        This method manages multiple room interaction types:
        - Pillar collection
        - Pit damage
        - Item pickup (health/vision potions)
        - Logging and tracking exploration

        Interaction Precedence:
        1. Pillar collection
        2. Pit damage
        3. Item collection
        4. Logging exploration state

        Args:
            hero: The hero character in the room

        Returns:
            List[str]: Messages describing room interactions
        """
        messages = []
        room = self.get_room(*hero.location)

        # Clear player location tracking
        print(f"\nPlayer at {hero.location}")  # Just show current location

        # Handle pillar collection (only log when actually found)
        if room.hasPillar:
            if room.pillarType not in hero.pillars:
                print(f"Found new Pillar {room.pillarType}!")
                hero.collect_pillar(room.pillarType)
                room.hasPillar = False
                messages.append(f"You found the {room.pillarType} pillar!")

        # Handle pit damage
        if room.hasPit:
            damage = random.randint(10, 20)
            hero.take_damage(damage)
            messages.append(f"You fell into a pit and took {damage} damage!")

        # Handle item collection
        if room.hasHealthPot:
            hero.collect_potion("healing")
            room.hasHealthPot = False
            messages.append("You found a healing potion!")

        if room.hasVisionPot:
            hero.collect_potion("vision")
            room.hasVisionPot = False
            messages.append("You found a vision potion!")

        # Handle pillar collection with more detailed feedback
        if room.hasPillar:
            print(f"Attempting to collect pillar: {room.pillarType}")
            print(f"Current pillars: {hero.pillars}")
            if room.pillarType not in hero.pillars:  # Only collect if we don't have it
                hero.collect_pillar(room.pillarType)
                room.hasPillar = False
                messages.append(f"You found the {room.pillarType} pillar!")
                print(f"Pillars after collection: {hero.pillars}")
            else:
                messages.append(f"You've already collected the {room.pillarType} pillar.")

        return messages

    def get_visible_rooms(self) -> Dict[Tuple[int, int], Room]:
        """
        Retrieve all rooms that have been visited during exploration.

        This method:
        - Tracks explored dungeon areas
        - Supports map revelation mechanics
        - Enables partial dungeon visibility

        Returns:
            Dict[Tuple[int, int], Room]:
                Dictionary of visited room coordinates and their instances
        """
        visible = {}
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.maze[y][x].visited:
                    visible[(x, y)] = self.maze[y][x]
        return visible

    def __str__(self) -> str:
        """
        Generate a string representation of the entire dungeon.

        Creates an ASCII art-like visualization of the dungeon grid,
        showing:
        - Room connections
        - Room contents
        - Exploration state

        Returns:
            str: Textual representation of the dungeon layout
        """
        result = []
        for row in self.maze:
            room_lines = [str(room).split('\n') for room in row]
            if result:
                result.append('     ' * len(row))
            for i in range(3):
                result.append('  '.join(room[i] for room in room_lines))
        return '\n'.join(result)