class Action:
    """
    A class containing static methods for performing game actions in the Battleship game.
    """
    """
        Perform a shooting action in the Battleship game.
        This method allows a player to shoot at a specific coordinate on the enemy's grid.
        It checks if the shot is within valid bounds, determines whether it hits an enemy's ship,
        and records the result of the move.
        Args:
            player (Player): The player performing the shooting action.
            enemy (Player): The enemy player being targeted.
            X (int): The X-coordinate of the shot (1-based index, must be between 1 and 10).
            Y (int): The Y-coordinate of the shot (1-based index, must be between 1 and 10).
        Returns:
            bool: True if the shot hits an enemy's ship, False otherwise.
        Raises:
            ValueError: If the coordinates (X, Y) are out of the valid range (1 to 10).
        Notes:
            - If the shot hits an enemy's ship, the corresponding position is removed from the ship's positions.
            - The result of the shot (hit or miss) is recorded using the player's `record_move` method.
        """
    @staticmethod
    def shoot(player, enemy, X, Y):
        if not (1 <= X <= 10 and 1 <= Y <= 10):
            print(f"Error: ({X}, {Y}) must be between 1 and 10.")
            return False

        hit = False
        # Check if the shot hits an enemy's ship
        for boat_positions in enemy.boats.values():
            if (X, Y) in boat_positions:
                hit = True
                boat_positions.remove((X, Y))  # Remove the hit position from the ship
                print(f"Hit! The shot at ({X}, {Y}) hit a boat from {enemy.name}.")
                break

        if not hit:
            print(f"Miss! The shot at ({X}, {Y}) missed.")

        # Pass `hit` directly to `record_move()`
        player.record_move(X, Y, hit)

        return hit
