import random
from typing import Tuple
from ..base.hero import Hero
from ..base.dungeon_character import DungeonCharacter


class Warrior(Hero):
    """
    Warrior hero class - a powerful tank character with high damage and health.

    Stats:
    - HP: 125 (Highest health pool)
    - Attack Speed: 4 (Slower attack speed)
    - Hit Chance: 80% (High accuracy)
    - Block Chance: 20% (Lower evasion)
    - Damage: 35-60 (Highest damage per hit)

    Special Ability: Crushing Blow - A powerful attack with a 40% chance to
    deal massive damage (75-175), much higher than regular attacks.
    """

    def __init__(self, name: str):
        """
        Initialize warrior with predefined stats.

        Creates a new Warrior character with the given name and sets all
        statistics to their predefined values as specified in the assignment.

        Args:
            name (str): The name of the Warrior character
        """
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
        Crushing Blow: A chance to deal massive damage to an opponent.

        The Warrior attempts a powerful attack with a 40% chance of success.
        If successful, the attack deals significant damage (75-175 HP),
        much higher than regular attacks. This ability is particularly
        effective against high-HP monsters.

        Args:
            opponent (DungeonCharacter): The target of the crushing blow

        Returns:
            Tuple[bool, str]: A tuple containing:
                - bool: True if the crushing blow succeeded, False if it missed
                - str: A message describing the outcome of the crushing blow
        """
        if random.random() < 0.4:  # 40% chance to succeed
            damage = random.randint(75, 175)
            opponent.take_damage(damage)
            return True, f"Crushing Blow hits for {damage} damage!"
        return False, "Crushing Blow misses!"

    def __str__(self) -> str:
        """
        Return string representation including class type.

        Extends the base Hero string representation by prefixing
        the class name "Warrior".

        Returns:
            str: String representation of the Warrior character
        """
        return f"Warrior {super().__str__()}"