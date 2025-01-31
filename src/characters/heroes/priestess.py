import random
from typing import Tuple
from ..base.hero import Hero
from ..base.dungeon_character import DungeonCharacter


class Priestess(Hero):
    """
    Priestess hero class - frail fighter with a healing ability.

    Stats:
    - HP: 75
    - Attack Speed: 5
    - Hit Chance: 70%
    - Block Chance: 30%
    - Damage: 25-45
    """

    def __init__(self, name: str):
        """Initialize priestess with predefined stats."""
        super().__init__(
            name=name,
            hp=75,
            min_damage=25,
            max_damage=45,
            attack_speed=5,
            hit_chance=0.7,
            block_chance=0.3
        )

    def special_skill(self, opponent: DungeonCharacter) -> Tuple[bool, str]:
        """
        Heal: Restore 25-50 HP if not at full health.

        Returns:
            Tuple of (success, message)
        """
        if self.hp < self._max_hp:  # Only heal if not at full health
            heal_amount = random.randint(25, 50)
            old_hp = self.hp
            self.hp += heal_amount
            actual_heal = self.hp - old_hp  # Calculate actual amount healed
            return True, f"Healed for {actual_heal} HP!"
        return False, "Already at full health!"

    def __str__(self) -> str:
        """Return string representation including class type."""
        return f"Priestess {super().__str__()}"  # Changed Priest to Priestess