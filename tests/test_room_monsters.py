import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dungeon.room import Room


def test_room_monsters():
    # Create a test room
    room = Room(sql_room)
    room.visited = True  # So we can see the contents

    print("\n=== Room Monster Test ===")

    # Test monster spawning
    print("\nTesting normal monster spawn (30% chance):")
    for i in range(5):
        test_room = Room(sql_room)
        test_room.spawn_monster()
        if test_room.monster:
            print(f"Spawned: {test_room.monster}")
        else:
            print("No monster spawned")

    # Test forced monster spawn
    print("\nTesting forced monster spawn:")
    room.spawn_monster(force=True)
    print(f"Monster in room: {room.monster}")
    print(f"Room display: {room.get_room_display()}")

    # Test monster death and drops
    print("\nTesting monster death and drops:")
    if room.monster:
        # "Kill" the monster
        room.monster.take_damage(999)
        print(f"Monster dead? {not room.monster.is_alive}")

        # Get drops
        drops = room.clear_monster()
        print(f"Monster dropped: {drops}")
        print(f"Monster still in room? {'Yes' if room.monster else 'No'}")
        print(f"New room display: {room.get_room_display()}")

    # Test entrance/exit protection
    print("\nTesting entrance/exit monster protection:")
    entrance = Room(sql_room)
    entrance.isEntrance = True
    entrance.spawn_monster()
    print(f"Monster at entrance? {'Yes' if entrance.monster else 'No'}")

    exit_room = Room(sql_room)
    exit_room.isExit = True
    exit_room.spawn_monster()
    print(f"Monster at exit? {'Yes' if exit_room.monster else 'No'}")


if __name__ == "__main__":
    test_room_monsters()