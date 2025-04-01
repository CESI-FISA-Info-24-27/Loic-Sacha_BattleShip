import pygame

def draw_back_button(screen, font, screen_width, screen_height, text="Retour"):
    """
    Draws a "Back" button centered at the bottom of the screen.

    Args:
        screen (pygame.Surface): Surface on which to draw the button.
        font (pygame.font.Font): Font used for the text.
        screen_width (int): Width of the screen.
        screen_height (int): Height of the screen.
        text (str): Text displayed on the button (default: "Retour").

    Returns:
        pygame.Rect: Rectangle representing the button (useful for detecting clicks).
    """
    button_width = 150
    button_height = 40
    button_x = (screen_width - button_width) // 2
    button_y = screen_height - button_height - 20
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Draw the button
    pygame.draw.rect(screen, (200, 0, 0), button_rect)  # Red background
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)  # White border

    # Draw the text at the center of the button
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (button_rect.x + (button_width - text_surface.get_width()) // 2,
                               button_rect.y + (button_height - text_surface.get_height()) // 2))

    return button_rect

def reinit_button(screen, font, screen_width, screen_height, text="Réinitialiser la partie"):
    """
    Draws a button centered at the bottom of the screen.
    This button allow the player to start again the game.

    Args:
        screen (pygame.Surface): Surface on which to draw the button.
        font (pygame.font.Font): Font used for the text.
        screen_width (int): Width of the screen.
        screen_height (int): Height of the screen.
        text (str): Text displayed on the button (default: "Réinitialiser la partie").

    Returns:
        pygame.Rect: Rectangle representing the button (useful for detecting clicks).
    """
    button_width = 150
    button_height = 20
    button_x = (screen_width - button_width) // 2
    button_y = screen_height - button_height - 20
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Draw the button
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)  # White border

    # Draw the text at the center of the button
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (button_rect.x + (button_width - text_surface.get_width()) // 2,
                               button_rect.y + (button_height - text_surface.get_height()) // 2))

    return button_rect