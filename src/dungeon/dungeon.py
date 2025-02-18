# src/dungeon/dungeon.py
from typing import Tuple, Optional, List
from .room import Room
import random


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

    def get_room_in_direction(self, current_pos: Tuple[int, int], direction: str) -> Optional[Tuple[int, int]]:
        """
        Get coordinates of room in given direction from current position.
        Returns None if movement would be out of bounds.
        """
        x, y = current_pos
        new_x, new_y = x, y

        if direction == 'N':
            new_y -= 1
        elif direction == 'S':
            new_y += 1
        elif direction == 'E':
            new_x += 1
        elif direction == 'W':
            new_x -= 1

        # Check if new position would be in bounds
        if 0 <= new_x < self.size[0] and 0 <= new_y < self.size[1]:
            return (new_x, new_y)
        return None

    def move_hero(self, hero, direction: str) -> bool:
        """
        Attempt to move hero in given direction.
        Returns True if move was successful.
        """
        if not hero.location:
            return False

        # Validate the move using door checks
        current_room = self.get_room(*hero.location)
        if not current_room or not current_room.doors[direction]:
            return False

        # Calculate new position
        new_pos = self.get_room_in_direction(hero.location, direction)
        if not new_pos:
            return False

        # Check connecting door
        new_room = self.get_room(*new_pos)
        opposite_directions = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        if not new_room.doors[opposite_directions[direction]]:
            return False

        # Move is valid - update position
        hero.move(direction)
        new_room.visited = True

        # Apply room effects
        self.apply_room_effects(hero)

        return True

    def apply_room_effects(self, hero) -> List[str]:
        """
        Apply effects of current room to hero.
        Returns list of message strings describing what happened.
        """
        messages = []
        room = self.get_room(*hero.location)

        # Handle pit damage
        if room.hasPit:
            damage = random.randint(10, 20)  # Pit deals 10-20 damage
            hero.take_damage(damage)
            messages.append(f"You fell into a pit and took {damage} damage!")

        # Handle item collection
        if room.hasHealthPot:
            hero.collect_potion("healing")
            room.hasHealthPot = False
            messages.append("You found a healing potion!")

        if room.hasVisionPot:
            hero.collect_potion("vision")
            room.hasVisionPot = False
            messages.append("You found a vision potion!")

        if room.hasPillar:
            hero.collect_pillar(room.pillarType)
            room.hasPillar = False
            messages.append(f"You found the {room.pillarType} pillar!")

        return messages

    def reveal_adjacent_rooms(self, center_pos: Tuple[int, int]) -> None:
        """Mark all adjacent rooms as visited when using a vision potion."""
        x, y = center_pos
        # Check all adjacent positions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size[0] and 0 <= new_y < self.size[1]:
                self.maze[new_y][new_x].visited = True

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