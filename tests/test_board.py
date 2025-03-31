import pytest
from src.game.board import Board
from src.game.player import Player
from utils.boat_type import BoatType

class MockPlayer:
    def __init__(self, name):
        self.name = name
        self.boats = {}

    def set_boat_emplacement(self, boat_name, row, col):
        if boat_name not in self.boats:
            self.boats[boat_name] = []
        self.boats[boat_name].append((row, col))

@pytest.fixture
def setup_board(init_pygame):
    player = MockPlayer("Player 1")
    enemy = MockPlayer("Enemy")
    board = Board(player=player, enemy=enemy)
    return board, player, enemy

def test_place_enemy_boats(setup_board):
    board, _, enemy = setup_board
    board.place_enemy_boats()
    assert len(enemy.boats) == 5  # Ensure all 5 boats are placed
    for boat_positions in enemy.boats.values():
        assert len(boat_positions) > 0  # Ensure each boat has positions

def test_place_boat(setup_board):
    board, player, _ = setup_board
    event = type("MockEvent", (object,), {"type": "MOUSEBUTTONDOWN", "pos": (100, 100)})
    board.place_boat(event, player)
    assert hasattr(board, "current_boat")  # Ensure a boat is being placed
    assert len(player.boats) == 0  # No boats should be fully placed yet

def test_play_turn_player_hit(setup_board):
    board, player, enemy = setup_board
    enemy.boats = {"Destroyer": [(3, 3)]}
    event = type("MockEvent", (object,), {"type": "MOUSEBUTTONDOWN", "pos": (160, 160)})  # Assuming cell size = 40
    board.play_turn(event)
    assert board.grid[3][3] == 2  # Hit
    assert len(enemy.boats["Destroyer"]) == 0  # Boat position removed

def test_play_turn_player_miss(setup_board):
    board, player, enemy = setup_board
    enemy.boats = {"Destroyer": [(3, 3)]}
    event = type("MockEvent", (object,), {"type": "MOUSEBUTTONDOWN", "pos": (200, 200)})  # Assuming cell size = 40
    board.play_turn(event)
    assert board.grid[5][5] == 3  # Miss

def test_check_victory_player_wins(setup_board):
    board, _, enemy = setup_board
    enemy.boats = {"Destroyer": []}  # All enemy boats destroyed
    result = board.check_victory()
    assert result == "player"

def test_check_victory_ia_wins(setup_board):
    board, player, _ = setup_board
    player.boats = {"Destroyer": []}  # All player boats destroyed
    result = board.check_victory()
    assert result == "ia"

def test_check_victory_no_winner(setup_board):
    board, player, enemy = setup_board
    player.boats = {"Destroyer": [(1, 1)]}
    enemy.boats = {"Destroyer": [(2, 2)]}
    result = board.check_victory()
    assert result is None