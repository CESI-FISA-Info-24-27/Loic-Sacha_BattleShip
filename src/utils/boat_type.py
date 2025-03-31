from enum import Enum

class BoatType(Enum):
    """
    BoatType is an enumeration that represents different types of boats used in the game.

    Attributes:
        AIRCRAFT_CARRIER (str): Represents an Aircraft Carrier.
        CRUISER (str): Represents a Cruiser.
        DESTROYER (str): Represents a Destroyer.
        SUBMARINE (str): Represents a Submarine.
        TORPEDO (str): Represents a Torpedo.
    """
    AIRCRAFT_CARRIER = "Aircraft Carrier"
    CRUISER = "Cruiser"
    DESTROYER = "Destroyer"
    SUBMARINE = "Submarine"
    TORPEDO = "Torpedo"