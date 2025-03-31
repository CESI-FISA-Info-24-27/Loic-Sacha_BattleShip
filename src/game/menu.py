import pygame
from game.rules import Rules  # Import directly from rules.py

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, int(screen_height * 0.06))  # Font size relative to screen height
        self.small_font = pygame.font.SysFont(None, int(screen_height * 0.03))  # Font for small texts
        self.show_rules = False  # State to show or hide the rules
        self.rules = Rules(screen_width, screen_height)  # Instance of the Rules class
        self.update_buttons()  # Initialize buttons

    def update_buttons(self):
        """Updates the dimensions and positions of the buttons based on the window size."""
        button_width = int(self.screen_width * 0.25)
        button_height = int(self.screen_height * 0.08)
        button_x = (self.screen_width - button_width) // 2

        self.buttons = [
            {"label": "Mode Solo", "rect": pygame.Rect(button_x, int(self.screen_height * 0.3), button_width, button_height), "action": "solo"},
            {"label": "Règles", "rect": pygame.Rect(button_x, int(self.screen_height * 0.4), button_width, button_height), "action": "rules"},
            {"label": "Quitter", "rect": pygame.Rect(button_x, int(self.screen_height * 0.5), button_width, button_height), "action": "quit"},
        ]

    def draw(self, screen):
        """Draws the main menu or the rules page."""
        if self.show_rules:
            self.rules.draw(screen)
        else:
            self.draw_main_menu(screen)

    def draw_main_menu(self, screen):
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