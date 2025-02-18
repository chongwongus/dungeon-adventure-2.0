import unittest
from src.dungeon.dungeon import Dungeon
from src.dungeon.room import Room
from src.characters.heroes.warrior import Warrior


class TestMovementSystem(unittest.TestCase):
    def setUp(self):
        """Set up a test dungeon and hero."""
        # Create a small test dungeon
        self.dungeon = Dungeon(size=(4, 4))

        # Manually initialize maze
        self.dungeon.maze = []
        for y in range(4):
            row = []
            for x in range(4):
                row.append(Room())
            self.dungeon.maze.append(row)

        # Set entrance and exit
        self.dungeon.entrance = (0, 0)
        self.dungeon.exit = (3, 3)
        self.dungeon.maze[0][0].isEntrance = True
        self.dungeon.maze[3][3].isExit = True

        # Create hero
        self.hero = Warrior("TestHero")
        self.hero.location = self.dungeon.entrance

    def test_basic_movement(self):
        """Test basic movement in valid direction."""
        # Set up a simple path: entrance -> (1,0)
        x, y = self.dungeon.entrance
        room = self.dungeon.get_room(x, y)
        room.doors['E'] = True
        next_room = self.dungeon.get_room(x + 1, y)
        next_room.doors['W'] = True

        # Try moving east
        success = self.dungeon.move_hero(self.hero, 'E')
        self.assertTrue(success)
        self.assertEqual(self.hero.location, (1, 0))
        self.assertTrue(next_room.visited)

    def test_invalid_movement(self):
        """Test movement through walls."""
        x, y = self.dungeon.entrance
        room = self.dungeon.get_room(x, y)

        # Try moving east with no door
        room.doors['E'] = False
        success = self.dungeon.move_hero(self.hero, 'E')
        self.assertFalse(success)
        self.assertEqual(self.hero.location, (0, 0))

    def test_pit_damage(self):
        """Test pit damage when entering room."""
        # Set up path to pit
        x, y = self.dungeon.entrance
        room = self.dungeon.get_room(x, y)
        room.doors['E'] = True

        next_room = self.dungeon.get_room(x + 1, y)
        next_room.doors['W'] = True
        next_room.hasPit = True

        # Record initial HP and simulate damage
        initial_hp = self.hero.hp

        # Move into pit room
        success = self.dungeon.move_hero(self.hero, 'E')
        self.assertTrue(success)
        # Hero should take between 10-20 damage from pit
        self.assertGreaterEqual(initial_hp - self.hero.hp, 10)
        self.assertLessEqual(initial_hp - self.hero.hp, 20)

    def test_potion_collection(self):
        """Test collecting potions from room."""
        # Set up path to potion
        x, y = self.dungeon.entrance
        room = self.dungeon.get_room(x, y)
        room.doors['E'] = True

        next_room = self.dungeon.get_room(x + 1, y)
        next_room.doors['W'] = True
        next_room.hasHealthPot = True

        # Record initial potions
        initial_potions = self.hero.healing_potions

        # Move into potion room
        success = self.dungeon.move_hero(self.hero, 'E')
        self.assertTrue(success)
        self.assertEqual(self.hero.healing_potions, initial_potions + 1)
        self.assertFalse(next_room.hasHealthPot)  # Potion should be gone

    def test_boundary_movement(self):
        """Test movement at dungeon boundaries."""
        # Try moving west from entrance (0,0)
        success = self.dungeon.move_hero(self.hero, 'W')
        self.assertFalse(success)
        self.assertEqual(self.hero.location, (0, 0))

        # Move to bottom-right corner and try moving beyond
        self.hero.location = (3, 3)
        success = self.dungeon.move_hero(self.hero, 'E')
        self.assertFalse(success)
        self.assertEqual(self.hero.location, (3, 3))


if __name__ == '__main__':
    unittest.main()