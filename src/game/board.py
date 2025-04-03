import pygame
import string
from game.button import draw_back_button  # Import directly from button.py
from game.button import reinit_button
from utils.boat_type import BoatType 
import random
from game.ia import AI

class Board:
    """The `Board` class represents the game board for the Battleship game. It manages the player's and enemy's grids, 
    handles boat placement, tracks hits and misses, and facilitates the gameplay logic.
    Attributes:
        rows (int): Number of rows in the grid. Default is 10.
        cols (int): Number of columns in the grid. Default is 10.
        cell_size (int): Size of each cell in pixels. Default is 40.
        player_grid (list): 2D list representing the player's grid. Each cell contains a dictionary with keys:
            - "ai_hit" (bool): Whether the AI has hit this cell.
            - "ship" (bool): Whether a ship occupies this cell.
        enemy_grid (list): 2D list representing the enemy's grid. Each cell contains a dictionary with keys:
            - "player_hit" (bool): Whether the player has hit this cell.
            - "ship" (bool): Whether a ship occupies this cell.
        font (pygame.font.Font): Font used for rendering text on the board.
        order_font (pygame.font.Font): Font used for rendering order-related text.
        title_font (pygame.font.Font): Font used for rendering the title.
        select_font (pygame.font.Font): Font used for rendering selection text.
        button_font (pygame.font.Font): Font used for rendering button text.
        back_button (pygame.Rect): Button for returning to the main menu.
        reinit_button (pygame.Rect): Button for resetting the grid.
        player (Player): The player object.
        enemy (Player): The enemy object.
        ai (AI): The AI object managing the enemy's moves.
        placement_complete (bool): Indicates whether all boats have been placed on the player's grid.
    Methods:
        __init__(self, rows=10, cols=10, cell_size=40, player=None, enemy=None):
            Initializes the board with the specified dimensions, player, and enemy. Sets up the grids and fonts.
        place_enemy_boats(self):
            Randomly places the enemy's boats on the grid, ensuring no overlap and staying within boundaries.
        draw(self, screen):
            Renders the game board, including grids, titles, and buttons, on the given screen.
        _draw_grid(self, screen, margin_x, margin_y, grid, show_ships, show_hits, title):
            Helper method to draw a single grid with optional ship and hit visibility.
        handle_event(self, event):
            Handles user input events for boat placement, shooting, and button interactions.
        place_boat(self, event, player):
            Handles the placement of boats on the player's grid based on user input.
        is_continuous(self, positions, new_position):
            Checks if the given positions form a continuous line (either horizontal or vertical).
        play_turn(self, event):
            Manages the gameplay turn, alternating between the player and the AI.
        check_victory(self):
            Checks if either the player or the AI has won the game by sinking all enemy boats.
        reset_grid(self):
            Resets the game board, clearing all boats and hits, and allowing for a new game setup."""
    def __init__(self, rows=10, cols=10, cell_size=40, player=None, enemy=None):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.player_grid = [[{"ai_hit": False, "ship": False} for _ in range(cols)] for _ in range(rows)]
        self.enemy_grid = [[{"player_hit": False, "ship": False} for _ in range(cols)] for _ in range(rows)]
        self.font = pygame.font.SysFont(None, 24)  # Font for numbers and letters
        self.order_font = pygame.font.SysFont(None, 20)
        self.title_font = pygame.font.SysFont(None, 48)  # Font for the title
        self.select_font = pygame.font.SysFont(None, 40)
        self.button_font = pygame.font.SysFont(None, 30)  # Font for the button
        self.back_button = None  # Back button
        self.reinit_button = None
        self.winner = None
        self.player_hits = 0
        self.ai_hits = 0

        # Assign player and enemy
        self.player = player
        self.enemy = enemy
        self.ai = AI(strategy="smart")  # Choosing the strategy

        # Initialize the placement_complete attribute
        self.placement_complete = False  # Indicates whether all boats have been placed

        # Generate the enemy's grid if it does not already exist
        if self.enemy and not self.enemy.boats:
            self.place_enemy_boats()

    def place_enemy_boats(self):
        """
        Randomly places enemy boats on the game board while ensuring that they do not overlap 
        and remain within the grid boundaries.
        The method attempts to place the following boats:
        - Aircraft Carrier (size 5)
        - Cruiser (size 4)
        - Destroyer (size 3)
        - Submarine (size 3)
        - Torpedo (size 2)
        Each boat is placed by randomly selecting a starting position and direction 
        (horizontal or vertical). The method ensures that the boat's positions are valid 
        (i.e., within the grid and not overlapping with other boats). If a boat cannot be 
        placed after 100 attempts, a ValueError is raised.
        Raises:
            ValueError: If a boat cannot be placed after 100 attempts.
        """
        boats = [
            {"type": BoatType.AIRCRAFT_CARRIER, "size": 5},
            {"type": BoatType.CRUISER, "size": 4},
            {"type": BoatType.DESTROYER, "size": 3},
            {"type": BoatType.SUBMARINE, "size": 3},
            {"type": BoatType.TORPEDO, "size": 2},
        ]

        for boat in boats:
            placed = False
            attempts = 0  # To avoid infinite loops
            while not placed and attempts < 100:  # Limit the number of attempts
                attempts += 1

                # Generate a random starting position
                start_row = random.randint(0, self.rows - 1)
                start_col = random.randint(0, self.cols - 1)

                # Choose a random direction (0 = horizontal, 1 = vertical)
                direction = random.choice([0, 1])

                # Calculate the boat's positions
                positions = []
                for i in range(boat["size"]):
                    if direction == 0:  # Horizontal
                        row, col = start_row, start_col + i
                    else:  # Vertical
                        row, col = start_row + i, start_col

                    # Check if the position is valid
                    if row >= self.rows or col >= self.cols or self.enemy_grid[row][col]["ship"]:
                        break
                    positions.append((row, col))

                # If all positions are valid, place the boat
                if len(positions) == boat["size"]:
                    for row, col in positions:
                        self.enemy_grid[row][col]["ship"] = True  # Mark the grid
                    self.enemy.boats[boat["type"].value] = positions  # Register the boat
                    placed = True

            if not placed:
                raise ValueError(f"Failed to place the boat: {boat['type'].value}")

    def draw(self, screen):
        """
        Draws the game board and UI elements on the screen.
        This method is responsible for rendering the game interface, including the title, 
        player and enemy names, grids, and buttons. It visually represents the player's 
        and enemy's game boards, as well as the current state of the game.
        Args:
            screen (pygame.Surface): The surface on which the game elements will be drawn.
        Elements drawn:
            - Background with a dark gray color.
            - Title of the game at the top center of the screen.
            - Player and enemy names displayed at the top left and top right corners, respectively.
            - Two grids:
                - Left grid: Displays the player's ships and the AI's hits.
                - Right grid: Displays the player's hits on the enemy's ships.
            - A "Reinitialize" button at the bottom center of the screen.
            - A "Back" button at the bottom right of the screen.
        """
        screen.fill((30, 30, 30))  # Dark gray background
        
        # Draw the title
        title = self.title_font.render("Battle Ship Royale - Mode Solo", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 10))

        # Draw player names
        player_text = self.font.render(f"Player: {self.player.name}", True, (255, 255, 255))
        enemy_text = self.font.render(f"Enemy: {self.enemy.name}", True, (255, 255, 255))
        screen.blit(player_text, (10, 60))
        screen.blit(enemy_text, (screen.get_width() - enemy_text.get_width() - 10, 60))

        # Calculate margins for the two grids
        grid_width = self.cols * self.cell_size
        grid_height = self.rows * self.cell_size
        margin_x_left = (screen.get_width() // 4) - (grid_width // 2)
        margin_x_right = (3 * screen.get_width() // 4) - (grid_width // 2)
        margin_y = (screen.get_height() - grid_height) // 2 + 50  # Offset to leave space for the title

        if self.winner == "player":
        # Afficher un message de victoire
            victory_text = self.title_font.render("Victoire ! Vous avez gagné !", True, (255, 255, 255))
            screen.blit(victory_text, (screen.get_width() // 2 - victory_text.get_width() // 2, screen.get_height() // 2 - victory_text.get_height() // 2))
        elif self.winner == "ia":
            # Afficher un message de défaite
            defeat_text = self.title_font.render("Défaite ! L'IA a gagné !", True, (255, 255, 255))
            screen.blit(defeat_text, (screen.get_width() // 2 - defeat_text.get_width() // 2, screen.get_height() // 2 - defeat_text.get_height() // 2))
        else:
            # Draw the left grid (Player's ships and AI's hits)
            self._draw_grid(screen, margin_x_left, margin_y, self.player_grid, show_ships=True, show_hits=True, title="Votre plateau")

            # Draw the right grid (Player's hits on the enemy's ships)
            self._draw_grid(screen, margin_x_right, margin_y, self.enemy_grid, show_ships=False, show_hits=True, title="Plateau ennemi")

        # Draw the reinitialization button
        self.reinit_button = reinit_button(screen, self.order_font, screen.get_width(), screen.get_height() - 50, text="Réinitialiser")

        # Draw the back button
        self.back_button = draw_back_button(screen, self.button_font, screen.get_width(), screen.get_height(), text="Retour")


    def _draw_grid(self, screen, margin_x, margin_y, grid, show_ships, show_hits, title):
        """
        Draws a grid on the given screen with optional visual indicators for ships, hits, and titles.
        Args:
            screen (pygame.Surface): The surface on which the grid will be drawn.
            margin_x (int): The x-coordinate margin for the grid's top-left corner.
            margin_y (int): The y-coordinate margin for the grid's top-left corner.
            grid (list of list of dict): The grid data structure containing cell information.
                Each cell is a dictionary with keys such as "ship", "player_hit", and "ai_hit".
            show_ships (bool): If True, displays ships on the grid.
            show_hits (bool): If True, displays hit markers (crosses or circles) on the grid.
            title (str): The title to display above the grid.
        Grid Cell Dictionary Keys:
            - "ship" (bool): Indicates whether a ship occupies the cell.
            - "player_hit" (bool): Indicates whether the player has hit this cell.
            - "ai_hit" (bool): Indicates whether the AI has hit this cell.
        Visual Elements:
            - Ships are displayed as blue cells if `show_ships` is True.
            - Player hits are displayed as red crosses for hits and white crosses for misses if `show_hits` is True.
            - AI hits are displayed as red circles for hits and white circles for misses.
            - Row numbers are displayed on the left of the grid.
            - Column letters are displayed above the grid.
        Note:
            This method uses the `pygame` library for rendering graphical elements.
        """
        # Draw the grid title
        grid_title = self.font.render(title, True, (255, 255, 255))
        screen.blit(grid_title, (margin_x + (self.cols * self.cell_size) // 2 - grid_title.get_width() // 2, margin_y - 40))

        # Draw the grid
        for row in range(self.rows):
            for col in range(self.cols):
                x = margin_x + col * self.cell_size
                y = margin_y + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                # Draw the background color
                if show_ships and grid[row][col]["ship"]:
                    pygame.draw.rect(screen, (0, 128, 255), rect)  # Blue for ship
                else:
                    pygame.draw.rect(screen, (173, 216, 230), rect)  # Light blue for empty

                # Draw a smaller cross if the cell was hit by the player
                if show_hits and grid[row][col].get("player_hit", False):
                    if grid[row][col]["ship"]:
                        line_color = (255, 0, 0)  # Red for a hit
                    else:
                        line_color = (255, 255, 255)  # White for a miss
                    offset = self.cell_size // 6  # Smaller cross offset
                    pygame.draw.line(screen, line_color, (x + offset, y + offset), (x + self.cell_size - offset, y + self.cell_size - offset), 2)  # Diagonal \
                    pygame.draw.line(screen, line_color, (x + offset, y + self.cell_size - offset), (x + self.cell_size - offset, y + offset), 2)  # Diagonal /

                # Draw a larger circle if the AI hit this cell
                if grid[row][col].get("ai_hit", False):
                    if grid[row][col]["ship"]:
                        circle_color = (255, 0, 0)  # Red for a hit
                    else:
                        circle_color = (255, 255, 255)  # White for a miss
                    center = (x + self.cell_size // 2, y + self.cell_size // 2)
                    radius = self.cell_size // 3  # Larger circle radius
                    pygame.draw.circle(screen, circle_color, center, radius, 2)

                # Draw the cell border
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
        
    def handle_event(self, event):
        """
        Handles events triggered by the user, such as mouse clicks.
        Args:
            event (pygame.event.Event): The event object containing information about the user action.
        Returns:
            str or None: Returns "menu" if the "Back" button is clicked to navigate to the main menu.
                         Returns None for other actions.
        Behavior:
            - If the "Back" button is clicked, the function returns "menu" to indicate a transition to the main menu.
            - If the "Reset" button is clicked, the game grid is reset by calling the `reset_grid` method.
            - If boat placement is complete, the function processes a player's turn by calling the `play_turn` method.
            - If boat placement is not complete, the function handles boat placement by calling the `place_boat` method.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verify if the "Back" button is clicked
            if self.back_button.collidepoint(event.pos):
                return "menu"  # Retour au menu principal

            # Verify if the "Reset" button is clicked
            if self.reinit_button.collidepoint(event.pos):
                self.reset_grid()

            # If boat placement is complete, handle the player's turn
            if self.placement_complete:
                self.play_turn(event)
            else:
                self.place_boat(event, self.player)
        return None
    
    def place_boat(self, event, player):
        """
        Handles the placement of boats on the player's grid during the setup phase of the game.
        This method allows the player to place boats on their grid by clicking on the game board.
        Boats are placed one at a time, and their positions are validated to ensure they are
        continuous and aligned either horizontally or vertically.
        Args:
            event (pygame.event.Event): The Pygame event triggered by the player's interaction,
                        typically a mouse button click.
            player (Player): The player object representing the current player, used to store
                     the boat positions.
        Behavior:
            - Calculates the grid cell based on the mouse click position.
            - Ensures the clicked cell is within the grid boundaries.
            - Initializes the placement of the current boat if not already started.
            - Adds the clicked cell to the current boat's positions if it is valid.
            - Validates that the boat's positions are continuous and aligned.
            - Marks the grid cell as occupied by a ship.
            - Once the current boat is fully placed (all required positions are filled), its
              positions are saved to the player's boat emplacements.
            - Proceeds to the next boat until all boats are placed.
            - Marks the placement phase as complete when all boats are placed.
        Notes:
            - The method relies on the `BoatType` enumeration to determine the boats' names and sizes.
            - The `is_continuous` method is used to validate the continuity of the boat's positions.
            - The `player_grid` attribute is updated to reflect the placement of boats.
            - The `placement_complete` attribute is set to True when all boats are placed.
        Raises:
            None
        """
        if not hasattr(self, "placement_complete") or not self.placement_complete:
            if event.type == pygame.MOUSEBUTTONDOWN:
                grid_width = self.cols * self.cell_size
                grid_height = self.rows * self.cell_size
                margin_x_left = (pygame.display.get_surface().get_width() // 4) - (grid_width // 2)
                margin_y = (pygame.display.get_surface().get_height() - grid_height) // 2 + 50

                x, y = event.pos
                col = (x - margin_x_left) // self.cell_size
                row = (y - margin_y) // self.cell_size

                if 0 <= col < self.cols and 0 <= row < self.rows:
                    if not hasattr(self, "current_boat_index"):
                        self.current_boat_index = 0
                        self.current_boat = {
                            "name": list(BoatType)[self.current_boat_index].name,
                            "positions": [],
                            "size": list(BoatType)[self.current_boat_index].size
                        }

                    if len(self.current_boat["positions"]) == 0:
                        self.current_boat["positions"].append((row, col))
                        self.player_grid[row][col]["ship"] = True
                    else:
                        first_row, first_col = self.current_boat["positions"][0]
                        if (row == first_row or col == first_col) and (row, col) not in self.current_boat["positions"]:
                            if self.player_grid[row][col]["ship"]:
                                return
                            if not self.is_continuous(self.current_boat["positions"], (row, col)):
                                return
                            self.current_boat["positions"].append((row, col))
                            self.player_grid[row][col]["ship"] = True

                    if len(self.current_boat["positions"]) == self.current_boat["size"]:
                        for position in self.current_boat["positions"]:
                            player.set_boat_emplacement(self.current_boat["name"], position[0], position[1])

                        self.current_boat_index += 1
                        if self.current_boat_index < len(BoatType):
                            self.current_boat = {
                                "name": list(BoatType)[self.current_boat_index].name,
                                "positions": [],
                                "size": list(BoatType)[self.current_boat_index].size
                            }
                        else:
                            del self.current_boat
                            del self.current_boat_index
                            self.placement_complete = True
                        
    def is_continuous(self, positions, new_position):
        """
        Determines if a new position, when added to a list of existing positions, 
        forms a continuous line either horizontally or vertically.
        Args:
            positions (list of tuple): A list of tuples representing the existing positions 
                                       on the board. Each tuple contains two integers 
                                       (row, column).
            new_position (tuple): A tuple representing the new position to be added. 
                                  It contains two integers (row, column).
        Returns:
            bool: True if all positions, including the new position, form a continuous 
                  line either horizontally or vertically. False otherwise.
        """
        all_positions = positions + [new_position]
        rows = [pos[0] for pos in all_positions]
        cols = [pos[1] for pos in all_positions]

        # Verify if all positions are in a continuous line
        if len(set(rows)) == 1:  # Même ligne
            return sorted(cols) == list(range(min(cols), max(cols) + 1))
        elif len(set(cols)) == 1:  # Same column
            return sorted(rows) == list(range(min(rows), max(rows) + 1))
        return False
    
    def play_turn(self, event):
        """
        Handles the logic for a single turn in the game, alternating between the player and the AI.
        Parameters:
            event (pygame.event.Event): The event triggered by the player, typically a mouse click.
        Player's Turn:
            - Checks if it's the player's turn to play.
            - Determines the grid cell clicked by the player based on the mouse position.
            - Validates if the clicked cell is within the enemy grid bounds.
            - If the cell has already been targeted, informs the player and ends the turn.
            - If the cell contains an enemy ship, marks it as a hit and notifies the player.
            - If the cell does not contain a ship, marks it as a miss and notifies the player.
            - Ends the player's turn and switches to the AI's turn.
        AI's Turn:
            - Executes the AI's move by selecting a cell on the player's grid.
            - If the selected cell contains a player's ship, marks it as a hit and updates the AI's strategy.
            - If the selected cell does not contain a ship, marks it as a miss and updates the AI's strategy.
            - Ends the AI's turn and switches back to the player's turn.
        Notes:
            - The player's grid and the enemy's grid are represented as 2D arrays of cells.
            - Each cell is a dictionary containing information about whether it contains a ship and whether it has been hit.
            - The AI's behavior is determined by the `choose_move` and `update_last_hit` methods.
        Raises:
            AttributeError: If the `player_turn` attribute is not initialized properly.
        """
        if not hasattr(self, "player_turn"):
            self.player_turn = True 

        if self.player_turn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                grid_width = self.cols * self.cell_size
                grid_height = self.rows * self.cell_size
                margin_x_right = (3 * pygame.display.get_surface().get_width() // 4) - (grid_width // 2)
                margin_y = (pygame.display.get_surface().get_height() - grid_height) // 2 + 50

                x, y = event.pos
                col = (x - margin_x_right) // self.cell_size
                row = (y - margin_y) // self.cell_size

                if 0 <= col < self.cols and 0 <= row < self.rows:
                    cell = self.enemy_grid[row][col]

                    if cell["player_hit"]:
                        print("You have already targeted this cell.")
                        return

                    if cell["ship"]:
                        print(f"Player hit an enemy ship at ({row}, {col})!")
                        cell["player_hit"] = True
                        self.player_hits += 1  # Incrémenter les coups réussis du joueur
                    else:
                        print(f"Player missed at ({row}, {col}).")
                        cell["player_hit"] = True

                    # Vérifier si le joueur a gagné
                    if self.player_hits == 17:
                        self.winner = "player"
                        return  # Arrêter le tour si le joueur a gagné

                    self.player_turn = False

        else:
            print("AI's turn...")
            row, col = self.ai.choose_move(self.player_grid, self.player.boats)
            cell = self.player_grid[row][col]

            if cell["ship"]:
                print(f"The AI hit your ship at ({row}, {col})!")
                cell["ai_hit"] = True
                self.ai_hits += 1  # Incrémenter les coups réussis de l'IA
                self.ai.update_last_hit(row, col, hit=True)
            else:
                print(f"The AI missed at ({row}, {col}).")
                cell["ai_hit"] = True
                self.ai.update_last_hit(row, col, hit=False)

            # Vérifier si l'IA a gagné
            if self.ai_hits == 17:
                self.winner = "ia"
                return  # Arrêter le tour si l'IA a gagné

            self.player_turn = True
        
    def check_victory(self):
        """
        Determines the winner of the game by checking the state of the boats for both players.

        Returns:
            str: Returns "player" if all enemy boats have been destroyed, 
                 "ia" if all player boats have been destroyed, 
                 or None if neither player has won yet.
        """
        if all(len(positions) == 0 for positions in self.enemy.boats.values()):
            self.winner = "player"
            return "player"
        if all(len(positions) == 0 for positions in self.player.boats.values()):
            self.winner = "ia"
            return "ia"
        return None
    
    def reset_grid(self):
        """
        Resets the game board grid to its initial state.

        This method clears the grid by reinitializing it with default values for each cell.
        It also resets the player's and enemy's boats, marks the placement process as incomplete,
        and removes any attributes related to the current boat if they exist.

        Attributes Reset:
        - `self.grid`: A 2D list where each cell is a dictionary with keys:
            - "player_hit": Indicates if the player has hit this cell (default: False).
            - "ai_hit": Indicates if the AI has hit this cell (default: False).
            - "ship": Indicates if a ship occupies this cell (default: False).
        - `self.player.boats`: Cleared dictionary of the player's boats.
        - `self.enemy.boats`: Cleared dictionary of the enemy's boats.
        - `self.placement_complete`: Set to False, indicating that ship placement is not complete.
        - `self.current_boat` and `self.current_boat_index`: Deleted if they exist.

        Prints:
        - A message "Grille réinitialisée !" to indicate the grid has been reset.
        """
        self.grid = [[{"player_hit": False, "ai_hit": False, "ship": False} for _ in range(self.cols)] for _ in range(self.rows)]
        self.player.boats = {}
        self.enemy.boats = {}
        self.placement_complete = False
        if hasattr(self, "current_boat"):
            del self.current_boat
        if hasattr(self, "current_boat_index"):
            del self.current_boat_index  
        print("Grille réinitialisée !")
