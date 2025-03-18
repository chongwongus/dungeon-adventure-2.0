import random
from abc import ABC
from .dungeon_character import DungeonCharacter


class Monster(DungeonCharacter, ABC):
    """
    Abstract base class for all monsters in the dungeon adventure game.

    Monsters extend DungeonCharacter with healing capabilities, allowing them
    to potentially recover hit points after taking damage. This class serves
    as the foundation for specific monster types like Ogre, Skeleton, and Gremlin.

    Attributes:
        heal_chance (float): Probability of healing after taking damage
        min_heal (int): Minimum amount of healing when triggered
        max_heal (int): Maximum amount of healing when triggered
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
            name (str): Monster name
            hp (int): Starting/max hit points
            min_damage (int): Minimum damage dealt
            max_damage (int): Maximum damage dealt
            attack_speed (int): Speed determines number of attacks
            hit_chance (float): Probability of landing an attack
            heal_chance (float): Probability of healing after taking damage
            min_heal (int): Minimum healing amount
            max_heal (int): Maximum healing amount
        """
        super().__init__(name, hp, min_damage, max_damage, attack_speed, hit_chance)
        self.heal_chance = heal_chance
        self.min_heal = min_heal
        self.max_heal = max_heal

    def take_damage(self, amount: int) -> int:
        """
        Take damage and possibly heal afterwards.

        Monsters have a chance to heal after taking damage, based on their
        heal_chance attribute. Healing only occurs if the monster remains
        alive after the damage is applied.

        Args:
            amount (int): Amount of damage to take

        Returns:
            int: Amount of healing done (0 if no healing occurred)
        """
        old_hp = self.hp
        super().take_damage(amount)
        damage_taken = old_hp - self.hp

        # Try to heal if still alive
        if self.is_alive and random.random() < self.heal_chance:
            heal_amount = random.randint(self.min_heal, self.max_heal)
            old_hp = self.hp
            self.hp += heal_amount
            actual_heal = self.hp - old_hp
            return actual_heal
        return 0

    def __str__(self) -> str:
        """
        Return string representation including healing stats.

        Extends the base character string representation with
        information about the monster's healing capabilities.

        Returns:
            str: String describing the monster and its healing abilities
        """
        return (f"{super().__str__()} | "
                f"Heal Chance: {self.heal_chance * 100}% | "
                f"Heal Amount: {self.min_heal}-{self.max_heal}")