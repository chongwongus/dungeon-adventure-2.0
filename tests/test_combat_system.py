import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.characters.heroes.warrior import Warrior
from src.characters.heroes.priestess import Priestess
from src.characters.heroes.thief import Thief

from src.characters.monsters.ogre import Ogre
from src.characters.monsters.skeleton import Skeleton
from src.characters.monsters.gremlin import Gremlin
from src.combat.combat_system import CombatSystem


def test_combat_warrior():
    # Create combatants
    warrior = Warrior("Conan")
    ogre = Ogre()

    print("\n=== Combat Test ===")
    print(f"{warrior.name} vs {ogre.name}")
    print(f"\nInitial Status:")
    print(f"{warrior}")
    print(f"{ogre}\n")

    # Create combat system
    combat = CombatSystem(warrior, ogre)

    # Test a few rounds of combat
    round_num = 1
    while not combat.is_combat_over():
        print(f"\nRound {round_num}:")

        # Every third round, use special ability
        use_special = (round_num % 3 == 0)
        if use_special:
            print(f"{warrior.name} attempts Crushing Blow!")

        # Execute round and show results
        messages = combat.execute_round(use_special)
        for msg in messages:
            print(msg)

        round_num += 1

        # Optional: break after certain number of rounds
        if round_num > 5:
            break

    print("\n=== Combat Ended ===")
    victor = combat.get_victor()
    if victor:
        print(f"{victor.name} is victorious!")
    else:
        print("Combat continues...")


def test_combat_priestess():
    # Create combatants
    priestess = Priestess("Aerith")
    skeleton = Skeleton()

    print("\n=== Priestess Combat Test ===")
    print(f"{priestess.name} vs {skeleton.name}")
    print(f"\nInitial Status:")
    print(f"{priestess}")
    print(f"{skeleton}\n")

    # Create combat system
    combat = CombatSystem(priestess, skeleton)

    # Test a few rounds of combat
    round_num = 1
    while not combat.is_combat_over():
        print(f"\nRound {round_num}:")

        # Use healing every other round when below 75% health
        use_special = (round_num % 2 == 0 and priestess.hp < 60)
        if use_special:
            print(f"{priestess.name} attempts to heal!")

        # Execute round and show results
        messages = combat.execute_round(use_special)
        for msg in messages:
            print(msg)

        round_num += 1

        # Optional: break after certain number of rounds
        if round_num > 5:
            break

        print("\n=== Combat Ended ===")
        victor = combat.get_victor()
        if victor:
            print(f"{victor.name} is victorious!")
        else:
            print("Combat continues...")


def test_combat_thief():
    # Create combatants
    thief = Thief("Garrett")
    gremlin = Gremlin()  # Gremlin has less HP but is faster

    print("\n=== Thief Combat Test ===")
    print(f"{thief.name} vs {gremlin.name}")
    print(f"\nInitial Status:")
    print(f"{thief}")
    print(f"{gremlin}\n")

    # Create combat system
    combat = CombatSystem(thief, gremlin)

    # Test a few rounds of combat
    round_num = 1
    while not combat.is_combat_over():
        print(f"\nRound {round_num}:")

        # Try surprise attack every other round
        use_special = (round_num % 2 == 0)
        if use_special:
            print(f"{thief.name} attempts Surprise Attack!")

        # Execute round and show results
        messages = combat.execute_round(use_special)
        for msg in messages:
            print(msg)

        round_num += 1

        # Optional: break after certain number of rounds
        if round_num > 5:
            break

        print("\n=== Combat Ended ===")
        victor = combat.get_victor()
        if victor:
            print(f"{victor.name} is victorious!")
        else:
            print("Combat continues...")


if __name__ == "__main__":
    print("Testing Warrior\n")
    test_combat_warrior()
    print("\n\nTesting Priest\n")
    test_combat_priestess()
    print("\n\nTesting Thief\n")
    test_combat_thief()