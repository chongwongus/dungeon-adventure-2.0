import pygame
from enum import Enum
from dungeon.easy_factory import EasyDungeonFactory
from dungeon.dfs_factory import DFSDungeonFactory
from characters.heroes.warrior import Warrior
from characters.heroes.priestess import Priestess
from characters.heroes.thief import Thief
from gui.game_window import GameWindow, MiniMap


class GameState(Enum):
    MENU = 1
    HERO_SELECT = 2
    PLAYING = 3
    COMBAT = 4
    GAME_OVER = 5
    VICTORY = 6


class DungeonGame:
    def __init__(self):
        pygame.init()

        # Initialize state variables
        self.dungeon = None
        self.hero = None
        self.game_window = None
        self.state = GameState.MENU

        # Add movement cooldown
        self.last_move_time = 0
        self.move_cooldown = 200  # Milliseconds between moves

        # Add a flag to track if debug logs should be printed
        self.debug_log_minimap = False

        # Start initial game
        self.init_game(Warrior, EasyDungeonFactory)

    def init_game(self, hero_class, factory_class):
        """Initialize a new game with selected hero and dungeon factory."""
        # Create dungeon
        factory = factory_class()  # Create factory instance
        self.dungeon = factory.create()  # Create dungeon

        # Create hero
        self.hero = hero_class("Player")  # Can add name selection later
        self.hero.location = self.dungeon.entrance

        # Initialize or update game window
        if self.game_window is None:
            self.game_window = GameWindow(self.dungeon, factory.pillar_locations)
        else:
            # Update existing window with new dungeon and pillar locations
            self.game_window.dungeon = self.dungeon
            self.game_window.minimap = MiniMap(self.dungeon, factory.pillar_locations)

        self.game_window.event_log.add_message("Welcome to Dungeon Adventure!")

        # Set initial game state
        self.state = GameState.PLAYING

    def handle_menu(self):
        """Handle menu state interactions."""
        # This will be implemented when we add the menu system
        # For now, just start a new game with default settings
        self.init_game(Warrior, EasyDungeonFactory)

    def can_move(self) -> bool:
        """Check if enough time has passed to allow movement."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_cooldown:
            self.last_move_time = current_time
            return True
        return False

    def handle_playing(self):
        """Handle playing state interactions."""
        keys = pygame.key.get_pressed()

        # Only handle movement if cooldown has expired
        if self.can_move():
            # Store old position to check what we find in new room
            old_x, old_y = self.hero.location

            # Handle movement
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
                    # Set the debug_log_minimap flag to True
                    self.debug_log_minimap = True

                    # Only log interesting findings in the new room
                    new_x, new_y = self.hero.location
                    new_room = self.dungeon.get_room(new_x, new_y)

                    if new_room.hasPillar:
                        self.game_window.event_log.add_message(f"Found a pillar: {new_room.pillarType}!")
                    if new_room.hasHealthPot:
                        self.game_window.event_log.add_message("Found a health potion!")
                    if new_room.hasVisionPot:
                        self.game_window.event_log.add_message("Found a vision potion!")
                    if new_room.hasPit:
                        self.game_window.event_log.add_message("Careful! There's a pit here!", True)
                    if new_room.monster:
                        self.game_window.event_log.add_message(f"Encountered a {new_room.monster.name}!", True)
                elif messages:
                    # Only log the error message
                    self.game_window.event_log.add_message(messages[0], True)

        # Handle item usage (no cooldown needed)
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
        elif (self.hero.location == self.dungeon.exit and
              self.hero.has_all_pillars()):
            self.state = GameState.VICTORY

    def run(self):
        """Main game loop."""
        running = True
        clock = pygame.time.Clock()

        while running:
            # Handle events
            for event in pygame.event.get():
                if not self.game_window.handle_event(event):
                    running = False
                    break

            # Handle current game state
            if self.state == GameState.MENU:
                self.handle_menu()
            elif self.state == GameState.PLAYING:
                self.handle_playing()

            # Update and draw every frame
            self.game_window.update(self.hero)
            self.game_window.draw(self.hero, self.debug_log_minimap)  # Pass debug_log_minimap here

            # Reset the debug flag after drawing
            self.debug_log_minimap = False

            # Cap frame rate
            clock.tick(120)

        pygame.quit()


if __name__ == "__main__":
    game = DungeonGame()
    game.run()