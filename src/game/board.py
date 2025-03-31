import pygame
import string
from game.button import draw_back_button  # Import directly from button.py
from game.player import Player

class Board:
    """
    Represents the game board for the Battleship game.
    Attributes:
        rows (int): Number of rows in the grid. Default is 10.
        cols (int): Number of columns in the grid. Default is 10.
        cell_size (int): Size of each cell in pixels. Default is 40.
        grid (list): 2D list representing the state of the grid. 
            0 = empty, 1 = ship, 2 = hit, 3 = miss.
        font (pygame.font.Font): Font used for rendering numbers and letters.
        title_font (pygame.font.Font): Font used for rendering the title.
        button_font (pygame.font.Font): Font used for rendering the back button.
        player_name (str): Name of the player. Default is "Joueur".
        enemy_name (str): Name of the enemy. Default is "Adversaire".
        back_button (pygame.Rect): Rect object representing the back button.
    Methods:
        __init__(rows=10, cols=10, cell_size=40, player_name="Joueur", enemy_name="Adversaire"):
            Initializes the Board object with the specified dimensions, cell size, and player names.
        draw(screen):
            Draws the grid, player names, and other game information on the screen.
        handle_event(event):
            Handles events for the back button. Returns "menu" if the back button is clicked.
    """
    def __init__(self, rows=10, cols=10, cell_size=40, player_name="Joueur", enemy_name="Adversaire"):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]  # 0 = empty, 1 = ship, 2 = hit, 3 = miss
        self.font = pygame.font.SysFont(None, 24)  # Font for numbers and letters
        self.title_font = pygame.font.SysFont(None, 48)  # Font for the title
        self.select_font = pygame.font.SysFont(None, 40)
        self.button_font = pygame.font.SysFont(None, 30)  # Font for the button
        self.player_name = player_name
        self.enemy_name = enemy_name
        self.back_button = None  # Back button
        
        self.player = Player(self.player_name)

    def draw(self, screen):
        """
        Draws the game board, grid, and related information on the screen.
        This method handles rendering the game interface, including the title, player names,
        the grid with its cells, row numbers, column letters, and a back button.
        Args:
            screen (pygame.Surface): The surface on which to draw the game elements.
        The following elements are drawn:
            - A dark gray background.
            - The game title centered at the top of the screen.
            - Player and enemy names displayed at the top corners.
            - A grid representing the game board, with cells color-coded based on their state:
                - Light blue for empty cells.
                - Green for cells containing a ship.
                - Red for cells that have been hit.
                - Gray for cells that have been missed.
            - Row numbers displayed to the left of the grid.
            - Column letters displayed above the grid.
            - A back button at the bottom of the screen.
        """
        """Draws the grid and game information on the screen."""
        screen.fill((30, 30, 30))  # Dark gray background

        # Draw the title
        title = self.title_font.render("Battle Ship Royale - Mode Solo", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 10))

        # Draw player names
        player_text = self.font.render(f"Player: {self.player_name}", True, (255, 255, 255))
        enemy_text = self.font.render(f"Enemy: {self.enemy_name}", True, (255, 255, 255))
        screen.blit(player_text, (10, 60))
        screen.blit(enemy_text, (screen.get_width() - enemy_text.get_width() - 10, 60))

        if sum(len(coords) for coords in self.player.boats.values()) < 20:
            chose_emplacement = self.select_font.render("Cliquez sur la grille pour placer vos navires.", True, (255, 255, 255))
            screen.blit(chose_emplacement, (screen.get_width() // 2 - chose_emplacement.get_width() // 2, 110))

        # Calculate margins to center the grid
        grid_width = self.cols * self.cell_size
        grid_height = self.rows * self.cell_size
        margin_x = (screen.get_width() - grid_width) // 2
        margin_y = (screen.get_height() - grid_height) // 2 + 50  # Offset to leave space for the title

        # Draw the grid
        for row in range(self.rows):
            for col in range(self.cols):
                x = margin_x + col * self.cell_size
                y = margin_y + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                # Cell color based on its state
                if self.grid[row][col] == 0:  # Empty
                    color = (173, 216, 230)  # Light blue
                elif self.grid[row][col] == 1:  # Ship
                    color = (0, 128, 0)  # Green
                elif self.grid[row][col] == 2:  # Hit
                    color = (255, 0, 0)  # Red
                elif self.grid[row][col] == 3:  # Miss
                    color = (169, 169, 169)  # Gray

                pygame.draw.rect(screen, color, rect)  # Fill the cell
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black border

        # Draw row numbers (on the left)
        for row in range(self.rows):
            text = self.font.render(str(row), True, (255, 255, 255))  # White
            screen.blit(text, (margin_x - 20, margin_y + row * self.cell_size + self.cell_size // 4))

        # Draw column letters (on top)
        for col in range(self.cols):
            letter = string.ascii_uppercase[col]  # Convert index to letter (A, B, C, ...)
            text = self.font.render(letter, True, (255, 255, 255))  # White
            screen.blit(text, (margin_x + col * self.cell_size + self.cell_size // 4, margin_y - 20))

        # Draw the back button
        self.back_button = draw_back_button(screen, self.button_font, screen.get_width(), screen.get_height())

    def handle_event(self, event):
        """
        Handles the event for the back button.

        This method checks if a mouse button down event occurs and if the 
        back button is clicked. If the back button is clicked, it triggers 
        a return to the main menu.

        Args:
            event (pygame.event.Event): The event to handle, typically a 
            mouse event.

        Returns:
            str or None: Returns "menu" if the back button is clicked, 
            otherwise returns None.
        """
        """Handles events for the back button."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "menu"  # Return to the main menu
            self.place_boat(event, self.player)
        return None
    
    def place_boat(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Calculer la position du clic dans la grille
            grid_width = self.cols * self.cell_size
            grid_height = self.rows * self.cell_size
            margin_x = (pygame.display.get_surface().get_width() - grid_width) // 2
            margin_y = (pygame.display.get_surface().get_height() - grid_height) // 2 + 50

            x, y = event.pos
            col = (x - margin_x) // self.cell_size
            row = (y - margin_y) // self.cell_size

            if 0 <= col < self.cols and 0 <= row < self.rows:
                # Vérifie si la case est vide avant d'ajouter un bateau
                if self.grid[row][col] == 0:
                    self.grid[row][col] = 1  # Marquer comme bateau
                    player.set_boat_emplacement(f"Bateau{len(player.boats) + 1}", col + 1, row + 1)
