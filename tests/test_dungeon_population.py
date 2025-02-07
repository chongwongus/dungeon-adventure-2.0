import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dungeon.dfs_factory import DFSDungeonFactory
from src.dungeon.easy_factory import EasyDungeonFactory


def count_room_contents(dungeon):
    """Helper function to count what's in the dungeon."""
    stats = {
        'monsters': 0,
        'health_potions': 0,
        'vision_potions': 0,
        'pits': 0,
        'pillars': 0
    }

    # Check all rooms
    for y in range(dungeon.size[1]):
        for x in range(dungeon.size[0]):
            room = dungeon.get_room(x, y)
            if room.monster:
                stats['monsters'] += 1
            if room.hasHealthPot:
                stats['health_potions'] += 1
            if room.hasVisionPot:
                stats['vision_potions'] += 1
            if room.hasPit:
                stats['pits'] += 1
            if room.hasPillar:
                stats['pillars'] += 1

    return stats


def test_dungeon_population():
    # Test both factory types
    factories = {
        "DFS": DFSDungeonFactory(),
        "Easy": EasyDungeonFactory()
    }

    size = (8, 8)  # 64 rooms total

    print("\n=== Dungeon Population Test ===")

    for factory_name, factory in factories.items():
        print(f"\nTesting {factory_name} Factory:")

        # Create dungeon
        dungeon = factory.create(size)

        # Count contents
        stats = count_room_contents(dungeon)

        # Display results
        print(f"In a {size[0]}x{size[1]} dungeon:")
        print(f"Monsters: {stats['monsters']}")
        print(f"Health Potions: {stats['health_potions']}")
        print(f"Vision Potions: {stats['vision_potions']}")
        print(f"Pits: {stats['pits']}")
        print(f"Pillars: {stats['pillars']}")

        # Verify important properties
        assert stats['pillars'] == 4, "Must have exactly 4 pillars"
        assert dungeon.entrance is not None, "Must have an entrance"
        assert dungeon.exit is not None, "Must have an exit"

        # Print a few sample rooms
        print("\nSample Rooms:")
        for y in range(min(3, size[1])):
            for x in range(min(3, size[0])):
                room = dungeon.get_room(x, y)
                room.visited = True  # So we can see contents
                print(f"\nRoom ({x}, {y}):")
                print(str(room))
                if room.monster:
                    print(f"Contains: {room.monster}")


if __name__ == "__main__":
    test_dungeon_population()