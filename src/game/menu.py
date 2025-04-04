import pygame
from game.rules import Rules  # Import directly from rules.py

class Menu:
    """
    Menu class for managing the main menu of the game.
    Attributes:
        screen_width (int): The width of the game screen.
        screen_height (int): The height of the game screen.
        font (pygame.font.Font): The font used for main menu text.
        small_font (pygame.font.Font): The font used for smaller texts like version info.
        show_rules (bool): A flag indicating whether the rules page is displayed.
        rules (Rules): An instance of the Rules class for displaying game rules.
        buttons (list): A list of dictionaries representing menu buttons with their labels, positions, and actions.
    Methods:
        __init__(screen_width, screen_height):
            Initializes the Menu instance with screen dimensions and sets up fonts, rules, and buttons.
        update_buttons():
            Updates the dimensions and positions of the buttons based on the current screen size.
        draw(screen):
            Draws the main menu or the rules page on the given screen.
        draw_main_menu(screen):
            Draws the main menu, including the title, buttons, and version information.
        handle_event(event):
            Handles user input events, such as resizing the window or clicking buttons.
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, 48)
        self.buttons = []
        self.multiplayer_buttons = []  # Boutons spécifiques au mode multijoueur
        self.show_multiplayer_options = False  # Indicateur pour afficher les options multijoueurs
        self.show_rules = False  # Indicateur pour afficher les règles
        self.update_buttons()

    def update_buttons(self):
        """
        Updates the dimensions and positions of the menu buttons dynamically based on the current window size.
        This method recalculates the width, height, and position of each button to ensure they are properly
        aligned and scaled relative to the screen dimensions. The buttons are centered horizontally and 
        positioned vertically at specific percentages of the screen height.
        Attributes:
            button_width (int): The calculated width of each button, set to 25% of the screen width.
            button_height (int): The calculated height of each button, set to 8% of the screen height.
            button_x (int): The x-coordinate for centering the buttons horizontally.
        Updates:
            self.buttons (list): A list of dictionaries where each dictionary represents a button with:
                - "label" (str): The text displayed on the button.
                - "rect" (pygame.Rect): The rectangle defining the button's position and dimensions.
                - "action" (str): The action associated with the button (e.g., "solo", "rules", "quit").
        """
        """Updates the dimensions and positions of the buttons based on the window size."""
        button_width = int(self.screen_width * 0.25)
        button_height = int(self.screen_height * 0.08)
        button_x = (self.screen_width - button_width) // 2

        self.buttons = [
            {"label": "Mode Solo", "rect": pygame.Rect(button_x, int(self.screen_height * 0.3), button_width, button_height), "action": "solo"},
            {"label": "Multijoueur", "rect": pygame.Rect(button_x, int(self.screen_height * 0.4), button_width, button_height), "action": "multiplayer"},
            {"label": "Règles", "rect": pygame.Rect(button_x, int(self.screen_height * 0.5), button_width, button_height), "action": "rules"},
            {"label": "Quitter", "rect": pygame.Rect(button_x, int(self.screen_height * 0.6), button_width, button_height), "action": "quit"},
        ]

        # Boutons spécifiques au mode multijoueur
        self.multiplayer_buttons = [
            {"label": "Créer une Partie", "rect": pygame.Rect(button_x, int(self.screen_height * 0.4), button_width, button_height), "action": "create_match"},
            {"label": "Rejoindre une Partie", "rect": pygame.Rect(button_x, int(self.screen_height * 0.5), button_width, button_height), "action": "join_match"},
            {"label": "Retour", "rect": pygame.Rect(button_x, int(self.screen_height * 0.6), button_width, button_height), "action": "menu"},
        ]

    def draw(self, screen):
        """Dessine le menu principal ou les options multijoueurs."""
        screen.fill((30, 30, 30))  # Fond gris foncé
        title = self.font.render("Battle Ship Royale", True, (255, 255, 255))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, int(self.screen_height * 0.1)))

        buttons_to_draw = self.multiplayer_buttons if self.show_multiplayer_options else self.buttons

        for button in buttons_to_draw:
            pygame.draw.rect(screen, (0, 128, 255), button["rect"])  # Fond bleu
            pygame.draw.rect(screen, (255, 255, 255), button["rect"], 2)  # Bordure blanche
            label = self.font.render(button["label"], True, (255, 255, 255))
            screen.blit(label, (button["rect"].x + button["rect"].width // 2 - label.get_width() // 2,
                                button["rect"].y + button["rect"].height // 2 - label.get_height() // 2))

    def draw_main_menu(self, screen):
        """
        Draws the main menu on the provided screen.
        This method renders the main menu interface, including the title, buttons, 
        and version information, onto the given Pygame screen surface.
        Args:
            screen (pygame.Surface): The Pygame surface where the main menu will be drawn.
        The main menu includes:
            - A dark gray background.
            - A centered title "Battle Ship Royale" at the top.
            - A list of buttons with labels, drawn with a blue background and white border.
            - The version information displayed in the bottom-right corner.
        """
        """Draws the main menu."""
        screen.fill((30, 30, 30))  # Dark gray background
        title = self.font.render("Battle Ship Royale", True, (255, 255, 255))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, int(self.screen_height * 0.1)))

        for button in self.buttons:
            pygame.draw.rect(screen, (0, 128, 255), button["rect"])  # Button background
            pygame.draw.rect(screen, (255, 255, 255), button["rect"], 2)  # Border
            label = self.font.render(button["label"], True, (255, 255, 255))
            screen.blit(label, (button["rect"].x + button["rect"].width // 2 - label.get_width() // 2,
                                button["rect"].y + button["rect"].height // 2 - label.get_height() // 2))

        # Display the version in the bottom right corner
        version_text = self.small_font.render("Version 1.0.0", True, (200, 200, 200))
        screen.blit(version_text, (self.screen_width - version_text.get_width() - 10, self.screen_height - version_text.get_height() - 10))

    def handle_event(self, event):
        """Gère les événements du menu."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
            buttons_to_check = self.multiplayer_buttons if self.show_multiplayer_options else self.buttons

            for button in buttons_to_check:
                if button["rect"].collidepoint(event.pos):
                    if button["action"] == "solo":
                        return "solo"
                    elif button["action"] == "multiplayer":
                        self.show_multiplayer_options = True
                        return "connect"
                    elif button["action"] == "create_match":
                        return "create_match"
                    elif button["action"] == "join_match":
                        return "join_match"
                    elif button["action"] == "menu":
                        self.show_multiplayer_options = False
                    elif button["action"] == "quit":
                        pygame.quit()
                        exit()
        return None