from enum import Enum

from src.characters.heroes.priestess import Priestess
from src.characters.heroes.thief import Thief
from src.characters.heroes.warrior import Warrior


class HeroFactory():

    @staticmethod
    def create(
            hero_type: str,
            name: str,
            hp: str,
            vision_potions: int,
            healing_potions: int,
            pillars: str,
            active_vision: bool,
            loc_x: int,
            loc_y: int):

        hero_class_map = {
            HeroTypes.PRIESTESS.value: Priestess,
            HeroTypes.THIEF.value: Thief,
            HeroTypes.WARRIOR.value: Warrior,
        }
        hero_class = hero_class_map[hero_type]

        hero = hero_class(name)
        hero.hp = hp
        hero._vision_potions = vision_potions
        hero._healing_potions = healing_potions
        for pillar in pillars.split(","):
            hero.collect_pillar(pillar)
        hero._active_vision = active_vision
        hero._location = (loc_x, loc_y)
        return hero

class HeroTypes(Enum):
    # Dungeon Table Names

    PRIESTESS = "<class 'src.characters.heroes.priestess.Priestess'>"
    THIEF = "<class 'src.characters.heroes.priestess.Thief'>"
    WARRIOR = "<class 'src.characters.heroes.priestess.Warrior'>"