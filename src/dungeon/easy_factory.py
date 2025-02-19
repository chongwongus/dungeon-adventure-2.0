import random
from .dungeon import Dungeon
from .dungeon_factory import DungeonFactory
from .room import Room

class EasyDungeonFactory(DungeonFactory):
    """Creates dungeons with simpler, more open layouts."""

    def create(self, size=(8, 8)) -> Dungeon:
        """Create dungeon using simple generation."""
        self.dungeon = Dungeon(size)
        self.initialize_maze()
        self.generate_maze_easy()
        self.ensure_critical_path()
        self.validate_connections()
        self.populate_rooms(self.dungeon)  # This will also print layout
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
        """Generate a simple maze structure ensuring good connectivity."""
        # First create a grid where every room connects to adjacent rooms
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                # Connect to room to the east
                if x < self.dungeon.size[0] - 1:
                    self.ensure_bidirectional_connection(self.dungeon, x, y, x + 1, y, 'E', 'W')
                # Connect to room to the south
                if y < self.dungeon.size[1] - 1:
                    self.ensure_bidirectional_connection(self.dungeon, x, y, x, y + 1, 'S', 'N')

        # Then randomly remove some connections while ensuring reachability
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                # Try to remove east connections
                if x < self.dungeon.size[0] - 1 and random.random() < 0.3:
                    self.remove_connection(self.dungeon, x, y, x + 1, y, 'E', 'W')
                    if not self.dungeon.is_room_reachable(self.dungeon.entrance, self.dungeon.exit):
                        self.ensure_bidirectional_connection(self.dungeon, x, y, x + 1, y, 'E', 'W')

                # Try to remove south connections
                if y < self.dungeon.size[1] - 1 and random.random() < 0.3:
                    self.remove_connection(self.dungeon, x, y, x, y + 1, 'S', 'N')
                    if not self.dungeon.is_room_reachable(self.dungeon.entrance, self.dungeon.exit):
                        self.ensure_bidirectional_connection(self.dungeon, x, y, x, y + 1, 'S', 'N')

    def ensure_critical_path(self) -> None:
        """Ensure there's a clear path from entrance to exit."""
        # Create a path from entrance to exit
        current_x, current_y = self.dungeon.entrance
        target_x, target_y = self.dungeon.exit

        while current_x != target_x or current_y != target_y:
            current_room = self.dungeon.maze[current_y][current_x]

            # Move horizontally first
            if current_x < target_x:
                self.ensure_bidirectional_connection(self.dungeon, current_x, current_y,
                                                  current_x + 1, current_y, 'E', 'W')
                current_x += 1
            elif current_x > target_x:
                self.ensure_bidirectional_connection(self.dungeon, current_x, current_y,
                                                  current_x - 1, current_y, 'W', 'E')
                current_x -= 1
            # Then move vertically
            elif current_y < target_y:
                self.ensure_bidirectional_connection(self.dungeon, current_x, current_y,
                                                  current_x, current_y + 1, 'S', 'N')
                current_y += 1
            elif current_y > target_y:
                self.ensure_bidirectional_connection(self.dungeon, current_x, current_y,
                                                  current_x, current_y - 1, 'N', 'S')
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

