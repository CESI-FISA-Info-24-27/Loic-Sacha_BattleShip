from enum import Enum

class BoatType(Enum):
    """
    BoatType is an enumeration that represents different types of boats used in the game, 
    along with their respective names and sizes.
    Attributes:
        AIRCRAFT_CARRIER (tuple): Represents an Aircraft Carrier with a size of 5.
        CRUISER (tuple): Represents a Cruiser with a size of 4.
        DESTROYER (tuple): Represents a Destroyer with a size of 3.
        SUBMARINE (tuple): Represents a Submarine with a size of 3.
        TORPEDO (tuple): Represents a Torpedo with a size of 2.
    Properties:
        size (int): Returns the size of the boat type.
        name (str): Returns the name of the boat type.
    """
    AIRCRAFT_CARRIER = ("Aircraft Carrier", 5)
    CRUISER = ("Cruiser", 4)
    DESTROYER = ("Destroyer", 3)
    SUBMARINE = ("Submarine", 3)
    TORPEDO = ("Torpedo", 2)

    @property
    def size(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]