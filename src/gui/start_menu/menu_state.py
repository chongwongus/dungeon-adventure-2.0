from enum import Enum

class MenuState(Enum):
    """
    Defines the possible states of the game start menu.

    Provides a structured approach to managing menu navigation
    and user interaction flow. Each state represents a specific
    phase of the game configuration process.

    Menu Progression:
    1. MAIN_MENU: Initial entry point
    2. HERO_SELECT: Character selection phase
    3. NAME_INPUT: Player name entry
    4. DIFFICULTY_SELECT: Game challenge level choice
    5. PLAYING: Transition to game start
    """
    MAIN_MENU = 0
    HERO_SELECT = 1
    NAME_INPUT = 2
    DIFFICULTY_SELECT = 3
    PLAYING = 4