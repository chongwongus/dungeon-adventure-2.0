from ..base.monster import Monster


class Skeleton(Monster):
    """Balanced monster with moderate stats."""

    def __init__(self):
        super().__init__(
            name="Skeleton",
            hp=100,
            min_damage=30,
            max_damage=50,
            attack_speed=3,
            hit_chance=0.8,
            heal_chance=0.3,
            min_heal=30,
            max_heal=50
        )
