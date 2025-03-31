import pygame
from utils import Board, Menu

def main():
    pygame.init()
    screen_width, screen_height = 800, 800
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Battle Ship Royale")

    # Initialization of states
    menu = Menu(screen_width, screen_height)
    board = Board(rows=10, cols=10, cell_size=50, player_name="Rohan FOSSE", enemy_name="IA")
    current_screen = "menu"  # Current screen: "menu" or "game"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Event handling based on the current screen
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "solo":
                    current_screen = "game"
            elif current_screen == "game":
                action = board.handle_event(event)
                if action == "menu":
                    current_screen = "menu"

        # Rendering based on the current screen
        screen.fill((0, 0, 0))  # Black background
        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game":
            board.draw(screen)

        pygame.display.flip()  # Updates the screen

    pygame.quit()

if __name__ == "__main__":
    main()