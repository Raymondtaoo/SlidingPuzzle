# Sliding Puzzle Game

## Overview
The Sliding Puzzle Game is a classic puzzle game where players rearrange shuffled tiles to form a complete image. This implementation is built using the Pygame library in Python, offering an interactive and engaging experience.

## Features
- **Customizable Puzzle Grid:** Players can play on a 3x3 grid.
- **Shuffle Mechanism:** Tiles can be shuffled randomly.
- **Image Tiles:** Each tile displays a portion of an image, adding to the challenge.
- **High Score Tracking:** Records and displays the best completion times.
- **Image Swapping:** Players can switch between different images.
- **Interactive Tiles:** Clickable tiles to move them into the empty space.
- **UI Elements:** Includes buttons for shuffle, reset, and image swap, plus a timer.

## Installation
1. **Python Installation:** Ensure Python is installed on your system.
2. **Pygame Library:** Install Pygame using `pip install pygame`.
3. **Clone/Download Repository:** Download the source code from the provided repository.

## Usage
1. **Start the Game:** Run `main.py` to start the game.
2. **Shuffle Tiles:** Click the 'Shuffle' button to shuffle the tiles.
3. **Move Tiles:** Click on a tile next to the empty space to move it.
4. **Swap Images:** Click the 'Swap' button to change the puzzle image.
5. **Reset Game:** Click the 'Reset' button to start over.
6. **Game Completion:** Arrange all tiles in the correct order to win.

## File Structure
- `main.py`: Main game script.
- `settings.py`: Contains game settings like colours, dimensions, and game speed.
- `sprite.py`: Defines the Tile, Button, and UIElement classes used in the game.

## Requirements
- Python 3.x
- Pygame library
