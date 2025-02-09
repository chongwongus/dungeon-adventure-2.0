from typing import List
from .combat_handler import CombatHandler, Combatant
from .combat_action import CombatAction


class SpecialAbilityHandler(CombatHandler):
    """Handles hero special ability usage"""

    def execute(self, attacker: Combatant, defender: Combatant) -> List[CombatAction]:
        if hasattr(attacker, 'special_skill'):
            monster_hp_before = defender.hp
            success, message = attacker.special_skill(defender)
            damage_dealt = monster_hp_before - defender.hp

            return [CombatAction(
                actor_name=attacker.name,
                action_type="special",
                success=success,
                damage=damage_dealt,
                message=message
            )]
        return []