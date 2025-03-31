class Player:
    def __init__(self, name):
        self.name = name
        self.is_enemy = False
        self.boats = {}
        self.move_historic = []

    def change_name(self, name):
        self.name = name

    def set_boat_emplacement(self, boat_name, X, Y):
        if not (1 <= X <= 10 and 1 <= Y <= 10):
            print(f"Error: ({X}, {Y}) must be between 1 and 10.")
            return

        for boat in self.boats.values():
            if (X, Y) in boat:
                print(f"Error: ({X}, {Y}) already attributed.")
                return

        if boat_name not in self.boats:
            self.boats[boat_name] = []

        if (X, Y) not in self.boats[boat_name]:
            self.boats[boat_name].append((X, Y))
            print(f"Boat '{boat_name}' added to ({X}, {Y}).")
        else:
            print(f"Error: ({X}, {Y}) already attributed to '{boat_name}'.")

    def record_move(self, X, Y, hit):
        """Enregistre le mouvement avec l'information du hit passée en paramètre."""
        self.move_historic.append(((X, Y), hit))
        print(f"Move at ({X}, {Y}) recorded. Hit: {hit}")
