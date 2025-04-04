import pygame
import requests
from game.board import Board

class MultiplayerBoard(Board):
    """
    Classe pour gérer le mode multijoueur.
    Hérite de la classe Board et ajoute des fonctionnalités pour la communication avec le serveur.
    """
    def __init__(self, rows, cols, cell_size, player):
        super().__init__(rows, cols, cell_size, player=player, enemy=None)
        self.server_url = "https://rfosse.pythonanywhere.com:5000"  # Adresse du serveur Flask
        self.match_code = None  # Code du match pour identifier la partie

    def create_match(self):
        """Crée un match sur le serveur."""
        url = f"{self.server_url}/create_match"
        data = {"player_id": self.player.name, "code": None}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.match_code = response.json().get("code")
            print(f"Match créé avec le code : {self.match_code}")
        else:
            print(f"Erreur lors de la création du match : {response.json()}")

    def join_match(self, code):
        """Rejoignez un match existant."""
        url = f"{self.server_url}/join_match"
        data = {"player_id": self.player.name, "code": code}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Rejoint le match avec le code : {code}")
        else:
            print(f"Erreur lors de la connexion au match : {response.json()}")

    def send_move(self, row, col):
        """Envoyez un mouvement au serveur."""
        url = f"{self.server_url}/send_move"
        data = {"match_code": self.match_code, "player_id": self.player.name, "row": row, "col": col}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Mouvement envoyé : ({row}, {col})")
        else:
            print(f"Erreur lors de l'envoi du mouvement : {response.json()}")

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