import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.characters.monsters.ogre import Ogre
from src.characters.monsters.gremlin import Gremlin
from src.characters.monsters.skeleton import Skeleton
from src.characters.heroes.warrior import Warrior  # For testing against


def test_monster_combat():
    # Create our monsters
    ogre = Ogre()
    gremlin = Gremlin()
    skeleton = Skeleton()

    # Create a warrior to fight them
    warrior = Warrior("Test Warrior")

    print("\n=== Monster Combat Test ===")

    # Test Ogre (tank)
    print("\nTesting Ogre:")
    print(f"Initial Status: {ogre}")
    for i in range(3):
        damage = 50  # Consistent damage for testing
        heal = ogre.take_damage(damage)
        print(f"Took {damage} damage", end=" ")
        if heal:
            print(f"and healed for {heal}!")
        else:
            print("(no healing)")
        print(f"Ogre HP: {ogre.hp}")

    # Test Gremlin (frequent healer)
    print("\nTesting Gremlin:")
    print(f"Initial Status: {gremlin}")
    for i in range(3):
        damage = 20  # Less damage since Gremlin has less HP
        heal = gremlin.take_damage(damage)
        print(f"Took {damage} damage", end=" ")
        if heal:
            print(f"and healed for {heal}!")
        else:
            print("(no healing)")
        print(f"Gremlin HP: {gremlin.hp}")

    # Test Skeleton (balanced)
    print("\nTesting Skeleton:")
    print(f"Initial Status: {skeleton}")
    for i in range(3):
        damage = 35  # Medium damage
        heal = skeleton.take_damage(damage)
        print(f"Took {damage} damage", end=" ")
        if heal:
            print(f"and healed for {heal}!")
        else:
            print("(no healing)")
        print(f"Skeleton HP: {skeleton.hp}")

    # Test speed-based attacks
    print("\nTesting Attack Speeds:")
    for monster in [ogre, gremlin, skeleton]:
        attacks = monster.get_num_attacks(warrior)
        print(f"{monster.name} gets {attacks} attacks per round against the warrior")

        # Test those attacks
        print(f"Example round from {monster.name}:")
        total_damage = 0
        for _ in range(attacks):
            hit, damage = monster.attack(warrior)
            if hit:
                print(f"Hit for {damage} damage!")
                total_damage += damage
            else:
                print("Miss!")
        print(f"Total damage dealt: {total_damage}\n")


if __name__ == "__main__":
    test_monster_combat()
