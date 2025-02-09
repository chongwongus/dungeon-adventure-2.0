from dataclasses import dataclass
from typing import List

@dataclass
class CombatAction:
    """Represents a single combat action with its results"""
    actor_name: str
    action_type: str  # "attack", "special", "block", "heal"
    success: bool
    damage: int = 0
    healing: int = 0
    message: str = ""

@dataclass
class RoundResult:
    """Contains all results from a combat round"""
    actions: List[CombatAction]
    hero_damage_taken: int
    monster_damage_taken: int
    hero_hp: int
    hero_max_hp: int
    monster_hp: int
    monster_max_hp: int
