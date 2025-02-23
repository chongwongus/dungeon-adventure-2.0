import pygame
from typing import Tuple
from ..constants import WHITE, BLACK, DARK_GRAY


class MiniMap:
    def __init__(self, dungeon, pillar_locations):
        self.dungeon = dungeon
        self.pillar_locations = pillar_locations
        self.font = pygame.font.Font(None, 20)

        # Log dungeon configuration
        self._log_dungeon_config()

        # Enhanced colors
        self.UNEXPLORED = (20, 20, 20)  # Very dark gray
        self.ROOM_BG = (60, 60, 60)  # Dark gray
        self.CURRENT = (50, 255, 50)  # Bright green for player
        self.ENTRANCE = (50, 150, 255)  # Blue
        self.EXIT = (255, 50, 50)  # Red
        self.DOOR = (255, 255, 255)  # White
        self.PILLAR = (255, 215, 0)  # Gold
        self.BORDER = (100, 100, 100)  # Medium gray

    def _log_dungeon_config(self):
        """Log initial dungeon configuration"""
        print("\n=== Dungeon Configuration ===")
        print(f"Size: {self.dungeon.size[0]}x{self.dungeon.size[1]}")
        print(f"Entrance: {self.dungeon.entrance}")
        print(f"Exit: {self.dungeon.exit}")
        print("\nPillar Locations:")
        for pillar, x, y in self.pillar_locations:
            print(f"- {pillar} Pillar at ({x}, {y})")
        print("===========================\n")

    def calculate_room_size(self, rect: pygame.Rect) -> Tuple[int, int]:
        """Calculate room size based on map rect and dungeon dimensions."""
        available_width = rect.width - 40  # 20px padding on each side
        available_height = rect.height - 40

        room_width = available_width // self.dungeon.size[0]
        room_height = available_height // self.dungeon.size[1]

        # Use smaller dimension to keep rooms square
        room_size = min(room_width, room_height)
        return room_size, room_size

    def draw_door(self, surface: pygame.Surface, room_rect: pygame.Rect, direction: str):
        """Draw a door in the specified direction."""
        door_width = max(4, room_rect.width // 8)
        door_length = room_rect.height // 3

        door_rects = {
            'N': pygame.Rect(room_rect.centerx - door_width // 2, room_rect.top,
                             door_width, door_length),
            'S': pygame.Rect(room_rect.centerx - door_width // 2, room_rect.bottom - door_length,
                             door_width, door_length),
            'E': pygame.Rect(room_rect.right - door_length, room_rect.centery - door_width // 2,
                             door_length, door_width),
            'W': pygame.Rect(room_rect.left, room_rect.centery - door_width // 2,
                             door_length, door_width)
        }

        if direction in door_rects:
            pygame.draw.rect(surface, self.DOOR, door_rects[direction])

    def draw_player_marker(self, surface: pygame.Surface, room_rect: pygame.Rect):
        """Draw a distinct player marker."""
        marker_size = min(room_rect.width, room_rect.height) // 2
        center = (room_rect.centerx, room_rect.centery)

        # Draw filled circle with border
        pygame.draw.circle(surface, self.CURRENT, center, marker_size // 2)
        pygame.draw.circle(surface, WHITE, center, marker_size // 2, 2)

    def draw(self, surface: pygame.Surface, rect: pygame.Rect, hero_pos: Tuple[int, int],
             debug_log_minimap: bool = False):
        """Draw the mini-map."""
        pygame.draw.rect(surface, DARK_GRAY, rect)

        # Calculate room size and offset
        room_width, room_height = self.calculate_room_size(rect)
        offset_x = rect.left + (rect.width - (room_width * self.dungeon.size[0])) // 2
        offset_y = rect.top + (rect.height - (room_height * self.dungeon.size[1])) // 2

        if debug_log_minimap:
            self._log_debug_info(hero_pos)

        # Draw rooms
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                self._draw_room(surface, x, y, room_width, room_height,
                                offset_x, offset_y, hero_pos)

        # Draw pillars
        self._draw_pillars(surface, room_width, room_height, offset_x, offset_y)

    def _draw_room(self, surface, x, y, room_width, room_height, offset_x, offset_y, hero_pos):
        """Draw a single room with its doors."""
        room = self.dungeon.get_room(x, y)
        room_rect = pygame.Rect(
            offset_x + x * room_width,
            offset_y + y * room_height,
            room_width,
            room_height
        )

        # Determine room color
        color = self.CURRENT if (x, y) == hero_pos else \
            self.ENTRANCE if (x, y) == self.dungeon.entrance else \
                self.EXIT if (x, y) == self.dungeon.exit else \
                    self.ROOM_BG

        # Draw room and border
        pygame.draw.rect(surface, color, room_rect)
        pygame.draw.rect(surface, self.BORDER, room_rect, 2)

        # Draw doors
        for direction, has_door in room.doors.items():
            if has_door:
                self.draw_door(surface, room_rect, direction)

    def _draw_pillars(self, surface, room_width, room_height, offset_x, offset_y):
        """Draw pillar indicators on the map."""
        for pillar, x, y in self.pillar_locations:
            room_rect = pygame.Rect(
                offset_x + x * room_width,
                offset_y + y * room_height,
                room_width,
                room_height
            )

            pillar_bg_rect = room_rect.inflate(-10, -10)
            pygame.draw.rect(surface, self.PILLAR, pillar_bg_rect)

            pillar_text = self.font.render(pillar, True, BLACK)
            text_rect = pillar_text.get_rect(center=room_rect.center)
            surface.blit(pillar_text, text_rect)

    def _log_debug_info(self, hero_pos):
        """Log debug information about the current room."""
        print(f"\nPlayer moved to: ({hero_pos[0]}, {hero_pos[1]})")
        room = self.dungeon.get_room(*hero_pos)
        if room.hasPillar:
            print(f"Room contains pillar: {room.pillarType}")
        if room.hasHealthPot:
            print("Room contains health potion")
        if room.hasVisionPot:
            print("Room contains vision potion")
        if room.hasPit:
            print("Room contains pit")
        if room.monster:
            print(f"Room contains monster: {room.monster.name}")