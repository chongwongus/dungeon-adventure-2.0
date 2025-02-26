from abc import ABC, abstractmethod

class Item(ABC):
    """
    Abstract base class representing fundamental item characteristics
    in the Dungeon Adventure game.

    This class defines the minimal contract that all game items must
    implement, ensuring a consistent approach to item representation
    and interaction.

    Core Item Design Considerations:
    1. Mandatory Naming
       - Every item must have a unique identifier
       - Provides basic item recognition

    2. Descriptive Capabilities
       - Supports item description
       - Enables rich item information display

    3. Polymorphic Behavior
       - Allows creation of diverse item types
       - Supports extension through inheritance

    Abstract Method Requirements:
    Subclasses must implement an initialization method that
    provides at minimum:
    - A name for the item
    - A descriptive text

    Usage Example:
    ```python
    class SpecificItem(Item):
        def __init__(self, name, description):
            super().__init__(name, description)
            # Additional item-specific initialization
    ```

    Inheritance Strategy:
    Provides a blueprint for creating:
    - Collectible items
    - Interactive objects
    - Game world elements
    """

    @abstractmethod
    def __init__(self, name: str, description: str):
        """
        Initialize a new item with its fundamental characteristics.

        This abstract method establishes the core requirements
        for item creation, ensuring that all items have:
        - A name
        - A descriptive text

        Args:
            name (str): The unique identifier for the item
            description (str): Detailed description of the item

        Note:
            This is an abstract method that must be implemented
            by all subclasses, providing a consistent initialization
            pattern for game items.
        """
        self.name = name
        self.description = description

    def __str__(self):
        """
        Provide a string representation of the item.

        Returns the item's name when the item is converted to a string,
        allowing for simple and intuitive item identification.

        Returns:
            str: The name of the item
        """
        return self.name
