import unittest

from src.characters.heroes.priestess import Priestess
from src.database.sqlite_hero_configuration import SqliteHeroConfiguration

class TestSqliteHeroConfiguration(unittest.TestCase):

    def setUp(self):
        self.config = SqliteHeroConfiguration()
        self.config.__init__()

    def test_save_creates_tables_and_inserts_data(self):
        hero = Priestess("test")
        hero.collect_pillar('I')
        hero.collect_pillar('P')
        hero.collect_potion("healing")
        hero.collect_potion("healing")
        hero.collect_potion("vision")
        self.config.save(hero)
        sql_hero = self.config.load()

        self.assertEqual(sql_hero.name, hero.name)
        self.assertEqual(sql_hero.hp, hero.hp)
        self.assertEqual(sql_hero.pillars, hero.pillars)
        self.assertEqual(sql_hero.healing_potions, hero.healing_potions)
        self.assertEqual(sql_hero.vision_potions, hero.vision_potions)
        self.assertEqual(sql_hero.location, hero.location)
        self.assertEqual(type(sql_hero), type(hero))



if __name__ == '__main__':
    unittest.main()