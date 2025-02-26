import random

from .dungeon import Dungeon
from .dungeon_factory import DungeonFactory
from .room import Room


class DFSDungeonFactory(DungeonFactory):
    """
    Generates dungeons using a Depth-First Search (DFS) maze generation algorithm.

    This factory creates complex dungeon layouts with intricate pathways
    and guaranteed room connectivity. The generation process mimics how
    a depth-first search would explore and map out a graph.

    Methods:
        create(): Primary method for generating a complete dungeon
        initialize_maze(): Set up the initial empty dungeon grid
        generate_maze_dfs(): Core algorithm for creating maze-like pathways
        add_random_connections(): Introduce additional random room connections
    """

    def create(self, size=(8, 8)) -> Dungeon:
        """
        Generate a complete dungeon using the DFS algorithm.

        This method orchestrates the entire dungeon creation process by:
        1. Creating a base dungeon with specified size
        2. Initializing an empty maze grid
        3. Generating maze structure using depth-first search
        4. Adding random additional connections
        5. Populating rooms with monsters, items, and pillars

        The method ensures a fully functional, interconnected dungeon
        that provides an interesting exploration experience.

        Args:
            size (tuple, optional): Dimensions of the dungeon grid.
                                    Defaults to an 8x8 grid.

        Returns:
            Dungeon: A fully generated and populated dungeon instance
        """
        self.dungeon = Dungeon(size)
        self.initialize_maze()
        self.generate_maze_dfs()
        self.add_random_connections()
        self.populate_rooms(self.dungeon)
        return self.dungeon

    def initialize_maze(self) -> None:
        """
        Initialize an empty maze grid for dungeon generation.

        This method:
        1. Creates a 2D list of empty Room instances
        2. Sets the entrance at the top-left corner
        3. Sets the exit at the bottom-right corner
        4. Marks the entrance and exit rooms appropriately

        The grid is prepared as a blank canvas for the maze generation
        algorithm to create pathways and connections.
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

    def generate_maze_dfs(self) -> None:
        """
        Generate dungeon pathways using Depth-First Search algorithm.

        This complex method creates a maze-like structure by:
        1. Using a stack-based approach to explore room connections
        2. Randomly selecting unvisited neighboring rooms
        3. Creating bidirectional paths between current and selected rooms
        4. Backtracking when no unvisited neighbors exist

        Key Algorithmic Steps:
        - Start at the entrance
        - Mark current room as visited
        - Identify unvisited neighboring rooms
        - Randomly choose a neighbor
        - Create a path between current room and chosen neighbor
        - Recursively continue or backtrack
        - Ensure complete exploration of the dungeon grid

        The randomness ensures each generated dungeon is unique while
        maintaining full connectivity.
        """
        visited = set()
        stack = [self.dungeon.entrance]

        while stack:
            current = stack[-1]
            x, y = current
            visited.add(current)

            # Get unvisited neighbors
            neighbors = []
            possible_moves = [
                ('N', (x, y - 1)),
                ('S', (x, y + 1)),
                ('E', (x + 1, y)),
                ('W', (x - 1, y))
            ]

            for direction, (nx, ny) in possible_moves:
                if (0 <= nx < self.dungeon.size[0] and
                        0 <= ny < self.dungeon.size[1] and
                        (nx, ny) not in visited):
                    neighbors.append((direction, (nx, ny)))

            if neighbors:
                direction, next_cell = random.choice(neighbors)
                nx, ny = next_cell

                # Create path between cells
                self.dungeon.maze[y][x].doors[direction] = True
                opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
                self.dungeon.maze[ny][nx].doors[opposite[direction]] = True

                stack.append(next_cell)
            else:
                stack.pop()

    def add_random_connections(self) -> None:
        """
        Introduce additional random connections to enhance dungeon complexity.

        This method adds extra pathways with a 15% probability for:
        - East-facing connections
        - South-facing connections

        Purpose:
        - Break up the strict DFS-generated path
        - Create more interesting and less predictable dungeon layouts
        - Provide alternative navigation routes

        The method ensures that added connections do not compromise
        the overall dungeon structure or connectivity.
        """
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                if x < self.dungeon.size[0] - 1:
                    if random.random() < 0.15:  # 15% chance
                        self.dungeon.maze[y][x].doors['E'] = True
                        self.dungeon.maze[y][x + 1].doors['W'] = True

                if y < self.dungeon.size[1] - 1:
                    if random.random() < 0.15:
                        self.dungeon.maze[y][x].doors['S'] = True
                        self.dungeon.maze[y + 1][x].doors['N'] = True