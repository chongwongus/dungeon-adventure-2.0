from typing import List, Tuple, Optional
from src.characters.base.dungeon_character import DungeonCharacter
from src.characters.base.hero import Hero
from src.characters.base.monster import Monster


class CombatSystem:
    """Manages combat between hero and monsters."""

    def __init__(self, hero: Hero, monster: Monster):
        self.hero = hero
        self.monster = monster
        self.combat_log: List[str] = []

    def log_message(self, message: str):
        """Add message to combat log."""
        self.combat_log.append(message)

    def execute_round(self, use_special: bool = False) -> List[str]:
        """Execute one full round of combat."""
        self.combat_log = []

        if not self.hero.is_alive or not self.monster.is_alive:
            return ["Combat already ended!"]

        # Log initial HP for this round
        hero_starting_hp = self.hero.hp
        monster_starting_hp = self.monster.hp

        # Get number of attacks
        hero_attacks = self.hero.get_num_attacks(self.monster)
        monster_attacks = self.monster.get_num_attacks(self.hero)

        # Hero's turn
        if use_special:
            success, message = self.hero.special_skill(self.monster)
            self.log_message(message)
            if monster_starting_hp != self.monster.hp:
                damage_dealt = monster_starting_hp - self.monster.hp
                self.log_message(f"Monster took {damage_dealt} damage!")
        else:
            for _ in range(hero_attacks):
                if not self.monster.is_alive:
                    break
                hit, damage = self.hero.attack(self.monster)
                if hit:
                    self.log_message(f"{self.hero.name} hits for {damage} damage!")
                else:
                    self.log_message(f"{self.hero.name} misses!")

        # Monster's turn (if still alive)
        if self.monster.is_alive:
            for _ in range(monster_attacks):
                if not self.hero.is_alive:
                    break
                hit, damage = self.monster.attack(self.hero)
                if hit:
                    hero_hp_before = self.hero.hp
                    was_blocked = self.hero.take_damage(damage)
                    if was_blocked:
                        self.log_message(f"{self.monster.name} attacks but {self.hero.name} blocks!")
                    else:
                        actual_damage = hero_hp_before - self.hero.hp
                        self.log_message(f"{self.monster.name} hits for {actual_damage} damage!")
                else:
                    self.log_message(f"{self.monster.name} misses!")

        # If hero was healed during their special ability
        if use_special and self.hero.hp > hero_starting_hp:
            heal_amount = self.hero.hp - hero_starting_hp
            self.log_message(f"{self.hero.name} healed for {heal_amount} HP!")

        # Status update
        self.log_message(f"\nStatus:")
        self.log_message(f"{self.hero.name}: {self.hero.hp}/{self.hero._max_hp} HP")
        self.log_message(f"{self.monster.name}: {self.monster.hp}/{self.monster._max_hp} HP")

        return self.combat_log

    def is_combat_over(self) -> bool:
        """Check if combat has ended."""
        return not self.hero.is_alive or not self.monster.is_alive

    def get_victor(self) -> Optional[DungeonCharacter]:
        """Return the winner of combat, if any."""
        if not self.hero.is_alive:
            return self.monster
        elif not self.monster.is_alive:
            return self.hero
        return None