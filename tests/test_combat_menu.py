"""Test cases for combat menu system"""
import pytest
from unittest.mock import patch
from src.characters.heroes.warrior import Warrior
from src.characters.monsters.ogre import Ogre
from src.combat.combat_system import CombatSystem
from src.combat.combat_menu import CombatMenu

def test_combat_menu_initialization():
    """Test combat menu setup"""
    hero = Warrior("Conan")
    monster = Ogre()
    combat_system = CombatSystem(hero, monster)
    menu = CombatMenu(combat_system)

    assert menu.hero == hero
    assert menu.monster == monster
    assert menu.combat == combat_system

@patch('random.randint')
def test_combat_menu_handle_choice(mock_randint):
    """Test combat menu choice handling"""
    # Set up healing potion to always heal 10 HP
    mock_randint.return_value = 10

    hero = Warrior("Conan")
    monster = Ogre()
    combat_system = CombatSystem(hero, monster)
    menu = CombatMenu(combat_system)

    # Test invalid choice
    result = menu.handle_choice("invalid")
    assert result is None

    # Test view status
    result = menu.handle_choice("5")
    assert result is None

    # Test using potion with none available
    result = menu.handle_choice("3")
    assert result is None

    # Test using potion with some available
    hero.collect_potion("healing")
    starting_hp = hero.hp
    hero.take_damage(20)  # Take some damage first
    assert hero.hp == starting_hp - 20  # Verify damage taken

    with patch('random.random', return_value=1.0):  # Ensure monster misses
        result = menu.handle_choice("3")
        assert result is not None  # Should get combat messages
        assert hero.hp == (starting_hp - 20 + 10)  # Should have healed 10 HP

@patch('random.random')
def test_combat_menu_escape(mock_random):
    """Test escape mechanics"""
    hero = Warrior("Conan")
    monster = Ogre()
    combat_system = CombatSystem(hero, monster)
    menu = CombatMenu(combat_system)

    # Test successful escape
    mock_random.return_value = 0.1  # Less than escape chance (0.4)
    result = menu.handle_choice("4")
    assert result is not None
    assert "Escaped from combat!" in result[0]  # First message should be escape

    # Test failed escape
    mock_random.return_value = 0.9  # Greater than escape chance (0.4)
    with patch('random.randint', return_value=0):  # Make monster miss on free attack
        result = menu.handle_choice("4")
        assert result is not None
        assert "Failed to escape!" not in result  # Message is printed directly
        assert "misses" in result[0]  # Monster should miss

def test_combat_menu_display(capsys):
    """Test display methods"""
    hero = Warrior("Conan")
    monster = Ogre()
    combat_system = CombatSystem(hero, monster)
    menu = CombatMenu(combat_system)

    # Test status display
    menu.display_status()
    captured = capsys.readouterr()
    assert "Current Status:" in captured.out
    assert hero.name in captured.out
    assert monster.name in captured.out
    assert "HP:" in captured.out
    assert "Potions:" in captured.out

    # Test menu display
    menu.display_menu()
    captured = capsys.readouterr()
    assert "What would you like to do?" in captured.out
    assert "1. Attack" in captured.out
    assert "2. Special Attack" in captured.out
    assert "3. Use Healing Potion" in captured.out
    assert "4. Try to Run" in captured.out
    assert "5. View Status" in captured.out

if __name__ == "__main__":
    pytest.main([__file__])