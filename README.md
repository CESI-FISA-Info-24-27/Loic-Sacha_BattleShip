<div style="display: flex; align-items: center;">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSi6jTh-1egIrH6NTX0RgA9ayAWr_Dsq1fE0w&s" alt="Logo CESI" width="150" style="margin-right: 20px;"/>
  <h1>Battle Ship Project</h1>
</div>

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com) [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

# Battle Ship Solo

## Description

Battle Ship Solo est un jeu de bataille navale en solo développé avec Pygame. Le joueur affronte une IA dans une bataille stratégique où il doit placer ses navires et tenter de couler la flotte ennemie.

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/CESI-FISA-Info-24-27/Loic-Sacha_BattleShip
   cd Loic-Sacha_BattleShip
   ```
2. Créez et activez un environnement virtuel :

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Sur Windows
   source .venv/bin/activate  # Sur Linux/Mac
   ```
3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Pour lancer le jeu, exécutez le fichier `main.py` :

```bash
python src/main.py
```

## Génération de la Documentation

La documentation du projet est générée avec **Sphinx** et peut être consultée en ligne ou localement.

### Générer la documentation localement :

1. Assurez-vous que Sphinx est installé dans votre environnement virtuel :

   ```bash
   pip install sphinx
   ```
2. Générez la documentation HTML :

   ```bash
   cd source
   make html
   ```
3. Ouvrez le fichier `build/html/index.html` dans un navigateur pour consulter la documentation.

## Structure du Projet

- `src/main.py`: Point d'entrée de l'application.
- `src/game/`: Contient la logique du jeu.
  - `board.py`: Gère le plateau de jeu.
  - `player.py`: Gère les actions des joueurs.
  - `enemy.py`: Gère les actions de l'IA ennemie.
  - `action.py`: Contient les actions principales du jeu (tir, etc.).
- `src/assets/`: Contient les ressources du jeu.
  - `sounds/`: Effets sonores et musique.
  - `fonts/`: Fichiers de polices.
- `src/utils/`: Contient des fonctions utilitaires.
  - `helpers.py`: Fonctions pour gérer les entrées utilisateur et dessiner des éléments.
- `source/`: Contient les fichiers de configuration et les fichiers `.rst` pour la documentation Sphinx.
- `requirements.txt`: Liste des dépendances.
- `.gitignore`: Fichiers à ignorer par Git.

## Contributeurs

* **Sacha COLBERT-LISBONA** _alias_ [@Sunit34140](https://github.com/Sunit34140)
* **Loïc SERRE** _alias_ [@LoicSERRE](https://github.com/LoicSERRE)
