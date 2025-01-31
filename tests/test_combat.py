import sys
import os
# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.characters.heroes.warrior import Warrior
from src.characters.base.dungeon_character import DungeonCharacter


def test_warrior_combat():
    # Create our warrior
    warrior = Warrior("Conan")

    # Create a dummy opponent (using DungeonCharacter directly for testing)
    class DummyMonster(DungeonCharacter):
        def __init__(self):
            super().__init__(
                name="Training Dummy",
                hp=100,
                min_damage=10,
                max_damage=20,
                attack_speed=2,
                hit_chance=0.6
            )

    dummy = DummyMonster()

    print("\n=== Combat Test ===")
    print(f"{warrior.name} vs {dummy.name}")
    print(f"\nInitial Status:")
    print(f"{warrior}")
    print(f"{dummy}\n")

    # Test regular attack
    hit, damage = warrior.attack(dummy)
    print("\nWarrior attacks!")
    if hit:
        print(f"Hit! Dealt {damage} damage")
    else:
        print("Miss!")
    print(f"Dummy HP: {dummy.hp}")

    # Test special ability
    print("\nWarrior uses Crushing Blow!")
    success, message = warrior.special_skill(dummy)
    print(message)
    print(f"Dummy HP: {dummy.hp}")

    # Test taking damage
    print("\nDummy counterattacks!")
    hit, damage = dummy.attack(warrior)
    if hit:
        print(f"Hit! Dealt {damage} damage")
        if warrior.hp < 100:
            print("Warrior blocked some damage!")
    else:
        print("Miss!")
    print(f"Warrior HP: {warrior.hp}")

    # Test multiple attack rounds to see blocking in action
    print("\n=== Testing Blocking Mechanics ===")
    for i in range(5):  # Test 5 rounds of attacks
        print(f"\nRound {i+1}:")
        print("Dummy attacks warrior!")
        hit, damage = dummy.attack(warrior)
        if hit:
            old_hp = warrior.hp  # Store HP before damage
            blocked = not warrior.take_damage(damage)  # take_damage returns True if damage was taken
            if blocked:
                print(f"BLOCKED! Warrior avoided {damage} damage!")
            else:
                hp_lost = old_hp - warrior.hp
                print(f"Hit! Dealt {hp_lost} damage (Warrior HP: {warrior.hp})")
        else:
            print("Miss!")

    print("\n=== Final Status ===")
    print(warrior)
    print(dummy)



if __name__ == "__main__":
    test_warrior_combat()