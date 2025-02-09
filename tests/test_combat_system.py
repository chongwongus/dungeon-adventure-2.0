import sys
import os
import unittest
from typing import List, Tuple, Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.characters.heroes.warrior import Warrior
from src.characters.heroes.priestess import Priestess
from src.characters.heroes.thief import Thief
from src.characters.monsters.ogre import Ogre
from src.characters.monsters.skeleton import Skeleton
from src.characters.monsters.gremlin import Gremlin

# Import the new combat system components
from src.combat.combat_system import CombatSystem
from src.combat.combat_action import CombatAction, RoundResult
from src.combat.basic_attack_handler import BasicAttackHandler
from src.combat.special_attack_handler import SpecialAbilityHandler
from src.combat.combat_logger import CombatLogger


class TestCombatActions(unittest.TestCase):
    """Test individual combat actions and data structures"""

    def test_combat_action_creation(self):
        """Test creating combat actions with different parameters"""
        action = CombatAction(
            actor_name="Test",
            action_type="attack",
            success=True,
            damage=10
        )
        self.assertEqual(action.actor_name, "Test")
        self.assertEqual(action.damage, 10)
        self.assertTrue(action.success)

    def test_round_result_creation(self):
        """Test creating round results"""
        actions = [
            CombatAction("Hero", "attack", True, 10),
            CombatAction("Monster", "block", True)
        ]
        result = RoundResult(
            actions=actions,
            hero_damage_taken=0,
            monster_damage_taken=10,
            hero_hp=100,
            hero_max_hp=100,
            monster_hp=90,
            monster_max_hp=100
        )
        self.assertEqual(len(result.actions), 2)
        self.assertEqual(result.hero_damage_taken, 0)
        self.assertEqual(result.monster_damage_taken, 10)


class TestCombatSystem(unittest.TestCase):
    """Test the main combat system functionality"""

    def setUp(self):
        """Set up fresh instances for each test"""
        self.warrior = Warrior("TestWarrior")
        self.priestess = Priestess("TestPriestess")
        self.thief = Thief("TestThief")
        self.ogre = Ogre()
        self.skeleton = Skeleton()
        self.gremlin = Gremlin()

    def test_basic_combat_round(self):
        """Test a basic combat round without special abilities"""
        combat = CombatSystem(self.warrior, self.ogre)
        result = combat.execute_round(use_special=False)

        self.assertIsInstance(result, RoundResult)
        self.assertTrue(len(result.actions) > 0)
        self.assertGreaterEqual(result.hero_hp, 0)
        self.assertGreaterEqual(result.monster_hp, 0)

    def test_special_ability_combat(self):
        """Test combat rounds with special abilities"""
        # Test Warrior's Crushing Blow
        combat = CombatSystem(self.warrior, self.ogre)
        result = combat.execute_round(use_special=True)
        special_actions = [a for a in result.actions if a.action_type == "special"]
        self.assertTrue(len(special_actions) <= 1)  # Could miss

        # Test Priestess's Healing
        combat = CombatSystem(self.priestess, self.ogre)
        self.priestess.hp = self.priestess.hp // 2  # Damage priestess first
        result = combat.execute_round(use_special=True)
        heal_actions = [a for a in result.actions if "heal" in a.message.lower()]
        self.assertTrue(len(heal_actions) <= 1)

    def test_combat_resolution(self):
        """Test combat ending conditions"""
        combat = CombatSystem(self.warrior, self.gremlin)

        # Force near-death scenario
        self.gremlin.hp = 1
        result = combat.execute_round(use_special=True)

        if self.gremlin.hp <= 0:
            self.assertTrue(combat.is_combat_over())
            victor = combat.get_victor()
            self.assertEqual(victor, self.warrior)


class TestCombatHandlers(unittest.TestCase):
    """Test the individual combat handlers"""

    def setUp(self):
        self.warrior = Warrior("TestWarrior")
        self.ogre = Ogre()
        self.basic_handler = BasicAttackHandler()
        self.special_handler = SpecialAbilityHandler()

    def test_basic_attack_handler(self):
        """Test the basic attack handler"""
        actions = self.basic_handler.execute(self.warrior, self.ogre)
        self.assertTrue(isinstance(actions, list))
        for action in actions:
            self.assertTrue(isinstance(action, CombatAction))
            self.assertEqual(action.actor_name, self.warrior.name)

    def test_special_attack_handler(self):
        """Test the special ability handler"""
        actions = self.special_handler.execute(self.warrior, self.ogre)
        self.assertTrue(isinstance(actions, list))
        if actions:  # Special might miss
            self.assertEqual(actions[0].action_type, "special")


class TestCombatLogger(unittest.TestCase):
    """Test the combat logging functionality"""

    def setUp(self):
        self.warrior = Warrior("TestWarrior")
        self.ogre = Ogre()
        self.combat = CombatSystem(self.warrior, self.ogre)

    def test_logger_formatting(self):
        """Test the logger's message formatting"""
        result = self.combat.execute_round()
        messages = CombatLogger.format_round_result(result)

        self.assertTrue(isinstance(messages, list))
        self.assertTrue(any("Status:" in msg for msg in messages))
        self.assertTrue(any("HP" in msg for msg in messages))
        self.assertTrue(any(self.warrior.name in msg for msg in messages))
        self.assertTrue(any(self.ogre.name in msg for msg in messages))


class TestCharacterCombinations(unittest.TestCase):
    """Test different character combinations in combat"""

    def setUp(self):
        self.heroes = [
            Warrior("TestWarrior"),
            Priestess("TestPriestess"),
            Thief("TestThief")
        ]
        self.monsters = [
            Ogre(),
            Skeleton(),
            Gremlin()
        ]

    def test_all_combinations(self):
        """Test every hero vs every monster"""
        for hero in self.heroes:
            for monster in self.monsters:
                with self.subTest(hero=hero.name, monster=monster.name):
                    combat = CombatSystem(hero, monster)
                    result = combat.execute_round()

                    self.assertIsInstance(result, RoundResult)
                    self.assertTrue(len(result.actions) > 0)
                    self.assertGreaterEqual(result.hero_hp, 0)
                    self.assertGreaterEqual(result.monster_hp, 0)


def run_tests():
    unittest.main(argv=[''], verbosity=2)


if __name__ == '__main__':
    run_tests()