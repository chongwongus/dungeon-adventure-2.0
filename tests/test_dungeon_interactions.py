import unittest
from src.dungeon.dungeon import Dungeon
from src.dungeon.room import Room
from src.characters.heroes.warrior import Warrior
from src.characters.monsters.ogre import Ogre


class TestDungeonInteractions(unittest.TestCase):
    def setUp(self):
        """Set up a test dungeon and hero."""
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

    def test_vision_potion(self):
        """Test vision potion revealing adjacent rooms."""
        # Set up rooms around entrance
        x, y = self.dungeon.entrance
        current_room = self.dungeon.get_room(x, y)
        current_room.doors['E'] = True

        # Set up connecting room
        next_room = self.dungeon.get_room(x + 1, y)
        next_room.doors['W'] = True  # Add connecting door

        # Set hero's vision potion state
        self.hero.active_vision = True

        # Move to trigger vision potion
        success, messages, _ = self.dungeon.move_hero(self.hero, 'E')
        self.assertTrue(success)

        # Check that adjacent rooms are revealed
        for dx, dy in [(0, 1), (1, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            new_x, new_y = x + dx + 1, y + dy  # +1 to x because we moved east
            if 0 <= new_x < self.dungeon.size[0] and 0 <= new_y < self.dungeon.size[1]:
                room = self.dungeon.get_room(new_x, new_y)
                self.assertTrue(room.visited, f"Room at ({new_x}, {new_y}) should be visited")

        # Vision effect should be consumed
        self.assertFalse(self.hero.active_vision)

    def test_combat_initiation(self):
        """Test that entering a room with monster initiates combat."""
        # Set up room with monster
        x, y = self.dungeon.entrance
        room = self.dungeon.get_room(x, y)
        room.doors['E'] = True

        next_room = self.dungeon.get_room(x + 1, y)
        next_room.doors['W'] = True
        next_room.monster = Ogre()

        # Move into monster room
        success, messages, combat = self.dungeon.move_hero(self.hero, 'E')
        self.assertTrue(success)
        self.assertIsNotNone(combat)
        self.assertIn("encounter", " ".join(messages).lower())

    def test_complete_dungeon_run(self):
        """Test a complete dungeon run with multiple interactions."""
        # Set up a path with various interactions
        path = [
            ((0, 0), 'E', {'hasHealthPot': True}),
            ((1, 0), 'E', {'monster': Ogre()}),
            ((2, 0), 'S', {'hasPillar': True, 'pillarType': Room.PILLARS[0]}),
            ((2, 1), 'W', {'hasVisionPot': True}),
        ]

        # Set up the rooms
        for (x, y), direction, contents in path:
            room = self.dungeon.get_room(x, y)
            room.doors[direction] = True
            next_x, next_y = x, y
            if direction == 'E':
                next_x += 1
            elif direction == 'W':
                next_x -= 1
            elif direction == 'S':
                next_y += 1
            elif direction == 'N':
                next_y -= 1

            next_room = self.dungeon.get_room(next_x, next_y)
            opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
            next_room.doors[opposite[direction]] = True

            # Set up room contents
            for attr, value in contents.items():
                setattr(next_room, attr, value)

        # Follow the path and check interactions
        expected_events = [
            "healing potion",
            "encounter",
            "pillar",
            "vision potion"
        ]

        for (x, y), direction, _ in path:
            success, messages, combat = self.dungeon.move_hero(self.hero, direction)
            self.assertTrue(success)
            message_text = " ".join(messages).lower()
            self.assertTrue(any(event in message_text for event in expected_events))

    def test_winning_condition(self):
        """Test that collecting all pillars triggers winning condition message."""
        x, y = self.dungeon.entrance
        room = self.dungeon.get_room(x, y)
        room.doors['E'] = True

        next_room = self.dungeon.get_room(x + 1, y)
        next_room.doors['W'] = True

        # Add all pillars to one room for testing
        for pillar in Room.PILLARS:
            self.hero.collect_pillar(pillar)

        # One more pillar should trigger win condition
        next_room.hasPillar = True
        next_room.pillarType = Room.PILLARS[0]  # This won't actually be collected due to check

        success, messages, _ = self.dungeon.move_hero(self.hero, 'E')
        self.assertTrue(success)
        self.assertTrue(any("all the pillars" in msg.lower() for msg in messages))


if __name__ == '__main__':
    unittest.main()