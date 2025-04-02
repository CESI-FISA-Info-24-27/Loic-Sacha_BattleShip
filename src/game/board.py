import pygame
import string
from game.button import draw_back_button  # Import directly from button.py
from game.button import reinit_button
from utils.boat_type import BoatType 
import random

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
    def __init__(self, rows=10, cols=10, cell_size=40, player=None, enemy=None):
        """Initializes the game board.
            rows (int, optional): Number of rows in the grid. Defaults to 10.
            cols (int, optional): Number of columns in the grid. Defaults to 10.
            cell_size (int, optional): Size of each cell in pixels. Defaults to 40.
            player (Player, optional): Object representing the player. Defaults to None.
            enemy (Player, optional): Object representing the enemy. Defaults to None.
        Attributes:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
            cell_size (int): Size of each cell in pixels.
            grid (list): 2D list representing the game grid. 
                         0 = empty, 1 = ship, 2 = hit, 3 = miss.
            font (pygame.font.Font): Font used for numbers and letters.
            title_font (pygame.font.Font): Font used for the title.
            select_font (pygame.font.Font): Font used for selection text.
            button_font (pygame.font.Font): Font used for button text.
            back_button (None or pygame.Rect): Back button object, initialized as None.
            player (Player): The player object.
            enemy (Player): The enemy object.
            placement_complete (bool): Indicates whether all ships have been placed. Defaults to False.
        Notes:
            If the enemy object is provided and does not already have boats, 
            the `place_enemy_boats` method is called to generate the enemy's grid.

        Args:
            rows (int, optional): _description_. Defaults to 10.
            cols (int, optional): _description_. Defaults to 10.
            cell_size (int, optional): _description_. Defaults to 40.
            player (_type_, optional): _description_. Defaults to None.
            enemy (_type_, optional): _description_. Defaults to None.
        """
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[{"player_hit": False, "ai_hit": False, "ship": False} for _ in range(cols)] for _ in range(rows)]  # 0 = empty, 1 = ship, 2 = hit, 3 = miss
        self.font = pygame.font.SysFont(None, 24)  # Font for numbers and letters
        self.order_font = pygame.font.SysFont(None, 20)
        self.title_font = pygame.font.SysFont(None, 48)  # Font for the title
        self.select_font = pygame.font.SysFont(None, 40)
        self.button_font = pygame.font.SysFont(None, 30)  # Font for the button
        self.back_button = None  # Back button
        self.reinit_button = None

        # Assign player and enemy
        self.player = player
        self.enemy = enemy

        # Initialize the placement_complete attribute
        self.placement_complete = False  # Indicates whether all boats have been placed
        self.first_shot = True

        # Generate the enemy's grid if it does not already exist
        if self.enemy and not self.enemy.boats:
            self.place_enemy_boats()

    def place_enemy_boats(self):
        """
        Places enemy boats randomly on the game board.
        This method generates random positions and orientations for each type of 
        enemy boat and ensures that they are placed without overlapping or going 
        out of bounds. The boats are stored in the `self.enemy.boats` dictionary.
        The boats to be placed are:
            - Aircraft Carrier (size 5)
            - Cruiser (size 4)
            - Destroyer (size 3)
            - Submarine (size 3)
            - Torpedo (size 2)
        The placement process involves:
            1. Randomly selecting a starting position on the board.
            2. Randomly choosing a direction (horizontal or vertical).
            3. Validating that the boat fits within the board boundaries and does 
               not overlap with other boats.
            4. Storing the boat's positions if placement is valid.
        Raises:
            ValueError: If the board dimensions or boat configurations are invalid.
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
            while not placed:
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
                    if row >= self.rows or col >= self.cols or any((row, col) in b for b in self.enemy.boats.values()):
                        break
                    positions.append((row, col))

                # If all positions are valid, place the boat
                if len(positions) == boat["size"]:
                    self.enemy.boats[boat["type"].value] = positions  # Register the boat
                    placed = True

    def draw(self, screen):
        """
        Draws the game board and UI elements on the provided screen.
        Args:
            screen (pygame.Surface): The surface on which to draw the game board and UI.
        The method performs the following tasks:
        - Fills the screen with a dark gray background.
        - Displays the game title at the top of the screen.
        - Shows the names of the player and the enemy.
        - Displays a message indicating whether all boats have been placed or prompts the user to place the current boat.
        - Centers and draws the game grid, with cell colors representing their states:
            - Light blue for empty cells.
            - Green for cells containing ships.
            - Red for hit cells.
            - Gray for missed cells.
        - Adds row numbers on the left side of the grid.
        - Adds column letters on top of the grid.
        - Draws a back button at the bottom of the screen.
        Note:
            - The method assumes the existence of attributes such as `title_font`, `font`, `select_font`, `player`, 
              `enemy`, `placement_complete`, `current_boat`, `cols`, `rows`, `cell_size`, and `grid`.
            - The `draw_back_button` function is used to render the back button.
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
        order_lines = [
            "Ordre :",
            "",
            "Aircraft Carrier (taille : 5)",
            "Cruiser (taille : 4)",
            "Destroyer (taille : 3)",
            "Submarine (taille : 3)",
            "Torpedo (taille : 2)"
        ]

        y_pos = screen.get_height() * 0.5

        for line in order_lines:
            order_text = self.order_font.render(line, True, (255, 255, 255))
            x_pos = screen.get_width() * (7/8) - order_text.get_width() * 0.5
            screen.blit(order_text, (x_pos, y_pos))
            y_pos += order_text.get_height() + 5
        
        historic = self.player.move_historic

        for line in historic:
            historic_text = self.order_font.render(line, True, (255, 255, 255))
            x_pos = screen.get_width() * (1/8) - historic_text.get_width() * 0.5
            screen.blit(historic_text, (x_pos, y_pos))
            y_pos += historic_text.get_height() + 5


        # Display the current boat being placed or completion message
        if hasattr(self, "placement_complete") and self.placement_complete and self.first_shot:
            completion_message = self.select_font.render("Tous les bateaux ont été placés !", True, (0, 255, 0))
            screen.blit(completion_message, (screen.get_width() // 2 - completion_message.get_width() // 2, 110))
        elif hasattr(self, "current_boat") and not self.placement_complete:
            boat_info = self.select_font.render(
                f"Placer le bateau : {self.current_boat['name']} (taille : {self.current_boat['size']})",
                True,
                (255, 255, 255)
            )
            screen.blit(boat_info, (screen.get_width() // 2 - boat_info.get_width() // 2, 110))
            
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

                # Draw the background color
                if self.grid[row][col]["ship"]:
                    pygame.draw.rect(screen, (0, 128, 255), rect)  # Blue for ship
                else:
                    pygame.draw.rect(screen, (173, 216, 230), rect)  # Light blue for empty

                # Draw a cross if the player hit this cell
                if self.grid[row][col]["player_hit"]:
                    line_color = self.grid[row][col].get("hit_color", (255, 255, 255))  # Default to white
                    pygame.draw.line(screen, line_color, (x, y), (x + self.cell_size, y + self.cell_size), 3)  # Diagonal \
                    pygame.draw.line(screen, line_color, (x, y + self.cell_size), (x + self.cell_size, y), 3)  # Diagonal /

                # Draw a circle if the AI hit this cell
                if self.grid[row][col]["ai_hit"]:
                    if self.grid[row][col]["ship"]:
                        circle_color = (255, 0, 0)  # Red for a hit
                    else:
                        circle_color = (255, 255, 255)  # White for a miss
                    center = (x + self.cell_size // 2, y + self.cell_size // 2)
                    radius = self.cell_size // 4
                    pygame.draw.circle(screen, circle_color, center, radius, 3)

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

        # Draw the back button
        self.reinit_button = reinit_button(screen, self.order_font, screen.get_width(), screen.get_height() - 50)
        self.back_button = draw_back_button(screen, self.button_font, screen.get_width(), screen.get_height())

    def handle_event(self, event):
        """
        Handles events triggered during the game.
        Args:
            event (pygame.event.Event): The event to handle, typically triggered by user interaction.
        Returns:
            str or None: Returns "menu" if the back button is clicked to navigate to the main menu.
                         Returns None if no specific action is required.
        Behavior:
            - If the back button is clicked, the function returns "menu" to indicate a transition to the main menu.
            - If the boat placement phase is complete, it delegates the event to the `play_turn` method to handle the player's turn.
            - If the boat placement phase is not complete, it delegates the event to the `place_boat` method to handle boat placement.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "menu"  # Return to the main menu
            
            if self.reinit_button.collidepoint(event.pos):
                self.reset_grid()

            # If the boat placement is complete, start the game
            if self.placement_complete:
                self.play_turn(event)
            else:
                self.place_boat(event, self.player)
        return None
    
    def place_boat(self, event, player):
        """
        Handles the placement of boats on the game board.
        This method allows the player to place boats on the grid by clicking on the desired cells.
        It ensures that boats are placed according to the rules, such as alignment, continuity, 
        and avoiding overlap with other boats.
        Args:
            event (pygame.event.Event): The event triggered by the player's interaction, 
                                        typically a mouse click.
            player (Player): The player object to which the boats belong. This is used to 
                             register the boat positions.
        Rules for boat placement:
            - Boats must be placed either horizontally or vertically.
            - Boat positions must be continuous.
            - Boats cannot overlap with each other.
            - Each boat has a predefined size and must occupy the exact number of cells.
        Behavior:
            - The method tracks the current boat being placed and its positions.
            - Once a boat is fully placed, its positions are registered with the player.
            - The method proceeds to the next boat until all boats are placed.
            - When all boats are placed, the placement phase is marked as complete.
        Notes:
            - The grid is represented as a 2D array where cells with a value of 1 indicate 
              occupied positions.
            - The method uses attributes `current_boat` and `current_boat_index` to track 
              the placement progress.
            - The `placement_complete` attribute is set to True when all boats are placed.
        Raises:
            ValueError: If a position is invalid due to overlap or discontinuity.
        """
        
        # List of boats with their sizes
        boats = [
        {"type": BoatType.AIRCRAFT_CARRIER, "size": 5},  # 1 bateau de taille 5
        {"type": BoatType.CRUISER, "size": 4},           # 1 bateau de taille 4
        {"type": BoatType.DESTROYER, "size": 3},         # 1er bateau de taille 3
        {"type": BoatType.SUBMARINE, "size": 3},         # 2e bateau de taille 3
        {"type": BoatType.TORPEDO, "size": 2},           # 1 bateau de taille 2
    ]

        if not hasattr(self, "placement_complete") or not self.placement_complete:
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
                    # Vérifiez si un bateau est en cours de placement
                    if not hasattr(self, "current_boat_index"):
                        self.current_boat_index = 0  # Index du bateau à placer
                        self.current_boat = {
                            "name": boats[self.current_boat_index]["type"].value,
                            "positions": [],
                            "size": boats[self.current_boat_index]["size"]
                        }

                    # Ajouter la position si elle est valide
                    if len(self.current_boat["positions"]) == 0:
                        # Première position
                        self.current_boat["positions"].append((row, col))
                        self.grid[row][col]["ship"] = True
                    else:
                        # Vérifiez que la position est alignée avec les précédentes
                        first_row, first_col = self.current_boat["positions"][0]
                        if (row == first_row or col == first_col) and (row, col) not in self.current_boat["positions"]:
                            # Vérifiez qu'il n'y a pas de chevauchement
                            if self.grid[row][col]["ship"]:
                                return

                            # Vérifiez que toutes les positions sont continues
                            if not self.is_continuous(self.current_boat["positions"], (row, col)):
                                return

                            # Ajouter la position
                            self.current_boat["positions"].append((row, col))
                            self.grid[row][col]["ship"] = True

                    # Vérifiez si le bateau est complètement placé
                    if len(self.current_boat["positions"]) == self.current_boat["size"]:
                        # Enregistrez chaque position du bateau
                        for position in self.current_boat["positions"]:
                            player.set_boat_emplacement(self.current_boat["name"], position[0], position[1])

                        self.current_boat_index += 1  # Passez au bateau suivant

                        # Vérifiez s'il reste des bateaux à placer
                        if self.current_boat_index < len(boats):
                            self.current_boat = {
                                "name": boats[self.current_boat_index]["type"].value,
                                "positions": [],
                                "size": boats[self.current_boat_index]["size"]
                            }
                        else:
                            # Tous les bateaux ont été placés
                            del self.current_boat
                            del self.current_boat_index
                            self.placement_complete = True  # Mark placement as complete

            # Display the boat currently being placed
            if not hasattr(self, "current_boat_index"):
                self.current_boat_index = 0  # Index du bateau à placer
                self.current_boat = {"name": boats[self.current_boat_index]["type"].value, "positions": [], "size": boats[self.current_boat_index]["size"]}

    def is_continuous(self, positions, new_position):
        """
        Check if a new position, when added to a list of existing positions, forms a continuous line
        either horizontally or vertically.
        Args:
            positions (list of tuple): A list of tuples representing the existing positions on the board.
                                       Each tuple contains two integers (row, column).
            new_position (tuple): A tuple representing the new position to be added, containing two integers (row, column).
        Returns:
            bool: True if the new position, along with the existing positions, forms a continuous line
                  either horizontally or vertically. False otherwise.
        """
        all_positions = positions + [new_position]
        rows = [pos[0] for pos in all_positions]
        cols = [pos[1] for pos in all_positions]

        # Vérifiez si toutes les positions sont sur la même ligne ou la même colonne
        if len(set(rows)) == 1:  # Même ligne
            return sorted(cols) == list(range(min(cols), max(cols) + 1))
        elif len(set(cols)) == 1:  # Même colonne
            return sorted(rows) == list(range(min(rows), max(rows) + 1))
        return False
    
    def play_turn(self, event):
        """
        Handles the logic for a single turn in the game, alternating between the player and the AI.
        Parameters:
            event (pygame.event.Event): The event triggered by the player, typically a mouse click.
        Player Turn:
            - Checks if it's the player's turn.
            - Detects the grid cell clicked by the player based on the mouse position.
            - Validates if the cell has already been targeted.
            - Determines if the player's shot hits an enemy ship or misses.
            - Updates the game grid and switches the turn to the AI.
        AI Turn:
            - Randomly selects a grid cell to target.
            - Validates if the cell has already been targeted.
            - Determines if the AI's shot hits a player's ship or misses.
            - Updates the game grid and switches the turn back to the player.
        Grid Cell States:
            - 2: Indicates a hit on a ship.
            - 3: Indicates a missed shot.
        Notes:
            - The player's and AI's ships are stored in `self.player.boats` and `self.enemy.boats`, respectively.
            - The game grid is represented by `self.grid`.
            - The player's turn is tracked using `self.player_turn`.
        Returns:
            None
        """
        if not hasattr(self, "player_turn"):
            self.player_turn = True  # The player starts

        if self.player_turn:
            # Player's turn
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Calculer la position du clic dans la grille
                grid_width = self.cols * self.cell_size
                grid_height = self.rows * self.cell_size
                margin_x = (pygame.display.get_surface().get_width() - grid_width) // 2
                margin_y = (pygame.display.get_surface().get_height() - grid_height) // 2 + 50

                x, y = event.pos
                col = (x - margin_x) // self.cell_size
                row = (y - margin_y) // self.cell_size

                # Vérifier si le clic est dans les limites de la grille
                if 0 <= col < self.cols and 0 <= row < self.rows:
                    cell = self.grid[row][col]

                    # Check if the player has already hit this cell
                    if cell["player_hit"]:
                        print("You have already targeted this cell.")
                        return

                    # Check if an enemy ship is hit
                    if cell["ship"]:
                        # Vérifiez si le bateau appartient à l'ennemi
                        if any((row, col) in positions for positions in self.enemy.boats.values()):
                            print(f"Player hit an enemy ship at ({row}, {col})!")
                            cell["player_hit"] = True
                            cell["hit_color"] = (255, 0, 0)  # Rouge pour un bateau ennemi touché
                        else:
                            print(f"Player hit their own ship at ({row}, {col})!")
                            cell["player_hit"] = True
                            cell["hit_color"] = (255, 255, 255)  # Blanc pour un bateau allié touché
                    else:
                        print(f"Player missed at ({row}, {col}).")
                        cell["player_hit"] = True
                        cell["hit_color"] = (255, 255, 255)  # Blanc pour un tir manqué

                    # Marquer que le premier tir a été effectué
                    self.first_shot = False

                    # Passer au tour de l'IA immédiatement
                    self.player_turn = False
                    self.ai_turn()

        else:
            # AI's turn
            print("AI's turn...")
            while True:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                cell = self.grid[row][col]

                # Check if the AI has already hit this cell
                if cell["ai_hit"]:
                    continue

                # Check if a player's ship is hit
                if cell["ship"]:
                    print(f"The AI hit your ship at ({row}, {col})!")
                    cell["ai_hit"] = True
                else:
                    print(f"The AI missed at ({row}, {col}).")
                    cell["ai_hit"] = True

                # Switch to the player's turn
                self.player_turn = True
                break
    
    def check_victory(self):
        """
        Determines the winner of the game by checking if all boats of either the player
        or the enemy have been destroyed.

        Returns:
            str: "player" if the enemy has no remaining boats,
                 "ia" if the player has no remaining boats,
                 None if neither has lost all their boats yet.
        """
        if all(len(positions) == 0 for positions in self.enemy.boats.values()):
            return "player"
        if all(len(positions) == 0 for positions in self.player.boats.values()):
            return "ia"
        return None
    
    def reset_grid(self):
        self.grid = [[{"player_hit": False, "ai_hit": False, "ship": False} for _ in range(self.cols)] for _ in range(self.rows)]
        self.player.boats = {}
        self.enemy.boats = {}
        self.placement_complete = False
        if hasattr(self, "current_boat"):
            del self.current_boat
        if hasattr(self, "current_boat_index"):
            del self.current_boat_index  
        print("Grille réinitialisée !")

    def ai_turn(self):
        """
        Handles the AI's turn by randomly selecting a cell to target.
        """
        while True:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            cell = self.grid[row][col]

            # Check if the AI has already hit this cell
            if cell["ai_hit"]:
                continue

            # Check if a player's ship is hit
            if cell["ship"]:
                print(f"The AI hit your ship at ({row}, {col})!")
                cell["ai_hit"] = True
            else:
                print(f"The AI missed at ({row}, {col}).")
                cell["ai_hit"] = True

            # Switch back to the player's turn
            self.player_turn = True
            break