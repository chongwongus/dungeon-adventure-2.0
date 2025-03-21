import pygame
from src.gui.start_menu.game_start_menu_helper import draw_menu_buttons, draw_difficulty_selector

class GameMenu:
    """
    Manages the comprehensive game initialization interface.

    This class creates a sophisticated, interactive menu system
    that guides players through character and game configuration
    with an engaging, informative approach.

    Core Responsibilities:
    - Render character selection interface
    - Manage player input
    - Validate game configuration
    - Provide detailed character information

    Design Components:
    1. Font Management
       - Multiple font sizes for hierarchical information display
       - Supports different text purposes (titles, descriptions)

    2. Hero Selection System
       - Detailed character information
       - Hover-based information reveal
       - Visual selection feedback

    3. Configuration Validation
       - Tracks selected hero, name, and difficulty
       - Enables start button only when all requirements met
    """

    def __init__(self, screen, save_data):
        """
        Manages the comprehensive game initialization interface.

        This class creates a sophisticated, interactive menu system
        that guides players through character and game configuration
        with an engaging, informative approach.

        Core Responsibilities:
        - Render character selection interface
        - Manage player input
        - Validate game configuration
        - Provide detailed character information

        Design Components:
        1. Font Management
           - Multiple font sizes for hierarchical information display
           - Supports different text purposes (titles, descriptions)

        2. Hero Selection System
           - Detailed character information
           - Hover-based information reveal
           - Visual selection feedback

        3. Configuration Validation
           - Tracks selected hero, name, and difficulty
           - Enables start button only when all requirements met
        """
        self.screen = screen
        self.save_data = save_data
        self.font_large = pygame.font.Font(None, 64)  # Title
        self.font_medium = pygame.font.Font(None, 36)  # Hero names, buttons
        self.font_small = pygame.font.Font(None, 24)   # Descriptions

        # Menu state
        self.selected_hero = None
        self.hero_options = [
            {
                "class": "Warrior",
                "description": "Tank",
                "details": [
                    "Health: 125 HP",
                    "Attack Speed: Normal",
                    "Special: Crushing Blow",
                    "Block Chance: 20%",
                    "Style: High damage, high health"
                ],
                "rect": None,
                "hovered": False
            },
            {
                "class": "Priestess",
                "description": "Healer",
                "details": [
                    "Health: 75 HP",
                    "Attack Speed: Fast",
                    "Special: Healing",
                    "Block Chance: 30%",
                    "Style: Support, sustain damage"
                ],
                "rect": None,
                "hovered": False
            },
            {
                "class": "Thief",
                "description": "Rogue",
                "details": [
                    "Health: 75 HP",
                    "Attack Speed: Very Fast",
                    "Special: Surprise Attack",
                    "Block Chance: 40%",
                    "Style: Quick strikes, high evasion"
                ],
                "rect": None,
                "hovered": False
            }
        ]

        # Input fields
        self.player_name = ""
        self.name_input_rect = None
        self.name_input_active = False

        # Difficulty selection
        self.selected_difficulty = None
        self.easy_rect = None
        self.hard_rect = None

        # Start button
        self.load_rect = None
        self.start_rect = None
        self.can_start = False

    def handle_event(self, event):
        """
        Process user interactions with the start menu.

        Comprehensive event handling that supports:
        - Mouse movement tracking
        - Hero selection
        - Name input
        - Difficulty selection
        - Start game validation

        Event Handling Workflow:
        1. Track mouse position for hover effects
        2. Process mouse clicks for selections
        3. Manage text input for player name
        4. Update start button availability
        5. Return game settings when ready to start

        Returns configured game settings or None if configuration incomplete
        """
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Update hover states
            for hero in self.hero_options:
                hero["hovered"] = hero["rect"] and hero["rect"].collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check hero selection
            for hero in self.hero_options:
                if hero["rect"].collidepoint(mouse_pos):
                    self.selected_hero = hero["class"]
                    self.update_start_button()
                    return

            # Check name input
            if self.name_input_rect.collidepoint(mouse_pos):
                self.name_input_active = True
            else:
                self.name_input_active = False

            # Check difficulty selection
            if self.easy_rect.collidepoint(mouse_pos):
                self.selected_difficulty = "easy"
                self.update_start_button()
            elif self.hard_rect.collidepoint(mouse_pos):
                self.selected_difficulty = "hard"
                self.update_start_button()

            # Check start button
            if self.can_start and self.start_rect.collidepoint(mouse_pos):
                return self.get_game_settings()

            if self.save_data and self.load_rect.collidepoint(mouse_pos):
                return self.load_game_settings()

        elif event.type == pygame.KEYDOWN and self.name_input_active:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif len(self.player_name) < 15 and event.unicode.isalnum():
                self.player_name += event.unicode
            self.update_start_button()

        return None

    def update_start_button(self):
        """
        Dynamically manage start button activation.

        Validates game configuration by checking:
        - Hero class selection
        - Player name entry
        - Difficulty level choice

        Ensures comprehensive configuration before allowing game start
        """
        self.can_start = (self.selected_hero and
                          self.player_name.strip() and
                          self.selected_difficulty)

    def draw(self):
        """
        Render the complete game start menu interface.

        Creates a visually rich, informative menu that:
        - Displays game title
        - Renders hero selection section
        - Manages name input
        - Handles difficulty selection
        - Provides start game button

        Rendering Strategy:
        1. Clear screen
        2. Draw title
        3. Create hero selection area
        4. Implement name input field
        5. Add difficulty selection
        6. Render start button
        7. Manage visual state and interactions
        """
        self.screen.fill((0, 0, 0))  # Clear screen

        # Draw title
        title = self.font_large.render("Dungeon Adventure", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

        # Draw hero selection (left side)
        hero_section = pygame.Rect(50, 100, self.screen.get_width() // 2 - 100, 400)
        pygame.draw.rect(self.screen, (32, 32, 32), hero_section)

        hero_title = self.font_medium.render("Choose Your Hero", True, (255, 255, 255))
        self.screen.blit(hero_title, (hero_section.x + 20, hero_section.y + 20))

        for i, hero in enumerate(self.hero_options):
            hero_rect = pygame.Rect(
                hero_section.x + 20,
                hero_section.y + 80 + i * 100,
                hero_section.width - 40,
                80
            )
            hero["rect"] = hero_rect

            # Enhanced highlighting for selected hero
            if hero["class"] == self.selected_hero:
                # Draw glowing border with more subtle colors
                glow_rect = hero_rect.inflate(6, 6)
                pygame.draw.rect(self.screen, (120, 120, 40), glow_rect)  # Darker gold glow
                pygame.draw.rect(self.screen, (100, 100, 30), hero_rect)  # Darker background
            else:
                pygame.draw.rect(self.screen, (64, 64, 64), hero_rect)  # Normal background

            # Add border
            pygame.draw.rect(self.screen, (128, 128, 128), hero_rect, 2)

            # If this is the selected hero, add some visual flair
            if hero["class"] == self.selected_hero:
                # Add a small indicator
                pygame.draw.circle(self.screen, (255, 215, 0),
                                   (hero_rect.x + 10, hero_rect.centery), 5)

                # Make text brighter
                hero_text = self.font_medium.render(hero["class"], True, (255, 255, 0))
                desc_text = self.font_small.render(hero["description"], True, (255, 255, 200))
            else:
                hero_text = self.font_medium.render(hero["class"], True, (255, 255, 255))
                desc_text = self.font_small.render(hero["description"], True, (200, 200, 200))

            self.screen.blit(hero_text, (hero_rect.x + 30, hero_rect.y + 10))
            self.screen.blit(desc_text, (hero_rect.x + 30, hero_rect.y + 45))

            # Draw details box when hovered - unified position for all classes
            if hero["hovered"]:
                base_y = hero_section.y + 20  # Fixed position at top of hero section
                detail_box = pygame.Rect(
                    hero_rect.x,
                    base_y - 120,  # Position above the "Choose Your Hero" text
                    300,  # Fixed width for details
                    200   # Fixed height for details
                )
                pygame.draw.rect(self.screen, (32, 32, 32), detail_box)
                pygame.draw.rect(self.screen, (128, 128, 128), detail_box, 2)

                # Draw details
                for i, detail in enumerate(hero["details"]):
                    detail_text = self.font_small.render(detail, True, (255, 255, 255))
                    self.screen.blit(detail_text, (detail_box.x + 10, detail_box.y + 10 + i * 30))

        draw_difficulty_selector(self)

        # Draw start button
        draw_menu_buttons(self)
        pygame.display.flip()

    def load_game_settings(self):
        print("loading...")
        return {
            "hero_class": "load",
            "player_name": "load",
            "difficulty": "load"
        }
    def get_game_settings(self):
        """
        Compile and return the final game configuration.

        Collects and packages:
        - Selected hero class
        - Player name
        - Chosen difficulty level

        Returns a comprehensive dictionary of game settings
        when all configuration requirements are met.
        """
        """Return the selected game settings."""
        if self.can_start:
            return {
                "hero_class": self.selected_hero,
                "player_name": self.player_name,
                "difficulty": self.selected_difficulty
            }
        return None