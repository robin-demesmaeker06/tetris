# Tetris

A feature-rich implementation of the classic arcade game **Tetris**, built using Python and Pygame. This project features a clean modular structure, a leveling system, sound effects, and modern gameplay mechanics like "Ghost" pieces and a "Hold" system.

## 🎮 Features
* **Classic Gameplay:** Standard Tetris mechanics with 7 tetromino shapes and color coding.
* **Modern Mechanics:**
    * **Ghost Piece:** Displays a grey outline showing exactly where the current piece will land.
    * **Hold System:** Press 'C' to swap or hold a piece for later use.
    * **Next Piece Preview:** Displays the upcoming tetromino in the sidebar.
* **Progression:**
    * **Scoring:** Score points based on lines cleared (100 to 1200 points).
    * **Leveling:** Level up every 10 lines cleared. Speed increases from Level 1 (500ms) to Level 5 (150ms).
* **Audio:** Integrated background music (`music.mp3`) and sound effects for rotation, clearing lines, dropping pieces, and leveling up.

## 🛠️ Requirements
* **Python 3.10+**
* **Pygame** (Version 2.6.1)

## 🚀 Installation & Setup (Source)

It is recommended to use a **virtual environment** to manage dependencies. This method works on Arch Linux, Ubuntu, macOS, and Windows.

### 1. Clone the repository
```bash
git clone [https://github.com/robin-demesmaeker06/tetris.git](https://github.com/robin-demesmaeker06/tetris.git)
cd tetris

```
2. Setup Audio Directory

The game expects audio files to be in a specific folder structure. Ensure your assets folder is set up correctly:
Plaintext

tetris/
├── assets/
│   └── sounds/
│       ├── music.mp3
│       ├── rotate.wav
│       ├── clear.wav
│       ├── drop.wav
│       └── levelup.wav

3. Create and activate a virtual environment

Linux / macOS:
```bash

python3 -m venv venv
source venv/bin/activate
```
Windows:
```powerShell

python -m venv venv
venv\Scripts\activate
```
4. Install dependencies
```bash

pip install -r requirements.txt
```
📦 Building the Executable

You can compile the game into a standalone executable using pyinstaller (included in requirements).

    Generate the build:
```bash

    pyinstaller --noconfirm --onedir --windowed --name "Tetris" main.py
```
    Copy Assets:

        Locate the new dist/Tetris/ folder.

        Important: You must manually copy the assets folder into dist/Tetris/ so the executable can find the sound files.

    Run:

        Linux: 
```bash
        ./dist/Tetris/Tetris
```
        Windows: Open dist\Tetris\Tetris.exe

🕹️ Controls
Key	Action
Left / Right Arrow	Move current block
Up Arrow	Rotate block
Down Arrow	Soft Drop (fall faster)
Space	Hard Drop (instant placement)
C	Hold / Swap Piece
Esc	Pause / Quit Game
📂 Project Structure

    main.py: The entry point. Handles the game loop, input, rendering, and audio.

    settings.py: Configuration for screen dimensions, colors, shapes (SHAPES), and speed settings (LEVEL_SPEEDS).

    utils.py: Logic for collisions (check_collision), rotation (rotate_shape), and row clearing (clear_rows).

📜 License

This project is licensed under the MIT License.

Copyright (c) 2026 Robin Demesmaeker. Permission is granted to use, copy, modify, and distribute this software under the conditions of the license.

Created by robin-demesmaeker06