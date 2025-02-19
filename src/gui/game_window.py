import pygame
from typing import Optional
import random

from .constants import *
from .components import EventLog, StatsDisplay, MiniMap, CombatUI
from src.combat.combat_system import CombatSystem


class GameWindow:
    """Main game window handler"""

    def __init__(self, dungeon, pillar_locations, hero):
        # Initialize pygame window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dungeon Adventure")

        # Store references
        self.dungeon = dungeon
        self.hero = hero

        # Initialize UI components
        self.event_log = EventLog()
        self.stats_display = StatsDisplay()
        self.minimap = MiniMap(dungeon, pillar_locations)
        self.combat_ui = CombatUI()

        # Game state
        self.in_combat = False
        self.combat_system = None
        self.selected_action = None
        self.victory = False
        self.death_screen_shown = False
        self.final_death_screen = None

        # Define component rectangles
        self._init_layout()

    def _init_layout(self):
        """Initialize UI layout rectangles"""
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

    def update(self, hero):
        """Update game state for each frame."""
        # Update combat state if in combat
        if self.in_combat and self.combat_system:
            # Update any combat animations or effects
            pass

        # Update stats display flashing effect
        self.stats_display.update()

        # Check for game over condition
        if not hero.is_alive and not self.death_screen_shown:
            self.draw_game_over()

        # Check for victory condition
        if self.check_victory_condition(hero):
            self.victory = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame events. Returns False if game should quit."""
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            return self._handle_key_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and self.in_combat:
            return self._handle_combat_click(event.pos)

        return True

    def _handle_key_event(self, event: pygame.event.Event) -> bool:
        """Handle keyboard input"""
        if self.in_combat:
            # Combat controls
            if event.key in [pygame.K_1, pygame.K_KP1]:
                return self.handle_combat_action("attack")
            elif event.key in [pygame.K_2, pygame.K_KP2]:
                return self.handle_combat_action("special")
            elif event.key in [pygame.K_3, pygame.K_KP3]:
                return self.handle_combat_action("potion")
            elif event.key in [pygame.K_4, pygame.K_KP4]:
                return self.handle_combat_action("run")
        else:
            # Log scrolling
            if event.key == pygame.K_PAGEUP:
                self.event_log.scroll_position = max(0, self.event_log.scroll_position - 1)
            elif event.key == pygame.K_PAGEDOWN:
                self.event_log.scroll_position = min(
                    len(self.event_log.messages) - 10,
                    self.event_log.scroll_position + 1
                )
        return True

    def _handle_combat_click(self, pos) -> bool:
        """Handle mouse clicks during combat"""
        action = self.combat_ui.handle_click(pos)
        if action:
            self.selected_action = action
            return self.handle_combat_action(action)
        return True

    def start_combat(self, hero, monster):
        """Initialize combat with a monster"""
        self.in_combat = True
        self.combat_system = CombatSystem(hero, monster)
        self.event_log.add_message(f"Combat started with {monster.name}!", True)

    def end_combat(self, victor):
        """End combat and handle results"""
        self.in_combat = False
        self.combat_system = None
        self.selected_action = None
        self.event_log.add_message(f"Combat ended! {victor.name} is victorious!")

    def handle_combat_action(self, action: str) -> bool:
        """Handle combat menu selection. Returns True if combat should continue."""
        if not self.combat_system:
            return False

        result = self._execute_combat_action(action)
        if result:
            self._process_combat_result(result)

        return self.in_combat

    def _execute_combat_action(self, action: str) -> Optional[object]:
        """Execute the selected combat action"""
        if action == "attack":
            return self.combat_system.execute_round(use_special=False)
        elif action == "special":
            return self.combat_system.execute_round(use_special=True)
        elif action == "potion":
            return self._handle_potion_use()
        elif action == "run":
            return self._handle_escape_attempt()
        return None

    def _handle_potion_use(self) -> Optional[object]:
        """Handle using a healing potion"""
        if self.hero.healing_potions > 0:
            heal_amount = self.hero.use_healing_potion()
            if heal_amount:
                self.event_log.add_message(f"Used a healing potion and recovered {heal_amount} HP!")
                return self.combat_system.execute_round(monster_only=True)
        else:
            self.event_log.add_message("No healing potions remaining!", True)
        return None

    def _handle_escape_attempt(self) -> Optional[object]:
        """Handle attempt to run from combat"""
        if random.random() < 0.4:  # 40% escape chance
            self.event_log.add_message("Successfully escaped from combat!")
            self.in_combat = False
            return None
        else:
            self.event_log.add_message("Failed to escape!", True)
            return self.combat_system.execute_round(monster_only=True)

    def _process_combat_result(self, result):
        """Process the results of a combat round"""
        for action in result.actions:
            self.event_log.add_message(action.message)

        if self.combat_system.is_combat_over():
            victor = self.combat_system.get_victor()

            if not self.hero.is_alive:
                self._handle_hero_death(victor)
            else:
                self._handle_monster_death(victor)

    def _handle_hero_death(self, victor):
        """Handle hero death in combat"""
        self.event_log.add_message(f"Game Over! {self.hero.name} has fallen!", True)
        self.end_combat(victor)

    def _handle_monster_death(self, victor):
        """Handle monster death in combat"""
        self.event_log.add_message(f"Victory! {victor.name} has defeated the {self.combat_system.monster.name}!")
        self.end_combat(victor)

        # Process drops
        current_room = self.dungeon.get_room(*self.hero.location)
        drops = current_room.clear_monster()
        for item in drops:
            if item == "health_potion":
                self.hero.collect_potion("healing")
                self.event_log.add_message("Found a health potion!")
            elif item == "vision_potion":
                self.hero.collect_potion("vision")
                self.event_log.add_message("Found a vision potion!")

    def check_victory_condition(self, hero) -> bool:
        """Check if the player has won"""
        if hero.location == self.dungeon.exit and hero.has_all_pillars():
            self.victory = True
            self.event_log.add_message(
                "Congratulations! You've collected all pillars and reached the exit!",
                True
            )
            return True
        return False

    def draw(self, hero, debug_log_minimap=False):
        """Draw the game window and all components."""
        self.screen.fill(BLACK)

        if self.in_combat and self.combat_system:
            self._draw_combat_screen()
        else:
            self._draw_normal_screen(hero, debug_log_minimap)

        if self.victory:
            self._draw_victory_screen()

        pygame.display.flip()

    def _draw_combat_screen(self):
        """Draw the combat interface"""
        self.combat_ui.draw_combat_screen(
            self.screen,
            self.hero,
            self.combat_system.monster,
            self.selected_action
        )

    def _draw_normal_screen(self, hero, debug_log_minimap):
        """Draw the normal game interface"""
        pygame.draw.rect(self.screen, DARK_GRAY, self.main_view_rect)
        self.minimap.draw(self.screen, self.minimap_rect, hero.location, debug_log_minimap)
        self.event_log.draw(self.screen, self.log_rect)
        self.stats_display.draw(self.screen, self.stats_rect, hero)

    def _draw_victory_screen(self):
        """Draw the victory overlay"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(192)
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 64)
        text = font.render("Victory!", True, (255, 215, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def draw_game_over(self):
        """Draw Dark Souls style death screen"""
        if not self.death_screen_shown:
            self._create_death_screen()
        else:
            self.screen.blit(self.final_death_screen, (0, 0))
            pygame.display.flip()

    def _create_death_screen(self):
        """Create the death screen with fade effect"""
        # Initial fade to black
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))

        for alpha in range(0, 255, 5):
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            pygame.time.delay(20)

        # Create and fade in text
        font = pygame.font.Font(None, 120)
        text = font.render("YOU DIED", True, (139, 0, 0))
        text_bright = font.render("YOU DIED", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to Restart or ESC to Quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3))

        for alpha in range(0, 255, 5):
            self.screen.fill((0, 0, 0))

            text_bright.set_alpha(alpha // 2)
            self.screen.blit(text_bright, text_rect)

            text.set_alpha(alpha)
            self.screen.blit(text, text_rect)

            if alpha > 128:
                restart_text.set_alpha(alpha)
                self.screen.blit(restart_text, restart_rect)

            pygame.display.flip()
            pygame.time.delay(20)

        self.death_screen_shown = True
        self.final_death_screen = self.screen.copy()

