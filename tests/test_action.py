import pytest
from src.game.action import Action

class MockPlayer:
    def __init__(self, name):
        self.name = name
        self.boats = {}
        self.moves = []

    def record_move(self, X, Y, hit):
        self.moves.append((X, Y, hit))

@pytest.fixture
def setup_players():
    player = MockPlayer("Player 1")
    enemy = MockPlayer("Enemy")
    enemy.boats = {
        "Battleship": [(3, 4), (3, 5), (3, 6)],
        "Destroyer": [(7, 8), (7, 9)]
    }
    return player, enemy

def test_shoot_hit(setup_players):
    player, enemy = setup_players
    result = Action.shoot(player, enemy, 3, 4)
    assert result is True
    assert (3, 4, True) in player.moves
    assert (3, 4) not in enemy.boats["Battleship"]

def test_shoot_miss(setup_players):
    player, enemy = setup_players
    result = Action.shoot(player, enemy, 1, 1)
    assert result is False
    assert (1, 1, False) in player.moves

def test_shoot_out_of_bounds(setup_players):
    player, enemy = setup_players
    result = Action.shoot(player, enemy, 11, 5)
    assert result is False
    assert (11, 5, False) not in player.moves