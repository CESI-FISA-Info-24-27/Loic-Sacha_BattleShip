import pytest

from src.game.board import Board
from src.game.player import Player
from utils.boat_type import BoatType

def test_board_initialization():
    board = Board(rows=10, cols=10, cell_size=40)
    assert board.rows == 10
    assert board.cols == 10
    assert board.cell_size == 40
    assert len(board.player_grid) == 10
    assert len(board.enemy_grid) == 10
    assert all(len(row) == 10 for row in board.player_grid)
    assert all(len(row) == 10 for row in board.enemy_grid)

def test_place_enemy_boats():
    board = Board(rows=10, cols=10, cell_size=40, enemy=type("Enemy", (object,), {"boats": {}})())
    board.place_enemy_boats()
    assert len(board.enemy.boats) == 5
    for boat_positions in board.enemy.boats.values():
        assert len(boat_positions) > 0
        for row, col in boat_positions:
            assert board.enemy_grid[row][col]["ship"] is True

def test_reset_grid():
    board = Board(rows=10, cols=10, cell_size=40, player=type("Player", (object,), {"boats": {}})(), enemy=type("Enemy", (object,), {"boats": {}})())
    board.player_grid[0][0]["ship"] = True
    board.enemy_grid[0][0]["player_hit"] = True
    board.reset_grid()
    assert all(cell["ship"] is False for row in board.player_grid for cell in row)
    assert all(cell["player_hit"] is False for row in board.enemy_grid for cell in row)
    assert board.player.boats == {}
    assert board.enemy.boats == {}
    assert board.placement_complete is False

def test_is_continuous():
    board = Board()
    positions = [(0, 0), (0, 1)]
    new_position = (0, 2)
    assert board.is_continuous(positions, new_position) is True

    new_position = (1, 0)
    assert board.is_continuous(positions, new_position) is False

def test_check_victory():
    player = type("Player", (object,), {"boats": {"boat1": [], "boat2": []}})()
    enemy = type("Enemy", (object,), {"boats": {"boat1": [], "boat2": []}})()
    board = Board(player=player, enemy=enemy)
    assert board.check_victory() == "player"

    enemy.boats = {"boat1": [(0, 0)], "boat2": []}
    assert board.check_victory() is None

    player.boats = {"boat1": [(0, 0)], "boat2": []}
    assert board.check_victory() == "ia"