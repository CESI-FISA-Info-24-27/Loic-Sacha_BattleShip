class Action:
    @staticmethod
    def shoot(player, enemy, X, Y):
        if not (1 <= X <= 10 and 1 <= Y <= 10):
            print(f"Error: ({X}, {Y}) must be between 1 and 10.")
            return False

        hit = False
        # Vérifie si le tir touche un bateau de l'ennemi
        for boat_positions in enemy.boats.values():
            if (X, Y) in boat_positions:
                hit = True
                boat_positions.remove((X, Y))  # Retire la position du bateau touché
                print(f"Hit! The shot at ({X}, {Y}) hit a boat from {enemy.name}.")
                break

        if not hit:
            print(f"Miss! The shot at ({X}, {Y}) missed.")

        # Passe maintenant `hit` directement à `record_move()`
        player.record_move(X, Y, hit)

        return hit
