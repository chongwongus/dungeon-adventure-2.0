import tkinter as tk
from tkinter import ttk, messagebox
import random
from dungeon.DFSDungeonFactory import DFSDungeonFactory
from dungeon.EasyDungeonFactory import EasyDungeonFactory
from dungeon.Dungeon import Dungeon
from Adventurer import Adventurer
from dungeon.DungeonFactory import DungeonFactory


class DungeonGUI:
    """Main GUI class for Dungeon Adventure game. Handles all user interface and game display logic."""

    def __init__(self, root):
        """
        Initializes the GUI with a root window.
        Args:
            root: tkinter root window
        """

        self.root = root
        self.root.title("Dungeon Adventure")
        self.root.geometry("800x600")

        self.dungeon: Dungeon = None
        self.player = None
        self.show_start_screen()

    def show_start_screen(self):
        """
        Displays the game's start screen with options for:
        - Player name input
        - Maze size selection
        - Difficulty selection
        - Instructions button
        - Start game button
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create start screen
        start_frame = ttk.Frame(self.root, padding="20")
        start_frame.pack(expand=True)

        ttk.Label(start_frame, text="Dungeon Adventure",
                  font=('Arial', 24, 'bold')).pack(pady=20)

        # Name entry
        ttk.Label(start_frame, text="Enter your name:").pack(pady=10)
        self.name_entry = ttk.Entry(start_frame)
        self.name_entry.pack(pady=10)

        # Maze size entry
        size_frame = ttk.Frame(start_frame)
        size_frame.pack(pady=10)

        ttk.Label(size_frame, text="Maze Size:").pack()
        self.size_entry = ttk.Entry(size_frame, width=10)
        self.size_entry.insert(0, "8")  # Default value
        self.size_entry.pack(pady=5)

        ttk.Button(start_frame, text="View Instructions",
                   command=self.show_instructions).pack(pady=10)

        ttk.Button(start_frame, text="Start Game",
                   command=self.validate_and_start).pack(pady=20)

        difficulty_frame = ttk.Frame(start_frame)
        difficulty_frame.pack(pady=10)

        ttk.Label(difficulty_frame, text="Difficulty:").pack()
        self.difficulty_var = tk.StringVar(value="easy")
        ttk.Radiobutton(difficulty_frame, text="Easy (Random Generation)",
                        variable=self.difficulty_var,
                        value="easy").pack()
        ttk.Radiobutton(difficulty_frame, text="Hard (DFS Generation)",
                        variable=self.difficulty_var,
                        value="hard").pack()

    def show_instructions(self):
        """
        Creates a new window displaying game instructions including:
        - Controls
        - Items
        - Game objectives
        - Tips for playing
        """
        instruction_window = tk.Toplevel(self.root)
        instruction_window.title("How to Play")
        instruction_window.geometry("500x400")

        instructions = ttk.Frame(instruction_window, padding="20")
        instructions.pack(fill="both", expand=True)

        # Game instructions
        ttk.Label(instructions, text="How to Play Dungeon Adventure",
                  font=('Arial', 14, 'bold')).pack(pady=10)

        instruction_text = """
        Goal:
        • Collect all four Pillars of OO (A, E, I, P) and reach the Exit

        Controls:
        • Movement: WASD keys or Arrow keys
        • Use Health Potion: Click button or press 'H'
        • Use Vision Potion: Click button or press 'V'

        Items:
        • HP: Health Potion - Randomly heals 5-15 HP 
        • VP: Vision Potion - Reveals surrounding rooms
        • X: Pit - Randomly deals 1-20 damage
        • A,E,I,P: Pillars - Collect all four to win

        Tips:
        • Watch your HP - don't let it reach 0
        • Use Vision Potions to plan your route
        • Collect Health Potions when you find them
        • The exit (O) requires all pillars to leave
        """

        text_widget = tk.Text(instructions, wrap="word", height=15, width=50)
        text_widget.insert("1.0", instruction_text)
        text_widget.config(state="disabled")  # Make read-only
        text_widget.pack(pady=10)

        ttk.Button(instructions, text="Close",
                   command=instruction_window.destroy).pack()

    def validate_and_start(self):
        """
        Validates user inputs from start screen and initializes game:
        - Checks for valid name
        - Validates maze size (1-50)
        - Creates dungeon with selected difficulty
        - Initializes player
        If validation fails, shows appropriate error message.
        """
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Warning", "Please enter a name!")
            return

        try:
            size = int(self.size_entry.get())
            if size >= 51 or size <= 0:
                messagebox.showwarning("Warning", "Please enter a size below 50!")
                return
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number!")
            return

        difficulty = self.difficulty_var.get()
        
        dungeonFactory:DungeonFactory = None
        if difficulty == "easy":
            dungeonFactory = EasyDungeonFactory() 
        else:
            dungeonFactory = DFSDungeonFactory()
            
        self.dungeon = dungeonFactory.create((size, size))
        self.player = Adventurer(name)
        self.player.currLocation = self.dungeon.entrance

        self.setup_game_screen()

    def setup_game_screen(self):
        """
        Sets up the main game interface including:
        - Scrollable maze display
        - Player status and HP bar
        - Action buttons
        - Event log
        - Key bindings for movement
        Configures automatic scrolling to follow player.
        """

        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main game layout
        self.cell_size = 50
        self.padding = 5

        # Game area (left side)
        game_frame = ttk.Frame(self.root, padding="10")
        game_frame.grid(row=0, column=0, sticky="nsew")

        # Create canvas with scrollbars
        canvas_frame = ttk.Frame(game_frame)
        canvas_frame.pack(expand=True, fill="both")

        # Calculate canvas size based on maze size
        canvas_size = (self.cell_size + self.padding) * self.dungeon.size[0]

        # Create scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal")
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical")

        # Create canvas with scrollbar command
        self.canvas = tk.Canvas(canvas_frame,
                                width=min(canvas_size, 600),  # Max width 600
                                height=min(canvas_size, 600),  # Max height 600
                                xscrollcommand=h_scrollbar.set,
                                yscrollcommand=v_scrollbar.set,
                                bg='grey')

        # Configure scrollbars
        h_scrollbar.config(command=self.canvas.xview)
        v_scrollbar.config(command=self.canvas.yview)

        # Pack canvas and scrollbars
        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", expand=True, fill="both")

        # Set canvas scroll region
        self.canvas.configure(scrollregion=(0, 0, canvas_size, canvas_size))

        # Rest of your existing control panel code
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=1, sticky="nsew")

        # Player info section with HP bar
        player_frame = ttk.LabelFrame(control_frame, text="Player Status", padding="5")
        player_frame.pack(pady=10, fill="x")

        self.player_info = ttk.Label(player_frame, text="")
        self.player_info.pack(pady=5)

        # HP Bar frame
        hp_frame = ttk.Frame(player_frame)
        hp_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(hp_frame, text="HP:").pack(side="left")

        # Create HP bar using Canvas
        self.hp_bar = tk.Canvas(hp_frame, width=150, height=20, bg='grey')
        self.hp_bar.pack(side="left", padx=5)

        # Action buttons
        ttk.Button(control_frame, text="Use Health Potion",
                   command=self.use_health_potion).pack(pady=5)
        ttk.Button(control_frame, text="Use Vision Potion",
                   command=self.use_vision_potion).pack(pady=5)

        # Add Restart button
        ttk.Button(control_frame, text="Restart Game",
                   command=self.show_start_screen).pack(pady=20)

        # Add event log
        log_frame = ttk.LabelFrame(control_frame, text="Event Log", padding="5")
        log_frame.pack(pady=10, fill="both", expand=True)

        self.event_log = tk.Text(log_frame, width=30, height=10, wrap="word")
        self.event_log.pack(padx=5, pady=5, fill="both", expand=True)

        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        # Bind movement keys
        self.root.bind('<w>', lambda e: self.try_move('N'))
        self.root.bind('<s>', lambda e: self.try_move('S'))
        self.root.bind('<a>', lambda e: self.try_move('W'))
        self.root.bind('<d>', lambda e: self.try_move('E'))
        self.root.bind('<Up>', lambda e: self.try_move('N'))
        self.root.bind('<Down>', lambda e: self.try_move('S'))
        self.root.bind('<Left>', lambda e: self.try_move('W'))
        self.root.bind('<Right>', lambda e: self.try_move('E'))

        # Add method to center on player after movement
        def center_on_player():
            if not hasattr(self, 'player') or not self.player:
                return
            x, y = self.player.currLocation
            # Calculate center point of player's position
            px = x * (self.cell_size + self.padding) + self.cell_size / 2
            py = y * (self.cell_size + self.padding) + self.cell_size / 2

            # Center view on player
            self.canvas.xview_moveto((px - self.canvas.winfo_width() / 2) / canvas_size)
            self.canvas.yview_moveto((py - self.canvas.winfo_height() / 2) / canvas_size)

        # Modify try_move to center on player after movement
        old_try_move = self.try_move

        def new_try_move(direction):
            result = old_try_move(direction)
            center_on_player()
            return result

        self.try_move = new_try_move

        # Initial display update
        self.update_display()
        # Center on player initially
        self.root.after(100, center_on_player)  # Slight delay to ensure canvas is ready

    def add_event_message(self, message):
        """
        Adds a message to the event log at the top.
        Args:
            message: String message to display
        """
        self.event_log.insert("1.0", message + "\n\n")
        self.event_log.see("1.0")  # Scroll to top

    def update_hp_bar(self):
        """
        Updates the HP bar visualization with pulsing effect when HP is low
        - Shows current HP as red bar
        - Changes shade based on HP percentage
        - Displays HP numbers
        """
        self.hp_bar.delete("all")
        hp_percent = self.player.hp / 100

        # Background (empty health)
        self.hp_bar.create_rectangle(0, 0, 150, 20, fill='#333333')

        # Foreground (current health)
        width = 150 * hp_percent

        # Determine color and pulsing
        if hp_percent <= 0.25:  # Below 25% health
            # Create pulsing effect by alternating colors
            import time
            pulse = int(time.time() * 2) % 2  # Alternates between 0 and 1 every 0.5 seconds
            color = '#ff0000' if pulse else '#ff8888'  # Alternates between bright and lighter red
            # Schedule next update for smooth pulsing
            self.root.after(50, self.update_hp_bar)
        else:
            color = '#ff0000' if hp_percent > 0.5 else '#ff4444'

        self.hp_bar.create_rectangle(0, 0, width, 20, fill=color)
        self.hp_bar.create_text(75, 10, text=f"{self.player.hp}/100",
                                fill='white', font=('Arial', 10, 'bold'))

    def update_display(self):
        """
        Updates the entire game display:
        - Redraws all rooms
        - Updates player info
        - Updates HP bar
        Called after any game state change.
        """
        self.canvas.delete('all')

        # Draw all rooms
        for y in range(self.dungeon.size[1]):
            for x in range(self.dungeon.size[0]):
                self.draw_room(x, y, self.dungeon.get_room(x, y))

        # Update player info and HP bar
        self.player_info.config(text=str(self.player))
        self.update_hp_bar()

    def draw_room(self, x, y, room):
        """
        Draws a single room on the canvas with:
        - Background color based on room type
        - Doors in appropriate positions
        - Room contents if visited
        - Player position if current room
        Args:
            x: x-coordinate of room
            y: y-coordinate of room
            room: Room object to draw
        """

        # Calculate pixel coordinates
        px = x * (self.cell_size + self.padding)
        py = y * (self.cell_size + self.padding)

        # Draw room background
        if not room.visited:
            color = 'dark grey'
        elif room.isEntrance:
            color = 'green'
        elif room.isExit:
            color = 'red'
        else:
            color = 'white'

        self.canvas.create_rectangle(px, py,
                                     px + self.cell_size,
                                     py + self.cell_size,
                                     fill=color, outline='black')

        # Draw doors
        door_width = 10
        if room.doors['N']:
            self.canvas.create_rectangle(px + self.cell_size / 2 - door_width / 2, py,
                                         px + self.cell_size / 2 + door_width / 2, py + door_width,
                                         fill='brown')
        if room.doors['S']:
            self.canvas.create_rectangle(px + self.cell_size / 2 - door_width / 2,
                                         py + self.cell_size - door_width,
                                         px + self.cell_size / 2 + door_width / 2,
                                         py + self.cell_size,
                                         fill='brown')
        if room.doors['W']:
            self.canvas.create_rectangle(px, py + self.cell_size / 2 - door_width / 2,
                                         px + door_width, py + self.cell_size / 2 + door_width / 2,
                                         fill='brown')
        if room.doors['E']:
            self.canvas.create_rectangle(px + self.cell_size - door_width,
                                         py + self.cell_size / 2 - door_width / 2,
                                         px + self.cell_size, py + self.cell_size / 2 + door_width / 2,
                                         fill='brown')

        # Draw room contents if visited
        if room.visited:
            text = ''
            if room.hasPillar:
                text = room.pillarType
            elif room.hasPit:
                text = 'PIT'
            elif room.hasHealthPot:
                text = 'HP'
            elif room.hasVisionPot:
                text = 'VP'

            if text:
                self.canvas.create_text(px + self.cell_size / 2,
                                        py + self.cell_size / 2,
                                        text=text)

        # Draw player position
        if (x, y) == self.player.currLocation:
            self.canvas.create_oval(px + self.cell_size / 4, py + self.cell_size / 4,
                                    px + 3 * self.cell_size / 4, py + 3 * self.cell_size / 4,
                                    fill='blue')

    def try_move(self, direction):
        """
        Attempts to move player in specified direction.
        If move is valid:
        - Updates player position
        - Processes new room
        - Updates display
        - Checks game state
        Args:
            direction: 'N', 'S', 'E', or 'W'
        """
        if self.dungeon.is_valid_move(self.player.currLocation, direction):
            self.player.move(direction)
            self.process_room()
            self.update_display()
            self.check_game_state()

    def process_room(self):
        """
        Processes effects of current room:
        - Marks room as visited
        - Applies pit damage if present
        - Collects items if present
        - Adds appropriate event messages
        """
        x, y = self.player.currLocation
        current_room = self.dungeon.get_room(x, y)
        current_room.visited = True

        if current_room.hasPit:
            damage = random.randint(1, 20)
            self.player.take_dmg(damage)
            self.add_event_message(f"You fell into a pit! Took {damage} damage!")

        if current_room.hasHealthPot:
            self.player.healingPot += 1
            current_room.hasHealthPot = False
            self.add_event_message("Found a health potion!")

        if current_room.hasVisionPot:
            self.player.visionPot += 1
            current_room.hasVisionPot = False
            self.add_event_message("Found a vision potion!")

        if current_room.hasPillar:
            self.player.add_pillar(current_room.pillarType)
            current_room.hasPillar = False
            self.add_event_message(f"Found the Pillar of {current_room.pillarType}!")

    def use_health_potion(self):
        """
        Attempts to use a health potion:
        - Checks if potion is available
        - Applies healing if possible
        - Updates display and adds event message
        """
        if self.player.use_healing_pot():
            self.add_event_message(f"Used healing potion! HP is now {self.player.hp}")
            self.update_display()
        else:
            self.add_event_message("No healing potions available!")

    def use_vision_potion(self):
        """
        Attempts to use a vision potion:
        - Checks if potion is available
        - Reveals surrounding rooms if possible
        - Updates display and adds event message
        """
        if self.player.use_vision_pot():
            x, y = self.player.currLocation
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    room = self.dungeon.get_room(x + dx, y + dy)
                    if room:
                        room.visited = True
            self.add_event_message("Used vision potion! Surrounding rooms revealed.")
            self.update_display()
        else:
            self.add_event_message("No vision potions available!")

    def check_game_state(self):
        """
        Checks for win/lose conditions:
        - Player death (HP <= 0)
        - Victory (at exit with all pillars)
        Shows appropriate message and returns to start screen if game is over.
        """

        if self.player.hp <= 0:
            messagebox.showinfo("Game Over", "You have died!")
            self.show_start_screen()
        elif (self.player.currLocation == self.dungeon.exit and
              len(self.player.pillarsFound) == 4):
            messagebox.showinfo("Congratulations", "You've won the game!")
            self.show_start_screen()


if __name__ == "__main__":
    root = tk.Tk()
    gui = DungeonGUI(root)
    root.mainloop()