import pytest
import pygame
from src.game.menu import Menu
from src.game.rules import Rules

@pytest.fixture
def setup_menu():
    pygame.init()
    screen_width = 800
    screen_height = 600
    menu = Menu(screen_width, screen_height)
    return menu

def test_menu_initialization(setup_menu):
    menu = setup_menu
    assert menu.screen_width == 800
    assert menu.screen_height == 600
    assert isinstance(menu.font, pygame.font.Font)
    assert isinstance(menu.small_font, pygame.font.Font)
    assert menu.show_rules is False
    assert menu.rules is not None  # Vérifie que `rules` est initialisé
    assert isinstance(menu.rules, Rules)
    assert len(menu.buttons) == 3

def test_update_buttons(setup_menu):
    menu = setup_menu
    menu.screen_width = 1024
    menu.screen_height = 768
    menu.update_buttons()
    assert len(menu.buttons) == 3
    for button in menu.buttons:
        assert "label" in button
        assert "rect" in button
        assert "action" in button
        assert isinstance(button["rect"], pygame.Rect)

def test_draw_main_menu(setup_menu):
    menu = setup_menu
    screen = pygame.Surface((menu.screen_width, menu.screen_height))
    menu.draw_main_menu(screen)
    # No assertion here, but ensure no exceptions are raised during drawing

def test_draw(setup_menu):
    menu = setup_menu
    screen = pygame.Surface((menu.screen_width, menu.screen_height))
    menu.draw(screen)
    menu.show_rules = True
    menu.draw(screen)
    # No assertion here, but ensure no exceptions are raised during drawing

def test_handle_event_resize(setup_menu):
    menu = setup_menu
    resize_event = pygame.event.Event(pygame.VIDEORESIZE, {"w": 1024, "h": 768})
    menu.handle_event(resize_event)
    assert menu.screen_width == 1024
    assert menu.screen_height == 768

def test_handle_event_button_click(setup_menu):
    menu = setup_menu
    solo_button = menu.buttons[0]
    click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": solo_button["rect"].center})
    action = menu.handle_event(click_event)
    assert action == "solo"

    rules_button = menu.buttons[1]
    click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": rules_button["rect"].center})
    menu.handle_event(click_event)
    menu.rules.draw(pygame.Surface((menu.screen_width, menu.screen_height)))  # Initialise `back_button`
    assert menu.show_rules is True

    quit_button = menu.buttons[2]
    with pytest.raises(SystemExit):
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": quit_button["rect"].center})
        menu.handle_event(click_event)