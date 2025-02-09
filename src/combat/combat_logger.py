from typing import List
from .combat_action import RoundResult


class CombatLogger:
    """Handles formatting and logging of combat results"""

    @staticmethod
    def format_round_result(result: RoundResult) -> List[str]:
        """Format a round result into a list of log messages"""
        messages = []

        # Action messages
        for action in result.actions:
            messages.append(action.message)

        # Status update
        messages.extend([
            "",
            "Status:",
            f"Hero: {result.hero_hp}/{result.hero_max_hp} HP",
            f"Monster: {result.monster_hp}/{result.monster_max_hp} HP",
            "",
            "Detailed Combat Info:"
        ])

        # Damage summary
        if result.hero_damage_taken > 0:
            messages.append(f"Hero took {result.hero_damage_taken} damage this round")
        if result.monster_damage_taken > 0:
            messages.append(f"Monster took {result.monster_damage_taken} damage this round")

        return messages