
from abc import abstractmethod
from typing import List, Tuple, Optional
import random

from .dungeon_character import DungeonCharacter

class Hero(DungeonCharacter):
    """Abstract base class for player characters (Warrior, Priestess, Thief)."""

    def __init__(self,
                 name: str,
                 hp: int,
                 min_damage: int,
                 max_damage: int,
                 attack_speed: int,
                 hit_chance: float,
                 block_chance: float):
        super().__init__(name, hp, min_damage, max_damage, attack_speed, hit_chance)
        self._block_chance = block_chance
        self._healing_potions = 0
        self._vision_potions = 0
        self._active_vision = False
        self._pillars_found: List[str] = []

    @property
    def healing_potions(self) -> int:
        return self._healing_potions

    @property
    def vision_potions(self) -> int:
        return self._vision_potions

    @property
    def pillars(self) -> List[str]:
        return self._pillars_found.copy()

    @property
    def active_vision(self) -> bool:
        return self._active_vision

    @active_vision.setter
    def active_vision(self, value: bool) -> None:
        self._active_vision = value

    def take_damage(self, amount: int) -> bool:
        """
        Attempt to block damage, then take any unblocked damage.
        Returns:
            bool: True if damage was blocked
        """
        if random.random() < self._block_chance:  # Successfully blocked
            return True  # Successfully blocked (no damage taken)
        super().take_damage(amount)  # Block failed, take damage
        return False  # Damage was taken

    def use_healing_potion(self) -> Optional[int]:
        if self._healing_potions > 0:
            self._healing_potions -= 1
            heal_amount = random.randint(5, 15)
            old_hp = self.hp
            self.hp += heal_amount
            return self.hp - old_hp
        return None

    def use_vision_potion(self) -> bool:
        """Use vision potion to reveal surrounding rooms."""
        if self._vision_potions > 0:
            self._vision_potions -= 1
            self._active_vision = True
            return True
        return False

    def collect_potion(self, potion_type: str) -> None:
        """Add potion to inventory."""
        if potion_type == "healing":
            self._healing_potions += 1
        elif potion_type == "vision":
            self._vision_potions += 1

    def collect_pillar(self, pillar_type: str) -> None:
        """Add pillar to collection if not already found."""
        if pillar_type not in self._pillars_found:
            self._pillars_found.append(pillar_type)

    @abstractmethod
    def special_skill(self, opponent: DungeonCharacter) -> Tuple[bool, str]:
        """Use hero's special ability."""
        pass

    def __str__(self) -> str:
        status = [
            super().__str__(),
            f"Health Potions: {self._healing_potions}",
            f"Vision Potions: {self._vision_potions}",
            f"Pillars Found: {', '.join(self._pillars_found) if self._pillars_found else 'None'}"
        ]
        return "\n".join(status)

    def has_all_pillars(self) -> bool:
        return len(self._pillars_found) == 4