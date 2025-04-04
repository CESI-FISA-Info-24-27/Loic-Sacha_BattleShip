import pygame
from utils import Board, Menu
from game.player import Player
from game.multiplayer import MultiplayerBoard  # Nouvelle classe pour le mode multijoueur

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
                elif action == "multiplayer":
                    # Initialisez le mode multijoueur
                    multiplayer_board = MultiplayerBoard(rows=10, cols=10, cell_size=50, player=player)
                    current_screen = "multiplayer"
            elif current_screen == "game":
                action = board.handle_event(event)
                if action == "menu":
                    current_screen = "menu"
            elif current_screen == "multiplayer":
                action = multiplayer_board.handle_event(event)
                if action == "menu":
                    current_screen = "menu"

        # Rendu en fonction de l'écran actuel
        screen.fill((0, 0, 0))  # Fond noir
        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game":
            board.draw(screen)
        elif current_screen == "multiplayer":
            multiplayer_board.draw(screen)

        pygame.display.flip()  # Mettre à jour l'écran

    pygame.quit()

if __name__ == "__main__":
    main()