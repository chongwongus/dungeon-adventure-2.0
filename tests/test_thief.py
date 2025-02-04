import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.characters.heroes.thief import Thief
from src.characters.base.dungeon_character import DungeonCharacter


def test_thief_combat():
    # Create our thief
    thief = Thief("Garrett")

    # Create a dummy opponent
    class DummyMonster(DungeonCharacter):
        def __init__(self):
            super().__init__(
                name="Training Dummy",
                hp=100,
                min_damage=15,
                max_damage=25,
                attack_speed=2,
                hit_chance=0.7
            )

    dummy = DummyMonster()

    print("\n=== Thief Combat Test ===")
    print(f"{thief.name} vs {dummy.name}")
    print(f"\nInitial Status:")
    print(f"{thief}")
    print(f"{dummy}\n")

    # Test multiple surprise attacks to see different outcomes
    print("Testing Surprise Attack multiple times:")
    for i in range(5):
        print(f"\nAttempt {i+1}:")
        success, message = thief.special_skill(dummy)
        print(message)
        print(f"Dummy HP: {dummy.hp}")

    # Test blocking
    print("\nTesting Thief's blocking (40% chance):")
    old_hp = thief.hp
    for i in range(3):
        print(f"\nDummy attacks thief!")
        hit, damage = dummy.attack(thief)
        if hit:
            blocked = not thief.take_damage(damage)
            if blocked:
                print(f"BLOCKED! Thief avoided {damage} damage!")
            else:
                damage_taken = old_hp - thief.hp
                print(f"Hit! Thief took {damage_taken} damage")
                old_hp = thief.hp
        else:
            print("Miss!")
        print(f"Thief HP: {thief.hp}")

    print("\n=== Final Status ===")
    print(thief)
    print(dummy)


if __name__ == "__main__":
    test_thief_combat()