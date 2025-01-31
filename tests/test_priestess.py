# tests/test_priestess.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.characters.heroes.priestess import Priestess
from src.characters.base.dungeon_character import DungeonCharacter


def test_priestess_combat():
    # Create our priestess
    priestess = Priestess("Aerith")

    # Create a dummy opponent
    class DummyMonster(DungeonCharacter):
        def __init__(self):
            super().__init__(
                name="Training Dummy",
                hp=100,
                min_damage=20,  # Higher damage to test healing
                max_damage=30,
                attack_speed=2,
                hit_chance=0.8
            )

    dummy = DummyMonster()

    print("\n=== Priestess Combat Test ===")
    print(f"{priestess.name} vs {dummy.name}")
    print(f"\nInitial Status:")
    print(f"{priestess}")
    print(f"{dummy}\n")

    # Test getting damaged first
    print("Dummy attacks priestess!")
    hit, damage = dummy.attack(priestess)
    if hit:
        priestess.take_damage(damage)
        print(f"Hit! Dealt {damage} damage")
        print(f"Priestess HP: {priestess.hp}")

    # Test healing ability
    print("\nPriestess uses healing ability!")
    success, message = priestess.special_skill(dummy)  # dummy param not used for healing
    print(message)
    print(f"Priestess HP after healing: {priestess.hp}")

    # Test healing at full HP
    print("\nTrying to heal at full HP...")
    priestess.hp = 75  # Set to max HP
    success, message = priestess.special_skill(dummy)
    print(message)

    # Test combat abilities
    print("\nTesting Priestess combat abilities:")
    print("Priestess attacks!")
    for i in range(3):  # Test a few attacks
        hit, damage = priestess.attack(dummy)
        if hit:
            print(f"Hit! Dealt {damage} damage")
            print(f"Dummy HP: {dummy.hp}")
        else:
            print("Miss!")

    print("\n=== Final Status ===")
    print(priestess)
    print(dummy)


if __name__ == "__main__":
    test_priestess_combat()