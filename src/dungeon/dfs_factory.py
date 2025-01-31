from typing import Tuple, List
import random
from .dungeon_factory import DungeonFactory
from .dungeon import Dungeon
from .room import Room


class DFSDungeonFactory(DungeonFactory):
    """Creates dungeons using Depth-First Search algorithm for more complex mazes."""

    def create(self, size: Tuple[int, int] = (8, 8)) -> Dungeon:
        """Create a dungeon using DFS generation."""
        self.dungeon = Dungeon(size)
        self.generate_maze_dfs()
        return self.dungeon

    def generate_maze_dfs(self) -> None:
        """Generate maze structure using DFS for a fully connected maze."""
        # Initialize maze grid
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

        # Generate paths using DFS
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

        self.add_random_connections()
        self.place_items(self.dungeon)

    def add_random_connections(self) -> None:
        """Add additional random connections to make maze more interesting."""
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
