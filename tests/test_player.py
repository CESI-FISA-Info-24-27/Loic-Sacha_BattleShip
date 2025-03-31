import pytest
from src.game.player import Player

@pytest.fixture
def player():
    return Player("Test Player")

def test_initialization(player):
    assert player.name == "Test Player"
    assert player.is_enemy is False
    assert player.boats == {}
    assert player.move_historic == []

def test_change_name(player):
    player.change_name("New Name")
    assert player.name == "New Name"

def test_set_boat_emplacement_valid(player):
    player.set_boat_emplacement("Battleship", 3, 4)
    assert player.boats == {"Battleship": [(3, 4)]}

def test_set_boat_emplacement_out_of_bounds(player):
    player.set_boat_emplacement("Battleship", 11, 5)
    assert player.boats == {}

def test_set_boat_emplacement_duplicate_coordinates(player):
    player.set_boat_emplacement("Battleship", 3, 4)
    player.set_boat_emplacement("Battleship", 3, 4)
    assert player.boats == {"Battleship": [(3, 4)]}

def test_set_boat_emplacement_already_attributed(player):
    player.set_boat_emplacement("Battleship", 3, 4)
    player.set_boat_emplacement("Destroyer", 3, 4)
    assert player.boats == {"Battleship": [(3, 4)]}

def test_record_move(player):
    player.record_move(3, 4, True)
    assert player.move_historic == [((3, 4), True)]
    player.record_move(5, 6, False)
    assert player.move_historic == [((3, 4), True), ((5, 6), False)]