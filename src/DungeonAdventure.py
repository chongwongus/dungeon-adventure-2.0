import random
from dungeon.Dungeon import Dungeon
from Adventurer import Adventurer

class DungeonAdventure:
    def __init__(self):
        self.dungeon = None
        self.player = None
        self.game_over = False

    def play_game(self):
        self.display_intro()
        name = input("Enter your name: ")
        self.player = Adventurer(name)
        self.dungeon = Dungeon()

        self.player.currLocation = self.dungeon.entrance

        while not self.game_over:
            self.display_current_room()
            self.handle_menu()
            self.check_game_state()

    def display_intro(self):
        print("\n=== Welcome to Dungeon Adventure! ===")
        print("Find all four Pillars of OO and reach the exit to win!")
        print("Watch out for pits, and use potions wisely!\n")


    def handle_menu(self):
        """Handles player input and menu options"""
        print("\nWhat would you like to do?")
        print("1. Move (N/S/E/W)")
        print("2. Use Health Potion")
        print("3. Use Vision Potion")
        print("4. View Character Status")
        print("5. Quit")
        print("D. Display Full Dungeon (Debug)")

        choice = input("Enter your choice: ").upper()

        if choice == '1':
            direction = input("Enter direction (N/S/E/W): ").upper()
            if direction in ['N', 'S', 'E', 'W']:
                if self.dungeon.is_valid_move(self.player.currLocation, direction):
                    self.player.move(direction)
                    self.process_room()
                    print("\n\n")
                else:
                    print("You can't move in that direction!")
            else:
                print("Invalid direction!")

        elif choice == '2':
            if self.player.use_healing_pot():
                print(f"Used healing potion! HP is now {self.player.hp}")
            else:
                print("No healing potions available!")

        elif choice == '3':
            if self.player.use_vision_pot():
                print("Used vision potion! Showing surrounding rooms:")
                self.display_vision()
            else:
                print("No vision potions available!")

        elif choice == '4':
            print("\n" + str(self.player))

        elif choice == '5':
            self.game_over = True
            print("Thanks for playing!")

        elif choice == 'D':
            print("\nFull Dungeon Layout:")
            print(str(self.dungeon))

        else:
            print("Invalid choice!")

    def process_room(self):
        """Process current room's contents"""
        x, y = self.player.currLocation
        current_room = self.dungeon.get_room(x, y)
        current_room.visited = True

        if current_room.hasPit:
            damage = random.randint(1, 20)
            self.player.take_dmg(damage)
            print(f"\n\nYou fell into a pit! Took {damage} damage!")

        if current_room.hasHealthPot:
            self.player.healingPot += 1
            current_room.hasHealthPot = False
            print("\n\nFound a health potion!")

        if current_room.hasVisionPot:
            self.player.visionPot += 1
            current_room.hasVisionPot = False
            print("\n\nFound a vision potion!")

        if current_room.hasPillar:
            self.player.add_pillar(current_room.pillarType)
            current_room.hasPillar = False
            print(f"\n\nFound the Pillar of {current_room.pillarType}!")

    def display_current_room(self):
        """Displays current room and basic info"""
        x, y = self.player.currLocation
        current_room = self.dungeon.get_room(x, y)
        print(f"\nLocation: ({x}, {y})")
        print(current_room)
        print(f"HP: {self.player.hp}")

    def display_vision(self):
        """Shows surrounding rooms when vision potion is used"""
        x, y = self.player.currLocation
        for dy in [-1, 0, 1]:
            rooms = []
            for dx in [-1, 0, 1]:
                room = self.dungeon.get_room(x + dx, y + dy)
                rooms.append(str(room) if room else "   \n   \n   ")

            # Print rooms side by side, line by line
            for i in range(3):  # Each room has 3 lines
                print(''.join(room.split('\n')[i] for room in rooms))

    def check_game_state(self):
        """Checks if player has won or lost"""
        if self.player.hp <= 0:
            print("\nYou have died! Game Over!")
            self.game_over = True

        elif self.player.currLocation == self.dungeon.exit:
            if len(self.player.pillarsFound) == 4:
                print("\nCongratulations! You've won!")
                self.game_over = True
            else:
                print("\nYou need all four pillars to exit!")


if __name__ == "__main__":
    game = DungeonAdventure()
    game.play_game()
