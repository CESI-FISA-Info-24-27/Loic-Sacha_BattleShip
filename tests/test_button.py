import pygame
import pytest
from src.game.button import draw_back_button

def test_reinit_button_creates_correct_rect():
    screen_width = 800
    screen_height = 600
    button_width = 150
    button_height = 20
    expected_x = (screen_width - button_width) // 2
    expected_y = screen_height - button_height - 20

    screen = pygame.Surface((screen_width, screen_height))
    font = pygame.font.Font(None, 36)

    button_rect = reinit_button(screen, font, screen_width, screen_height)

    assert button_rect.x == expected_x
    assert button_rect.y == expected_y
    assert button_rect.width == button_width
    assert button_rect.height == button_height

def test_reinit_button_draws_text():
    screen_width = 800
    screen_height = 600
    text = "Réinitialiser la partie"

    screen = pygame.Surface((screen_width, screen_height))
    font = pygame.font.Font(None, 36)

    reinit_button(screen, font, screen_width, screen_height, text=text)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    button_width = 150
    button_height = 20
    button_x = (screen_width - button_width) // 2
    button_y = screen_height - button_height - 20

    text_x = button_x + (button_width - text_rect.width) // 2
    text_y = button_y + (button_height - text_rect.height) // 2

    screen_array = pygame.surfarray.array3d(screen)
    assert (screen_array[text_x, text_y] == [255, 255, 255]).all()