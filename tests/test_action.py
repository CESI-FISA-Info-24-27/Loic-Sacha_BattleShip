import pytest

from src.game.action import Action
from src.game.player import Player

def test_shoot_hit():
    class MockPlayer:
        def __init__(self, name):
            self.name = name
            self.moves = []

        def record_move(self, X, Y, hit):
            self.moves.append((X, Y, hit))

    player = MockPlayer("Player 1")
    enemy = MockPlayer("Player 2")
    enemy.boats = {"battleship": [(3, 4), (3, 5)]}

    result = Action.shoot(player, enemy, 3, 4)

    assert result is True
    assert (3, 4, True) in player.moves
    assert (3, 4) not in enemy.boats["battleship"]


def test_shoot_miss():
    class MockPlayer:
        def __init__(self, name):
            self.name = name
            self.moves = []

        def record_move(self, X, Y, hit):
            self.moves.append((X, Y, hit))

    player = MockPlayer("Player 1")
    enemy = MockPlayer("Player 2")
    enemy.boats = {"battleship": [(3, 4), (3, 5)]}

    result = Action.shoot(player, enemy, 1, 1)

    assert result is False
    assert (1, 1, False) in player.moves
    assert enemy.boats["battleship"] == [(3, 4), (3, 5)]


def test_shoot_out_of_bounds():
    class MockPlayer:
        def __init__(self, name):
            self.name = name
            self.moves = []

        def record_move(self, X, Y, hit):
            self.moves.append((X, Y, hit))

    player = MockPlayer("Player 1")
    enemy = MockPlayer("Player 2")
    enemy.boats = {"battleship": [(3, 4), (3, 5)]}

    result = Action.shoot(player, enemy, 11, 11)

    assert result is False
    assert len(player.moves) == 0