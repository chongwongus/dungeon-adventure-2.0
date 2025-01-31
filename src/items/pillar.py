from item import Item

class Pillar(Item):
    def __init__(self, x, y, name, description):
        super().__init__(x, y, "pillar", "Pillar", "A stone pillar.", True)