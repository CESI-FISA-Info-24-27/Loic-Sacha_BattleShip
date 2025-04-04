import pytest
import pygame

from src.game.rules import Rules

def test_rules_initialization():
    screen_width = 800
    screen_height = 600
    rules = Rules(screen_width, screen_height)

    assert rules.screen_width == screen_width
    assert rules.screen_height == screen_height
    assert rules.font is not None
    assert rules.small_font is not None
    assert rules.back_button is None

def test_rules_draw(mocker):
    screen_width = 800
    screen_height = 600
    rules = Rules(screen_width, screen_height)

    screen = mocker.Mock()
    mock_draw_back_button = mocker.patch("src.game.rules.draw_back_button", return_value=pygame.Rect(0, 0, 100, 50))

    rules.draw(screen)

    screen.fill.assert_called_once_with((30, 30, 30))
    assert mock_draw_back_button.called
    assert rules.back_button == mock_draw_back_button.return_value

def test_rules_handle_event_back_button_clicked(mocker):
    screen_width = 800
    screen_height = 600
    rules = Rules(screen_width, screen_height)
    rules.back_button = pygame.Rect(0, 0, 100, 50)

    event = mocker.Mock()
    event.type = pygame.MOUSEBUTTONDOWN
    event.pos = (50, 25)  # Inside the back button

    result = rules.handle_event(event)

    assert result == "menu"

def test_rules_handle_event_no_click(mocker):
    screen_width = 800
    screen_height = 600
    rules = Rules(screen_width, screen_height)
    rules.back_button = pygame.Rect(0, 0, 100, 50)

    event = mocker.Mock()
    event.type = pygame.MOUSEBUTTONDOWN
    event.pos = (150, 75)  # Outside the back button

    result = rules.handle_event(event)

    assert result is None