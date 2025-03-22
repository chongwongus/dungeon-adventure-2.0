# Dungeon Adventure 2.0 🏰

An expanded Python dungeon crawler where heroes battle monsters and collect the four Pillars of Object-Oriented Programming while navigating through a procedurally generated dungeon filled with challenges, combat, and strategic choices.

## 🎮 Game Overview

In Dungeon Adventure 2.0, players choose a hero class and venture into a dangerous dungeon. The main objectives are:

- Choose your hero class (Warrior, Priestess, or Thief)
- Battle monsters with unique abilities and combat styles
- Collect all four Pillars of OO (Abstraction, Encapsulation, Inheritance, and Polymorphism)
- Navigate hazards and use items strategically
- Reach the exit with all pillars to win

## 🌟 New Features in 2.0

- **Character Classes**:
  - 🗡️ Warrior: High HP, crushing blow ability
  - 📿 Priestess: Healing magic, support skills
  - 🗝️ Thief: Quick, chance for surprise attacks
- **Combat System**:
  - Turn-based battles
  - Speed-based attack system
  - Special abilities unique to each class
  - Monster healing mechanics
- **Monsters**:
  - Ogres: Tough but slow
  - Gremlins: Quick and numerous
  - Skeletons: Balanced threat
- **Save System**:
  - Save your progress
  - Resume previous adventures
- **Enhanced GUI**:
  - Character selection screen
  - Combat interface
  - Monster visualization
  - Save/Load interface

## 🎯 Original Features

- Procedural dungeon generation
- Multiple game elements:
  - Hero with health management
  - Four collectible Pillars
  - Hazardous pits
  - Support items (healing and vision potions)
- Object-oriented architecture
- Visual dungeon representation

## 🛠️ Technical Implementation

### Prerequisites

- Python 3.x
- Additional dependencies listed in `requirements.txt`

### Installation

```bash
git clone https://github.com/chongwongus/dungeon-adventure-2.0.git
cd dungeon-adventure-2.0
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

## 🏗️ Architecture

The project demonstrates advanced object-oriented principles:

### Key Components

- **Character System**
  - Abstract base classes for characters
  - Specialized hero and monster classes
  - Combat mechanics integration

- **Dungeon System**
  - Procedural generation
  - Room management
  - Monster placement logic

- **Database Integration**
  - SQLite for game data
  - Save/Load functionality
  - Monster statistics

- **GUI System**
  - Tkinter-based interface
  - Combat visualization
  - Character management
  - Dungeon rendering

## 🧪 Testing

Run the test suite:

```bash
python -m unittest discover tests
```

## 👥 Development

This project was developed as part of TCSS 504, showcasing:

- Advanced OOP principles
- Database integration
- Combat system design
- Save state management
- GUI development
- Unit testing

## 📄 License

This project is available under the MIT License. See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 Course Objectives Met

- Implementation of advanced OOP concepts
- Database integration and management
- Complex system architecture
- GUI enhancement
- Save state handling
- Combat system implementation
- Extended unit testing
- Modern software engineering practices

---

*Note: This project is an enhanced version of the original Dungeon Adventure created for TCSS 502.*
