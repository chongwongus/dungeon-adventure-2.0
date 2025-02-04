from ..base.monster import Monster


class Gremlin(Monster):
    """Fast attacker with frequent healing but low HP."""

    def __init__(self):
        super().__init__(
            name="Gremlin",
            hp=70,
            min_damage=15,
            max_damage=30,
            attack_speed=5,
            hit_chance=0.8,
            heal_chance=0.4,
            min_heal=20,
            max_heal=40
        )
