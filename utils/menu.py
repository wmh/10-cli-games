"""Menu system for game selection"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import os

console = Console()

GAMES = [
    {"id": 1, "name": "Breakout (打磚塊)", "status": "✅", "file": "game_001_breakout"},
    {"id": 2, "name": "Snake", "status": "⏳", "file": "game_002_snake"},
    {"id": 3, "name": "Pong", "status": "⏳", "file": "game_003_pong"},
    {"id": 4, "name": "Space Invaders", "status": "⏳", "file": "game_004_space_invaders"},
    {"id": 5, "name": "Tetris", "status": "⏳", "file": "game_005_tetris"},
    {"id": 6, "name": "Pac-Man", "status": "⏳", "file": "game_006_pacman"},
    {"id": 7, "name": "Asteroids", "status": "⏳", "file": "game_007_asteroids"},
    {"id": 8, "name": "2048", "status": "⏳", "file": "game_008_2048"},
    {"id": 9, "name": "Minesweeper", "status": "⏳", "file": "game_009_minesweeper"},
    {"id": 10, "name": "Sudoku", "status": "⏳", "file": "game_010_sudoku"},
    # Add more games as they are created
]

# Generate full list of 100 games
for i in range(11, 101):
    GAMES.append({
        "id": i,
        "name": f"Game {i} (Coming Soon)",
        "status": "⏳",
        "file": f"game_{i:03d}_placeholder"
    })

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def display_header():
    """Display the game header"""
    title = Text("🎮 100 CLI GAMES CHALLENGE 🎮", style="bold magenta", justify="center")
    subtitle = Text("One game per day for 100 days!", style="italic cyan", justify="center")
    header = Panel(
        Text.assemble(title, "\n", subtitle),
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(header)

def display_games_table(page=0, per_page=20):
    """Display games in a paginated table"""
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, len(GAMES))
    
    table = Table(title=f"Games {start_idx + 1}-{end_idx} of {len(GAMES)}", 
                  show_header=True, header_style="bold yellow")
    
    table.add_column("ID", style="cyan", width=5, justify="right")
    table.add_column("Game Name", style="white", width=35)
    table.add_column("Status", style="green", width=8, justify="center")
    
    for game in GAMES[start_idx:end_idx]:
        status_style = "green" if game["status"] == "✅" else "yellow"
        table.add_row(
            str(game["id"]),
            game["name"],
            Text(game["status"], style=status_style)
        )
    
    console.print(table)

def display_menu():
    """Display the main menu"""
    clear_screen()
    display_header()
    console.print()
    display_games_table(page=0, per_page=20)
    console.print()
    
    menu_text = """
[yellow]Commands:[/yellow]
  [cyan]1-100[/cyan]  - Play a game by number
  [cyan]n[/cyan]      - Next page
  [cyan]p[/cyan]      - Previous page
  [cyan]l[/cyan]      - List all games
  [cyan]q[/cyan]      - Quit
    """
    console.print(Panel(menu_text, border_style="green", padding=(0, 2)))

def get_game_by_id(game_id):
    """Get game information by ID"""
    for game in GAMES:
        if game["id"] == game_id:
            return game
    return None
