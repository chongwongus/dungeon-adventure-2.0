from abc import ABC, abstractmethod
import random
from typing import Tuple

from .room import Room
from .dungeon import Dungeon


class DungeonFactory(ABC):
    """Factory class for creating dungeons with different generation strategies."""

    @abstractmethod
    def create(self, size: Tuple[int, int] = (8, 8)) -> Dungeon:
        """Create a dungeon with the specified size."""
        pass

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

    def place_pillars(self, dungeon: Dungeon) -> None:
        """Place pillars ensuring they are reachable."""

        def find_reachable_rooms():
            """Find all rooms reachable from entrance."""
            reachable = []
            for y in range(dungeon.size[1]):
                for x in range(dungeon.size[0]):
                    if (x, y) != dungeon.entrance and (x, y) != dungeon.exit:
                        if dungeon.is_room_reachable(dungeon.entrance, (x, y)) and \
                                dungeon.is_room_reachable((x, y), dungeon.exit):
                            reachable.append((x, y))
            return reachable

        # Get all rooms that are reachable from entrance AND can reach the exit
        available_rooms = find_reachable_rooms()

        if len(available_rooms) < 4:
            # If we don't have enough reachable rooms, add more connections
            self.add_additional_connections(dungeon)
            available_rooms = find_reachable_rooms()

        # Place pillars in random reachable rooms
        pillars = list(Room.PILLARS)
        random.shuffle(available_rooms)  # Randomize placement

        # available_rooms.sort()  # Sort before placing pillars

        self.pillar_locations = []
        for i, pillar in enumerate(pillars):
            if i < len(available_rooms):
                x, y = available_rooms[i]
                dungeon.maze[y][x].hasPillar = True
                dungeon.maze[y][x].pillarType = pillar
                self.pillar_locations.append((pillar, x, y))  # Store pillar type and location
            else:
                raise RuntimeError("Unable to place all pillars in reachable locations")

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
