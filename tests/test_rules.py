import pytest
import pygame
from src.game.rules import Rules

@pytest.fixture
def setup_rules():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    rules = Rules(screen_width, screen_height)
    return rules, screen

def test_rules_initialization(setup_rules):
    rules, _ = setup_rules
    assert rules.screen_width == 800
    assert rules.screen_height == 600
    assert rules.font is not None
    assert rules.small_font is not None
    assert rules.back_button is None

def test_draw_rules_page(setup_rules):
    rules, screen = setup_rules
    rules.draw(screen)
    assert rules.back_button is not None  # Ensure the back button is drawn

def test_handle_event_back_button_clicked(setup_rules):
    rules, screen = setup_rules
    rules.draw(screen)
    back_button_rect = rules.back_button

    # Simulate a mouse click on the back button
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (back_button_rect.x + 1, back_button_rect.y + 1)})
    result = rules.handle_event(event)
    assert result == "menu"

def test_handle_event_no_click(setup_rules):
    rules, _ = setup_rules

    # Simulate an event that is not a mouse click
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    result = rules.handle_event(event)
    assert result is None