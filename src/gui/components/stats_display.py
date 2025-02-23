import pygame
from ..constants import WHITE, RED, DARK_GRAY

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

    def update(self):
        """Update flashing effect for low health warning."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_flash >= self.flash_interval:
            self.warning_flash = not self.warning_flash
            self.last_flash = current_time