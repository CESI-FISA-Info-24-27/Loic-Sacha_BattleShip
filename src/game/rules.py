import pygame
from game.button import draw_back_button  # Import the draw_back_button function

class Rules:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, int(screen_height * 0.06))  # Font for the title
        self.small_font = pygame.font.SysFont(None, int(screen_height * 0.03))  # Font for the rules text
        self.back_button = None  # Back button

    def draw(self, screen):
        """Draws the rules page."""
        screen.fill((30, 30, 30))  # Dark gray background
        title = self.font.render("Règles du Jeu", True, (255, 255, 255))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, int(self.screen_height * 0.05)))

        # Rules text
        rules = [
            "Chaque joueur a deux grilles (10x10) et une flotte composée de :",
            "  - 1 Porte-avions (5 cases)",
            "  - 1 Croiseur (4 cases)",
            "  - 2 Contre-torpilleurs (3 cases)",
            "  - 1 Torpilleur (2 cases)",
            "",
            "Placement des navires :",
            "  - Navires placés horizontalement ou verticalement,",
            "    sans chevauchement ni diagonales.",
            "",
            "Déroulement du jeu :",
            "  - Chaque joueur annonce une case (ex : 'B6').",
            "  - Réponses possibles : 'Raté', 'Touché', 'Touché-Coulé'.",
            "",
            "Objectif :",
            "  - Couler tous les navires adverses pour remporter la partie.",
        ]

        # Display each line of the rules
        for i, rule in enumerate(rules):
            rule_text = self.small_font.render(rule, True, (255, 255, 255))
            screen.blit(rule_text, (int(self.screen_width * 0.05), int(self.screen_height * 0.15) + i * int(self.screen_height * 0.03)))

        # Draw the back button
        self.back_button = draw_back_button(screen, self.small_font, screen.get_width(), screen.get_height())

    def handle_event(self, event):
        """Handles events for the back button."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "menu"  # Return to the main menu
        return None