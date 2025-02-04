import random
from typing import Tuple
from ..base.hero import Hero
from ..base.dungeon_character import DungeonCharacter


class Thief(Hero):
    """
    Thief hero class - quick fighter with surprise attack ability.

    Stats:
    - HP: 75
    - Attack Speed: 6
    - Hit Chance: 80%
    - Block Chance: 40%
    - Damage: 20-40
    """

    def __init__(self, name: str):
        """Initialize thief with predefined stats."""
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
        Surprise Attack:
        - 40% chance: Get an extra attack
        - 20% chance: Get caught (no attack)
        - 40% chance: Normal attack

        Returns:
            Tuple of (success, message)
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
        """Return string representation including class type."""
        return f"Thief {super().__str__()}"
