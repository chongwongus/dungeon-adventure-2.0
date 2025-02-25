import random
from typing import Optional, List
from src.characters.monsters.ogre import Ogre
from src.characters.monsters.gremlin import Gremlin
from src.characters.monsters.skeleton import Skeleton
from src.characters.base.monster import Monster


class Room:
    """A single room in the dungeon."""

    # Room display characters
    EMPTY = ' '
    PIT = 'X'
    ENTRANCE = 'i'
    EXIT = 'o'
    VISION_POT = 'V'
    HEALTH_POT = 'H'
    MULTIPLE_ITEMS = 'M'
    MONSTER = 'E'  # E for Enemy

    # Add Pillars list
    PILLARS = ['A', 'E', 'I', 'P']  # The four Pillars of OO

    def __init__(self):
        # Room state
        self.hasPit = False
        self.hasHealthPot = False
        self.hasVisionPot = False
        self.hasPillar = False
        self.isEntrance = False
        self.isExit = False
        self.pillarType = None
        self.doors = {
            'N': False, 'S': False,
            'E': False, 'W': False
        }
        self.visited = False

        # Monster and loot attributes
        self.monster: Optional[Monster] = None
        self.loot_drops = {
            'health_potion': 0.3,  # 30% chance
            'vision_potion': 0.2  # 20% chance
        }

    def spawn_monster(self, force: bool = False) -> None:
        """
        Attempt to spawn a monster in this room.
        Args:
            force: If True, guarantees a monster spawn
        """
        # Don't spawn in entrance/exit or if already has monster
        if (self.isEntrance or self.isExit or self.monster) and not force:
            return

        # 30% chance to spawn monster (or 100% if forced)
        if force or random.random() < 0.3:
            monster_types = [Ogre, Gremlin, Skeleton]
            monster_class = random.choice(monster_types)

            # Create monster with appropriate default values based on type
            # PLACEHOLDER HARD CODED VALUES FOR NOW
            if monster_class == Ogre:
                self.monster = Ogre(
                    hp=200,
                    min_damage=30,
                    max_damage=60,
                    attack_speed=2,
                    hit_chance=0.6,
                    heal_chance=0.1,
                    min_heal=30,
                    max_heal=60
                )
            elif monster_class == Skeleton:
                self.monster = Skeleton(
                    hp=100,
                    min_damage=30,
                    max_damage=50,
                    attack_speed=3,
                    hit_chance=0.8,
                    heal_chance=0.3,
                    min_heal=30,
                    max_heal=50
                )
            elif monster_class == Gremlin:
                self.monster = Gremlin(
                    hp=70,
                    min_damage=15,
                    max_damage=30,
                    attack_speed=5,
                    hit_chance=0.8,
                    heal_chance=0.4,
                    min_heal=20,
                    max_heal=40
                )

    def get_drops(self) -> List[str]:
        """
        Roll for loot drops when monster is defeated.
        Returns:
            List of items that dropped
        """
        drops = []
        for item, chance in self.loot_drops.items():
            if random.random() < chance:
                drops.append(item)
        return drops

    def clear_monster(self) -> List[str]:
        """
        Remove monster and get drops.
        Returns:
            List of dropped items
        """
        if self.monster and not self.monster.is_alive:
            drops = self.get_drops()
            self.monster = None
            return drops
        return []

    def get_room_display(self) -> str:
        """Return char representing room contents."""
        if self.isEntrance:
            return self.ENTRANCE
        if self.isExit:
            return self.EXIT
        if self.monster and self.visited:
            return self.MONSTER

        # Count visible items
        items = sum([self.hasPit, self.hasHealthPot,
                     self.hasVisionPot, self.hasPillar])

        if items > 1:
            return self.MULTIPLE_ITEMS
        elif self.hasPit:
            return self.PIT
        elif self.hasHealthPot:
            return self.HEALTH_POT
        elif self.hasVisionPot:
            return self.VISION_POT
        elif self.hasPillar:
            return self.pillarType
        else:
            return self.EMPTY

    def __str__(self) -> str:
        """Return ASCII representation of room."""
        top = ' * ' + ('-' if self.doors['N'] else ' * ') + ' * '
        mid = (' | ' if self.doors['W'] else ' * ') + \
              (self.get_room_display() + ' ' if self.visited else ' ? ') + \
              (' | ' if self.doors['E'] else ' * ')
        bot = ' * ' + (' - ' if self.doors['S'] else ' * ') + ' * '
        return top + '\n' + mid + '\n' + bot