#!/usr/bin/env python3
"""
100 CLI Games Challenge
Main entry point and menu system
"""
import sys
import importlib
from rich.console import Console
from rich.prompt import Prompt
from utils.menu import display_menu, get_game_by_id, GAMES, clear_screen

console = Console()

def run_game(game_id):
    """Load and run a specific game"""
    game = get_game_by_id(game_id)
    
    if not game:
        console.print(f"[red]Game {game_id} not found![/red]")
        return
    
    if game['status'] != '✅':
        console.print(f"[yellow]Game {game_id}: {game['name']} is not yet available![/yellow]")
        console.print("[yellow]Coming soon...[/yellow]")
        input("\nPress Enter to return to menu...")
        return
    
    try:
        # Dynamically import the game module
        module_name = f"games.{game['file']}"
        game_module = importlib.import_module(module_name)
        
        # Run the game's main function
        if hasattr(game_module, 'main'):
            clear_screen()
            game_module.main()
        else:
            console.print(f"[red]Error: Game module {module_name} has no main() function[/red]")
            input("\nPress Enter to return to menu...")
    
    except ImportError as e:
        console.print(f"[red]Error loading game: {e}[/red]")
        input("\nPress Enter to return to menu...")
    except Exception as e:
        console.print(f"[red]Error running game: {e}[/red]")
        input("\nPress Enter to return to menu...")

def list_all_games():
    """Display all 100 games in a formatted list"""
    clear_screen()
    console.print("\n[bold magenta]📋 Complete Game List (100 Games)[/bold magenta]\n")
    
    current_week = 0
    week_names = [
        "Week 1: Classic Arcade",
        "Week 2: Puzzle Games",
        "Week 3: Word Games",
        "Week 4: Card Games",
        "Week 5: Board Games",
        "Week 6: Adventure & RPG",
        "Week 7: Strategy Games",
        "Week 8: Racing & Sports",
        "Week 9: Quiz & Trivia",
        "Week 10: Reaction Games",
        "Week 11: Math & Logic",
        "Week 12: Simulation",
        "Week 13: Artistic",
        "Week 14: Multiplayer",
        "Week 15: Unique & Creative"
    ]
    
    for i, game in enumerate(GAMES):
        week = i // 7
        if week != current_week and week < len(week_names):
            console.print(f"\n[cyan bold]{week_names[week]}[/cyan bold]")
            current_week = week
        
        status = "✅" if game['status'] == "✅" else "⏳"
        console.print(f"  {game['id']:3d}. {status} {game['name']}")
    
    console.print()

def main():
    """Main program loop"""
    console.print("[bold green]Welcome to 100 CLI Games Challenge![/bold green]")
    console.print("Loading...")
    
    page = 0
    max_page = 4  # 100 games / 20 per page = 5 pages
    
    while True:
        display_menu()
        
        try:
            choice = Prompt.ask("\n[cyan]Enter your choice[/cyan]").strip().lower()
            
            if choice == 'q':
                console.print("\n[yellow]Thanks for playing! See you tomorrow! 👋[/yellow]")
                break
            
            elif choice == 'n':
                page = min(page + 1, max_page)
                continue
            
            elif choice == 'p':
                page = max(page - 1, 0)
                continue
            
            elif choice == 'l':
                list_all_games()
                input("\nPress Enter to return to menu...")
                continue
            
            elif choice.isdigit():
                game_id = int(choice)
                if 1 <= game_id <= 100:
                    run_game(game_id)
                else:
                    console.print("[red]Please enter a number between 1 and 100[/red]")
                    input("\nPress Enter to continue...")
            
            else:
                console.print("[red]Invalid choice! Please try again.[/red]")
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Goodbye! 👋[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
