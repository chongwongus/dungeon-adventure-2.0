import pygame
from typing import Tuple, Dict, Optional
from ..constants import *


class FirstPersonView:
    """Renders a first-person perspective of the dungeon"""

    def __init__(self, screen_rect: pygame.Rect):
        self.rect = screen_rect

        # Color definitions
        self.WALL_COLOR = (80, 80, 80)  # Gray
        self.CEILING_COLOR = (40, 40, 60)  # Dark blue-gray
        self.FLOOR_COLOR = (60, 50, 40)  # Brown
        self.DOOR_COLOR = (120, 80, 40)  # Wood brown

        # Placeholder colors for content
        self.MONSTER_COLOR = (200, 40, 40)  # Red
        self.ITEM_COLOR = (220, 220, 40)  # Yellow
        self.PILLAR_COLOR = (40, 200, 200)  # Cyan

        # Placeholder for future textures
        self.textures = {}

    def draw(self, surface: pygame.Surface, dungeon, hero_pos: Tuple[int, int], hero_direction: str):
        """
        Draw the first-person view from the hero's perspective.

        Args:
            surface: Pygame surface to draw on
            dungeon: Dungeon object with room data
            hero_pos: (x, y) coordinates of hero
            hero_direction: Direction hero is facing ('N', 'S', 'E', 'W')
        """
        # Clear the view area
        pygame.draw.rect(surface, BLACK, self.rect)

        # Get current room
        current_room = dungeon.get_room(*hero_pos)
        if not current_room:
            return

        # Basic corridor drawing (floor, ceiling, walls)
        self._draw_corridor(surface)

        # Draw doors in available directions
        self._draw_doors(surface, current_room, hero_direction)

        # Draw room contents if visible
        if current_room.monster and current_room.monster.is_alive:
            self._draw_monster(surface, current_room.monster)

        if current_room.hasPillar:
            self._draw_pillar(surface, current_room.pillarType)

        if current_room.hasHealthPot:
            self._draw_item(surface, "health_potion", (self.rect.width // 4, self.rect.bottom - 100))

        if current_room.hasVisionPot:
            self._draw_item(surface, "vision_potion", (self.rect.width * 3 // 4, self.rect.bottom - 100))

        # Draw entrance/exit indicators
        if current_room.isEntrance:
            self._draw_text(surface, "ENTRANCE", (self.rect.centerx, 40))

        if current_room.isExit:
            self._draw_text(surface, "EXIT", (self.rect.centerx, 40))

    def _draw_corridor(self, surface: pygame.Surface):
        """Draw the basic corridor structure (floor, ceiling, walls)"""
        width, height = self.rect.width, self.rect.height

        # Draw ceiling
        ceiling_rect = pygame.Rect(0, 0, width, height // 3)
        pygame.draw.rect(surface, self.CEILING_COLOR, ceiling_rect)

        # Draw floor
        floor_rect = pygame.Rect(0, height * 2 // 3, width, height // 3)
        pygame.draw.rect(surface, self.FLOOR_COLOR, floor_rect)

        # Draw left wall (trapezoid)
        left_wall = [
            (0, 0),  # Top left
            (width // 4, height // 3),  # Middle left
            (width // 4, height * 2 // 3),  # Bottom left
            (0, height)  # Bottom far left
        ]
        pygame.draw.polygon(surface, self.WALL_COLOR, left_wall)

        # Draw right wall (trapezoid)
        right_wall = [
            (width, 0),  # Top right
            (width * 3 // 4, height // 3),  # Middle right
            (width * 3 // 4, height * 2 // 3),  # Bottom right
            (width, height)  # Bottom far right
        ]
        pygame.draw.polygon(surface, self.WALL_COLOR, right_wall)

        # Draw perspective lines
        pygame.draw.line(surface, (0, 0, 0), (0, 0), (width // 4, height // 3), 2)
        pygame.draw.line(surface, (0, 0, 0), (width, 0), (width * 3 // 4, height // 3), 2)
        pygame.draw.line(surface, (0, 0, 0), (0, height), (width // 4, height * 2 // 3), 2)
        pygame.draw.line(surface, (0, 0, 0), (width, height), (width * 3 // 4, height * 2 // 3), 2)

        # Horizontal dividing lines
        pygame.draw.line(surface, (0, 0, 0), (0, height // 3), (width, height // 3), 2)
        pygame.draw.line(surface, (0, 0, 0), (0, height * 2 // 3), (width, height * 2 // 3), 2)

        # Vertical dividing lines
        pygame.draw.line(surface, (0, 0, 0), (width // 4, height // 3), (width // 4, height * 2 // 3), 2)
        pygame.draw.line(surface, (0, 0, 0), (width * 3 // 4, height // 3), (width * 3 // 4, height * 2 // 3), 2)

    def _get_relative_doors(self, room, hero_direction: str) -> Dict[str, bool]:
        """
        Convert absolute door directions to relative (forward, left, right)
        based on hero's facing direction
        """
        # Map of how directions change based on facing
        direction_map = {
            'N': {'forward': 'N', 'left': 'W', 'right': 'E'},
            'S': {'forward': 'S', 'left': 'E', 'right': 'W'},
            'E': {'forward': 'E', 'left': 'N', 'right': 'S'},
            'W': {'forward': 'W', 'left': 'S', 'right': 'N'}
        }

        # Get mapping for current direction
        dir_map = direction_map.get(hero_direction, {})

        # Return dictionary of relative directions with door presence
        return {
            'forward': room.doors.get(dir_map.get('forward', ''), False),
            'left': room.doors.get(dir_map.get('left', ''), False),
            'right': room.doors.get(dir_map.get('right', ''), False)
        }

    def _draw_doors(self, surface: pygame.Surface, room, hero_direction: str):
        """Draw doors based on available exits and hero's facing direction"""
        width, height = self.rect.width, self.rect.height

        # Get available doors adjusted for hero's perspective
        doors = self._get_relative_doors(room, hero_direction)

        # Draw forward door (if present)
        if doors.get('forward'):
            self._draw_forward_door(surface)

        # Draw left door (if present)
        if doors.get('left'):
            self._draw_left_door(surface)

        # Draw right door (if present)
        if doors.get('right'):
            self._draw_right_door(surface)

    def _draw_forward_door(self, surface: pygame.Surface):
        """Draw door at the end of the corridor"""
        width, height = self.rect.width, self.rect.height

        # Calculate door dimensions (centered in corridor)
        door_width = width // 3
        door_height = height // 3

        # Door position
        x = (width - door_width) // 2
        y = height // 3

        # Draw door
        door_rect = pygame.Rect(x, y, door_width, door_height)
        pygame.draw.rect(surface, self.DOOR_COLOR, door_rect)
        pygame.draw.rect(surface, (0, 0, 0), door_rect, 2)  # Border

        # Draw door handle
        handle_x = x + door_width * 3 // 4
        handle_y = y + door_height // 2
        pygame.draw.circle(surface, (0, 0, 0), (handle_x, handle_y), 5)

    def _draw_left_door(self, surface: pygame.Surface):
        """Draw door on the left wall"""
        width, height = self.rect.width, self.rect.height

        # Door as a polygon to match perspective
        door_poly = [
            (width // 8, height // 3 + height // 12),  # Top left
            (width // 4 - 10, height // 3 + height // 12),  # Top right
            (width // 4 - 10, height * 2 // 3 - height // 12),  # Bottom right
            (width // 8, height * 2 // 3 - height // 12)  # Bottom left
        ]

        # Draw door
        pygame.draw.polygon(surface, self.DOOR_COLOR, door_poly)
        pygame.draw.polygon(surface, (0, 0, 0), door_poly, 2)  # Border

        # Door handle
        handle_x = width // 4 - 20
        handle_y = height // 2
        pygame.draw.circle(surface, (0, 0, 0), (handle_x, handle_y), 3)

    def _draw_right_door(self, surface: pygame.Surface):
        """Draw door on the right wall"""
        width, height = self.rect.width, self.rect.height

        # Door as a polygon to match perspective
        door_poly = [
            (width * 3 // 4 + 10, height // 3 + height // 12),  # Top left
            (width * 7 // 8, height // 3 + height // 12),  # Top right
            (width * 7 // 8, height * 2 // 3 - height // 12),  # Bottom right
            (width * 3 // 4 + 10, height * 2 // 3 - height // 12)  # Bottom left
        ]

        # Draw door
        pygame.draw.polygon(surface, self.DOOR_COLOR, door_poly)
        pygame.draw.polygon(surface, (0, 0, 0), door_poly, 2)  # Border

        # Door handle
        handle_x = width * 3 // 4 + 20
        handle_y = height // 2
        pygame.draw.circle(surface, (0, 0, 0), (handle_x, handle_y), 3)

    def _draw_monster(self, surface: pygame.Surface, monster):
        """Draw a monster in the corridor"""
        width, height = self.rect.width, self.rect.height

        # Center position for monster
        center_x = width // 2
        center_y = height // 2

        # Size based on monster type (placeholder)
        size = min(width, height) // 4

        # Draw monster silhouette (placeholder)
        monster_rect = pygame.Rect(center_x - size // 2, center_y - size // 2, size, size)
        pygame.draw.rect(surface, self.MONSTER_COLOR, monster_rect)
        pygame.draw.rect(surface, (0, 0, 0), monster_rect, 2)  # Border

        # Draw monster name
        self._draw_text(surface, monster.name, (center_x, center_y - size // 2 - 20))

    def _draw_pillar(self, surface: pygame.Surface, pillar_type: str):
        """Draw a pillar in the corridor"""
        width, height = self.rect.width, self.rect.height

        # Center position for pillar
        center_x = width // 2
        center_y = height // 2

        # Pillar dimensions
        pillar_width = width // 8
        pillar_height = height // 3

        # Draw pillar
        pillar_rect = pygame.Rect(center_x - pillar_width // 2, center_y - pillar_height // 2,
                                  pillar_width, pillar_height)
        pygame.draw.rect(surface, self.PILLAR_COLOR, pillar_rect)
        pygame.draw.rect(surface, (0, 0, 0), pillar_rect, 2)  # Border

        # Draw pillar name
        self._draw_text(surface, f"Pillar of {pillar_type}", (center_x, center_y - pillar_height // 2 - 20))

    def _draw_item(self, surface: pygame.Surface, item_type: str, pos: Tuple[int, int]):
        """Draw an item in the corridor"""
        # Draw item as a simple circle for now
        if item_type == "health_potion":
            color = (255, 0, 0)  # Red for health
            label = "Health Potion"
        elif item_type == "vision_potion":
            color = (0, 0, 255)  # Blue for vision
            label = "Vision Potion"
        else:
            color = (255, 255, 0)  # Yellow default
            label = "Item"

        # Draw item
        pygame.draw.circle(surface, color, pos, 15)
        pygame.draw.circle(surface, (0, 0, 0), pos, 15, 2)  # Border

        # Draw label
        self._draw_text(surface, label, (pos[0], pos[1] - 25))

    def _draw_text(self, surface: pygame.Surface, text: str, pos: Tuple[int, int]):
        """Helper to draw text with shadow"""
        font = pygame.font.Font(None, 24)

        # Shadow
        shadow = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(pos[0] + 2, pos[1] + 2))
        surface.blit(shadow, shadow_rect)

        # Text
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=pos)
        surface.blit(text_surf, text_rect)