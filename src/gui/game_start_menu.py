import pygame
from enum import Enum

class MenuState(Enum):
    MAIN_MENU = 0
    HERO_SELECT = 1
    NAME_INPUT = 2
    DIFFICULTY_SELECT = 3
    PLAYING = 4


class GameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        # Menu state
        self.selected_hero = None
        self.hero_options = [
            {"class": "Warrior", "description": "High HP, Crushing Blow ability", "rect": None},
            {"class": "Priestess", "description": "Healing ability, balanced stats", "rect": None},
            {"class": "Thief", "description": "Fast attacks, Surprise Attack ability", "rect": None}
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

    def handle_event(self, event):
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
        """Update whether the start button can be clicked"""
        self.can_start = (self.selected_hero and
                          self.player_name.strip() and
                          self.selected_difficulty)

    def draw(self):
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
                # Draw glowing border
                glow_rect = hero_rect.inflate(6, 6)
                pygame.draw.rect(self.screen, (200, 200, 0), glow_rect)  # Gold glow
                pygame.draw.rect(self.screen, (255, 255, 0), hero_rect)  # Bright yellow background
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
            self.screen.get_width() // 2 - 100,
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

    def get_game_settings(self):
        """Return the selected game settings."""
        if self.can_start:
            return {
                "hero_class": self.selected_hero,
                "player_name": self.player_name,
                "difficulty": self.selected_difficulty
            }
        return None
