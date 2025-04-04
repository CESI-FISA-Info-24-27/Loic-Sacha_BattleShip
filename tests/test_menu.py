import pytest
import pygame
from src.game.menu import Menu
from src.game.rules import Rules

def test_menu_initialization():
    screen_width = 800
    screen_height = 600
    menu = Menu(screen_width, screen_height)

    assert menu.screen_width == screen_width
    assert menu.screen_height == screen_height
    assert isinstance(menu.font, pygame.font.Font)
    assert isinstance(menu.small_font, pygame.font.Font)
    assert not menu.show_rules
    assert isinstance(menu.rules, Rules)
    assert len(menu.buttons) == 4
    assert menu.buttons[0]["label"] == "Mode Solo"
    assert menu.buttons[1]["label"] == "Difficulté"
    assert menu.buttons[2]["label"] == "Règles"
    assert menu.buttons[3]["label"] == "Quitter"

def test_update_buttons():
    screen_width = 800
    screen_height = 600
    menu = Menu(screen_width, screen_height)

    menu.screen_width = 1024
    menu.screen_height = 768
    menu.update_buttons()

    button_width = int(menu.screen_width * 0.25)
    button_height = int(menu.screen_height * 0.08)
    button_x = (menu.screen_width - button_width) // 2

    assert menu.buttons[0]["rect"].width == button_width
    assert menu.buttons[0]["rect"].height == button_height
    assert menu.buttons[0]["rect"].x == button_x

def test_draw_main_menu(mocker):
    screen_width = 800
    screen_height = 600
    menu = Menu(screen_width, screen_height)
    screen = mocker.Mock()

    menu.draw_main_menu(screen)

    screen.fill.assert_called_once_with((30, 30, 30))
    assert screen.blit.call_count > 0

def test_handle_event_quit(mocker):
    screen_width = 800
    screen_height = 600
    menu = Menu(screen_width, screen_height)
    mocker.patch("pygame.quit")
    mocker.patch("builtins.exit")

    quit_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": menu.buttons[3]["rect"].center})
    menu.handle_event(quit_event)

    pygame.quit.assert_called_once()
    exit.assert_called_once()

def test_handle_event_solo():
    screen_width = 800
    screen_height = 600
    menu = Menu(screen_width, screen_height)

    solo_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": menu.buttons[0]["rect"].center})
    action = menu.handle_event(solo_event)

    assert action == "solo"

def test_handle_event_rules():
    screen_width = 800
    screen_height = 600
    menu = Menu(screen_width, screen_height)

    rules_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": menu.buttons[2]["rect"].center})
    menu.handle_event(rules_event)

    assert menu.show_rules