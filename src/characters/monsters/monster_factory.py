from src.characters.monsters.dragon import Dragon
from src.characters.monsters.gremlin import Gremlin
from src.characters.monsters.ogre import Ogre
from src.characters.monsters.skeleton import Skeleton


class MonsterFactory():

    @staticmethod
    def create_monster(name: str,
                       hp: int,
                       min_damage: int,
                       max_damage: int,
                       attack_speed: int,
                       hit_chance: float,
                       heal_chance: float,
                       max_heal: int,
                       min_heal: int):
        monsters = {
            "gremlin": Gremlin(hp, min_damage,max_damage,attack_speed,hit_chance,heal_chance,min_heal,max_heal),
            "ogre": Ogre(hp, min_damage,max_damage,attack_speed,hit_chance,heal_chance,min_heal,max_heal),
            "skeleton": Skeleton(hp, min_damage,max_damage,attack_speed,hit_chance,heal_chance,min_heal,max_heal),
            "dragon": Dragon(hp, min_damage,max_damage,attack_speed,hit_chance,heal_chance,min_heal,max_heal),
        }
        monster = monsters[name.lower()]
        
        setattr(monster, 'hp', hp)
        setattr(monster, 'min_damage', min_damage)
        setattr(monster, 'max_damage', max_damage)
        setattr(monster, 'attack_speed', attack_speed)
        setattr(monster, 'hit_chance', hit_chance)
        setattr(monster, 'heal_chance', heal_chance)
        setattr(monster, 'max_heal', max_heal)
        setattr(monster, 'min_heal', min_heal)
        return monster
        