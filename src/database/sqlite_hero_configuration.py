from src.characters.base.hero import Hero
from src.characters.heroes.hero_factory import HeroFactory
from src.database.sqlite_configuration import SqliteConfiguration

class SqliteHeroConfiguration(SqliteConfiguration):

    def __init__(self):
        SqliteConfiguration.__init__(self)
        SqliteConfiguration.open_db(self)

        cursor = self._con.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS hero ("
                       "hero_type TEXT, "
                       "name TEXT, "
                       "hp INTEGER, "
                       "vision_potions INTEGER, "
                       "healing_potions INTEGER, "
                       "pillars TEXT, "
                       "active_vision BOOLEAN, "
                       "loc_x INTEGER, "
                       "loc_y INTEGER)"
                       )
        self._con.commit()
        SqliteConfiguration.close_db(self)

    def save(self, hero: Hero):
        SqliteConfiguration.open_db(self)

        cursor = self._con.cursor()
        cursor.execute(f"DELETE FROM hero")
        hero_type = str(type(hero))
        hero_loc = hero.location if hero.location is not None else (0,0)
        pillars_str = ','.join([str(pillar) for pillar in hero.pillars])
        cursor.execute(f"INSERT INTO hero VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            hero_type,
            hero.name,
            hero.hp,
            hero.vision_potions,
            hero.healing_potions,
            pillars_str,
            hero.active_vision,
            hero_loc[0],
            hero_loc[1]
        ))

        self._con.commit()
        SqliteConfiguration.close_db(self)
        return hero

    def load(self):
        SqliteConfiguration.open_db(self)

        hero = None;

        cursor = self._con.cursor()
        cursor.execute("SELECT * FROM hero")
        row = cursor.fetchone()
        print(row)
        if len(row) > 0:
            hero = HeroFactory.create(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        self._con.commit()
        SqliteConfiguration.close_db(self)
        print(hero.location)
        return hero