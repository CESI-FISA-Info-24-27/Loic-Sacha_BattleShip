class Player:
    """
    Représente un joueur dans le jeu de bataille navale.

    Attributes:
        name (str): Le nom du joueur.
        is_enemy (bool): Indique si le joueur est un ennemi.
        boats (dict): Un dictionnaire contenant les bateaux et leurs emplacements.
        move_historic (list): Une liste des mouvements effectués par le joueur.
    """

    def __init__(self, name):
        """
        Initialise un joueur avec un nom.

        Args:
            name (str): Le nom du joueur.
        """
        self.name = name
        self.is_enemy = False
        self.boats = {}
        self.move_historic = []

    def change_name(self, name):
        """
        Change le nom du joueur.

        Args:
            name (str): Le nouveau nom du joueur.
        """
        self.name = name

    def set_boat_emplacement(self, boat_name, X, Y):
        """
        Définit l'emplacement d'un bateau sur la grille.

        Args:
            boat_name (str): Le nom du bateau.
            X (int): La position X sur la grille (entre 1 et 10).
            Y (int): La position Y sur la grille (entre 1 et 10).

        Raises:
            ValueError: Si les coordonnées (X, Y) sont hors limites ou déjà attribuées.
        """
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
        """
        Enregistre un mouvement effectué par le joueur.

        Args:
            X (int): La position X du mouvement.
            Y (int): La position Y du mouvement.
            hit (bool): Indique si le mouvement a touché un bateau.
        """
        self.move_historic.append(((X, Y), hit))
        print(f"Move at ({X}, {Y}) recorded. Hit: {hit}")