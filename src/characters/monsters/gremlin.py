from ..base.monster import Monster


class Gremlin(Monster):
    """Fast attacker with frequent healing but low HP."""

    def __init__(self,
                 hp: int,
                 min_damage: int,
                 max_damage: int,
                 attack_speed: int,
                 hit_chance: float,
                 heal_chance: float,
                 min_heal: int,
                 max_heal: int):
        super().__init__(
            name="Gremlin",
            hp=hp,
            min_damage=min_damage,
            max_damage=max_damage,
            attack_speed=attack_speed,
            hit_chance=hit_chance,
            heal_chance=heal_chance,
            min_heal=min_heal,
            max_heal=max_heal
        )
