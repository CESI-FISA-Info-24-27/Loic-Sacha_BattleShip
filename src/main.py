import pygame
from utils import Board, Menu
from game.player import Player

def main():
    """
    The main function initializes the game and handles the main game loop.
    This function sets up the Pygame environment, creates the game window, and initializes
    the game state, including the menu and game board. It manages the event loop, switching
    between the menu and game screens based on user input, and renders the appropriate screen
    content.
    Key Components:
    - Initializes Pygame and creates a resizable game window.
    - Sets up the player and enemy objects.
    - Manages the game state, switching between "menu" and "game" screens.
    - Handles user input events for both the menu and game screens.
    - Updates the display and ensures a smooth game loop.
    The game loop continues running until the user closes the game window.
    Note:
    - The function assumes the existence of `Player`, `Menu`, and `Board` classes with
      appropriate methods (`handle_event` and `draw`) to manage their respective functionalities.
    """
    pygame.init()
    screen_width, screen_height = 1200, 800
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Battle Ship")

    # Create players
    player = Player(name="Rohan FOSSE")
    enemy = Player(name="IA")

    # Initialize state
    menu = Menu(screen_width, screen_height)
    board = Board(rows=10, cols=10, cell_size=50, player=player, enemy=enemy)
    current_screen = "menu"  # Current screen: "menu" or "game"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle events based on the current screen
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "solo":
                    current_screen = "game"
                    menu.play_music(menu.ingame_music)  # Switch to in-game music
            elif current_screen == "game":
                action = board.handle_event(event)
                if action == "menu":
                    current_screen = "menu"
                    menu.play_music(menu.menu_music)  # Switch back to menu music

        # Render based on the current screen
        screen.fill((0, 0, 0))  # Black background
        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game":
            board.draw(screen)

        pygame.display.flip()  # Update the screen

    pygame.quit()

if __name__ == "__main__":
    main()