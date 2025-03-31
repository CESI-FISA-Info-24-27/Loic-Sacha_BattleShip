# This file is intentionally left blank.
from game.player import Player
from game.action import Action

player1 = Player("Alice")
player2 = Player("Rachid")

player1.set_boat_emplacement("Destroyer", 2, 3)
player2.set_boat_emplacement("Destroyer", 2, 4)

print(player1.name)
print(player2.name)

print(player1.boats)
print(player2.boats)

Action.shoot(player1, player2, 2, 4)
Action.shoot(player2, player1, 2, 3)

print(player1.move_historic)
print(player2.move_historic)