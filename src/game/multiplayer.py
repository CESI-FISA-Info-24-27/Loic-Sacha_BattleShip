import pygame
from game.board import Board
from utils.battleship_connection import BattleshipConnection  # Importez la classe BattleshipConnection

class MultiplayerBoard(Board):
    """
    Classe pour gérer le mode multijoueur.
    Hérite de la classe Board et utilise BattleshipConnection pour la communication avec le serveur.
    """
    def __init__(self, rows, cols, cell_size, player, port=5000, matchmaking_url="https://rfosse.pythonanywhere.com"):
        super().__init__(rows, cols, cell_size, player=player, enemy=None)
        self.connection = BattleshipConnection(username=player.name, port=port, matchmaking_url=matchmaking_url)
        self.match_code = None  # Code du match pour identifier la partie

    def create_match(self):
        """Crée un match sur le serveur."""
        self.connection.propose_match(target_username=None)  # Crée une partie sans cible spécifique
        self.match_code = self.connection.match_code
        print(f"Partie créée avec succès. Code de la partie : {self.match_code}")

    def join_match(self, code):
        """Rejoindre une partie existante."""
        if self.connection.join_match(match_code=code):
            self.match_code = code
            print(f"Rejoint la partie avec succès. Adversaire : {self.connection.opponent}")

    def send_move(self, row, col):
        """Envoyez un mouvement au serveur."""
        move = (row, col)
        self.connection.send_move(move)
        print(f"Mouvement envoyé : {move}")

    def handle_event(self, event):
        """Gérez les événements pour le mode multijoueur."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.placement_complete:
                # Envoyez le mouvement au serveur
                grid_width = self.cols * self.cell_size
                grid_height = self.rows * self.cell_size
                margin_x = (pygame.display.get_surface().get_width() // 4) - (grid_width // 2)
                margin_y = (pygame.display.get_surface().get_height() - grid_height) // 2 + 50

                x, y = event.pos
                col = (x - margin_x) // self.cell_size
                row = (y - margin_y) // self.cell_size

                if 0 <= col < self.cols and 0 <= row < self.rows:
                    self.send_move(row, col)