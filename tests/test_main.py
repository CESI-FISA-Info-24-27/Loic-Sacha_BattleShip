import pytest
import pygame
from src.main import main

@pytest.fixture
def mock_pygame(monkeypatch):
    """
    Mock Pygame functions to prevent actual game window creation and event handling.
    """
    monkeypatch.setattr(pygame, "init", lambda: None)
    monkeypatch.setattr(pygame.display, "set_mode", lambda *args, **kwargs: None)
    monkeypatch.setattr(pygame.display, "set_caption", lambda *args: None)
    monkeypatch.setattr(pygame.display, "flip", lambda: None)
    monkeypatch.setattr(pygame, "quit", lambda: None)
    monkeypatch.setattr(pygame.event, "get", lambda: [{"type": pygame.QUIT}])

def test_main_quit(mock_pygame, init_pygame):
    """
    Test that the main function initializes and quits the game loop correctly.
    """
    try:
        main()
    except SystemExit:
        pytest.fail("main() raised SystemExit unexpectedly!")