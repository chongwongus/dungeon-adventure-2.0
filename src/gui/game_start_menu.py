import pygame
from enum import Enum

class MenuState(Enum):
    """
    Defines the possible states of the game start menu.

    Provides a structured approach to managing menu navigation
    and user interaction flow. Each state represents a specific
    phase of the game configuration process.

    Menu Progression:
    1. MAIN_MENU: Initial entry point
    2. HERO_SELECT: Character selection phase
    3. NAME_INPUT: Player name entry
    4. DIFFICULTY_SELECT: Game challenge level choice
    5. PLAYING: Transition to game start
    """
    MAIN_MENU = 0
    HERO_SELECT = 1
    NAME_INPUT = 2
    DIFFICULTY_SELECT = 3
    PLAYING = 4

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

    def __init__(self, screen):
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
        self.start_rect = None
        self.can_start = False
        self.can_load = False

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
        7. Render load button
        8. Manage visual state and interactions
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

        # Draw settings section (right side)
        settings_section = pygame.Rect(
            self.screen.get_width() // 2 + 50,
            100,
            self.screen.get_width() // 2 - 100,
            400
        )
        pygame.draw.rect(self.screen, (32, 32, 32), settings_section)

        # Name input
        name_label = self.font_medium.render("Your Name:", True, (255, 255, 255))
        self.screen.blit(name_label, (settings_section.x + 20, settings_section.y + 20))

        self.name_input_rect = pygame.Rect(
            settings_section.x + 20,
            settings_section.y + 70,
            settings_section.width - 40,
            40
        )

        color = (100, 100, 255) if self.name_input_active else (64, 64, 64)
        pygame.draw.rect(self.screen, color, self.name_input_rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.name_input_rect, 2)

        name_text = self.font_medium.render(self.player_name + ("_" if self.name_input_active else ""), True,
                                            (255, 255, 255))
        self.screen.blit(name_text, (self.name_input_rect.x + 10, self.name_input_rect.y + 5))

        # Difficulty selection
        diff_label = self.font_medium.render("Difficulty:", True, (255, 255, 255))
        self.screen.blit(diff_label, (settings_section.x + 20, settings_section.y + 150))

        self.easy_rect = pygame.Rect(
            settings_section.x + 20,
            settings_section.y + 200,
            (settings_section.width - 60) // 2,
            60
        )

        self.hard_rect = pygame.Rect(
            settings_section.x + 40 + (settings_section.width - 60) // 2,
            settings_section.y + 200,
            (settings_section.width - 60) // 2,
            60
        )

        # Highlight selected difficulty
        easy_color = (64, 128, 64) if self.selected_difficulty == "easy" else (64, 64, 64)
        hard_color = (128, 64, 64) if self.selected_difficulty == "hard" else (64, 64, 64)

        pygame.draw.rect(self.screen, easy_color, self.easy_rect)
        pygame.draw.rect(self.screen, hard_color, self.hard_rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.easy_rect, 2)
        pygame.draw.rect(self.screen, (128, 128, 128), self.hard_rect, 2)

        easy_text = self.font_medium.render("Easy", True, (255, 255, 255))
        hard_text = self.font_medium.render("Hard", True, (255, 255, 255))

        self.screen.blit(easy_text, (
        self.easy_rect.centerx - easy_text.get_width() // 2, self.easy_rect.centery - easy_text.get_height() // 2))
        self.screen.blit(hard_text, (
        self.hard_rect.centerx - hard_text.get_width() // 2, self.hard_rect.centery - hard_text.get_height() // 2))

        # Draw start button
        self.start_rect = pygame.Rect(
            self.screen.get_width() // 2 + 100,
            550,
            200,
            60
        )

        start_color = (0, 128, 0) if self.can_start else (64, 64, 64)
        pygame.draw.rect(self.screen, start_color, self.start_rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.start_rect, 2)

        start_text = self.font_medium.render("Start Game", True, (255, 255, 255))
        self.screen.blit(start_text, (
        self.start_rect.centerx - start_text.get_width() // 2, self.start_rect.centery - start_text.get_height() // 2))

        pygame.display.flip()

        # Draw load button
        self.load_rect = pygame.Rect(
            self.screen.get_width() // 2 - 300,
            550,
            200,
            60
        )

        load_color = (0, 128, 0) if self.can_load else (64, 64, 64)
        pygame.draw.rect(self.screen, load_color, self.load_rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.load_rect, 2)

        load_text = self.font_medium.render("Load Game", True, (255, 255, 255))
        self.screen.blit(load_text, (
            self.load_rect.centerx - load_text.get_width() // 2,
            self.load_rect.centery - load_text.get_height() // 2))

        pygame.display.flip()

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