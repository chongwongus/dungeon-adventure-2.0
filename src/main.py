import pygame
from enum import Enum
from dungeon.easy_factory import EasyDungeonFactory
from dungeon.dfs_factory import DFSDungeonFactory
from characters.heroes.warrior import Warrior
from characters.heroes.priestess import Priestess
from characters.heroes.thief import Thief
from gui.game_window import GameWindow
from gui.game_start_menu import GameMenu, MenuState


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    COMBAT = 3
    GAME_OVER = 4
    VICTORY = 5


class DungeonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Dungeon Adventure")
        self.reset_game()

    def reset_game(self):
        """Reset all game state variables"""
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
        # Create dungeon based on difficulty
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

    def handle_menu(self):
        """Handle menu state interactions."""
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
        """Handle playing state interactions."""
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
        """Main game loop."""
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


if __name__ == "__main__":
    game = DungeonGame()
    game.run()
