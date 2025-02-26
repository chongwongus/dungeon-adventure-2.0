from dataclasses import dataclass
from typing import List

@dataclass
class CombatAction:
    """
    Represents a single action taken during a combat encounter.

    This data class captures the comprehensive details of a specific
    combat action, providing insight into what occurred during an
    attack, special ability, healing, or blocking event.

    Attributes:
        actor_name (str): Name of the character performing the action
        action_type (str): Type of action (attack, special, block, heal)
        success (bool): Whether the action was successful
        damage (int, optional): Amount of damage dealt
        healing (int, optional): Amount of healing performed
        message (str, optional): Descriptive message about the action
    """
    actor_name: str
    action_type: str  # "attack", "special", "block", "heal"
    success: bool
    damage: int = 0
    healing: int = 0
    message: str = ""

@dataclass
class RoundResult:
    """
    Encapsulates the complete results of a single combat round.

    Provides a comprehensive overview of a combat round, tracking:
    - All actions performed
    - Damage dealt to both combatants
    - Current health status of hero and monster

    Attributes:
        actions (List[CombatAction]): Detailed list of all actions in the round
        hero_damage_taken (int): Total damage received by the hero
        monster_damage_taken (int): Total damage received by the monster
        hero_hp (int): Hero's remaining health points
        hero_max_hp (int): Hero's maximum health points
        monster_hp (int): Monster's remaining health points
        monster_max_hp (int): Monster's maximum health points
    """
    actions: List[CombatAction]
    hero_damage_taken: int
    monster_damage_taken: int
    hero_hp: int
    hero_max_hp: int
    monster_hp: int
    monster_max_hp: int
