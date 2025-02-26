from abc import ABC, abstractmethod
from typing import List, Protocol, Tuple, Union


class Combatant(Protocol):
    """
    Defines the essential interface for any character participating in combat.

    This protocol establishes a standardized set of properties and methods
    that any combat participant must implement. It ensures that different
    character types (heroes, monsters) can interact seamlessly within
    the combat system.

    Required Properties:
        name (str): Unique identifier for the combatant
        hp (int): Current health points
        is_alive (bool): Indicates whether the combatant can still fight

    Required Methods:
        get_num_attacks(opponent: Combatant) -> int:
            Determine the number of attacks based on combat speed
        attack(opponent: Combatant) -> Tuple[bool, int]:
            Attempt to attack an opponent, returning hit success and damage
        take_damage(amount: int) -> Union[bool, int]:
            Process damage, potentially returning block result or healing

    The protocol allows for:
    - Consistent combat interactions
    - Flexible implementation of different character types
    - Easy extension of combat mechanics
    """

    @property
    def name(self) -> str: ...

    @property
    def hp(self) -> int: ...

    @property
    def is_alive(self) -> bool: ...

    def get_num_attacks(self, opponent: 'Combatant') -> int: ...

    def attack(self, opponent: 'Combatant') -> Tuple[bool, int]: ...

    def take_damage(self, amount: int) -> Union[bool, int]: ...


class CombatHandler(ABC):
    """
    Abstract base class for implementing different types of combat actions.

    Serves as a blueprint for creating specific combat action handlers,
    such as basic attacks, special abilities, or other unique combat interactions.

    Key Responsibilities:
    - Define a standard interface for combat action execution
    - Enable polymorphic handling of different combat action types
    - Support modular design of combat mechanics

    Subclasses must implement the execute method to define:
    - How a specific type of combat action is processed
    - Generation of combat actions
    - Interaction between attacker and defender

    Abstract Method:
        execute(attacker: Combatant, defender: Combatant) -> List[CombatAction]:
            Process a combat action and generate a list of resulting actions.

    Design Pattern:
    - Uses the Template Method pattern
    - Implements Strategy pattern for combat actions
    """

    @abstractmethod
    def execute(self, attacker: Combatant, defender: Combatant) -> List['CombatAction']:
        """
        Execute a specific type of combat action.

        This abstract method must be implemented by subclasses to define
        how a particular type of combat action is processed.

        Args:
            attacker (Combatant): The character initiating the action
            defender (Combatant): The target of the action

        Returns:
            List[CombatAction]: A list of actions resulting from the combat interaction

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        pass


# Import at bottom to avoid circular import
from .combat_action import CombatAction