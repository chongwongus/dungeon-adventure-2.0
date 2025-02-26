from abc import abstractmethod
from typing import List, Tuple, Optional
import random

from .dungeon_character import DungeonCharacter


class Hero(DungeonCharacter):
    """
    Abstract base class for player characters (Warrior, Priestess, Thief).

    Heroes are controlled by the player and extend the DungeonCharacter class
    with additional capabilities like blocking attacks, using potions,
    and special abilities unique to each hero class. Heroes can also
    collect the pillars needed to complete the dungeon adventure.

    Attributes:
        class_name (str): The name of the hero's class
        _block_chance (float): Probability (0.0-1.0) of blocking an attack
        _healing_potions (int): Count of healing potions in inventory
        _vision_potions (int): Count of vision potions in inventory
        _active_vision (bool): Whether a vision potion effect is active
        _pillars_found (List[str]): List of collected pillar types
    """

    def __init__(self,
                 name: str,
                 hp: int,
                 min_damage: int,
                 max_damage: int,
                 attack_speed: int,
                 hit_chance: float,
                 block_chance: float):
        """
        Initialize hero attributes and call parent constructor.

        Args:
            name (str): Hero's name
            hp (int): Starting/max hit points
            min_damage (int): Minimum damage dealt
            max_damage (int): Maximum damage dealt
            attack_speed (int): Speed determines number of attacks
            hit_chance (float): Probability of landing an attack
            block_chance (float): Probability of blocking an attack
        """
        super().__init__(name, hp, min_damage, max_damage, attack_speed, hit_chance)

        self.class_name = self.__class__.__name__
        self._block_chance = block_chance
        self._healing_potions = 0
        self._vision_potions = 0
        self._active_vision = False
        self._pillars_found: List[str] = []

    @property
    def healing_potions(self) -> int:
        """
        Get the number of healing potions in inventory.

        Returns:
            int: Count of healing potions
        """
        return self._healing_potions

    @property
    def vision_potions(self) -> int:
        """
        Get the number of vision potions in inventory.

        Returns:
            int: Count of vision potions
        """
        return self._vision_potions

    @property
    def pillars(self) -> List[str]:
        """
        Get a copy of the list of collected pillars.

        Returns:
            List[str]: Names of all collected pillars
        """
        return self._pillars_found.copy()

    @property
    def active_vision(self) -> bool:
        """
        Check if a vision potion effect is currently active.

        Returns:
            bool: True if vision effect is active, False otherwise
        """
        return self._active_vision

    @active_vision.setter
    def active_vision(self, value: bool) -> None:
        """
        Set the active status of vision potion effect.

        Args:
            value (bool): New vision effect status
        """
        self._active_vision = value

    def take_damage(self, amount: int) -> bool:
        """
        Attempt to block damage, then take any unblocked damage.

        Heroes have a chance to block attacks based on their block_chance.
        If the block is successful, no damage is taken.

        Args:
            amount (int): Amount of damage to potentially take

        Returns:
            bool: True if damage was blocked, False if damage was taken
        """
        if random.random() < self._block_chance:  # Successfully blocked
            return True  # Successfully blocked (no damage taken)
        super().take_damage(amount)  # Block failed, take damage
        return False  # Damage was taken

    def use_healing_potion(self) -> Optional[int]:
        """
        Use a healing potion to restore hit points.

        Consumes one healing potion and restores a random amount of HP
        between 5 and 15.

        Returns:
            Optional[int]: Amount of HP actually restored, or None if no potions available
        """
        if self._healing_potions > 0:
            self._healing_potions -= 1
            heal_amount = random.randint(5, 15)
            old_hp = self.hp
            self.hp += heal_amount
            return self.hp - old_hp
        return None

    def use_vision_potion(self) -> bool:
        """
        Use a vision potion to reveal surrounding rooms.

        Consumes one vision potion and activates the vision effect,
        which will reveal rooms adjacent to the hero when moving.

        Returns:
            bool: True if potion was used successfully, False if no potions available
        """
        if self._vision_potions > 0:
            self._vision_potions -= 1
            self._active_vision = True
            return True
        return False

    def collect_potion(self, potion_type: str) -> None:
        """
        Add a potion to the hero's inventory.

        Args:
            potion_type (str): Type of potion to add ("healing" or "vision")
        """
        if potion_type == "healing":
            self._healing_potions += 1
        elif potion_type == "vision":
            self._vision_potions += 1

    def collect_pillar(self, pillar_type: str) -> None:
        """
        Add a pillar to the hero's collection if not already found.

        Heroes need to collect all pillars to win the game. This method
        ensures each pillar is only collected once.

        Args:
            pillar_type (str): Type of pillar to collect
        """
        print(f"Hero attempting to collect pillar: {pillar_type}")  # Debug print
        if pillar_type not in self._pillars_found:
            self._pillars_found.append(pillar_type)
            print(f"Pillar collected! Current pillars: {self._pillars_found}")  # Debug print
        else:
            print(f"Pillar {pillar_type} already in collection: {self._pillars_found}")  # Debug print

    @abstractmethod
    def special_skill(self, opponent: DungeonCharacter) -> Tuple[bool, str]:
        """
        Use the hero's special ability.

        Each hero subclass implements a unique special skill.
        This method must be overridden by concrete hero classes.

        Args:
            opponent (DungeonCharacter): Target of the special skill

        Returns:
            Tuple[bool, str]: Success status and descriptive message
        """
        pass

    def __str__(self) -> str:
        """
        Return a detailed string representation of the hero.

        Includes basic character info plus inventory and pillar status.

        Returns:
            str: Multi-line description of hero status
        """
        status = [
            super().__str__(),
            f"Health Potions: {self._healing_potions}",
            f"Vision Potions: {self._vision_potions}",
            f"Pillars Found: {', '.join(self._pillars_found) if self._pillars_found else 'None'}"
        ]
        return "\n".join(status)

    def has_all_pillars(self) -> bool:
        """
        Check if the hero has collected all required pillars.

        Returns:
            bool: True if all 4 pillars have been collected, False otherwise
        """
        return len(self._pillars_found) == 4