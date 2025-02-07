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
        # First place pillars (this was your original place_items logic)
        self.place_pillars(dungeon)

        # Then add monsters to rooms
        self.place_monsters(dungeon)

        # Finally add other items
        self.place_items(dungeon)

    def place_pillars(self, dungeon: Dungeon) -> None:
        """Place pillars ensuring they are reachable."""
        # Get available rooms (except entrance/exit)
        available_rooms = [(x, y) for x in range(dungeon.size[0])
                           for y in range(dungeon.size[1])
                           if (x, y) != dungeon.entrance and (x, y) != dungeon.exit]

        # Place pillars
        pillar_rooms = []
        pillars = list(Room.PILLARS)

        while len(pillar_rooms) < 4:
            room_pos = random.choice(available_rooms)
            x, y = room_pos

            # Check if room can be reached from entrance
            if dungeon.is_room_reachable(dungeon.entrance, room_pos):
                pillar_rooms.append(room_pos)
                available_rooms.remove(room_pos)
                dungeon.maze[y][x].hasPillar = True
                dungeon.maze[y][x].pillarType = pillars[len(pillar_rooms) - 1]

    def place_monsters(self, dungeon: Dungeon) -> None:
        """Place monsters throughout the dungeon."""
        # Iterate through all rooms
        for y in range(dungeon.size[1]):
            for x in range(dungeon.size[0]):
                room = dungeon.get_room(x, y)
                # Don't spawn in entrance, exit, or pillar rooms (yet)
                if not (room.isEntrance or room.isExit or room.hasPillar):
                    room.spawn_monster()  # 30% chance by default

    def place_items(self, dungeon: Dungeon) -> None:
        """Place health potions, vision potions, and pits."""
        for y in range(dungeon.size[1]):
            for x in range(dungeon.size[0]):
                room = dungeon.get_room(x, y)
                # Don't place items in entrance/exit or pillar rooms
                if (x, y) not in [dungeon.entrance, dungeon.exit] and not room.hasPillar:
                    # 10% chance for each item type
                    if random.random() < 0.1:
                        room.hasHealthPot = True
                    if random.random() < 0.1:
                        room.hasVisionPot = True
                    if random.random() < 0.1:
                        room.hasPit = True