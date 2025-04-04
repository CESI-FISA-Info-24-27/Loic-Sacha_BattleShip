import pygame
from utils import Board, Menu
from game.player import Player
from game.multiplayer import MultiplayerBoard  # Nouvelle classe pour le mode multijoueur
import time

def main():
    pygame.init()
    screen_width, screen_height = 1200, 800
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Battle Ship Royale")

    # Créez les joueurs
    player = Player(name="Loïc SERRE")
    enemy = Player(name="Enemy")

    # Initialisez les états
    menu = Menu(screen_width, screen_height)
    board = Board(rows=10, cols=10, cell_size=50, player=player, enemy=enemy)
    multiplayer_board = None  # Instance pour le mode multijoueur
    current_screen = "menu"  # Écran actuel : "menu", "game", ou "multiplayer"
    is_waiting_for_opponent = False  # Indicateur pour l'attente d'un adversaire
    last_check_time = time.time()  # Dernière vérification de l'état de la partie

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gérer les événements en fonction de l'écran actuel
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "solo":
                    current_screen = "game"
                elif action == "connect":
                    # Connectez le joueur au serveur
                    multiplayer_board = MultiplayerBoard(rows=10, cols=10, cell_size=50, player=player)
                    multiplayer_board.register_player()
                    current_screen = "multiplayer_menu"
                elif action == "rules":
                    menu.show_rules = True
                elif action == "quit":
                    running = False
            elif current_screen == "multiplayer_menu":
                action = menu.handle_event(event)
                if action == "create_match":
                    multiplayer_board.create_match()
                    is_waiting_for_opponent = True
                    current_screen = "multiplayer"
                elif action == "join_match":
                    match_code = input("Entrez le code de la partie : ")
                    multiplayer_board.join_match(match_code)
                    is_waiting_for_opponent = True
                    current_screen = "multiplayer"
                elif action == "menu":
                    current_screen = "menu"
            elif current_screen == "multiplayer":
                if not is_waiting_for_opponent:
                    action = multiplayer_board.handle_event(event)
                    if action == "menu":
                        current_screen = "menu"

        # Vérifiez l'état de la partie toutes les 2 secondes
        if current_screen == "multiplayer" and is_waiting_for_opponent:
            if time.time() - last_check_time > 2:  # Vérifiez toutes les 2 secondes
                last_check_time = time.time()
                if multiplayer_board.check_match_status():  # Vérifie si l'adversaire a rejoint
                    is_waiting_for_opponent = False  # Arrête l'attente

        # Rendu en fonction de l'écran actuel
        screen.fill((0, 0, 0))  # Fond noir
        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game":
            board.draw(screen)
        elif current_screen == "multiplayer_menu":
            menu.draw(screen)
        elif current_screen == "multiplayer":
            multiplayer_board.draw(screen)

        pygame.display.flip()  # Mettre à jour l'écran

    pygame.quit()

if __name__ == "__main__":
    main()