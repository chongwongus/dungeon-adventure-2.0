from abc import ABC, abstractmethod
import random
from typing import Tuple, Optional


class DungeonCharacter(ABC):
    """Abstract base class for all characters in the dungeon."""

    def __init__(self,
                 name: str,
                 hp: int,
                 min_damage: int,
                 max_damage: int,
                 attack_speed: int,
                 hit_chance: float):
        """
        Initialize base character attributes.

        Args:
            name: Character name
            hp: Starting/max hit points
            min_damage: Minimum damage dealt
            max_damage: Maximum damage dealt
            attack_speed: Speed determines number of attacks (1 is slowest)
            hit_chance: Probability of landing an attack (0.0 to 1.0)
        """
        self._name = name
        self._max_hp = hp
        self._hp = hp
        self._min_damage = min_damage
        self._max_damage = max_damage
        self._attack_speed = attack_speed
        self._hit_chance = hit_chance
        self._curr_location: Optional[Tuple[int, int]] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """Set HP ensuring it stays between 0 and max_hp."""
        self._hp = max(0, min(value, self._max_hp))

    @property
    def is_alive(self) -> bool:
        """Check if character is still alive."""
        return self._hp > 0

    @property
    def location(self) -> Optional[Tuple[int, int]]:
        return self._curr_location

    @location.setter
    def location(self, value: Tuple[int, int]) -> None:
        self._curr_location = value

    def move(self, direction: str) -> None:
        """Update location based on direction."""
        if not self._curr_location:
            return

        x, y = self._curr_location
        if direction == 'N':
            self._curr_location = (x, y - 1)
        elif direction == 'S':
            self._curr_location = (x, y + 1)
        elif direction == 'E':
            self._curr_location = (x + 1, y)
        elif direction == 'W':
            self._curr_location = (x - 1, y)

    def get_num_attacks(self, opponent: 'DungeonCharacter') -> int:
        """
        Calculate number of attacks based on speed ratio.
        A character gets an extra attack for each multiple of opponent's speed.
        """
        speed_ratio = self._attack_speed / opponent._attack_speed
        return max(1, int(speed_ratio))

    def attack(self, opponent: 'DungeonCharacter') -> Tuple[bool, int]:
        """
        Attempt to attack opponent.

        Returns:
            Tuple of (hit_success, damage_dealt)
        """
        if random.random() < self._hit_chance:
            damage = random.randint(self._min_damage, self._max_damage)
            opponent.take_damage(damage)
            return True, damage
        return False, 0

    def take_damage(self, amount: int) -> None:
        """Take damage and update HP."""
        self.hp = self.hp - amount

    def __str__(self) -> str:
        return f"{self.name} (HP: {self.hp}/{self._max_hp})"