<div style="display: flex; align-items: center;">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSi6jTh-1egIrH6NTX0RgA9ayAWr_Dsq1fE0w&s" alt="Logo CESI" width="150" style="margin-right: 20px;"/>
  <h1>Battle Ship Project</h1>
</div>

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com) [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

# Battle Ship Royale Solo

## Description
Battle Ship Royale Solo is a single-player battleship game developed with Pygame. The player faces an AI-controlled enemy in a strategic battle where they must place their ships and try to sink the enemy's fleet.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/CESI-FISA-Info-24-27/Loic-Sacha_BattleShip
   cd Loic-Sacha_BattleShip
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To launch the game, run the `main.py` file:
```
python src/main.py
```

## Project Structure

- `src/main.py`: Entry point of the application.
- `src/game/`: Contains the game logic.
  - `board.py`: Manages the game board.
  - `player.py`: Handles player actions.
  - `enemy.py`: Handles enemy actions.
- `src/assets/`: Contains game resources.
  - `sounds/`: Sound effects and music.
  - `fonts/`: Font files.
- `src/utils/`: Contains utility functions.
  - `helpers.py`: Functions for handling user input and drawing elements.
- `requirements.txt`: List of dependencies.
- `.gitignore`: Files to be ignored by Git.

## Authors
* **Sacha COLBERT-LISBONA** _alias_ [@Sunit34140](https://github.com/Sunit34140)
* **Loïc SERRE** _alias_ [@LoicSERRE](https://github.com/LoicSERRE)