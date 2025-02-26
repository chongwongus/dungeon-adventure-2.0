import pygame
from typing import Optional, List
import random

from .constants import *
from .components import EventLog, StatsDisplay, MiniMap, CombatUI
from .components.first_person_view import FirstPersonView
from src.combat.combat_system import CombatSystem


class GameWindow:
    """
    Central management system for the game's graphical interface.

    Serves as the primary controller that coordinates all
    visual and interactive elements of the Dungeon Adventure game.

    Design Architecture:
    1. UI Component Management
       - Event log tracking
       - Stats display
       - Minimap rendering
       - Combat interface
       - First-person view rendering

    2. Game State Tracking
       - Combat status
       - Player location
       - Exploration progress
       - Victory/defeat conditions

    3. Input Handling System
       - Keyboard movement
       - Combat action selection
       - Item usage
       - Menu navigation

    Interaction Workflow:
    The GameWindow provides a comprehensive bridge between
    game logic and user interaction, ensuring a smooth and
    intuitive player experience across different game states.
    """

    def __init__(self, dungeon, pillar_locations, hero):
        """
        Initialize the game window's comprehensive UI system.

        Sets up all necessary components for a rich,
        interactive game experience:
        - Create pygame display surface
        - Initialize UI components
        - Track game and player state
        - Prepare for different game modes

        Initialization Strategy:
        1. Set up display window
        2. Store game references (dungeon, hero)
        3. Initialize UI components
        4. Prepare game state trackers
        5. Configure initial view settings
        """
        # Initialize pygame window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dungeon Adventure")

        # Store references
        self.dungeon = dungeon
        self.hero = hero

        # Track hero's facing direction (start facing east)
        self.hero_direction = 'E'

        # Initialize UI components
        self.event_log = EventLog()
        self.stats_display = StatsDisplay()
        self.minimap = MiniMap(dungeon, pillar_locations)
        self.combat_ui = CombatUI()
        self.first_person_view = FirstPersonView(pygame.Rect(0, 0, MAIN_VIEW_WIDTH, WINDOW_HEIGHT))

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
        """Initialize UI layout rectangles for different components."""
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
        """
        Update game state for each frame.

        Manages dynamic elements of the game interface:
        - Update combat state
        - Refresh stats display
        - Check game-ending conditions
        - Manage visual state changes

        Comprehensive State Management:
        1. Process ongoing combat mechanics
        2. Update visual indicators
        3. Check for victory or defeat
        4. Maintain smooth game progression
        """
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
        """
        Central event processing method for game interactions.

        Manages all user inputs across different game states:
        - Quit game detection
        - Keyboard input handling
        - Combat interactions
        - Movement controls

        Event Handling Strategy:
        1. Detect system-level events (quit)
        2. Process keyboard inputs
        3. Manage combat-specific interactions
        4. Support seamless mode transitions
        """
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
        """
        Process keyboard inputs for movement and interactions.

        Comprehensive input handling that supports:
        - Combat mode controls
        - Exploration movement
        - Item usage
        - Log scrolling

        Input Processing Workflow:
        1. Determine current game mode
        2. Map keyboard inputs to specific actions
        3. Validate and execute interactions
        4. Provide user feedback
        """
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
            # Simple directional movement (one room at a time)
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                # Check if there's a door to the north
                current_room = self.dungeon.get_room(*self.hero.location)
                if not current_room.doors.get('N', False):
                    self.event_log.add_message("No door in that direction", "movement", True)
                    return True

                # Try to move north
                self.hero_direction = 'N'
                result = self.dungeon.move_hero(self.hero, 'N')
                if isinstance(result, tuple) and len(result) == 3:
                    success, messages, combat = result
                    self._handle_movement_result(success, messages, combat, "North")

            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                # Check if there's a door to the south
                current_room = self.dungeon.get_room(*self.hero.location)
                if not current_room.doors.get('S', False):
                    self.event_log.add_message("No door in that direction", "movement", True)
                    return True

                # Try to move south
                self.hero_direction = 'S'
                result = self.dungeon.move_hero(self.hero, 'S')
                if isinstance(result, tuple) and len(result) == 3:
                    success, messages, combat = result
                    self._handle_movement_result(success, messages, combat, "South")

            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                # Check if there's a door to the west
                current_room = self.dungeon.get_room(*self.hero.location)
                if not current_room.doors.get('W', False):
                    self.event_log.add_message("No door in that direction", "movement", True)
                    return True

                # Try to move west
                self.hero_direction = 'W'
                result = self.dungeon.move_hero(self.hero, 'W')
                if isinstance(result, tuple) and len(result) == 3:
                    success, messages, combat = result
                    self._handle_movement_result(success, messages, combat, "West")

            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                # Check if there's a door to the east
                current_room = self.dungeon.get_room(*self.hero.location)
                if not current_room.doors.get('E', False):
                    self.event_log.add_message("No door in that direction", "movement", True)
                    return True

                # Try to move east
                self.hero_direction = 'E'
                result = self.dungeon.move_hero(self.hero, 'E')
                if isinstance(result, tuple) and len(result) == 3:
                    success, messages, combat = result
                    self._handle_movement_result(success, messages, combat, "East")

            # Handle potion usage outside of combat
            elif event.key == pygame.K_h:  # Use healing potion
                if self.hero.healing_potions > 0:
                    heal_amount = self.hero.use_healing_potion()
                    if heal_amount:
                        self.event_log.add_message(f"Used a healing potion and recovered {heal_amount} HP!", "item")
                else:
                    self.event_log.add_message("No healing potions remaining!", "item", True)

            elif event.key == pygame.K_v:  # Use vision potion
                if self.hero.vision_potions > 0:
                    self.hero.use_vision_potion()
                    self.event_log.add_message("Used a vision potion. Surrounding rooms revealed!", "item")
                    self.dungeon.reveal_adjacent_rooms(self.hero.location)
                else:
                    self.event_log.add_message("No vision potions remaining!", "item", True)

            # Log scrolling
            if event.key == pygame.K_PAGEUP:
                self.event_log.scroll_position = max(0, self.event_log.scroll_position - 1)
            elif event.key == pygame.K_PAGEDOWN:
                self.event_log.scroll_position = min(
                    len(self.event_log.messages) - 10,
                    self.event_log.scroll_position + 1
                )
        return True

    def _handle_movement_result(self, success: bool, messages: List[str], combat, direction: str):
        """
        Process the results of a movement attempt.

        Args:
            success: Whether the movement succeeded
            messages: Messages to display about the move
            combat: Combat system if a battle started
            direction: Direction that was moved
        """
        if success:
            self.event_log.add_message(f"Moved {direction}", "movement")
            new_room = self.dungeon.get_room(*self.hero.location)

            # Check for monster in the new room
            if new_room.monster and new_room.monster.is_alive:
                self.start_combat(self.hero, new_room.monster)
            # Display other room messages
            elif messages:
                for msg in messages:
                    self.event_log.add_message(msg)
        else:
            # Movement failed
            for msg in messages:
                self.event_log.add_message(msg, "movement", True)

    def _turn_left(self):
        """Turn the player 90 degrees to the left."""
        turn_map = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        self.hero_direction = turn_map[self.hero_direction]

    def _turn_right(self):
        """Turn the player 90 degrees to the right."""
        turn_map = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        self.hero_direction = turn_map[self.hero_direction]

    def _handle_combat_click(self, pos) -> bool:
        """
        Handle mouse clicks during combat.

        Args:
            pos: (x, y) mouse position

        Returns:
            True to continue, False to quit
        """
        action = self.combat_ui.handle_click(pos)
        if action:
            self.selected_action = action
            return self.handle_combat_action(action)
        return True

    def start_combat(self, hero, monster):
        """
        Initiate a combat encounter.

        Manages the transition into combat mode:
        - Set up combat system
        - Initialize combat UI
        - Log combat start
        - Prepare combat state

        Combat Initialization Process:
        1. Change game state to combat mode
        2. Create combat system instance
        3. Clear previous combat messages
        4. Provide user feedback
        """

        self.in_combat = True
        self.combat_system = CombatSystem(hero, monster)
        self.event_log.add_message(f"Combat started with {monster.name}!", "combat", True)

        # Clear previous combat messages
        self.combat_ui.combat_messages = []
        self.combat_ui.add_combat_message(f"Combat started with {monster.name}!")

    def end_combat(self, victor):
        """
        End combat and handle results.

        Args:
            victor: The winning combatant
        """
        self.in_combat = False
        self.combat_system = None
        self.selected_action = None
        self.event_log.add_message(f"Combat ended! {victor.name} is victorious!", "combat")

    def handle_combat_action(self, action: str) -> bool:
        """
        Handle combat menu selection. Returns True if combat should continue.

        Args:
            action: The selected combat action

        Returns:
            True if combat continues, False if it ends
        """
        if not self.combat_system:
            return False

        result = self._execute_combat_action(action)
        if result:
            self._process_combat_result(result)

        return self.in_combat

    def _execute_combat_action(self, action: str) -> Optional[object]:
        """
        Execute the selected combat action.

        Args:
            action: The combat action to execute

        Returns:
            Combat result or None
        """
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
        """
        Handle using a healing potion during combat.

        Returns:
            Combat result or None
        """
        if self.hero.healing_potions > 0:
            heal_amount = self.hero.use_healing_potion()
            if heal_amount:
                message = f"Used a healing potion and recovered {heal_amount} HP!"
                self.event_log.add_message(message, "item")
                self.combat_ui.add_combat_message(message)
                return self.combat_system.execute_round(monster_only=True)
        else:
            message = "No healing potions remaining!"
            self.event_log.add_message(message, "item", True)
            self.combat_ui.add_combat_message(message)
        return None

    def _handle_escape_attempt(self) -> Optional[object]:
        """
        Handle attempt to run from combat.

        Returns:
            Combat result or None
        """
        if random.random() < 0.4:  # 40% escape chance
            message = "Successfully escaped from combat!"
            self.event_log.add_message(message, "combat")
            self.combat_ui.add_combat_message(message)
            self.in_combat = False
            return None
        else:
            message = "Failed to escape!"
            self.event_log.add_message(message, "combat", True)
            self.combat_ui.add_combat_message(message)
            return self.combat_system.execute_round(monster_only=True)

    def _process_combat_result(self, result):
        """
        Process the results of a combat round.

        Args:
            result: The combat result to process
        """
        for action in result.actions:
            self.event_log.add_message(action.message, "combat")
            self.combat_ui.add_combat_message(action.message)

        if self.combat_system.is_combat_over():
            victor = self.combat_system.get_victor()

            if not self.hero.is_alive:
                self._handle_hero_death(victor)
            else:
                self._handle_monster_death(victor)

    def _handle_hero_death(self, victor):
        """
        Handle hero death in combat.

        Args:
            victor: The victorious monster
        """
        message = f"Game Over! {self.hero.name} has fallen!"
        self.event_log.add_message(message, "combat", True)
        self.combat_ui.add_combat_message(message)
        self.end_combat(victor)

    def _handle_monster_death(self, victor):
        """
        Handle monster death in combat.

        Args:
            victor: The victorious hero
        """
        message = f"Victory! {victor.name} has defeated the {self.combat_system.monster.name}!"
        self.event_log.add_message(message, "combat")
        self.combat_ui.add_combat_message(message)
        self.end_combat(victor)

        # Process drops
        current_room = self.dungeon.get_room(*self.hero.location)
        drops = current_room.clear_monster()
        for item in drops:
            if item == "health_potion":
                self.hero.collect_potion("healing")
                self.event_log.add_message("Found a health potion!", "item")
            elif item == "vision_potion":
                self.hero.collect_potion("vision")
                self.event_log.add_message("Found a vision potion!", "item")

    def check_victory_condition(self, hero) -> bool:
        """
        Determine if the player has met victory conditions.

        Checks comprehensive win state by verifying:
        - Player location (exit reached)
        - Pillar collection status

        Victory Validation Strategy:
        1. Check exit location
        2. Verify pillar collection
        3. Trigger victory sequence
        4. Log victory message
        """
        if hero.location == self.dungeon.exit and hero.has_all_pillars():
            self.victory = True
            self.event_log.add_message(
                "Congratulations! You've collected all pillars and reached the exit!",
                "system", True
            )
            return True
        return False

    def draw(self, hero, debug_log_minimap=False):
        """
        Render the complete game interface.

        Manages rendering across different game states:
        - Normal exploration view
        - Combat interface
        - Victory screen

        Rendering Workflow:
        1. Clear screen
        2. Determine current game state
        3. Render appropriate view
        4. Update display
        5. Optional debug logging
        """
        self.screen.fill(BLACK)

        if self.in_combat and self.combat_system:
            self._draw_combat_screen()
        else:
            self._draw_normal_screen(hero, debug_log_minimap)

        if self.victory:
            self._draw_victory_screen()

        pygame.display.flip()

    def _draw_normal_screen(self, hero, debug_log_minimap):
        """
        Draw the normal game interface when not in combat.

        Args:
            hero: The player character
            debug_log_minimap: Whether to log minimap debug info
        """
        # Draw first-person view in the main area
        self.first_person_view.draw(self.screen, self.dungeon, hero.location, self.hero_direction)

        # Draw side panel UI components
        self.minimap.draw(self.screen, self.minimap_rect, hero.location, debug_log_minimap)
        self.event_log.draw(self.screen, self.log_rect)
        self.stats_display.draw(self.screen, self.stats_rect, hero)

        # Draw directional indicators at the bottom of the screen
        self._draw_direction_indicator()

    def _draw_direction_indicator(self):
        """Draw a compass showing which direction the player is facing."""
        # Define position at the bottom of the main view
        x = self.main_view_rect.width // 2
        y = self.main_view_rect.height - 40
        radius = 30

        # Draw circle background
        pygame.draw.circle(self.screen, (40, 40, 40), (x, y), radius)
        pygame.draw.circle(self.screen, (200, 200, 200), (x, y), radius, 2)

        # Draw direction letters
        font = pygame.font.Font(None, 24)
        directions = {
            'N': (x, y - radius + 10),
            'E': (x + radius - 10, y),
            'S': (x, y + radius - 10),
            'W': (x - radius + 10, y)
        }

        for dir_letter, pos in directions.items():
            # Current direction is highlighted
            color = (255, 255, 0) if dir_letter == self.hero_direction else (150, 150, 150)
            size = 28 if dir_letter == self.hero_direction else 24
            dir_font = pygame.font.Font(None, size)

            text = dir_font.render(dir_letter, True, color)
            text_rect = text.get_rect(center=pos)
            self.screen.blit(text, text_rect)

    def _draw_combat_screen(self):
        """Draw the combat interface."""
        self.combat_ui.draw_combat_screen(
            self.screen,
            self.hero,
            self.combat_system.monster,
            self.selected_action
        )

    def _draw_victory_screen(self):
        """Draw the victory overlay."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(192)
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 64)
        text = font.render("Victory!", True, (255, 215, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def draw_game_over(self):
        """
        Create dramatic game over screen.

        Implements a cinematic death sequence with:
        - Fade to black effect
        - Dramatic "YOU DIED" text
        - Restart/quit options

        Death Screen Design:
        1. Progressive black fade
        2. Animated text rendering
        3. Provide player action options
        """
        if not self.death_screen_shown:
            self._create_death_screen()
        else:
            self.screen.blit(self.final_death_screen, (0, 0))
            pygame.display.flip()

    def _create_death_screen(self):
        """Create the death screen with fade effect."""
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