import pytest
import pygame
from src.main import main

def test_main_initialization(mocker):
    # Mock pygame and its methods
    mocker.patch("pygame.init")
    mocker.patch("pygame.display.set_mode")
    mocker.patch("pygame.display.set_caption")
    mocker.patch("pygame.event.get", return_value=[])
    mocker.patch("pygame.quit")
    mocker.patch("pygame.display.flip")

    # Mock dependencies
    mock_menu = mocker.Mock()
    mock_board = mocker.Mock()
    mock_player = mocker.Mock()
    mocker.patch("src.main.Menu", return_value=mock_menu)
    mocker.patch("src.main.Board", return_value=mock_board)
    mocker.patch("src.main.Player", return_value=mock_player)

    # Run the main function
    mocker.patch("builtins.input", side_effect=KeyboardInterrupt)  # Simulate exit
    main()

    # Assertions
    pygame.init.assert_called_once()
    pygame.display.set_mode.assert_called_once_with((1200, 800), pygame.RESIZABLE)
    pygame.display.set_caption.assert_called_once_with("Battle Ship")
    pygame.quit.assert_called_once()

def test_main_menu_to_game_transition(mocker):
    # Mock pygame and its methods
    mocker.patch("pygame.init")
    mocker.patch("pygame.display.set_mode")
    mocker.patch("pygame.display.set_caption")
    mocker.patch("pygame.quit")
    mocker.patch("pygame.display.flip")

    # Mock dependencies
    mock_menu = mocker.Mock()
    mock_menu.handle_event.return_value = "solo"
    mock_menu.play_music = mocker.Mock()
    mock_board = mocker.Mock()
    mock_board.handle_event.return_value = None
    mock_player = mocker.Mock()
    mocker.patch("src.main.Menu", return_value=mock_menu)
    mocker.patch("src.main.Board", return_value=mock_board)
    mocker.patch("src.main.Player", return_value=mock_player)

    # Mock events
    mocker.patch("pygame.event.get", side_effect=[
        [{"type": pygame.QUIT}],  # Simulate quit event
    ])

    # Run the main function
    main()

    # Assertions
    mock_menu.handle_event.assert_called()
    mock_menu.play_music.assert_called_with(mock_menu.ingame_music)
    mock_board.handle_event.assert_not_called()