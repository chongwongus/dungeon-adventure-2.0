import pygame
from typing import Tuple
from ..constants import WHITE, BLACK, DARK_GRAY


class MiniMap:
    """
    Generates a dynamic, informative top-down dungeon map.

    Serves as a critical navigation and information tool that
    transforms the complex dungeon grid into an easily
    comprehensible visual representation.

    Core Mapping Responsibilities:
    - Render dungeon room grid
    - Track and display player location
    - Visualize room contents and state
    - Support exploration progression

    Design Components:
    1. Room Rendering System
       - Calculate optimal room sizes
       - Support variable dungeon dimensions
       - Maintain visual consistency

    2. Color-Coded Information
       - Use distinct colors for different room states
       - Provide instant visual feedback
       - Communicate complex dungeon information at a glance

    Visualization Strategies:
    The minimap transforms abstract dungeon data into an
    intuitive, information-rich visual representation that
    helps players understand their environment quickly and
    effectively.
    """

    def __init__(self, dungeon, pillar_locations):
        """
        Initialize the minimap rendering system.

        Sets up the foundational components for dungeon visualization:
        - Store dungeon reference
        - Track pillar locations
        - Prepare font for room labeling
        - Define a comprehensive color palette

        Initialization Process:
        1. Attempt to load custom font
        2. Provide system font fallback
        3. Create a rich color scheme for different room states

        Color Palette Design:
        - Unexplored rooms: Very dark gray
        - Visited rooms: Dark gray
        - Player location: Bright green
        - Entrance: Blue
        - Exit: Red
        - Doors: White
        - Special elements (pillars): Gold

        Args:
            dungeon: The dungeon object to be visualized
            pillar_locations: List of special pillar locations
        """
        self.dungeon = dungeon
        self.pillar_locations = pillar_locations
        try:
            self.font = pygame.font.Font("src/assets/fonts/ActionMan.ttf", 16)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, 16)

        # Enhanced colors
        self.UNEXPLORED = (20, 20, 20)  # Very dark gray
        self.ROOM_BG = (60, 60, 60)  # Dark gray
        self.CURRENT = (50, 255, 50)  # Bright green for player
        self.ENTRANCE = (50, 150, 255)  # Blue
        self.EXIT = (255, 50, 50)  # Red
        self.DOOR = (255, 255, 255)  # White
        self.PILLAR = (255, 215, 0)  # Gold
        self.BORDER = (100, 100, 100)  # Medium gray
        self.MONSTER = (255, 0, 0)  # Red for monsters
        self.TRAP = (255, 100, 0)  # Orange for traps

    def calculate_room_size(self, rect: pygame.Rect) -> Tuple[int, int]:
        """
        Dynamically calculate optimal room size for minimap rendering.

        This method ensures that:
        - Rooms are consistently sized
        - The entire map fits within the available space
        - The aspect ratio remains square-like

        Size Calculation Strategy:
        1. Determine available width and height
        2. Divide space by dungeon grid dimensions
        3. Choose the smaller dimension to maintain square rooms
        4. Add padding to prevent edge-to-edge rendering

        Adaptive Rendering Considerations:
        - Supports different dungeon sizes
        - Maintains visual clarity
        - Prevents room distortion

        Args:
            rect: The rectangular area allocated for the minimap

        Returns:
            Tuple of (room_width, room_height)
        """
        available_width = rect.width - 40  # 20px padding on each side
        available_height = rect.height - 40

        room_width = available_width // self.dungeon.size[0]
        room_height = available_height // self.dungeon.size[1]

        # Use smaller dimension to keep rooms square
        room_size = min(room_width, room_height)
        return room_size, room_size

    def draw_door(self, surface: pygame.Surface, room_rect: pygame.Rect, direction: str):
        """
        Render door connections between rooms.

        Implements a sophisticated door rendering system that:
        - Represents room connectivity
        - Uses minimal but clear visual indicators
        - Supports all four cardinal directions

        Door Rendering Techniques:
        1. Calculate door width proportional to room size
        2. Create door rectangles for each direction
        3. Render doors with consistent styling

        Args:
            surface: Pygame surface for rendering
            room_rect: Rectangle representing the room
            direction: Door direction ('N', 'S', 'E', 'W')
        """
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
        """
        Create a distinctive marker for the player's current location.

        Designs a visual indicator that:
        - Clearly shows player position
        - Stands out from other room elements
        - Provides immediate spatial awareness

        Player Marker Design:
        - Filled circle in distinctive color
        - White border for contrast
        - Centered in the room
        - Sized proportionally to room dimensions

        Args:
            surface: Pygame surface for rendering
            room_rect: Rectangle representing the player's current room
        """
        marker_size = min(room_rect.width, room_rect.height) // 2
        center = (room_rect.centerx, room_rect.centery)

        # Draw filled circle with border
        pygame.draw.circle(surface, self.CURRENT, center, marker_size // 2)
        pygame.draw.circle(surface, WHITE, center, marker_size // 2, 2)

    def draw(self, surface: pygame.Surface, rect: pygame.Rect, hero_pos: Tuple[int, int],
             debug_log_minimap: bool = False):
        """
        Render the complete minimap visualization.

        Comprehensive rendering method that:
        1. Prepares the drawing surface
        2. Calculates room sizes and positioning
        3. Draws each room in the dungeon
        4. Optionally logs debug information

        Rendering Workflow:
        - Set up background
        - Compute room dimensions
        - Iterate through dungeon grid
        - Render each room with its current state
        - Highlight player location

        Args:
            surface: Pygame surface for rendering
            rect: Rectangular area for minimap
            hero_pos: Current player coordinates
            debug_log_minimap: Flag to enable detailed logging
        """
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

    def _draw_room(self, surface, x, y, room_width, room_height, offset_x, offset_y, hero_pos):
        """
        Render an individual room with its specific state and contents.

        This method is the core of the minimap's information display,
        responsible for:
        - Determining room color based on state
        - Rendering room background
        - Drawing doors
        - Displaying room-specific content

        Content Rendering Hierarchy:
        1. Determine room color (unexplored, visited, current)
        2. Draw room background
        3. Render doors
        4. Display special contents (pillars, monsters, items)
        5. Add player marker if applicable

        Args:
            surface: Pygame surface for rendering
            x, y: Room grid coordinates
            room_width, room_height: Dimensions of each room
            offset_x, offset_y: Positioning offsets
            hero_pos: Current player location
        """
        room = self.dungeon.get_room(x, y)
        room_rect = pygame.Rect(
            offset_x + x * room_width,
            offset_y + y * room_height,
            room_width,
            room_height
        )

        # Determine room color based on content/status
        if (x, y) == hero_pos:
            color = self.CURRENT
        elif (x, y) == self.dungeon.entrance:
            color = self.ENTRANCE
        elif (x, y) == self.dungeon.exit:
            color = self.EXIT
        else:
            color = self.ROOM_BG if room.visited else self.UNEXPLORED

        # Draw the room
        pygame.draw.rect(surface, color, room_rect)
        pygame.draw.rect(surface, self.BORDER, room_rect, 1)

        # Only draw details for visited rooms or the player's current room
        if not room.visited and (x, y) != hero_pos:
            return

        # Draw doors for visited rooms
        for direction, has_door in room.doors.items():
            if has_door:
                self.draw_door(surface, room_rect, direction)

        # Draw room contents
        center_x = room_rect.centerx
        center_y = room_rect.centery
        font = self.font

        # Check if this is a pillar room
        is_pillar_room = False
        for pillar, px, py in self.pillar_locations:
            if (x, y) == (px, py):
                is_pillar_room = True
                # Draw pillar in gold
                pillar_text = font.render(pillar, True, BLACK)
                pillar_rect = pillar_text.get_rect(center=(center_x, center_y))
                pygame.draw.rect(surface, self.PILLAR, pillar_rect.inflate(6, 6))
                surface.blit(pillar_text, pillar_rect)
                break

        # Draw other room contents if not a pillar room
        if not is_pillar_room:
            # Draw monster with skull emoji
            if room.monster and room.monster.is_alive:
                monster_text = font.render("☠", True, self.MONSTER)
                monster_rect = monster_text.get_rect(center=(center_x, center_y))
                surface.blit(monster_text, monster_rect)

            # Draw pit with spike emoji
            elif room.hasPit:
                pit_text = font.render("⚡", True, self.TRAP)
                pit_rect = pit_text.get_rect(center=(center_x, center_y))
                surface.blit(pit_text, pit_rect)

            # Draw potions
            elif room.hasHealthPot and room.hasVisionPot:
                potion_text = font.render("HP", True, WHITE)
                surface.blit(potion_text, (center_x - 10, center_y - 8))
                potion_text = font.render("VP", True, WHITE)
                surface.blit(potion_text, (center_x - 10, center_y + 8))
            elif room.hasHealthPot:
                potion_text = font.render("HP", True, WHITE)
                potion_rect = potion_text.get_rect(center=(center_x, center_y))
                surface.blit(potion_text, potion_rect)
            elif room.hasVisionPot:
                potion_text = font.render("VP", True, WHITE)
                potion_rect = potion_text.get_rect(center=(center_x, center_y))
                surface.blit(potion_text, potion_rect)

        # Draw player marker on top of everything else
        if (x, y) == hero_pos:
            self.draw_player_marker(surface, room_rect)

    def _log_debug_info(self, hero_pos):
        """
        Generate detailed debug information about the current room.

        Provides comprehensive logging that:
        - Prints player location
        - Details room contents
        - Supports development and testing

        Logging Details:
        - Current player coordinates
        - Presence of pillars
        - Health and vision potion locations
        - Pit traps
        - Monster presence

        Args:
            hero_pos: Current player location coordinates
        """
        print(f"\nPlayer at {hero_pos}")
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