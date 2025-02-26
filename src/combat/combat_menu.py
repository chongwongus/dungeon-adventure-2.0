from typing import List, Optional
from .combat_system import CombatSystem
from .combat_logger import CombatLogger


class CombatMenu:
    """
    Manages turn-based combat interactions and player choices.

    Provides an interactive interface for combat, allowing players to:
    - View current combat status
    - Choose combat actions
    - Use healing potions
    - Attempt to escape
    - Execute selected actions

    Attributes:
        combat (CombatSystem): Underlying combat system managing combat logic
        hero (Hero): Player's character
        monster (Monster): Current opponent
    """

    def __init__(self, combat_system: CombatSystem):
        self.combat = combat_system
        self.hero = combat_system.hero
        self.monster = combat_system.monster

    def display_status(self) -> None:
        """
        Display the current combat status for hero and monster.

        Shows:
        - Character names
        - Health points (with visual health bar)
        - Available potions
        """
        print("\nCurrent Status:")
        print(f"{self.hero.name}:")
        print(
            f"HP: {'█' * int(20 * self.hero.hp / self.hero._max_hp)}{'░' * int(20 * (1 - self.hero.hp / self.hero._max_hp))} {self.hero.hp}/{self.hero._max_hp}")
        print(f"Potions: {self.hero.healing_potions}")
        print(f"\n{self.monster.name}:")
        print(
            f"HP: {'█' * int(20 * self.monster.hp / self.monster._max_hp)}{'░' * int(20 * (1 - self.monster.hp / self.monster._max_hp))} {self.monster.hp}/{self.monster._max_hp}\n")

    def display_menu(self) -> None:
        """
        Display available combat action options to the player.

        Shows numbered menu of actions:
        1. Attack
        2. Special Attack
        3. Use Healing Potion
        4. Try to Run
        5. View Status
        """
        print("\nWhat would you like to do?")
        print("1. Attack")
        print("2. Special Attack")
        print("3. Use Healing Potion")
        print("4. Try to Run")
        print("5. View Status")

    def handle_choice(self, choice: str) -> Optional[List[str]]:
        """
        Process the player's selected combat action.

        Handles different action types:
        - Regular attack
        - Special attack
        - Healing potion use
        - Escape attempt
        - Status viewing

        Args:
            choice (str): Player's selected menu option

        Returns:
            Optional list of combat messages or None for status view
        """
        if choice == "1":  # Regular attack
            result = self.combat.execute_round(use_special=False)
            return CombatLogger.format_round_result(result)

        elif choice == "2":  # Special attack
            result = self.combat.execute_round(use_special=True)
            return CombatLogger.format_round_result(result)

        elif choice == "3":  # Use potion
            if self.hero.healing_potions > 0:
                heal_amount = self.hero.use_healing_potion()
                if heal_amount:
                    print(f"\nUsed a healing potion and recovered {heal_amount} HP!")
                    # Monster still gets their turn
                    result = self.combat.execute_round(monster_only=True)
                    return CombatLogger.format_round_result(result)
            else:
                print("\nNo healing potions remaining!")
            return None

        elif choice == "4":  # Try to run
            escape_chance = 0.4  # 40% chance to escape
            import random
            if random.random() < escape_chance:
                print("\nSuccessfully escaped from combat!")
                return ["Escaped from combat!"]
            else:
                print("\nFailed to escape!")
                # Monster gets free attack
                result = self.combat.execute_round(monster_only=True)
                return CombatLogger.format_round_result(result)

        elif choice == "5":  # View status
            self.display_status()
            return None

        else:
            print("\nInvalid choice!")
            return None

    def start_combat(self) -> None:
        """
        Initiate and manage the entire combat encounter.

        Handles the full combat loop, including:
        - Initial combat display
        - Player action selection
        - Combat resolution
        - Victory/defeat conditions
        """
        print("\n" + "=" * 60)
        print(f"⚔️  {self.hero.name} vs {self.monster.name} ⚔️".center(60))
        print("=" * 60 + "\n")

        self.display_status()

        while not self.combat.is_combat_over():
            self.display_menu()
            choice = input("\nEnter your choice (1-5): ")

            messages = self.handle_choice(choice)
            if messages:
                for msg in messages:
                    print(msg)

                if self.combat.is_combat_over():
                    victor = self.combat.get_victor()
                    print("\n" + "=" * 60)
                    print(f"Combat Ended! {victor.name} is victorious!")
                    print("=" * 60 + "\n")
                    break

                self.display_status()

            if messages and "Escaped from combat!" in messages:
                break