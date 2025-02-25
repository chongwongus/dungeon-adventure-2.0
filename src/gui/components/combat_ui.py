import pygame
from ..constants import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK


class CombatUI:
    """
    Handles the combat user interface, including character portraits, health bars,
    action buttons, and the combat log.
    """

    def __init__(self):
        """Initialize the Combat UI elements and resources."""
        # Initialize fonts
        try:
            self.font = pygame.font.Font("src/assets/fonts/ActionMan.ttf", 24)
            self.title_font = pygame.font.Font("src/assets/fonts/ActionMan.ttf", 32)
        except FileNotFoundError:
            print("Could not load Action Man font, falling back to system default")
            self.font = pygame.font.SysFont("arial", 24)
            self.title_font = pygame.font.SysFont("arial", 32, bold=True)

        # Simple placeholder portraits (64x64 colored rectangles for now)
        self.portraits = {
            'Warrior': self._create_portrait((0, 0, 255)),  # Blue
            'Priestess': self._create_portrait((255, 255, 0)),  # Yellow
            'Thief': self._create_portrait((0, 255, 0)),  # Green
            'Ogre': self._create_portrait((255, 0, 0)),  # Red
            'Skeleton': self._create_portrait((128, 128, 128)),  # Gray
            'Gremlin': self._create_portrait((255, 0, 255))  # Purple
        }

        self.action_buttons = {
            'attack': pygame.Rect(0, 0, 200, 50),
            'special': pygame.Rect(0, 0, 200, 50),
            'potion': pygame.Rect(0, 0, 200, 50),
            'run': pygame.Rect(0, 0, 200, 50)
        }

        # Combat log
        self.combat_messages = []
        self.max_combat_messages = 5

    def add_combat_message(self, message: str):
        """
        Add a message to the combat log.

        Args:
            message: The combat message to display
        """
        self.combat_messages.append(message)
        # Keep only the most recent messages
        if len(self.combat_messages) > self.max_combat_messages:
            self.combat_messages.pop(0)

    def _create_portrait(self, color):
        """
        Create a simple colored square as a placeholder portrait.

        Args:
            color: RGB tuple for the portrait color

        Returns:
            A pygame Surface with the portrait
        """
        surface = pygame.Surface((64, 64))
        surface.fill(color)
        # Add a border
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 2)
        return surface

    def _get_character_portrait(self, character):
        """
        Get the appropriate portrait based on character class.

        Args:
            character: The character (hero or monster) to get a portrait for

        Returns:
            A pygame Surface with the character's portrait
        """
        # For heroes, use their class name
        if hasattr(character, 'class_name'):
            return self.portraits.get(character.class_name)
        # For monsters, use their name
        return self.portraits.get(character.__class__.__name__)

    def draw_combat_screen(self, screen, hero, monster, selected_action=None):
        """
        Draw the complete combat interface.

        Args:
            screen: The pygame screen to draw on
            hero: The player character
            monster: The monster being fought
            selected_action: Currently selected combat action, if any
        """
        # Draw combat background
        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        # Draw portraits
        hero_portrait = self._get_character_portrait(hero)
        monster_portrait = self._get_character_portrait(monster)

        if hero_portrait:
            screen.blit(hero_portrait, (50, 200))
        if monster_portrait:
            screen.blit(monster_portrait, (686, 200))

        # Draw health bars
        self._draw_health_bar(screen, (50, 280), hero.hp, hero._max_hp)
        self._draw_health_bar(screen, (686, 280), monster.hp, monster._max_hp)

        # Draw names and stats
        hero_name = self.font.render(f"{hero.name} ({hero.class_name})", True, WHITE)
        hero_hp = self.font.render(f"HP: {hero.hp}/{hero._max_hp}", True, WHITE)
        screen.blit(hero_name, (50, 170))
        screen.blit(hero_hp, (50, 300))

        monster_name = self.font.render(f"{monster.name}", True, WHITE)
        monster_hp = self.font.render(f"HP: {monster.hp}/{monster._max_hp}", True, WHITE)
        screen.blit(monster_name, (686, 170))
        screen.blit(monster_hp, (686, 300))

        # Draw combat log
        log_rect = pygame.Rect(WINDOW_WIDTH // 4, 50, WINDOW_WIDTH // 2, 100)
        pygame.draw.rect(screen, (40, 40, 40), log_rect)
        pygame.draw.rect(screen, WHITE, log_rect, 2)

        # Show last few combat messages
        y_offset = log_rect.top + 10
        for msg in self.combat_messages[-4:]:
            txt = self.font.render(msg, True, WHITE)
            screen.blit(txt, (log_rect.left + 10, y_offset))
            y_offset += 22

        # Draw action buttons
        button_x = WINDOW_WIDTH // 2 - 100  # Center buttons
        button_start_y = 400
        button_spacing = 60

        for i, (action, rect) in enumerate(self.action_buttons.items()):
            rect.x = button_x
            rect.y = button_start_y + (i * button_spacing)

            # Highlight selected action
            color = (100, 100, 255) if action == selected_action else (64, 64, 64)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)

            # Button text
            text = self.font.render(action.title(), True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

            # Add potions count if it's the potion button
            if action == 'potion':
                potion_count = self.font.render(f"x{hero.healing_potions}", True, WHITE)
                screen.blit(potion_count, (rect.right + 10, rect.centery - 10))

    def _draw_health_bar(self, screen, pos, current, maximum):
        """
        Draw a health bar with border.

        Args:
            screen: The pygame screen to draw on
            pos: (x, y) position for the health bar
            current: Current health points
            maximum: Maximum health points
        """
        width = 200
        height = 20

        # Background (empty bar)
        pygame.draw.rect(screen, (64, 0, 0), (*pos, width, height))

        # Health fill
        health_width = int((current / maximum) * width)
        pygame.draw.rect(screen, (255, 0, 0), (*pos, health_width, height))

        # Border
        pygame.draw.rect(screen, WHITE, (*pos, width, height), 2)

    def handle_click(self, pos):
        """
        Handle mouse clicks on the combat UI.

        Args:
            pos: (x, y) mouse position

        Returns:
            The action selected, or None if no action was clicked
        """
        for action, rect in self.action_buttons.items():
            if rect.collidepoint(pos):
                return action
        return None