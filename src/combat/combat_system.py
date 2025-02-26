from typing import List, Optional
from .combat_action import CombatAction, RoundResult
from .combat_handler import Combatant
from .basic_attack_handler import BasicAttackHandler
from .special_attack_handler import SpecialAbilityHandler


class CombatSystem:
    """
    Manages combat interactions between heroes and monsters.

    Coordinates the complex mechanics of turn-based combat,
    utilizing modular attack handlers to process combat rounds.

    Attributes:
        hero (Combatant): Player's character
        monster (Combatant): Current opponent
        basic_attack_handler (BasicAttackHandler): Handles standard attacks
        special_ability_handler (SpecialAbilityHandler): Manages special abilities
    """

    def __init__(self, hero: Combatant, monster: Combatant):
        self.hero = hero
        self.monster = monster
        self.basic_attack_handler = BasicAttackHandler()
        self.special_ability_handler = SpecialAbilityHandler()

    def execute_round(self, use_special: bool = False, monster_only: bool = False) -> RoundResult:
        """
        Execute a complete round of combat.

        Processes attacks for hero and monster, with options for:
        - Using hero's special ability
        - Monster-only turns

        Args:
            use_special (bool): Trigger hero's special ability
            monster_only (bool): Execute only monster's turn

        Returns:
            RoundResult: Comprehensive details of the combat round
        """
        if not self.hero.is_alive or not self.monster.is_alive:
            return RoundResult(
                actions=[CombatAction(
                    actor_name="System",
                    action_type="info",
                    success=False,
                    message="Combat already ended!"
                )],
                hero_damage_taken=0,
                monster_damage_taken=0,
                hero_hp=self.hero.hp,
                hero_max_hp=self.hero._max_hp,
                monster_hp=self.monster.hp,
                monster_max_hp=self.monster._max_hp
            )

        # Track starting and actual damage
        hero_starting_hp = self.hero.hp
        monster_starting_hp = self.monster.hp
        total_hero_damage = 0
        total_monster_damage = 0

        # Collect all actions
        all_actions = []

        # Hero's turn
        if use_special:
            all_actions.extend(
                self.special_ability_handler.execute(self.hero, self.monster)
            )
        else:
            all_actions.extend(
                self.basic_attack_handler.execute(self.hero, self.monster)
            )

        # Monster's turn (if still alive)
        if self.monster.is_alive:
            all_actions.extend(
                self.basic_attack_handler.execute(self.monster, self.hero)
            )

        # Calculate damage from actual HP changes only
        hero_damage_taken = hero_starting_hp - self.hero.hp
        monster_damage_taken = monster_starting_hp - self.monster.hp

        return RoundResult(
            actions=all_actions,
            hero_damage_taken=max(0, hero_damage_taken),  # Ensure non-negative
            monster_damage_taken=max(0, monster_damage_taken),  # Ensure non-negative
            hero_hp=self.hero.hp,
            hero_max_hp=self.hero._max_hp,
            monster_hp=self.monster.hp,
            monster_max_hp=self.monster._max_hp
        )

    def is_combat_over(self) -> bool:
        """
        Determine if the current combat encounter has concluded.

        Returns:
            bool: True if either hero or monster has been defeated
        """
        return not self.hero.is_alive or not self.monster.is_alive

    def get_victor(self) -> Optional[Combatant]:
        """
        Identify the winner of the combat encounter.

        Returns:
            Optional[Combatant]: Winning character, or None if combat ongoing
        """
        if not self.hero.is_alive:
            return self.monster
        elif not self.monster.is_alive:
            return self.hero
        return None