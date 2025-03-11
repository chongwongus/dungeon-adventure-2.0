import pygame

from src.characters.heroes.priestess import Priestess
from src.characters.heroes.thief import Thief
from src.characters.heroes.warrior import Warrior
from src.dungeon.dfs_factory import DFSDungeonFactory
from src.dungeon.easy_factory import EasyDungeonFactory
from src.game.game_state import GameState
from src.gui import GameWindow
from src.gui.start_menu.game_start_menu import GameMenu


class DungeonGame:
    """
    Primary game controller for the Dungeon Adventure experience.

    Serves as the central management system that coordinates
    all aspects of game initialization, progression, and
    state management.

    Core Responsibilities:
    1. Game Initialization
       - Set up pygame environment
       - Prepare initial game state
       - Create UI components

    2. State Management
       - Handle menu interactions
       - Manage gameplay progression
       - Control game state transitions

    3. User Interaction
       - Process input events
       - Coordinate game responses
       - Manage movement and actions

    Design Architecture:
    - Event-driven game loop
    - Modular state handling
    - Flexible game configuration
    - Responsive user interface

    Key Methods:
    - reset_game(): Reinitialize game state
    - init_game(): Set up new game configuration
    - handle_menu(): Manage menu interactions
    - handle_playing(): Process active gameplay
    - run(): Main game execution loop

    Interaction Workflow:
    The game progresses through different states, responding
    to user inputs and game events, creating a dynamic and
    engaging gameplay experience.
    """
    def __init__(self):
        """
        Initialize the Dungeon Adventure game environment.

        Sets up critical game components:
        - Pygame initialization
        - Display window creation
        - Initial game state preparation

        Initialization Strategy:
        1. Initialize pygame system
        2. Create game display window
        3. Prepare initial game state
        4. Set up game loop parameters

        Game Setup Considerations:
        - Consistent window sizing
        - Proper pygame configuration
        - Flexible game state management
        """
        self.move_cooldown = None
        self.last_move_time = None
        self.hero = None
        self.dungeon = None
        self.game_window = None
        self.menu = None
        self.state = None

        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Dungeon Adventure")
        self.reset_game()

    def reset_game(self):
        """
        Reset all game state variables to initial conditions.

        Comprehensive game state reinitialization that:
        - Clears existing game progress
        - Resets to initial menu state
        - Prepares for new game start

        Reset Process:
        1. Set game state to menu
        2. Clear existing game objects
        3. Reset time-based mechanics
        4. Prepare for new game configuration
        """
        self.state = GameState.MENU
        self.menu = GameMenu(self.screen)
        self.game_window = None
        self.dungeon = None
        self.hero = None
        self.last_move_time = 0
        self.move_cooldown = 200

    def handle_game_over(self):
        """Handle game over state and check for restart"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    self.reset_game()
                    return True
                elif event.key == pygame.K_ESCAPE:  # Quit
                    return False

        # Draw game over screen
        if self.game_window:
            self.game_window.draw_game_over()
        return True

    def init_game(self, settings):
        """
        Initialize a new game based on player configuration.

        Comprehensive game setup process that:
        - Selects dungeon generation strategy
        - Creates hero character
        - Initializes game window
        - Prepares initial game state

        Configuration Steps:
        1. Choose dungeon generation method
        2. Create hero based on player selection
        3. Set up game window
        4. Transition to playing state

        Flexibility Considerations:
        - Supports different difficulty levels
        - Allows multiple hero types
        - Enables dynamic game initialization
        """
        factory_class = EasyDungeonFactory if settings['difficulty'] == 'easy' else DFSDungeonFactory
        factory = factory_class()
        self.dungeon = factory.create()

        # Create hero based on class selection
        hero_class = {
            'Warrior': Warrior,
            'Priestess': Priestess,
            'Thief': Thief
        }[settings['hero_class']]

        self.hero = hero_class(settings['player_name'])
        self.hero.location = self.dungeon.entrance

        # Initialize game window with hero reference
        self.game_window = GameWindow(self.dungeon, factory.pillar_locations, self.hero)
        self.game_window.event_log.add_message(f"Welcome, {self.hero.name}!")

        # Set game state to playing
        self.state = GameState.PLAYING

    def save_game(self):
        self.hero

    def handle_menu(self):
        """
        Manage interactions within the game's start menu.

        Handles user interface and configuration selection:
        - Process menu events
        - Manage user selections
        - Transition to game initialization

        Menu Interaction Workflow:
        1. Process pygame events
        2. Handle menu interactions
        3. Check for game start conditions
        4. Render menu interface
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            self.menu.handle_event(event)

            # Check if menu is complete and game should start
            settings = self.menu.get_game_settings()
            if settings:
                self.init_game(settings)

        self.menu.draw()
        return True

    def can_move(self) -> bool:
        """Check if enough time has passed to allow movement."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_cooldown:
            self.last_move_time = current_time
            return True
        return False

    def handle_playing(self):
        """
        Manage active gameplay interactions and state.

        Comprehensive method that:
        - Processes user inputs
        - Handles movement and actions
        - Manages game state transitions
        - Updates game display

        Gameplay Management:
        1. Process system events
        2. Handle hero movement
        3. Manage item usage
        4. Check game-ending conditions
        5. Update game window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if not self.game_window.handle_event(event):
                if not self.hero.is_alive:
                    self.state = GameState.GAME_OVER
                    return True

        if not self.game_window.in_combat:
            keys = pygame.key.get_pressed()
            if self.can_move():
                direction = None
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    direction = 'N'
                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    direction = 'S'
                elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    direction = 'W'
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    direction = 'E'

                if direction:
                    success, messages, combat = self.dungeon.move_hero(self.hero, direction)
                    if success:
                        new_room = self.dungeon.get_room(*self.hero.location)
                        if new_room.monster and new_room.monster.is_alive:
                            self.game_window.start_combat(self.hero, new_room.monster)
                        elif messages:
                            for msg in messages:
                                self.game_window.event_log.add_message(msg)
                    elif messages:
                        for msg in messages:
                            self.game_window.event_log.add_message(msg, True)

            # Handle item usage
            if keys[pygame.K_h]:  # Health potion
                if self.hero.use_healing_potion():
                    self.game_window.event_log.add_message("Used a healing potion!")
                else:
                    self.game_window.event_log.add_message("No healing potions!", True)
            elif keys[pygame.K_v]:  # Vision potion
                if self.hero.use_vision_potion():
                    self.game_window.event_log.add_message("Used a vision potion!")
                else:
                    self.game_window.event_log.add_message("No vision potions!", True)

        # Update game state based on conditions
        if not self.hero.is_alive:
            self.state = GameState.GAME_OVER
        elif self.game_window.check_victory_condition(self.hero):
            self.state = GameState.VICTORY

        self.game_window.update(self.hero)
        self.game_window.draw(self.hero)
        return True

    def run(self):
        """
        Execute the main game loop.

        Serves as the primary game execution method that:
        - Maintains continuous game operation
        - Manages state transitions
        - Handles frame timing
        - Coordinates game progression

        Game Loop Characteristics:
        - Event-driven processing
        - State-based execution
        - Consistent frame rate management
        - Graceful game termination
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            if self.state == GameState.MENU:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break

                    settings = self.menu.handle_event(event)
                    if settings:
                        self.init_game(settings)
                        break

                self.menu.draw()

            elif self.state == GameState.PLAYING:
                running = self.handle_playing()

            elif self.state == GameState.GAME_OVER:
                running = self.handle_game_over()

            clock.tick(60)

        pygame.quit()
