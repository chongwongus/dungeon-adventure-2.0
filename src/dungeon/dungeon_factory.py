from abc import ABC, abstractmethod
import random
from typing import Tuple

from .room import Room
from .dungeon import Dungeon

class DungeonFactory(ABC):
    """Factory class for creating dungeons with different generation strategies."""

    def __init__(self):
        self.pillar_locations = []  # List of (pillar_type, x, y) tuples

    @abstractmethod
    def create(self, size: Tuple[int, int] = (8, 8)) -> Dungeon:
        """Create a dungeon with the specified size."""
        pass

    def ensure_bidirectional_connection(self, dungeon: Dungeon, x1: int, y1: int, x2: int, y2: int, dir1: str,
                                        dir2: str) -> None:
        """Ensure doors are properly connected between two rooms."""
        room1 = dungeon.maze[y1][x1]
        room2 = dungeon.maze[y2][x2]
        room1.doors[dir1] = True
        room2.doors[dir2] = True

    def remove_connection(self, dungeon: Dungeon, x1: int, y1: int, x2: int, y2: int, dir1: str, dir2: str) -> None:
        """Remove connection between two rooms."""
        room1 = dungeon.maze[y1][x1]
        room2 = dungeon.maze[y2][x2]
        room1.doors[dir1] = False
        room2.doors[dir2] = False

    def verify_door_connections(self, dungeon: Dungeon) -> bool:
        """
        Verify all door connections are properly bidirectional.
        Returns True if all connections are valid.
        """
        valid = True
        print("\nVerifying door connections...")
        for y in range(dungeon.size[1]):
            for x in range(dungeon.size[0]):
                room = dungeon.maze[y][x]
                # Check east connections
                if x < dungeon.size[0] - 1:
                    next_room = dungeon.maze[y][x + 1]
                    if room.doors['E'] != next_room.doors['W']:
                        print(f"ERROR: Door mismatch at ({x}, {y}) East/West")
                        valid = False
                # Check south connections
                if y < dungeon.size[1] - 1:
                    next_room = dungeon.maze[y + 1][x]
                    if room.doors['S'] != next_room.doors['N']:
                        print(f"ERROR: Door mismatch at ({x}, {y}) South/North")
                        valid = False

        if valid:
            print("All door connections are valid!")
        else:
            print("Door connection errors found!")
        return valid

    def print_dungeon_layout(self, dungeon: Dungeon) -> None:
        """Print ASCII representation of dungeon layout."""
        print("\n=== Dungeon Layout ===")
        print(f"Size: {dungeon.size}")
        print(f"Entrance: {dungeon.entrance}")
        print(f"Exit: {dungeon.exit}")

        # Print layout with walls and doors
        for y in range(dungeon.size[1]):
            # Print horizontal walls for this row
            wall_line = ""
            room_line = ""
            for x in range(dungeon.size[0]):
                room = dungeon.get_room(x, y)
                # Print north wall/door
                wall_line += "+---" if not room.doors['N'] else "+-|-"
                # Print room identifier and east wall/door
                if (x, y) == dungeon.entrance:
                    room_char = "E"
                elif (x, y) == dungeon.exit:
                    room_char = "X"
                elif room.hasPillar:
                    room_char = room.pillarType
                else:
                    room_char = " "
                room_line += f"|{room_char:^3}" if not room.doors['E'] else f"|{room_char:^3} "
            wall_line += "+"
            room_line += "|"
            print(wall_line)
            print(room_line)

        # Print bottom wall
        print("+---" * dungeon.size[0] + "+")
        print("=====================\n")

    def populate_rooms(self, dungeon: Dungeon) -> None:
        """
        Populate rooms with monsters and items.
        Order matters: place pillars first, then monsters, then other items.
        """
        # First place pillars
        self.place_pillars(dungeon)

        # Then add monsters
        self.place_monsters(dungeon)

        # Finally add other items
        self.place_items(dungeon)

        # Print final layout and verify connections
        self.print_dungeon_layout(dungeon)
        self.verify_door_connections(dungeon)

    def place_pillars(self, dungeon: Dungeon) -> None:
        """Place pillars ensuring they are reachable."""
        self.pillar_locations = []  # Reset pillar locations
        available_rooms = [(x, y) for x in range(dungeon.size[0])
                          for y in range(dungeon.size[1])
                          if (x, y) != dungeon.entrance and (x, y) != dungeon.exit]

        pillar_rooms = []
        pillars = list(Room.PILLARS)
        random.shuffle(available_rooms)  # Randomize placement

        for i, pillar in enumerate(pillars):
            if i < len(available_rooms):
                x, y = available_rooms[i]
                if dungeon.is_room_reachable(dungeon.entrance, (x, y)) and \
                   dungeon.is_room_reachable((x, y), dungeon.exit):
                    pillar_rooms.append((x, y))
                    dungeon.maze[y][x].hasPillar = True
                    dungeon.maze[y][x].pillarType = pillar
                    self.pillar_locations.append((pillar, x, y))  # Track pillar location
                    print(f"Placed pillar {pillar} at ({x}, {y})")
                else:
                    print(f"Warning: Room ({x}, {y}) not reachable for pillar {pillar}")

    def place_monsters(self, dungeon: Dungeon) -> None:
        """Place monsters throughout the dungeon."""
        for y in range(dungeon.size[1]):
            for x in range(dungeon.size[0]):
                room = dungeon.get_room(x, y)
                if not (room.isEntrance or room.isExit or room.hasPillar):
                    room.spawn_monster()  # 30% chance by default

    def place_items(self, dungeon: Dungeon) -> None:
        """Place health potions, vision potions, and pits."""
        for y in range(dungeon.size[1]):
            for x in range(dungeon.size[0]):
                room = dungeon.get_room(x, y)
                if (x, y) not in [dungeon.entrance, dungeon.exit] and not room.hasPillar:
                    if random.random() < 0.1:
                        room.hasHealthPot = True
                    if random.random() < 0.1:
                        room.hasVisionPot = True
                    if random.random() < 0.1:
                        room.hasPit = True

    def add_additional_connections(self, dungeon: Dungeon) -> None:
        """Add more connections to ensure pillar reachability."""
        added_connections = False

        # Try to add connections until we have enough reachable rooms
        for y in range(dungeon.size[1]):
            for x in range(dungeon.size[0]):
                if added_connections:
                    break

                current = dungeon.get_room(x, y)

                # Try to connect to adjacent rooms
                if x < dungeon.size[0] - 1:  # Try east
                    next_room = dungeon.get_room(x + 1, y)
                    if not current.doors['E']:
                        current.doors['E'] = True
                        next_room.doors['W'] = True
                        added_connections = True

                if y < dungeon.size[1] - 1:  # Try south
                    next_room = dungeon.get_room(x, y + 1)
                    if not current.doors['S']:
                        current.doors['S'] = True
                        next_room.doors['N'] = True
                        added_connections = True
