import sys
import os
import pygame
import pytest

# Ajouter le dossier `src` au chemin de recherche des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    """
    Initialise Pygame une fois pour tous les tests.
    """
    pygame.init()
    yield
    pygame.quit()