# tests/test_blocking.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.characters.heroes.warrior import Warrior
from src.characters.monsters.ogre import Ogre


def test_blocking():
    # Create warrior with known block chance (20%)
    warrior = Warrior("Conan")

    print("\n=== Block Test ===")
    print(f"Initial HP: {warrior.hp}/{warrior._max_hp}")
    print(f"Block Chance: {warrior._block_chance * 100}%")

    # Test blocking multiple times
    damage_amount = 50  # Consistent damage amount for testing
    num_tests = 10

    for i in range(num_tests):
        print(f"\nBlock Test {i + 1}:")
        print(f"HP before: {warrior.hp}")

        # Try to deal damage
        was_blocked = warrior.take_damage(damage_amount)

        print(f"Block successful: {was_blocked}")
        print(f"HP after: {warrior.hp}")
        print(f"Damage taken: {damage_amount if not was_blocked else 0}")

        # Reset HP for next test
        warrior.hp = warrior._max_hp


def test_combat_blocking():
    """Test blocking in actual combat scenario"""
    warrior = Warrior("Conan")
    ogre = Ogre()
    initial_hp = warrior.hp

    print("\n=== Combat Block Test ===")
    print(f"Initial HP: {warrior.hp}")

    # Test ogre attack with manual block check
    _, damage = ogre.attack(warrior)
    print(f"Ogre attempts {damage} damage")

    # Try to block
    was_blocked = warrior.take_damage(damage)

    print(f"Block successful: {was_blocked}")
    print(f"Final HP: {warrior.hp}")
    if was_blocked:
        print("No damage should be taken")
        assert warrior.hp == initial_hp, "HP changed despite successful block!"
    else:
        print(f"Damage taken: {initial_hp - warrior.hp}")


if __name__ == "__main__":
    test_blocking()
    test_combat_blocking()
