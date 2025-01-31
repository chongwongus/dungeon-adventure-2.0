from typing import Tuple, Optional, List
from .room import Room


class Dungeon:
    """Represents the game dungeon, including rooms and maze generation."""

    def __init__(self, size: Tuple[int, int] = (8, 8)):
        self.size = size
        self.maze: List[List[Room]] = [[]]
        self.entrance: Optional[Tuple[int, int]] = None
        self.exit: Optional[Tuple[int, int]] = None

    def is_room_reachable(self, start: Tuple[int, int], target: Tuple[int, int]) -> bool:
        """Check if there is a path between start and target positions."""
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
        """Return the room at the given position if it exists."""
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            return self.maze[y][x]
        return None

    def is_valid_move(self, current_pos: Tuple[int, int], direction: str) -> bool:
        """Check if move from current position in given direction is valid."""
        x, y = current_pos
        current_room = self.get_room(x, y)

        if not current_room or not current_room.doors[direction]:
            return False

        new_x, new_y = x, y
        if direction == 'N':
            new_y -= 1
        elif direction == 'S':
            new_y += 1
        elif direction == 'E':
            new_x += 1
        elif direction == 'W':
            new_x -= 1

        if not (0 <= new_x < self.size[0] and 0 <= new_y < self.size[1]):
            return False

        dest_room = self.get_room(new_x, new_y)
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        return dest_room.doors[opposite[direction]]

    def __str__(self) -> str:
        """Return string representation of entire dungeon."""
        result = []
        for row in self.maze:
            room_lines = [str(room).split('\n') for room in row]
            if result:
                result.append('     ' * len(row))
            for i in range(3):
                result.append('  '.join(room[i] for room in room_lines))
        return '\n'.join(result)