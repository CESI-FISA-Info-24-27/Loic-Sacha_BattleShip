import pygame
import string
from game.button import draw_back_button  # Import directly from button.py

class Board:
    def __init__(self, rows=10, cols=10, cell_size=40, player_name="Joueur", enemy_name="Adversaire"):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]  # 0 = empty, 1 = ship, 2 = hit, 3 = miss
        self.font = pygame.font.SysFont(None, 24)  # Font for numbers and letters
        self.title_font = pygame.font.SysFont(None, 48)  # Font for the title
        self.button_font = pygame.font.SysFont(None, 30)  # Font for the button
        self.player_name = player_name
        self.enemy_name = enemy_name
        self.back_button = None  # Back button

    def draw(self, screen):
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
        """Handles events for the back button."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "menu"  # Return to the main menu
        return None