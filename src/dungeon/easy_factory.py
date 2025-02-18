import random
from .dungeon import Dungeon
from .dungeon_factory import DungeonFactory
from .room import Room


class EasyDungeonFactory(DungeonFactory):
    """Creates dungeons with simpler, more open layouts."""

    def create(self, size=(8, 8)) -> Dungeon:
        self.dungeon = Dungeon(size)
        self.initialize_maze()
        self.generate_maze_easy()
        self.ensure_critical_path()
        self.validate_connections()
        self.populate_rooms(self.dungeon)

        pillar_locations = {}
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                room = self.dungeon.get_room(x, y)
                if room.hasPillar:
                    pillar_locations[room.pillarType] = (x, y)

        print("\n--- DETAILED Pillar Locations ---")
        print(f"Dungeon Size: {self.dungeon.size}")
        for pillar in Room.PILLARS:
            if pillar in pillar_locations:
                x, y = pillar_locations[pillar]
                print(f"Pillar {pillar} at ({x}, {y})")
        print(f"Entrance at {self.dungeon.entrance}")
        print(f"Exit at {self.dungeon.exit}")
        print("--- End of Detailed Pillar Locations ---\n")

        return self.dungeon

    def initialize_maze(self) -> None:
        """Initialize empty maze grid."""
        self.dungeon.maze = []
        for y in range(self.dungeon.size[1]):
            row = []
            for x in range(self.dungeon.size[0]):
                row.append(Room())
            self.dungeon.maze.append(row)

        # Set entrance and exit
        self.dungeon.entrance = (0, 0)
        self.dungeon.exit = (self.dungeon.size[0] - 1, self.dungeon.size[1] - 1)
        self.dungeon.maze[0][0].isEntrance = True
        self.dungeon.maze[self.dungeon.size[1] - 1][self.dungeon.size[0] - 1].isExit = True

    def generate_maze_easy(self) -> None:
        """
        Generate a simple maze structure ensuring good connectivity.
        Uses a grid pattern with some random connections removed.
        """
        # First create a grid where every room connects to adjacent rooms
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                current_room = self.dungeon.maze[y][x]

                # Connect to room to the east
                if x < self.dungeon.size[0] - 1:
                    current_room.doors['E'] = True
                    self.dungeon.maze[y][x + 1].doors['W'] = True

                # Connect to room to the south
                if y < self.dungeon.size[1] - 1:
                    current_room.doors['S'] = True
                    self.dungeon.maze[y + 1][x].doors['N'] = True

        # Then randomly remove some connections while ensuring reachability
        # We'll try to remove each connection with a 30% chance
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                current_room = self.dungeon.maze[y][x]

                # Try to remove east connections
                if x < self.dungeon.size[0] - 1 and random.random() < 0.3:
                    # Temporarily remove connection
                    current_room.doors['E'] = False
                    self.dungeon.maze[y][x + 1].doors['W'] = False

                    # If removing this connection would break reachability, restore it
                    if not self.dungeon.is_room_reachable(self.dungeon.entrance, self.dungeon.exit):
                        current_room.doors['E'] = True
                        self.dungeon.maze[y][x + 1].doors['W'] = True

                # Try to remove south connections
                if y < self.dungeon.size[1] - 1 and random.random() < 0.3:
                    # Temporarily remove connection
                    current_room.doors['S'] = False
                    self.dungeon.maze[y + 1][x].doors['N'] = False

                    # If removing this connection would break reachability, restore it
                    if not self.dungeon.is_room_reachable(self.dungeon.entrance, self.dungeon.exit):
                        current_room.doors['S'] = True
                        self.dungeon.maze[y + 1][x].doors['N'] = True

    def ensure_critical_path(self) -> None:
        """Ensure there's a clear path from entrance to exit."""
        # Create a path from entrance to exit
        current_x, current_y = self.dungeon.entrance
        target_x, target_y = self.dungeon.exit

        while current_x != target_x or current_y != target_y:
            current_room = self.dungeon.maze[current_y][current_x]

            # Move horizontally first
            if current_x < target_x:
                current_room.doors['E'] = True
                self.dungeon.maze[current_y][current_x + 1].doors['W'] = True
                current_x += 1
            elif current_x > target_x:
                current_room.doors['W'] = True
                self.dungeon.maze[current_y][current_x - 1].doors['E'] = True
                current_x -= 1
            # Then move vertically
            elif current_y < target_y:
                current_room.doors['S'] = True
                self.dungeon.maze[current_y + 1][current_x].doors['N'] = True
                current_y += 1
            elif current_y > target_y:
                current_room.doors['N'] = True
                self.dungeon.maze[current_y - 1][current_x].doors['S'] = True
                current_y -= 1

    def validate_connections(self) -> None:
        """Validate that all door connections are bidirectional."""
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                current_room = self.dungeon.maze[y][x]

                # Check east connection
                if x < self.dungeon.size[0] - 1:
                    next_room = self.dungeon.maze[y][x + 1]
                    if current_room.doors['E'] != next_room.doors['W']:
                        # Fix inconsistency
                        current_room.doors['E'] = False
                        next_room.doors['W'] = False

                # Check south connection
                if y < self.dungeon.size[1] - 1:
                    next_room = self.dungeon.maze[y + 1][x]
                    if current_room.doors['S'] != next_room.doors['N']:
                        # Fix inconsistency
                        current_room.doors['S'] = False
                        next_room.doors['N'] = False
