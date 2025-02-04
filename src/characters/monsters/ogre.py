from ..base.monster import Monster


class Ogre(Monster):
    """High HP tank with strong attacks but slow and rarely heals."""

    def __init__(self):
        super().__init__(
            name="Ogre",
            hp=200,
            min_damage=30,
            max_damage=60,
            attack_speed=2,
            hit_chance=0.6,
            heal_chance=0.1,
            min_heal=30,
            max_heal=60
        )