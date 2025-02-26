from abc import ABC, abstractmethod
import random
from typing import Tuple, Optional


class DungeonCharacter(ABC):
    """
    Abstract base class for all characters in the dungeon adventure game.

    This class defines the common attributes and behaviors shared by all characters,
    including both heroes and monsters. It establishes the foundation for the
    character inheritance hierarchy.

    Attributes:
        _name (str): The character's name
        _max_hp (int): Maximum hit points the character can have
        _hp (int): Current hit points, representing character health
        _min_damage (int): Minimum damage the character can deal
        _max_damage (int): Maximum damage the character can deal
        _attack_speed (int): Determines number of attacks (1 is slowest)
        _hit_chance (float): Probability (0.0-1.0) of landing an attack
        _curr_location (Tuple[int, int], optional): Character's position in the dungeon
    """

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
        """
        Get the character's name.

        Returns:
            str: The character's name
        """
        return self._name

    @property
    def hp(self) -> int:
        """
        Get the character's current hit points.

        Returns:
            int: Current hit points
        """
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """
        Set character's hit points, ensuring value stays between 0 and max_hp.

        Args:
            value (int): New hit points value to set
        """
        self._hp = max(0, min(value, self._max_hp))

    @property
    def is_alive(self) -> bool:
        """
        Check if character is still alive.

        Returns:
            bool: True if character has more than 0 hit points, False otherwise
        """
        return self._hp > 0

    @property
    def location(self) -> Optional[Tuple[int, int]]:
        """
        Get the character's current location in the dungeon.

        Returns:
            Optional[Tuple[int, int]]: (x, y) coordinates or None if not positioned
        """
        return self._curr_location

    @location.setter
    def location(self, value: Tuple[int, int]) -> None:
        """
        Set the character's location in the dungeon.

        Args:
            value (Tuple[int, int]): (x, y) coordinates in the dungeon
        """
        self._curr_location = value

    def move(self, direction: str) -> None:
        """
        Update character's location based on direction.

        Changes the character's coordinates based on the specified direction.
        No movement occurs if the character has no current location.

        Args:
            direction (str): Direction to move ('N', 'S', 'E', or 'W')
        """
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

        A character gets an extra attack for each multiple of the opponent's speed.
        For example, a character with speed 6 attacking an opponent with speed 2
        would get 3 attacks per round.

        Args:
            opponent (DungeonCharacter): The character being attacked

        Returns:
            int: Number of attacks per round, minimum of 1
        """
        speed_ratio = self._attack_speed / opponent._attack_speed
        return max(1, int(speed_ratio))

    def attack(self, opponent: 'DungeonCharacter') -> Tuple[bool, int]:
        """
        Calculate attack damage but don't apply it.

        Determines if an attack hits based on hit chance and calculates
        the damage amount if successful. The actual damage application
        is handled separately.

        Args:
            opponent (DungeonCharacter): The character being attacked

        Returns:
            Tuple[bool, int]: (hit_success, damage_to_deal)
                               If hit_success is False, damage will be 0
        """
        if random.random() < self._hit_chance:
            damage = random.randint(self._min_damage, self._max_damage)
            return True, damage
        return False, 0

    def take_damage(self, amount: int) -> None:
        """
        Take damage and update HP.

        Reduces the character's hit points by the specified amount,
        ensuring HP doesn't go below 0.

        Args:
            amount (int): Amount of damage to apply
        """
        new_hp = max(0, self.hp - amount)  # Calculate new HP
        self.hp = new_hp

    def __str__(self) -> str:
        """
        Return string representation of the character.

        Returns:
            str: Character name and current/maximum hit points
        """
        return f"{self.name} (HP: {self.hp}/{self._max_hp})"