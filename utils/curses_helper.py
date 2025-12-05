"""
Curses helper utilities for games
Provides common functions for curses-based games
"""
import curses

def init_colors():
    """Initialize standard color pairs"""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)

def setup_game_screen(stdscr):
    """Standard setup for game screens"""
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(50)  # 50ms timeout for getch()
    init_colors()

def draw_box(stdscr, y, x, height, width, color_pair=0):
    """Draw a box with borders"""
    try:
        # Top border
        stdscr.addstr(y, x, '╔' + '═' * (width - 2) + '╗', curses.color_pair(color_pair))
        
        # Sides
        for i in range(1, height - 1):
            stdscr.addstr(y + i, x, '║', curses.color_pair(color_pair))
            stdscr.addstr(y + i, x + width - 1, '║', curses.color_pair(color_pair))
        
        # Bottom border
        stdscr.addstr(y + height - 1, x, '╚' + '═' * (width - 2) + '╝', curses.color_pair(color_pair))
    except curses.error:
        pass

def draw_text_centered(stdscr, y, text, color_pair=0, attr=curses.A_NORMAL):
    """Draw text centered on screen"""
    try:
        height, width = stdscr.getmaxyx()
        x = width // 2 - len(text) // 2
        stdscr.addstr(y, x, text, curses.color_pair(color_pair) | attr)
    except curses.error:
        pass

def show_message(stdscr, title, message, color=1):
    """Show a message and wait for keypress"""
    height, width = stdscr.getmaxyx()
    y = height // 2
    
    draw_text_centered(stdscr, y - 1, title, color, curses.A_BOLD)
    draw_text_centered(stdscr, y + 1, message, 6)
    draw_text_centered(stdscr, y + 3, "Press any key to continue...", 6)
    stdscr.refresh()
    
    stdscr.nodelay(0)
    stdscr.getch()
    stdscr.nodelay(1)

def check_terminal_size(stdscr, min_width=60, min_height=25):
    """Check if terminal is large enough"""
    height, width = stdscr.getmaxyx()
    if height < min_height or width < min_width:
        stdscr.clear()
        draw_text_centered(stdscr, height // 2 - 1, "Terminal too small!", 1, curses.A_BOLD)
        draw_text_centered(stdscr, height // 2 + 1, f"Need at least {min_width}x{min_height}", 6)
        draw_text_centered(stdscr, height // 2 + 2, f"Current: {width}x{height}", 6)
        stdscr.refresh()
        stdscr.nodelay(0)
        stdscr.getch()
        return False
    return True
