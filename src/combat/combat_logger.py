from typing import List
from .combat_action import RoundResult


class CombatLogger:
    """
    Handles the transformation of combat results into readable log messages.

    The CombatLogger acts as a translator between the game's technical
    combat mechanics and a narrative-driven combat experience. It takes
    the raw data from a combat round and converts it into a series of
    human-friendly messages that describe the combat's progression.

    Primary Responsibility:
    Convert RoundResult data into a list of descriptive messages that
    capture the essence of the combat round's events.

    Design Principles:
    - Clear and concise message generation
    - Comprehensive coverage of combat events
    - Easy-to-read format for players

    Static Method:
        format_round_result(result: RoundResult) -> List[str]:
            Transforms a combat round's technical data into a readable narrative.

    Example Transformation:
    Technical Data (RoundResult) -> Readable Messages:
    - Individual action descriptions
    - Current health status
    - Damage summary
    - Contextual combat information
    """

    @staticmethod
    def format_round_result(result: RoundResult) -> List[str]:
        """
        Convert a combat round's technical results into a human-readable narrative.

        This method performs several key transformations:
        1. Extracts and formats individual action messages
        2. Generates a status update for both combatants
        3. Provides a detailed breakdown of damage dealt
        4. Creates a comprehensive, easy-to-understand combat log

        Args:
            result (RoundResult): Comprehensive data about a single combat round

        Returns:
            List[str]: A series of messages describing the round's events

        Key Processing Steps:
        - Collect action-specific messages
        - Add health status information
        - Summarize damage received
        - Ensure readability and context

        Example Output:
        [
            "Warrior hits Ogre for 25 damage!",
            "Ogre misses!",
            "",
            "Status:",
            "Hero: 75/100 HP",
            "Monster: 50/100 HP",
            "",
            "Detailed Combat Info:",
            "Hero took 10 damage this round"
        ]
        """
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