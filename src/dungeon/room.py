class Room:
    """A single room in the dungeon with its contents and connections."""

    EMPTY = ' '
    PIT = 'X'
    ENTRANCE = 'i'
    EXIT = 'o'
    VISION_POT = 'V'
    HEALTH_POT = 'H'
    MULTIPLE_ITEMS = 'M'
    PILLARS = {'A', 'E', 'I', 'P'}

    def __init__(self):
        self.hasPit = False
        self.hasHealthPot = False
        self.hasVisionPot = False
        self.hasPillar = False
        self.isEntrance = False
        self.isExit = False
        self.pillarType = None
        self.doors = {
            'N': False,
            'S': False,
            'E': False,
            'W': False
        }
        self.visited = False
        self.monster = None  # New: track monster in room

    def __str__(self):
        """Return ASCII representation of room."""
        top = ' * ' + ('-' if self.doors['N'] else ' * ') + ' * '
        mid = (' | ' if self.doors['W'] else ' * ') + \
              (self.get_room_display() + ' ' if self.visited else ' ? ') + \
              (' | ' if self.doors['E'] else ' * ')
        bot = ' * ' + (' - ' if self.doors['S'] else ' * ') + ' * '
        return top + '\n' + mid + '\n' + bot

    def get_room_display(self):
        """Return char representing room contents."""
        if self.isEntrance:
            return self.ENTRANCE
        if self.isExit:
            return self.EXIT
        if self.monster is not None:  # New: show monster if present
            return 'M'

        items = sum([self.hasPit, self.hasHealthPot, self.hasVisionPot, self.hasPillar])

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
