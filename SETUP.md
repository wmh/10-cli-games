# Setup Instructions

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Install Python Dependencies

#### Option A: Using pip
```bash
pip install -r requirements.txt
```

#### Option B: Using pip3
```bash
pip3 install -r requirements.txt
```

#### Option C: Using python -m pip
```bash
python3 -m pip install -r requirements.txt
```

### 2. If pip is not installed

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3-pip
```

#### On macOS:
```bash
brew install python3
```

#### On Windows:
Python from python.org includes pip automatically.

### 3. Manual Installation (if pip doesn't work)
Install packages individually:
```bash
# Install rich for beautiful terminal output
pip3 install rich

# Install colorama for cross-platform color support
pip3 install colorama
```

## Running the Game

### Start the main menu:
```bash
python3 main.py
```

### Run a specific game directly:
```bash
python3 -m games.game_001_breakout
```

or

```bash
cd games
python3 game_001_breakout.py
```

## Troubleshooting

### ImportError: No module named 'rich'
Install the missing package:
```bash
pip3 install rich
```

### Permission denied
Use `python3` instead of `python` or add executable permission:
```bash
chmod +x main.py
./main.py
```

### Terminal size issues
Make sure your terminal window is at least 80x30 characters for the best experience.

## Development

### Adding a New Game
1. Create a new file in `games/` directory: `game_XXX_gamename.py`
2. Implement the game with a `main()` function
3. Update `utils/menu.py` to add the game to the list
4. Test the game independently and through the main menu

### Project Structure
```
100-cli-games/
├── main.py              # Main entry point
├── games/               # Individual game modules
├── utils/               # Shared utilities
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Notes
- Games are designed to run in the terminal
- Some games may require a larger terminal window
- Use 'q' to quit most games
- Arrow keys for navigation in most games
