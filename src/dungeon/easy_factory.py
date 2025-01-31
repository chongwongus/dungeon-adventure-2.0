from typing import Tuple
import random
from .dungeon_factory import DungeonFactory
from .dungeon import Dungeon
from .room import Room


class EasyDungeonFactory(DungeonFactory):
    """Creates dungeons with simpler, more open layouts."""

    def create(self, size: Tuple[int, int] = (8, 8)) -> Dungeon:
        """Create a dungeon using random generation."""
        self.dungeon = Dungeon(size)
        self.generate_maze_random()
        return self.dungeon

    def generate_maze_random(self) -> None:
        """Generate a simpler maze structure with guaranteed path to exit."""
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

        self.create_connected_maze()
        self.place_items(self.dungeon)

    def create_connected_maze(self) -> None:
        """Create a maze where every room is reachable."""
        # Create guaranteed path to exit
        current_x, current_y = 0, 0

        # Move right to near exit
        while current_x < self.dungeon.size[0] - 1:
            self.dungeon.maze[current_y][current_x].doors['E'] = True
            self.dungeon.maze[current_y][current_x + 1].doors['W'] = True
            current_x += 1

        # Move down to exit
        while current_y < self.dungeon.size[1] - 1:
            self.dungeon.maze[current_y][current_x].doors['S'] = True
            self.dungeon.maze[current_y + 1][current_x].doors['N'] = True
            current_y += 1

        # Add extra connections
        for x in range(self.dungeon.size[0]):
            for y in range(self.dungeon.size[1] - 1):
                if random.random() < 0.4:  # 40% chance
                    self.dungeon.maze[y][x].doors['S'] = True
                    self.dungeon.maze[y + 1][x].doors['N'] = True

        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0] - 1):
                if random.random() < 0.4:  # 40% chance
                    self.dungeon.maze[y][x].doors['E'] = True
                    self.dungeon.maze[y][x + 1].doors['W'] = True