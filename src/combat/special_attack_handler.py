from typing import List
from .combat_handler import CombatHandler, Combatant
from .combat_action import CombatAction


class SpecialAbilityHandler(CombatHandler):
    """
    Handles the execution of hero-specific special abilities.

    Processes special skills for heroes, converting them into
    standardized combat actions that can be integrated into
    the combat system.

    The handler supports various hero special abilities by:
    - Checking for special skill availability
    - Executing the special skill
    - Tracking damage or effects
    - Generating appropriate combat actions
    """

    def execute(self, attacker: Combatant, defender: Combatant) -> List[CombatAction]:
        """
        Execute the attacker's special skill against the defender.

        Processes the special ability if available, tracking:
        - Skill success
        - Damage dealt
        - Generating descriptive message

        Args:
            attacker (Combatant): Character using special ability
            defender (Combatant): Target of the special ability

        Returns:
            List[CombatAction]: Combat actions resulting from special ability
        """
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