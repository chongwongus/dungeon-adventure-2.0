from ..base.monster import Monster


class Ogre(Monster):
    """High HP tank with strong attacks but slow and rarely heals."""

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
            name="Ogre",
            hp=hp,
            min_damage=min_damage,
            max_damage=max_damage,
            attack_speed=attack_speed,
            hit_chance=hit_chance,
            heal_chance=heal_chance,
            min_heal=min_heal,
            max_heal=max_heal
        )