import random
from .dungeon import Dungeon
from .dungeon_factory import DungeonFactory
from .room import Room

class EasyDungeonFactory(DungeonFactory):
    """
    Generates dungeons with a simpler, more straightforward layout strategy.

    This factory creates dungeon layouts that are more predictable
    and user-friendly, contrasting with more complex maze generation
    approaches.

    Key Generation Characteristics:
    - Initial fully-connected grid creation
    - Controlled randomness in path removal
    - Guaranteed path between entrance and exit
    - Simplified navigation experience

    Methods provide a step-by-step approach to dungeon creation
    that ensures playability while maintaining an element of surprise.
    """

    def __init__(self):
        super().__init__()
        self.dungeon = None

    def create(self, size=(8, 8)) -> Dungeon:
        """
        Generate a complete dungeon using a simplified generation strategy.

        This method orchestrates the entire dungeon creation process
        through a series of carefully designed steps:

        1. Initialize an empty dungeon grid
        2. Generate a base maze structure
        3. Ensure a critical path exists between entrance and exit
        4. Validate room connections
        5. Populate rooms with monsters, items, and pillars

        The approach differs from DFS generation by:
        - Creating a more grid-like initial structure
        - Applying more controlled randomness
        - Explicitly ensuring navigability

        Args:
            size (tuple, optional): Dimensions of the dungeon grid.
                                    Defaults to an 8x8 grid.

        Returns:
            Dungeon: A fully generated and populated dungeon instance
        """
        self.dungeon = Dungeon(size)
        self.initialize_maze()
        self.generate_maze_easy()
        self.ensure_critical_path()
        self.validate_connections()
        self.populate_rooms(self.dungeon)  # This will also print layout
        return self.dungeon

    def initialize_maze(self) -> None:
        """
        Set up the initial empty dungeon grid.

        This method prepares the foundational structure for the dungeon by:
        - Creating a 2D grid of empty Room instances
        - Defining entrance at the top-left corner
        - Setting exit at the bottom-right corner
        - Marking entrance and exit rooms

        The initial grid serves as a blank canvas for the
        dungeon generation algorithm, providing a consistent
        starting point for maze creation.
        """
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
        Create a maze structure with simplified connectivity rules.

        This method generates the dungeon layout through a two-phase process:
        1. Initial Connection Phase:
           - Connect every room to its immediate neighbors
           - Create a fully connected grid
           - Establish east and south connections

        2. Randomization Phase:
           - Randomly remove some connections
           - Ensure path between entrance and exit remains viable
           - Introduce controlled unpredictability

        Key Algorithm Steps:
        - Start with a fully connected grid
        - Apply 30% chance of connection removal
        - Validate dungeon reachability after each removal
        - Maintain a guaranteed path between entrance and exit

        The approach creates a more predictable but still
        interesting dungeon layout.
        """
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
        """
        Guarantee a clear path between dungeon entrance and exit.

        This method creates a definitive route through the dungeon by:
        - Starting at the entrance coordinates
        - Moving systematically towards the exit
        - Prioritizing horizontal movement first
        - Then completing vertical movement
        - Establishing bidirectional connections along the path

        The algorithm ensures that:
        - There's always a way to traverse the dungeon
        - The path feels natural and less artificially constructed
        - Players can always progress through the dungeon

        Navigation Strategy:
        1. Move horizontally towards exit x-coordinate
        2. Move vertically towards exit y-coordinate
        3. Create connections in each movement step
        """
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
        """
        Verify and correct dungeon room connections.

        This method performs a comprehensive check of room connections to:
        - Ensure bidirectional consistency
        - Detect and correct connection mismatches
        - Maintain the integrity of the dungeon layout

        Validation Process:
        - Check east-facing connections
        - Verify south-facing connections
        - Correct any unidirectional door instances
        - Maintain symmetric room connections

        By systematically validating connections, the method
        prevents potential navigation issues and ensures a
        logically consistent dungeon structure.
        """
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

