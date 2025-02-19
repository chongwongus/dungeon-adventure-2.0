import pygame
from typing import List, Optional, Dict, Any
import time

from src.dungeon.room import Room

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
MAIN_VIEW_WIDTH = int(WINDOW_WIDTH * 0.7)
SIDE_PANEL_WIDTH = int(WINDOW_WIDTH * 0.3)
LOG_HEIGHT = 300
MINIMAP_SIZE = 250
STATS_HEIGHT = 150

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
DARK_GRAY = (32, 32, 32)


class EventLog:
    """Handles game event logging and display"""

    def __init__(self, max_messages: int = 100):
        self.messages: List[Dict[str, Any]] = []
        self.max_messages = max_messages
        self.scroll_position = 0
        self.font = pygame.font.Font(None, 24)

    def add_message(self, text: str, is_system: bool = False):
        """Add a message to the log and print to console."""
        message = {
            'text': text,
            'time': time.time(),
            'is_system': is_system,
            'color': RED if is_system else WHITE
        }
        self.messages.append(message)

        # Print to console with appropriate formatting
        if is_system:
            print(f"\033[91m[SYSTEM] {text}\033[0m")  # Red text for system messages
        else:
            print(f"[EVENT] {text}")

        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        # Auto-scroll to bottom
        self.scroll_position = max(0, len(self.messages) - 10)

    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        """Draw the log on the given surface."""
        # Draw background
        pygame.draw.rect(surface, DARK_GRAY, rect)

        # Calculate visible messages
        messages_per_page = rect.height // 25  # Approximate line height
        visible_messages = self.messages[self.scroll_position:
                                         self.scroll_position + messages_per_page]

        # Draw messages
        y = rect.top + 5
        for msg in visible_messages:
            text = self.font.render(msg['text'], True, msg['color'])
            surface.blit(text, (rect.left + 5, y))
            y += 25


class StatsDisplay:
    """Handles player stats display including flashing health warning"""

    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.warning_flash = False
        self.last_flash = 0
        self.flash_interval = 500  # milliseconds

    def draw(self, surface: pygame.Surface, rect: pygame.Rect, hero):
        """Draw stats including flashing health warning if HP is low."""
        pygame.draw.rect(surface, DARK_GRAY, rect)

        # Calculate health percentage
        health_percent = (hero.hp / hero._max_hp) * 100

        # Update warning flash
        current_time = pygame.time.get_ticks()
        if health_percent <= 30:
            if current_time - self.last_flash >= self.flash_interval:
                self.warning_flash = not self.warning_flash
                self.last_flash = current_time

        # Draw health (flashing if low)
        health_color = RED if health_percent <= 30 and self.warning_flash else WHITE
        health_text = f"HP: {hero.hp}/{hero._max_hp}"
        text = self.font.render(health_text, True, health_color)
        surface.blit(text, (rect.left + 10, rect.top + 10))

        # Draw inventory
        inventory_y = rect.top + 40
        potion_text = f"Health Potions: {hero.healing_potions}"
        text = self.font.render(potion_text, True, WHITE)
        surface.blit(text, (rect.left + 10, inventory_y))

        vision_text = f"Vision Potions: {hero.vision_potions}"
        text = self.font.render(vision_text, True, WHITE)
        surface.blit(text, (rect.left + 10, inventory_y + 30))

        # Draw pillars
        pillar_text = f"Pillars: {', '.join(hero.pillars) if hero.pillars else 'None'}"
        text = self.font.render(pillar_text, True, WHITE)
        surface.blit(text, (rect.left + 10, inventory_y + 60))


