import sys
import os
import time
from typing import List, Tuple, Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.characters.heroes.warrior import Warrior
from src.characters.heroes.priestess import Priestess
from src.characters.heroes.thief import Thief
from src.characters.monsters.ogre import Ogre
from src.characters.monsters.skeleton import Skeleton
from src.characters.monsters.gremlin import Gremlin
from src.combat.combat_system import CombatSystem
from src.combat.combat_logger import CombatLogger


def display_combat_header(hero_name: str, monster_name: str):
    """
    Create a visually appealing header for the combat demonstration.

    This function generates an ASCII-art style header that displays
    the combatants' names, providing a dramatic introduction to the fight.

    The header helps create a narrative context for the combat,
    making the demonstration more engaging and immersive.

    Args:
        hero_name (str): Name of the hero character
        monster_name (str): Name of the monster character
    """
    print("\n" + "=" * 60)
    print(f"⚔️  {hero_name} vs {monster_name} ⚔️".center(60))
    print("=" * 60 + "\n")


def display_stats(hero, monster):
    """
    Visualize the current health status of both combatants.

    Creates a graphical representation of health points using block characters:
    - Filled blocks (█) represent current health
    - Empty blocks (░) represent missing health
    - Displays exact HP values

    This visualization provides an intuitive way to track
    the combat progress and current health status.

    Args:
        hero: The player character
        monster: The opponent character
    """
    print(f"\n{hero.name}:")
    print(
        f"HP: {'█' * int(20 * hero.hp / hero._max_hp)}{'░' * int(20 * (1 - hero.hp / hero._max_hp))} {hero.hp}/{hero._max_hp}")
    print(f"{monster.name}:")
    print(
        f"HP: {'█' * int(20 * monster.hp / monster._max_hp)}{'░' * int(20 * (1 - monster.hp / monster._max_hp))} {monster.hp}/{monster._max_hp}\n")


def demonstrate_combat(hero, monster, rounds: int = 5, use_special_every: int = 3):
    """
    Simulate a complete combat encounter between a hero and a monster.

    This comprehensive demonstration function:
    - Displays initial combat setup
    - Executes combat rounds with optional special ability usage
    - Provides round-by-round combat reporting
    - Tracks and displays combat progress
    - Determines and announces the victor

    The function allows customization of:
    - Total number of combat rounds
    - Frequency of special ability usage

    Args:
        hero: The player character
        monster: The opponent character
        rounds (int, optional): Maximum number of combat rounds. Defaults to 5.
        use_special_every (int, optional): Frequency of special ability usage. Defaults to 3.
    """
    display_combat_header(hero.name, monster.name)

    print(f"Initial Status:")
    display_stats(hero, monster)

    combat = CombatSystem(hero, monster)
    round_num = 1

    while not combat.is_combat_over() and round_num <= rounds:
        print(f"\nRound {round_num}:")
        print("-" * 30)

        # Decide if using special ability this round
        use_special = (round_num % use_special_every == 0)
        if use_special:
            print(f"🌟 {hero.name} prepares to use their special ability!")

        # Execute round and display results
        result = combat.execute_round(use_special)
        messages = CombatLogger.format_round_result(result)

        # Display action messages with slight delay for readability
        for msg in messages:
            if msg.strip():  # Only print non-empty messages
                print(msg)
                time.sleep(0.2)  # Small delay between messages

        display_stats(hero, monster)
        round_num += 1

        if combat.is_combat_over():
            victor = combat.get_victor()
            print("\n" + "=" * 60)
            print(f"Combat Ended! {victor.name} is victorious!")
            print("=" * 60 + "\n")
            break

        time.sleep(0.5)  # Pause between rounds


def test_demonstrate_all_combinations():
    """
    Demonstrate combat scenarios for all hero types against different monsters.

    This function creates a comprehensive showcase of:
    - Warrior's high-health, high-damage approach (vs Ogre)
    - Priestess's healing and sustain capabilities (vs Skeleton)
    - Thief's speed and surprise attack mechanics (vs Gremlin)

    Provides a holistic view of how different hero types interact
    with various monster types, highlighting the nuanced combat system.
    """
    heroes = [
        Warrior("Conan"),
        Priestess("Aerith"),
        Thief("Edwin")
    ]

    monsters = [
        Ogre(),
        Skeleton(),
        Gremlin()
    ]

    # Show one combat for each hero type
    for hero in heroes:
        # Pick a monster that shows off the hero's strengths
        if isinstance(hero, Warrior):
            # Warrior vs Ogre - tank battle
            demonstrate_combat(hero, Ogre())
        elif isinstance(hero, Priestess):
            # Priestess vs Skeleton - healing helps with sustained damage
            demonstrate_combat(hero, Skeleton())
        elif isinstance(hero, Thief):
            # Thief vs Gremlin - speed vs speed
            demonstrate_combat(hero, Gremlin())


def test_epic_battle():
    """
    Stage an extended, high-stakes battle between a Warrior and an Ogre.

    Creates a prolonged combat scenario that:
    - Demonstrates sustained combat mechanics
    - Showcases Warrior's Crushing Blow ability
    - Explores combat dynamics over multiple rounds
    - Highlights the epic nature of dungeon combat

    Features a longer battle with more frequent special ability usage.
    """
    hero = Warrior("Conan")
    monster = Ogre()

    # Make it a bit more epic by increasing HP
    hero.hp = hero._max_hp
    monster.hp = monster._max_hp

    demonstrate_combat(hero, monster, rounds=10, use_special_every=2)


def test_healing_battle():
    """
    Showcase the Priestess's healing mechanics in an extended combat.

    Demonstrates the Priestess class by:
    - Starting with reduced health
    - Highlighting the healing special ability
    - Showing how healing can turn the tide of battle
    - Exploring sustainability in combat

    Provides insight into the support-oriented playstyle of the Priestess.
    """
    hero = Priestess("Aerith")
    monster = Skeleton()

    # Start priestess at lower HP to demonstrate healing
    hero.hp = hero._max_hp // 2

    demonstrate_combat(hero, monster, rounds=8, use_special_every=2)


def test_speed_battle():
    """
    Illustrate a fast-paced combat between quick characters.

    Features a battle between:
    - Thief (high speed, surprise attack)
    - Gremlin (rapid, low-health monster)

    Demonstrates:
    - Impact of attack speed
    - Importance of quick, decisive actions
    - Unique mechanics of fast-moving combatants
    """
    hero = Thief("Edwin")
    monster = Gremlin()

    demonstrate_combat(hero, monster, rounds=6, use_special_every=2)


if __name__ == "__main__":
    print("\n🎮 Welcome to the Dungeon Combat Demonstration! 🎮\n")

    while True:
        print("\nSelect a demo to run:")
        print("1. Show all hero types in combat")
        print("2. Epic Warrior vs Ogre battle")
        print("3. Healing-focused Priestess battle")
        print("4. Fast-paced Thief battle")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            test_demonstrate_all_combinations()
        elif choice == "2":
            test_epic_battle()
        elif choice == "3":
            test_healing_battle()
        elif choice == "4":
            test_speed_battle()
        elif choice == "5":
            print("\nThanks for watching the combat demos!\n")
            break
        else:
            print("\nInvalid choice. Please try again.")

        input("\nPress Enter to continue...")