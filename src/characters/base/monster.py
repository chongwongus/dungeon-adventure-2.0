import random
from abc import ABC
from .dungeon_character import DungeonCharacter


class Monster(DungeonCharacter, ABC):
    """
    Abstract base class for all monsters.
    Extends DungeonCharacter with healing abilities.
    """

    def __init__(self,
                 name: str,
                 hp: int,
                 min_damage: int,
                 max_damage: int,
                 attack_speed: int,
                 hit_chance: float,
                 heal_chance: float,
                 min_heal: int,
                 max_heal: int):
        """
        Initialize monster attributes.

        Args:
            name: Monster name
            hp: Starting/max hit points
            min_damage: Minimum damage dealt
            max_damage: Maximum damage dealt
            attack_speed: Speed determines number of attacks
            hit_chance: Probability of landing an attack
            heal_chance: Probability of healing after taking damage
            min_heal: Minimum healing amount
            max_heal: Maximum healing amount
        """
        super().__init__(name, hp, min_damage, max_damage, attack_speed, hit_chance)
        self._heal_chance = heal_chance
        self._min_heal = min_heal
        self._max_heal = max_heal

    def take_damage(self, amount: int) -> int:
        """
        Take damage and possibly heal.

        Args:
            amount: Amount of damage to take

        Returns:
            int: Amount healed (0 if no healing occurred)
        """
        # Take the damage first
        super().take_damage(amount)

        # Only try to heal if still alive and didn't die from the damage
        if self.is_alive and random.random() < self._heal_chance:
            heal_amount = random.randint(self._min_heal, self._max_heal)
            old_hp = self.hp
            self.hp += heal_amount
            return self.hp - old_hp  # Return actual amount healed
        return 0

    def __str__(self) -> str:
        """Return string representation including healing stats."""
        return (f"{super().__str__()} | "
                f"Heal Chance: {self._heal_chance * 100}% | "
                f"Heal Amount: {self._min_heal}-{self._max_heal}")