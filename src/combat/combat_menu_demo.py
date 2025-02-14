"""Interactive demo for combat menu system"""
from src.characters.heroes.warrior import Warrior
from src.characters.heroes.priestess import Priestess
from src.characters.heroes.thief import Thief
from src.characters.monsters.ogre import Ogre
from src.characters.monsters.skeleton import Skeleton
from src.characters.monsters.gremlin import Gremlin
from src.combat.combat_system import CombatSystem
from src.combat.combat_menu import CombatMenu


def demo_combat():
    """Run an interactive combat demo"""
    print("\nWelcome to the Combat Demo!")
    print("\nChoose your hero:")
    print("1. Warrior (High HP, Crushing Blow ability)")
    print("2. Priestess (Healing ability)")
    print("3. Thief (Fast attacks, Surprise Attack ability)")

    while True:
        choice = input("\nEnter choice (1-3): ")
        if choice == "1":
            hero = Warrior("Conan")
            break
        elif choice == "2":
            hero = Priestess("Aerith")
            break
        elif choice == "3":
            hero = Thief("Edwin")
            break
        else:
            print("Invalid choice!")

    print("\nChoose your opponent:")
    print("1. Ogre (High HP, slow)")
    print("2. Skeleton (Balanced)")
    print("3. Gremlin (Fast, low HP)")

    while True:
        choice = input("\nEnter choice (1-3): ")
        if choice == "1":
            monster = Ogre()
            break
        elif choice == "2":
            monster = Skeleton()
            break
        elif choice == "3":
            monster = Gremlin()
            break
        else:
            print("Invalid choice!")

    # Give the hero some potions for testing
    hero.collect_potion("healing")
    hero.collect_potion("healing")

    # Start combat
    combat_system = CombatSystem(hero, monster)
    menu = CombatMenu(combat_system)
    menu.start_combat()


if __name__ == "__main__":
    demo_combat()