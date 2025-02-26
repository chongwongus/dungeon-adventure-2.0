import pygame
import time
from typing import List, Dict, Any
from ..constants import WHITE, RED, DARK_GRAY


class EventLog:
    """
    Manages the game's event logging and display system.

    This class creates a robust event tracking mechanism that
    supports multiple message types, provides rich visualization,
    and maintains a comprehensive game event history.

    Core Responsibilities:
    - Log game events with contextual metadata
    - Render events in both console and UI
    - Support scrollable message history
    - Provide type-based message styling

    Message Type Categories:
    - Combat events
    - Item interactions
    - Movement notifications
    - System messages
    - Default generic messages

    Design Features:
    1. Flexible Logging
       - Supports multiple message types
       - Adds timestamp to each message
       - Maintains maximum message limit

    2. Visual Representation
       - Color-coded message types
       - Scrollable message history
       - Word-wrapping support

    3. Multi-Output Logging
       - Console printing
       - UI rendering
    """

    def __init__(self, max_messages: int = 100):
        """
        Initialize the event logging system.

        Sets up the foundational components for event tracking:
        - Create message storage
        - Configure maximum message limit
        - Set up font rendering
        - Define message type color palette

        Initialization Strategy:
        1. Attempt to load custom font
        2. Gracefully fall back to system font
        3. Prepare color mapping for different message types

        Args:
            max_messages (int, optional):
                Maximum number of messages to retain.
                Defaults to 100.
        """
        self.messages: List[Dict[str, Any]] = []
        self.max_messages = max_messages
        self.scroll_position = 0

        # Load Action Man font if available, else fall back to system default
        try:
            self.font = pygame.font.Font("src/assets/fonts/ActionMan.ttf", 16)
        except FileNotFoundError:
            print("Could not load Action Man font, falling back to system default")
            self.font = pygame.font.SysFont("arial", 16)

        # Different colors for different message types
        self.colors = {
            'combat': (255, 180, 180),  # Light red for combat
            'item': (180, 255, 180),  # Light green for items
            'movement': (180, 180, 255),  # Light blue for movement
            'system': (255, 255, 180),  # Light yellow for system messages
            'default': WHITE
        }

    def add_message(self, text: str, message_type: str = 'default', is_system: bool = False):
        """
        Log a new event message to the system.

        Comprehensive message logging that:
        - Stores message with contextual metadata
        - Prints to console with formatted prefix
        - Manages message history
        - Supports different message types

        Logging Workflow:
        1. Create message dictionary with rich metadata
        2. Append to message history
        3. Manage message list size
        4. Print to console with appropriate formatting

        Args:
            text (str): Message content
            message_type (str, optional):
                Categorization of message type.
                Defaults to 'default'.
            is_system (bool, optional):
                Indicates critical system messages.
                Defaults to False.
        """
        message = {
            'text': text,
            'time': time.time(),
            'type': message_type,
            'is_system': is_system,
            'color': self.colors.get(message_type, self.colors['default'])
        }
        self.messages.append(message)

        # Print to console with cleaner formatting
        prefix = "[!]" if is_system else "[+]"
        print(f"{prefix} {text}")

        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        self.scroll_position = max(0, len(self.messages) - 10)

    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        """
        Render the event log on a given surface.

        Implements a sophisticated rendering strategy that:
        - Draws log background
        - Handles message word-wrapping
        - Supports scrollable message history
        - Renders messages with type-specific coloration

        Rendering Process:
        1. Draw background rectangle
        2. Calculate visible messages
        3. Implement intelligent word-wrapping
        4. Render messages with type-specific colors
        5. Add scroll indicators if needed

        Args:
            surface (pygame.Surface): Surface to render log on
            rect (pygame.Rect): Rectangular area for log display
        """
        # Draw background
        pygame.draw.rect(surface, DARK_GRAY, rect)

        # Calculate visible messages
        messages_per_page = rect.height // 20  # Reduced from 25 to 20 for better spacing
        visible_messages = self.messages[self.scroll_position:
                                         self.scroll_position + messages_per_page]

        # Draw messages
        y = rect.top + 5
        max_width = rect.width - 10  # Leave 5px padding on each side

        for msg in visible_messages:
            # Word wrap text if it's too long
            words = msg['text'].split()
            lines = []
            current_line = []

            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                if self.font.size(test_line)[0] > max_width:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(test_line)
                        current_line = []

            if current_line:
                lines.append(' '.join(current_line))

            # Draw each line
            for line in lines:
                text = self.font.render(line, True, msg['color'])
                surface.blit(text, (rect.left + 5, y))
                y += 20

                if y > rect.bottom - 20:
                    break

        # Draw scroll indicators if needed
        if self.scroll_position > 0:
            pygame.draw.polygon(surface, WHITE,
                                [(rect.right - 15, rect.top + 5),
                                 (rect.right - 5, rect.top + 5),
                                 (rect.right - 10, rect.top + 15)])

        if self.scroll_position + messages_per_page < len(self.messages):
            pygame.draw.polygon(surface, WHITE,
                                [(rect.right - 15, rect.bottom - 15),
                                 (rect.right - 5, rect.bottom - 15),
                                 (rect.right - 10, rect.bottom - 5)])