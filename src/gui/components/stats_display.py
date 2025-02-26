import pygame
from ..constants import WHITE, RED, DARK_GRAY

class StatsDisplay:
    """
    Manages the comprehensive display of player statistics and status.

    Serves as a critical user interface component that provides
    real-time information about the player's current condition,
    inventory, and progression.

    Core Display Responsibilities:
    - Render health information
    - Display inventory contents
    - Provide visual health warnings
    - Support dynamic stat updates

    Design Components:
    1. Health Status Visualization
       - Track current and maximum health
       - Implement low-health warning system
       - Use color coding for health indication

    2. Inventory Tracking
       - Show current potion counts
       - Display collected pillars
       - Provide immediate resource information

    Warning Mechanism:
    The class implements a sophisticated health warning system
    that uses visual flashing to draw attention to critically
    low health levels, ensuring players are immediately aware
    of their character's vulnerable state.
    """

    def __init__(self):
        """
        Initialize the player statistics display system.

        Sets up the foundational components for stat visualization:
        - Prepare font for rendering
        - Configure health warning mechanism
        - Set up flashing interval for low health indicator

        Warning System Design:
        - Use a toggle-based flashing mechanism
        - Implement time-based flash interval
        - Provide subtle but noticeable health alerts

        Health Warning Characteristics:
        - Activates when health drops below 30%
        - Uses alternating visibility
        - Provides immediate visual feedback
        """
        self.font = pygame.font.Font(None, 28)
        self.warning_flash = False
        self.last_flash = 0
        self.flash_interval = 500  # milliseconds

    def draw(self, surface: pygame.Surface, rect: pygame.Rect, hero):
        """
        Render the complete player statistics display.

        Comprehensive method that visualizes:
        1. Current health status
        2. Healing potion inventory
        3. Vision potion inventory
        4. Collected pillars

        Rendering Strategy:
        - Draw dark gray background
        - Calculate health percentage
        - Implement low-health warning system
        - Render each stat category
        - Use color coding for emphasis

        Health Warning Mechanism:
        - Monitor health percentage
        - Implement flashing for critical health levels
        - Provide immediate visual alert

        Args:
            surface: Pygame surface for rendering
            rect: Rectangular area for stats display
            hero: Player character with current stats
        """
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
        """
        Update the dynamic elements of the stats display.

        Manages the health warning flash effect by:
        - Tracking time since last flash
        - Toggling warning visibility
        - Maintaining consistent warning interval

        Warning Update Process:
        1. Check elapsed time
        2. Toggle warning state if interval exceeded
        3. Update last flash timestamp

        Design Considerations:
        - Efficient time-based update mechanism
        - Minimal performance overhead
        - Consistent visual warning behavior
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_flash >= self.flash_interval:
            self.warning_flash = not self.warning_flash
            self.last_flash = current_time