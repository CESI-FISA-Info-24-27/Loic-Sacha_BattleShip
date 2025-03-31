import pygame
import pytest
from src.game.button import draw_back_button

@pytest.fixture
def setup_pygame():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.Font(None, 36)
    yield screen, font, screen_width, screen_height
    pygame.quit()

def test_draw_back_button_returns_rect(setup_pygame):
    screen, font, screen_width, screen_height = setup_pygame
    button_rect = draw_back_button(screen, font, screen_width, screen_height)
    assert isinstance(button_rect, pygame.Rect)

def test_draw_back_button_position(setup_pygame):
    screen, font, screen_width, screen_height = setup_pygame
    button_rect = draw_back_button(screen, font, screen_width, screen_height)
    expected_x = (screen_width - 150) // 2
    expected_y = screen_height - 40 - 20
    assert button_rect.x == expected_x
    assert button_rect.y == expected_y
    assert button_rect.width == 150
    assert button_rect.height == 40

def test_draw_back_button_text(setup_pygame):
    screen, font, screen_width, screen_height = setup_pygame
    draw_back_button(screen, font, screen_width, screen_height, text="Retour")
    text_surface = font.render("Retour", True, (255, 255, 255))
    button_x = (screen_width - 150) // 2
    button_y = screen_height - 40 - 20
    text_x = button_x + (150 - text_surface.get_width()) // 2
    text_y = button_y + (40 - text_surface.get_height()) // 2

    # Vérifiez que le texte est bien rendu sur la surface
    assert screen.get_at((text_x, text_y))[:3] == (255, 255, 255)  # Vérifie uniquement les valeurs RGB