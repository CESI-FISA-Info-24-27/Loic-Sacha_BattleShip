import pytest
from src.game.player import Player

def test_player_initialization():
    player = Player("Alice")
    assert player.name == "Alice"
    assert player.is_enemy is False
    assert player.boats == {}
    assert player.move_historic == []

def test_change_name():
    player = Player("Alice")
    player.change_name("Bob")
    assert player.name == "Bob"

def test_set_boat_emplacement_valid():
    player = Player("Alice")
    player.set_boat_emplacement("Battleship", 5, 5)
    assert player.boats == {"Battleship": [(5, 5)]}

def test_set_boat_emplacement_out_of_bounds():
    player = Player("Alice")
    player.set_boat_emplacement("Battleship", 11, 5)
    assert "Battleship" not in player.boats

def test_set_boat_emplacement_already_attributed():
    player = Player("Alice")
    player.set_boat_emplacement("Battleship", 5, 5)
    player.set_boat_emplacement("Battleship", 5, 5)
    assert player.boats == {"Battleship": [(5, 5)]}

def test_set_boat_emplacement_conflict():
    player = Player("Alice")
    player.set_boat_emplacement("Battleship", 5, 5)
    player.set_boat_emplacement("Cruiser", 5, 5)
    assert player.boats == {"Battleship": [(5, 5)]}
    assert "Cruiser" not in player.boats

def test_record_move():
    player = Player("Alice")
    player.record_move(3, 4, True)
    player.record_move(2, 2, False)
    assert player.move_historic == [((3, 4), True), ((2, 2), False)]