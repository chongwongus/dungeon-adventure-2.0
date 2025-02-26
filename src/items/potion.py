from abc import abstractmethod
from item import Item


class Potion(Item):
    """
    Represents a consumable potion item in the game world.

    Potions are specialized items that provide temporary effects
    or benefits to the player character. They are a critical
    resource management and strategic element in the game.

    Key Characteristics:
    1. Consumable Item Type
       - Inherits from base Item class
       - Supports unique potion initialization

    2. Effect Mechanism
       - Each potion has a specific effect
       - Supports varied gameplay strategies

    3. Usage Pattern
       - Abstract use method requires implementation
       - Ensures consistent potion interaction

    Design Components:
    - Name identification
    - Descriptive text
    - Specific effect definition
    - Abstract use mechanism

    Usage Strategy:
    - Define specific potion types
    - Implement unique use methods
    - Provide clear effect descriptions

    Example Implementation:
    ```python
    class HealingPotion(Potion):
        def __init__(self):
            super().__init__(
                "Healing Potion",
                "Restores health when consumed",
                "heal"
            )

        def use(self, character):
            # Implement specific healing logic
            character.heal(50)
    """
    def __init__(self, name: str, description: str, effect: str):
        """
        Initialize a new Potion item.

        Provides a comprehensive setup for potion items with:
        - Unique name
        - Descriptive text
        - Specific effect characterization

        Args:
            name (str): The name of the potion
            description (str): Detailed description of the potion
            effect (str): The primary effect of the potion
        """
        self.name = name
        self.description = description
        self.effect = effect

    @abstractmethod
    def use():
        """
        Abstract method defining potion usage mechanism.
        """
        pass