class MiniMap:
    """Handles mini-map display with fog of war"""

    def __init__(self, dungeon, pillar_locations):
        self.dungeon = dungeon
        self.pillar_locations = pillar_locations
        self.font = pygame.font.Font(None, 20)

        print("\n--- MINIMAP INITIALIZATION DEBUG ---")
        print(f"Dungeon Size: {dungeon.size}")
        print(f"Entrance: {dungeon.entrance}")
        print(f"Exit: {dungeon.exit}")
        for pillar, x, y in self.pillar_locations:
            print(f"Room at ({x},{y}): Pillar {pillar}")
        print("--- END MINIMAP INITIALIZATION DEBUG ---\n")

        # Enhanced colors
        self.UNEXPLORED = (20, 20, 20)  # Very dark gray
        self.ROOM_BG = (60, 60, 60)  # Dark gray
        self.CURRENT = (50, 255, 50)  # Bright green for player
        self.ENTRANCE = (50, 150, 255)  # Blue
        self.EXIT = (255, 50, 50)  # Red
        self.DOOR = (255, 255, 255)  # White
        self.PILLAR = (255, 215, 0)  # Gold
        self.BORDER = (100, 100, 100)  # Medium gray

    def calculate_room_size(self, rect: pygame.Rect) -> tuple[int, int]:
        """Calculate room size based on map rect and dungeon dimensions."""

        # Calculate available space (accounting for padding)
        available_width = rect.width - 40  # 20px padding on each side
        available_height = rect.height - 40

        # Calculate room size to fit in available space
        room_width = available_width // self.dungeon.size[0]
        room_height = available_height // self.dungeon.size[1]

        # Use smaller dimension to keep rooms square
        room_size = min(room_width, room_height)

        return room_size, room_size

    def draw_door(self, surface: pygame.Surface, room_rect: pygame.Rect, direction: str):
        """Draw a more visible door."""
        door_width = max(4, room_rect.width // 8)
        door_length = room_rect.height // 3

        if direction == 'N':
            door_rect = pygame.Rect(
                room_rect.centerx - door_width // 2,
                room_rect.top,
                door_width,
                door_length
            )
        elif direction == 'S':
            door_rect = pygame.Rect(
                room_rect.centerx - door_width // 2,
                room_rect.bottom - door_length,
                door_width,
                door_length
            )
        elif direction == 'E':
            door_rect = pygame.Rect(
                room_rect.right - door_length,
                room_rect.centery - door_width // 2,
                door_length,
                door_width
            )
        elif direction == 'W':
            door_rect = pygame.Rect(
                room_rect.left,
                room_rect.centery - door_width // 2,
                door_length,
                door_width
            )

        pygame.draw.rect(surface, self.DOOR, door_rect)

    def draw_player_marker(self, surface: pygame.Surface, room_rect: pygame.Rect):
        """Draw a distinct player marker."""
        marker_size = min(room_rect.width, room_rect.height) // 2
        center_x = room_rect.centerx
        center_y = room_rect.centery

        # Draw a filled circle for the player
        pygame.draw.circle(surface, self.CURRENT, (center_x, center_y), marker_size // 2)
        # Add a white border to make it stand out
        pygame.draw.circle(surface, WHITE, (center_x, center_y), marker_size // 2, 2)

    def _log_pillar_locations(self, dungeon):
        """Log pillar locations once during initialization."""
        print("\n--- Minimap Pillar Locations ---")
        for y in range(dungeon.size[1]):
            for x in range(dungeon.size[0]):
                room = dungeon.get_room(x, y)
                if room.hasPillar:
                    print(f"Minimap Pillar {room.pillarType} at ({x}, {y})")
        print("--- End of Minimap Pillar Locations ---\n")

    def draw(self, surface: pygame.Surface, rect: pygame.Rect, hero_pos: tuple[int, int], debug_log_minimap: bool = False):
        """Draw the mini-map."""
        # Draw background
        pygame.draw.rect(surface, DARK_GRAY, rect)

        # Calculate room size and offset
        room_width, room_height = self.calculate_room_size(rect)
        offset_x = rect.left + (rect.width - (room_width * self.dungeon.size[0])) // 2
        offset_y = rect.top + (rect.height - (room_height * self.dungeon.size[1])) // 2

        # Debug: Print calculated room size and offset
        if debug_log_minimap:
            print(f"Room size: {room_width}x{room_height}, Offset: ({offset_x}, {offset_y})")

        # Draw rooms
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                room = self.dungeon.get_room(x, y)
                room_rect = pygame.Rect(
                    offset_x + x * room_width,
                    offset_y + y * room_height,
                    room_width,
                    room_height
                )

                # Debug: Print room_rect for each room
                if debug_log_minimap:
                    print(f"Room at ({x}, {y}): {room_rect}")

                # Determine room color and always show all rooms
                if (x, y) == hero_pos:
                    color = self.CURRENT
                elif (x, y) == self.dungeon.entrance:
                    color = self.ENTRANCE
                elif (x, y) == self.dungeon.exit:
                    color = self.EXIT
                else:
                    color = self.ROOM_BG

                # Draw room with border
                pygame.draw.rect(surface, color, room_rect)
                pygame.draw.rect(surface, self.BORDER, room_rect, 2)

                # Draw doors
                for direction, has_door in room.doors.items():
                    if has_door:
                        self.draw_door(surface, room_rect, direction)

        # Draw pillar indicators based on the pillar_locations list
        for pillar, x, y in self.pillar_locations:
            room_rect = pygame.Rect(
                offset_x + x * room_width,
                offset_y + y * room_height,
                room_width,
                room_height
            )
            # Debug: Print pillar room_rect
            if debug_log_minimap:
                print(f"Pillar {pillar} at ({x}, {y}): {room_rect}")

            pillar_bg_rect = room_rect.inflate(-10, -10)  # Slightly smaller rect for background
            pygame.draw.rect(surface, self.PILLAR, pillar_bg_rect)  # Draw yellow background
            pillar_text = self.font.render(pillar, True, BLACK)
            text_rect = pillar_text.get_rect(center=room_rect.center)
            surface.blit(pillar_text, text_rect)  # Draw pillar text on top of the background


class GameWindow:
    """Main game window handler"""

    def __init__(self, dungeon, pillar_locations):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dungeon Adventure")

        # Store dungeon reference
        self.dungeon = dungeon

        # Initialize components
        self.event_log = EventLog()
        self.stats_display = StatsDisplay()
        self.minimap = MiniMap(dungeon, pillar_locations)

        # Define component rectangles
        self.main_view_rect = pygame.Rect(0, 0, MAIN_VIEW_WIDTH, WINDOW_HEIGHT)
        self.minimap_rect = pygame.Rect(
            MAIN_VIEW_WIDTH, 0,
            SIDE_PANEL_WIDTH, MINIMAP_SIZE
        )
        self.log_rect = pygame.Rect(
            MAIN_VIEW_WIDTH, MINIMAP_SIZE,
            SIDE_PANEL_WIDTH, LOG_HEIGHT
        )
        self.stats_rect = pygame.Rect(
            MAIN_VIEW_WIDTH, MINIMAP_SIZE + LOG_HEIGHT,
            SIDE_PANEL_WIDTH, STATS_HEIGHT
        )

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame events. Returns False if game should quit."""
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            # Handle log scrolling
            elif event.key == pygame.K_PAGEUP:
                self.event_log.scroll_position = max(0, self.event_log.scroll_position - 1)
            elif event.key == pygame.K_PAGEDOWN:
                self.event_log.scroll_position = min(
                    len(self.event_log.messages) - 10,
                    self.event_log.scroll_position + 1
                )
        return True

    def update(self, hero):
        """Update game state."""
        pass  # Will be implemented as we add more features

    def draw(self, hero, debug_log_minimap=False):
        """Draw the game window and all components."""
        self.screen.fill(BLACK)

        # Draw main view background
        pygame.draw.rect(self.screen, DARK_GRAY, self.main_view_rect)

        # Draw side panel components
        self.minimap.draw(self.screen, self.minimap_rect, hero.location, debug_log_minimap)
        self.event_log.draw(self.screen, self.log_rect)
        self.stats_display.draw(self.screen, self.stats_rect, hero)

        # Update display
        pygame.display.flip()
