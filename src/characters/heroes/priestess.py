import random
from typing import Tuple
from ..base.hero import Hero
from ..base.dungeon_character import DungeonCharacter


class Priestess(Hero):
    """
    Priestess hero class - a support character with self-healing abilities.

    Stats:
    - HP: 75 (Lower health pool)
    - Attack Speed: 5 (Moderate attack speed)
    - Hit Chance: 70% (Moderate accuracy)
    - Block Chance: 30% (Good defensive capabilities)
    - Damage: 25-45 (Balanced damage output)

    Special Ability: Healing - Can restore 25-50 HP to herself if not at full health.
    """

    def __init__(self, name: str):
        """
        Initialize priestess with predefined stats.

        Creates a new Priestess character with the given name and sets all
        statistics to their predefined values as specified in the assignment.

        Args:
            name (str): The name of the Priestess character
        """
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

        The Priestess can channel divine energy to heal herself, restoring
        a random amount of hit points. This ability can only be used when
        the Priestess has taken damage (is not at full HP). The opponent
        parameter is not used for this skill but is included to maintain
        a consistent interface with other hero classes.

        Args:
            opponent (DungeonCharacter): Not used for healing skill, included
                                         for interface consistency

        Returns:
            Tuple[bool, str]: A tuple containing:
                - bool: True if healing was successful, False otherwise
                - str: A message describing the outcome of the healing attempt
        """
        if self.hp < self._max_hp:  # Only heal if not at full health
            heal_amount = random.randint(25, 50)
            old_hp = self.hp
            self.hp += heal_amount
            actual_heal = self.hp - old_hp  # Calculate actual amount healed
            return True, f"Healed for {actual_heal} HP!"
        return False, "Already at full health!"

    def __str__(self) -> str:
        """
        Return string representation including class type.

        Extends the base Hero string representation by prefixing
        the class name "Priestess".

        Returns:
            str: String representation of the Priestess character
        """
        return f"Priestess {super().__str__()}"