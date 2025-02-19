import pygame
from ..constants import WHITE, WINDOW_WIDTH

class CombatUI:
    def __init__(self):
        # Simple placeholder portraits (64x64 colored rectangles for now)
        self.portraits = {
            'Warrior': self._create_portrait((0, 0, 255)),      # Blue
            'Priestess': self._create_portrait((255, 255, 0)),  # Yellow
            'Thief': self._create_portrait((0, 255, 0)),        # Green
            'Ogre': self._create_portrait((255, 0, 0)),         # Red
            'Skeleton': self._create_portrait((128, 128, 128)), # Gray
            'Gremlin': self._create_portrait((255, 0, 255))     # Purple
        }

        self.action_buttons = {
            'attack': pygame.Rect(0, 0, 200, 50),
            'special': pygame.Rect(0, 0, 200, 50),
            'potion': pygame.Rect(0, 0, 200, 50),
            'run': pygame.Rect(0, 0, 200, 50)
        }

    def _create_portrait(self, color):
        """Create a simple colored square as a placeholder portrait"""
        surface = pygame.Surface((64, 64))
        surface.fill(color)
        # Add a border
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 2)
        return surface

    def _get_character_portrait(self, character):
        """Get the appropriate portrait based on character class"""
        # For heroes, use their class name
        if hasattr(character, 'class_name'):
            return self.portraits.get(character.class_name)
        # For monsters, use their name
        return self.portraits.get(character.__class__.__name__)

    def draw_combat_screen(self, screen, hero, monster, selected_action=None):
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
        font = pygame.font.Font(None, 32)
        # Hero info
        hero_name = font.render(f"{hero.name} ({hero.class_name})", True, (255, 255, 255))
        hero_hp = font.render(f"HP: {hero.hp}/{hero._max_hp}", True, (255, 255, 255))
        screen.blit(hero_name, (50, 170))
        screen.blit(hero_hp, (50, 300))

        # Monster info
        monster_name = font.render(f"{monster.name}", True, (255, 255, 255))
        monster_hp = font.render(f"HP: {monster.hp}/{monster._max_hp}", True, (255, 255, 255))
        screen.blit(monster_name, (686, 170))
        screen.blit(monster_hp, (686, 300))

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
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)

            # Button text
            text = font.render(action.title(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

            # Add potions count if it's the potion button
            if action == 'potion':
                potion_count = font.render(f"x{hero.healing_potions}", True, (255, 255, 255))
                screen.blit(potion_count, (rect.right + 10, rect.centery - 10))

    def _draw_health_bar(self, screen, pos, current, maximum):
        """Draw a health bar with border"""
        width = 200
        height = 20

        # Background (empty bar)
        pygame.draw.rect(screen, (64, 0, 0), (*pos, width, height))

        # Health fill
        health_width = int((current / maximum) * width)
        pygame.draw.rect(screen, (255, 0, 0), (*pos, health_width, height))

        # Border
        pygame.draw.rect(screen, (255, 255, 255), (*pos, width, height), 2)

    def handle_click(self, pos):
        """Handle mouse clicks on the combat UI"""
        for action, rect in self.action_buttons.items():
            if rect.collidepoint(pos):
                return action
        return None