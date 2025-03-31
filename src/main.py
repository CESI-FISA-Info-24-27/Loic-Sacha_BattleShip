import pygame
from utils import Board, Menu

def main():
    """
    Main function to initialize and run the Battle Ship Royale game.
    This function sets up the game environment, including initializing Pygame, 
    creating the game window, and managing the game loop. It handles switching 
    between the menu and game screens, processes user input, and updates the 
    display accordingly.
    Functions:
    - Initializes Pygame and creates a resizable game window.
    - Manages the game loop, handling events and rendering the appropriate screen.
    - Switches between the "menu" and "game" states based on user actions.
    - Cleans up and quits Pygame when the game loop ends.
    Screens:
    - "menu": Displays the main menu and handles menu interactions.
    - "game": Displays the game board and handles gameplay interactions.
    Attributes:
    - screen_width (int): Width of the game window.
    - screen_height (int): Height of the game window.
    - menu (Menu): Instance of the Menu class for the main menu.
    - board (Board): Instance of the Board class for the game board.
    - current_screen (str): Tracks the current screen ("menu" or "game").
    - running (bool): Controls the main game loop.
    Event Handling:
    - QUIT: Exits the game.
    - Menu events: Switches to the game screen when "solo" is selected.
    - Game events: Switches back to the menu screen when "menu" is selected.
    Rendering:
    - Clears the screen with a black background.
    - Draws the menu or game board based on the current screen.
    Exits:
    - Ends the game loop and quits Pygame when the user closes the window.
    """
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