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
        self.font = pygame.font.SysFont(None, int(screen_height * 0.06))  # Font size relative to screen height
        self.small_font = pygame.font.SysFont(None, int(screen_height * 0.03))  # Font for small texts
        self.show_rules = False  # State to show or hide the rules
        self.rules = Rules(screen_width, screen_height)  # Instance of the Rules class
        self.update_buttons()  # Initialize buttons
        
        self.menu_music = "src/assets/sounds/music_menu.mp3"
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  
        
        self.ingame_music = "src/assets/sounds/music_ingame.mp3"
        pygame.mixer.music.load(self.ingame_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        # Play menu music by default
        self.play_music(self.menu_music)

    def play_music(self, music_path):
        """
        Plays background music in a loop.

        This method stops any currently playing music, loads a new music file,
        sets the volume, and plays the music in an infinite loop.

        Args:
            music_path (str): The file path to the music file to be played.

        Note:
            Ensure that the `pygame.mixer` module is initialized before calling
            this method, and the provided music file path is valid and accessible.
        """
        pygame.mixer.music.stop()  # Stop any currently playing music
        pygame.mixer.music.load(music_path)  # Load the new music file
        pygame.mixer.music.set_volume(0.5)  # Set the volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play the music in an infinite loop

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
                - "action" (str): The action associated with the button (e.g., "solo", "choose_difficulty", "rules", "quit").
        """
        """Updates the dimensions and positions of the buttons based on the window size."""
        button_width = int(self.screen_width * 0.25)
        button_height = int(self.screen_height * 0.08)
        button_x = (self.screen_width - button_width) // 2

        self.buttons = [
            {"label": "Mode Solo", "rect": pygame.Rect(button_x, int(self.screen_height * 0.3), button_width, button_height), "action": "solo"},
            {"label": "Difficulté", "rect": pygame.Rect(button_x, int(self.screen_height * 0.4), button_width, button_height), "action": "choose_difficulty"},
            {"label": "Règles", "rect": pygame.Rect(button_x, int(self.screen_height * 0.5), button_width, button_height), "action": "rules"},
            {"label": "Quitter", "rect": pygame.Rect(button_x, int(self.screen_height * 0.6), button_width, button_height), "action": "quit"},
        ]

    def draw(self, screen):
        """
        Draws the current menu screen on the provided surface.

        This method determines whether to display the main menu or the rules page
        based on the `show_rules` attribute. If `show_rules` is True, it draws the
        rules page using the `rules.draw` method. Otherwise, it displays the main
        menu using the `draw_main_menu` method.

        Args:
            screen (pygame.Surface): The surface on which to draw the menu.
        """
        """Draws the main menu or the rules page."""
        if self.show_rules:
            self.rules.draw(screen)
        else:
            self.draw_main_menu(screen)

    def draw_main_menu(self, screen):
        """
        Draws the main menu on the provided screen.
        This method renders the main menu interface, including the title, buttons, 
        and version information, onto the given Pygame screen surface.
        Args:
            screen (pygame.Surface): The Pygame surface where the main menu will be drawn.
        The main menu includes:
            - A dark gray background.
            - A centered title "Battle Ship" at the top.
            - A list of buttons with labels, drawn with a blue background and white border.
            - The version information displayed in the bottom-right corner.
        """
        """Draws the main menu."""
        screen.fill((30, 30, 30))  # Dark gray background
        title = self.font.render("Battle Ship", True, (255, 255, 255))
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
        """
        Handles events for the menu, including window resizing, button clicks, 
        and toggling the rules display.
        Args:
            event (pygame.event.Event): The event to handle.
        Returns:
            str or None: Returns "solo" if the solo mode button is clicked, 
            or None if no specific action is triggered. Exits the program 
            if the quit button is clicked.
        """
        """Handles button clicks."""
        if event.type == pygame.VIDEORESIZE:
            # Update window size and buttons
            self.screen_width, self.screen_height = event.w, event.h
            self.update_buttons()
            self.rules = Rules(self.screen_width, self.screen_height)  # Update rules

        if self.show_rules:
            action = self.rules.handle_event(event)
            if action == "menu":
                self.show_rules = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["action"] == "solo":
                            return "solo"  # Switch to solo mode
                        elif button["action"] == "rules":
                            self.show_rules = True  # Show rules
                        elif button["action"] == "quit":
                            pygame.quit()
                            exit()
        return None