import pygame
import time
from typing import List, Dict, Any
from ..constants import WHITE, RED, DARK_GRAY

class EventLog:
    """Handles game event logging and display"""

    def __init__(self, max_messages: int = 100):
        self.messages: List[Dict[str, Any]] = []
        self.max_messages = max_messages
        self.scroll_position = 0
        self.font = pygame.font.Font(None, 24)

    def add_message(self, text: str, is_system: bool = False):
        """Add a message to the log and print to console."""
        message = {
            'text': text,
            'time': time.time(),
            'is_system': is_system,
            'color': RED if is_system else WHITE
        }
        self.messages.append(message)

        # Print to console with cleaner formatting
        prefix = "[!]" if is_system else "[+]"
        print(f"{prefix} {text}")

        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        self.scroll_position = max(0, len(self.messages) - 10)

    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        """Draw the log on the given surface."""
        # Draw background
        pygame.draw.rect(surface, DARK_GRAY, rect)

        # Calculate visible messages
        messages_per_page = rect.height // 25  # Approximate line height
        visible_messages = self.messages[self.scroll_position:
                                       self.scroll_position + messages_per_page]

        # Draw messages
        y = rect.top + 5
        for msg in visible_messages:
            text = self.font.render(msg['text'], True, msg['color'])
            surface.blit(text, (rect.left + 5, y))
            y += 25