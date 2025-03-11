import pygame

def draw_button(self):
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

def draw_difficulty_selector(self):
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