import random

class AI:
    """
    Class representing the AI for the Battleship game.
    Implements a strategy combining Hunt/Target, parity, probability density, and advanced logic.
    """
    def __init__(self, strategy="smart"):
        """
        Initializes the AI with a given strategy.

        Args:
            strategy (str): The strategy to use ("random", "targeted", "smart").
        """
        self.strategy = strategy
        self.shots = []  # List of shots already made
        self.hits = []  # List of successful hits
        self.possible_targets = []  # Adjacent cells to explore in Target mode
        self.probability_grid = None  # Probability grid for density
        self.current_orientation = None  # Detected orientation ("horizontal" or "vertical")

    def choose_move(self, grid, player_boats):
        """
        Chooses a move based on the strategy.

        Args:
            grid (list): The game grid (2D list containing the state of the cells).
            player_boats (dict): The player's ships (for advanced strategies).

        Returns:
            tuple: The coordinates (row, col) of the chosen move.
        """
        if self.strategy == "random":
            return self.random_strategy(grid)
        elif self.strategy == "targeted":
            return self.targeted_strategy(grid)
        elif self.strategy == "smart":
            return self.smart_strategy(grid)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def random_strategy(self, grid):
        """
        Random strategy: chooses a random cell that has not been targeted yet.

        Args:
            grid (list): The game grid.

        Returns:
            tuple: The coordinates (row, col) of the chosen move.
        """
        rows = len(grid)
        cols = len(grid[0])
        while True:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            if (row, col) not in self.shots:
                self.shots.append((row, col))  # Record the shot
                return row, col

    def targeted_strategy(self, grid):
        """
        Targeted strategy: continues to shoot around a hit cell to sink the ship.

        Args:
            grid (list): The game grid.

        Returns:
            tuple: The coordinates (row, col) of the chosen move.
        """
        if self.possible_targets:
            target = self.possible_targets.pop(0)
            self.shots.append(target)
            return target

        # If there are successful hits, explore adjacent cells
        if self.hits:
            for hit in self.hits:
                row, col = hit
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # North, South, West, East

                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and (new_row, new_col) not in self.shots:
                        self.possible_targets.append((new_row, new_col))

            if self.possible_targets:
                target = self.possible_targets.pop(0)
                self.shots.append(target)
                return target

        # If no adjacent targets are available, return to Hunt mode
        return self.random_strategy(grid)

    def smart_strategy(self, grid):
        """
        Smart strategy: combines Hunt/Target, parity, and probability density.

        Args:
            grid (list): The game grid.

        Returns:
            tuple: The coordinates (row, col) of the chosen move.
        """
        # Step 1: If in Target mode, continue targeting around the last hit cell
        if self.hits or self.possible_targets:
            return self.targeted_strategy(grid)

        # Step 2: Hunt mode with parity (checkerboard pattern)
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if (row + col) % 2 == 0 and (row, col) not in self.shots:
                    self.shots.append((row, col))
                    return row, col

        # Step 3: Calculate probability density
        if self.probability_grid is None:
            self.probability_grid = self.calculate_probability(grid)

        max_prob = 0
        best_move = None
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if (row, col) not in self.shots and self.probability_grid[row][col] > max_prob:
                    max_prob = self.probability_grid[row][col]
                    best_move = (row, col)

        if best_move:
            self.shots.append(best_move)
            return best_move

        # Step 4: If no other strategy applies, shoot randomly
        return self.random_strategy(grid)

    def calculate_probability(self, grid):
        """
        Calculates a probability grid based on possible ship configurations.

        Args:
            grid (list): The game grid.

        Returns:
            list: A 2D grid containing probabilities for each cell.
        """
        rows = len(grid)
        cols = len(grid[0])
        probability_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # Iterate through all cells and calculate probabilities
        for row in range(rows):
            for col in range(cols):
                if (row, col) not in self.shots:
                    # Check horizontal configurations
                    for length in [5, 4, 3, 2]:  # Sizes of remaining ships
                        if col + length <= cols and all((row, c) not in self.shots for c in range(col, col + length)):
                            for c in range(col, col + length):
                                probability_grid[row][c] += 1

                    # Check vertical configurations
                    for length in [5, 4, 3, 2]:
                        if row + length <= rows and all((r, col) not in self.shots for r in range(row, row + length)):
                            for r in range(row, row + length):
                                probability_grid[r][col] += 1

        return probability_grid

    def update_last_hit(self, row, col, hit):
        """
        Updates the lists of shots and successful hits.

        Args:
            row (int): Row of the cell.
            col (int): Column of the cell.
            hit (bool): Indicates if the cell contains a ship.
        """
        if hit:
            self.hits.append((row, col))
        else:
            self.current_orientation = None