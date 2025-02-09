from typing import List, Optional
from .combat_action import CombatAction, RoundResult
from .combat_handler import Combatant
from .basic_attack_handler import BasicAttackHandler
from .special_attack_handler import SpecialAbilityHandler


class CombatSystem:
    """Manages combat between combatants using modular handlers"""

    def __init__(self, hero: Combatant, monster: Combatant):
        self.hero = hero
        self.monster = monster
        self.basic_attack_handler = BasicAttackHandler()
        self.special_ability_handler = SpecialAbilityHandler()

    def execute_round(self, use_special: bool = False) -> RoundResult:
        """Execute one full round of combat"""
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
        """Check if combat has ended"""
        return not self.hero.is_alive or not self.monster.is_alive

    def get_victor(self) -> Optional[Combatant]:
        """Return the winner of combat, if any"""
        if not self.hero.is_alive:
            return self.monster
        elif not self.monster.is_alive:
            return self.hero
        return None