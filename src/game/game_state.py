from enum import Enum

class GameState(Enum):
    """
    Defines the possible states of the Dungeon Adventure game.

    Provides a structured approach to managing game progression
    and user interaction flow. Each state represents a specific
    phase of the game experience.

    Game State Progression:
    1. MENU: Initial game setup and character selection
    2. PLAYING: Active dungeon exploration
    3. COMBAT: Ongoing battle interactions
    4. GAME_OVER: Player character defeat
    5. VICTORY: Successful game completion

    Design Rationale:
    - Enables clear state management
    - Supports clean state transition logic
    - Provides a comprehensive game flow model
    """
    MENU = 1
    PLAYING = 2
    COMBAT = 3
    GAME_OVER = 4
    VICTORY = 5
