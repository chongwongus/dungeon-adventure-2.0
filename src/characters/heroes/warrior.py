import random
from typing import Tuple
from ..base.hero import Hero
from ..base.dungeon_character import DungeonCharacter


class Warrior(Hero):
    """
    Warrior hero class - tough fighter with high HP and Crushing Blow ability.

    Stats:
    - HP: 125
    - Attack Speed: 4
    - Hit Chance: 80%
    - Block Chance: 20%
    - Damage: 35-60
    """

    def __init__(self, name: str):
        """Initialize warrior with predefined stats."""
        super().__init__(
            name=name,
            hp=125,
            min_damage=35,
            max_damage=60,
            attack_speed=4,
            hit_chance=0.8,
            block_chance=0.2
        )

    def special_skill(self, opponent: DungeonCharacter) -> Tuple[bool, str]:
        """
        Crushing Blow: 40% chance to deal massive damage (75-175).

        Returns:
            Tuple of (success, message)
        """
        if random.random() < 0.4:  # 40% chance to succeed
            damage = random.randint(75, 175)
            opponent.take_damage(damage)
            return True, f"Crushing Blow hits for {damage} damage!"
        return False, "Crushing Blow misses!"

    def __str__(self) -> str:
        """Return string representation including class type."""
        return f"Warrior {super().__str__()}"