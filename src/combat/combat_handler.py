from abc import ABC, abstractmethod
from typing import List, Protocol, Tuple, Union


class Combatant(Protocol):
    """Protocol defining required methods for any combatant"""

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
    """Abstract base class for different types of combat actions"""

    @abstractmethod
    def execute(self, attacker: Combatant, defender: Combatant) -> List['CombatAction']:
        """Execute this combat action and return results"""
        pass


# Import at bottom to avoid circular import
from .combat_action import CombatAction