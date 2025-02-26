import random
from typing import Tuple
from ..base.hero import Hero
from ..base.dungeon_character import DungeonCharacter


class Thief(Hero):
    """
    Thief hero class - a quick, agile fighter specializing in speed and evasion.

    Stats:
    - HP: 75 (Lower health pool)
    - Attack Speed: 6 (Fastest hero type)
    - Hit Chance: 80% (High accuracy)
    - Block Chance: 40% (Highest evasion)
    - Damage: 20-40 (Lower damage per hit)

    Special Ability: Surprise Attack - A risky maneuver with three possible outcomes:
    - 40% chance: Land two attacks in one turn
    - 20% chance: Get caught and miss the opportunity to attack
    - 40% chance: Perform a normal attack
    """

    def __init__(self, name: str):
        """
        Initialize thief with predefined stats.

        Creates a new Thief character with the given name and sets all
        statistics to their predefined values as specified in the assignment.

        Args:
            name (str): The name of the Thief character
        """
        super().__init__(
            name=name,
            hp=75,
            min_damage=20,
            max_damage=40,
            attack_speed=6,
            hit_chance=0.8,
            block_chance=0.4
        )

    def special_skill(self, opponent: DungeonCharacter) -> Tuple[bool, str]:
        """
        Surprise Attack: A high-risk, high-reward special ability.

        The Thief attempts a sneaky attack with three possible outcomes:
        1. Success (40% chance): The Thief gets two attacks in one turn,
           potentially dealing double damage.
        2. Caught (20% chance): The Thief is detected and fails to attack at all.
        3. Normal (40% chance): The Thief performs a regular attack.

        Each attack within the surprise attack is still subject to the
        Thief's regular hit chance.

        Args:
            opponent (DungeonCharacter): The target of the surprise attack

        Returns:
            Tuple[bool, str]: A tuple containing:
                - bool: True if at least one attack hit, False otherwise
                - str: A message describing the outcome of the surprise attack
        """
        roll = random.random()

        if roll < 0.4:  # 40% chance for bonus attack
            # First attack
            hit1, damage1 = self.attack(opponent)
            # Bonus attack
            hit2, damage2 = self.attack(opponent)

            if hit1 or hit2:
                message = []
                if hit1:
                    message.append(f"First strike hits for {damage1}")
                if hit2:
                    message.append(f"Bonus strike hits for {damage2}")
                return True, "Surprise Attack! " + " and ".join(message) + "!"
            return False, "Surprise Attack misses completely!"

        elif roll < 0.6:  # 20% chance to get caught
            return False, "Got caught attempting Surprise Attack!"

        else:  # 40% chance for normal attack
            hit, damage = self.attack(opponent)
            if hit:
                return True, f"Normal attack hits for {damage} damage!"
            return False, "Attack misses!"

    def __str__(self) -> str:
        """
        Return string representation including class type.

        Extends the base Hero string representation by prefixing
        the class name "Thief".

        Returns:
            str: String representation of the Thief character
        """
        return f"Thief {super().__str__()}"