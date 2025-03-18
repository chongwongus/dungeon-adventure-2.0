from src.characters.base.hero import Hero
from src.dungeon.dungeon import Dungeon

class GameData:

    def __init__(self, dungeon: Dungeon, hero: Hero):
        self.dungeon = dungeon
        self.hero = hero