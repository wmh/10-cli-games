"""
Game 007: 2048
A classic number puzzle game where you combine tiles to reach 2048.
"""

import curses
import random
from curses import wrapper

class Game2048:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.best_score = 0
        
        # Initialize curses
        curses.curs_set(0)
        self.stdscr.nodelay(0)
        self.stdscr.timeout(-1)  # Block until key press
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)   # 0 - empty
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)    # 2
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)    # 4
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # 8
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA) # 16
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_RED)     # 32
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED)     # 64
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # 128
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # 256
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_YELLOW) # 512
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_GREEN)  # 1024
        curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_GREEN)  # 2048
        curses.init_pair(13, curses.COLOR_WHITE, curses.COLOR_BLACK)  # > 2048
        
        self.colors = {
            0: 1, 2: 2, 4: 3, 8: 4, 16: 5, 32: 6, 64: 7,
            128: 8, 256: 9, 512: 10, 1024: 11, 2048: 12
        }
        
        # Start with two tiles
        self.add_new_tile()
        self.add_new_tile()
        
        self.game_over = False
        self.won = False
        self.continue_after_win = False
    
    def get_color(self, value):
        """Get color pair for a value"""
        if value == 0 or value in self.colors:
            return curses.color_pair(self.colors.get(value, 1))
        return curses.color_pair(13)  # For values > 2048
    
    def add_new_tile(self):
        """Add a new tile (2 or 4) to a random empty cell"""
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 2 if random.random() < 0.9 else 4
            return True
        return False
    
    def compress(self, line):
        """Remove zeros from line"""
        return [num for num in line if num != 0]
    
    def merge(self, line):
        """Merge adjacent equal numbers"""
        if len(line) < 2:
            return line, 0
        
        merged = []
        score_gain = 0
        i = 0
        while i < len(line):
            if i + 1 < len(line) and line[i] == line[i + 1]:
                merged.append(line[i] * 2)
                score_gain += line[i] * 2
                i += 2
            else:
                merged.append(line[i])
                i += 1
        return merged, score_gain
    
    def move_line_left(self, line):
        """Move and merge a line to the left"""
        compressed = self.compress(line)
        merged, score_gain = self.merge(compressed)
        merged += [0] * (4 - len(merged))
        return merged, score_gain
    
    def move_left(self):
        """Move all tiles left"""
        moved = False
        score_gain = 0
        for i in range(4):
            new_line, gain = self.move_line_left(self.board[i])
            if new_line != self.board[i]:
                moved = True
            self.board[i] = new_line
            score_gain += gain
        return moved, score_gain
    
    def rotate_board_clockwise(self):
        """Rotate board 90 degrees clockwise"""
        self.board = [[self.board[3-j][i] for j in range(4)] for i in range(4)]
    
    def move_right(self):
        """Move all tiles right"""
        self.rotate_board_clockwise()
        self.rotate_board_clockwise()
        moved, score_gain = self.move_left()
        self.rotate_board_clockwise()
        self.rotate_board_clockwise()
        return moved, score_gain
    
    def move_up(self):
        """Move all tiles up"""
        self.rotate_board_clockwise()
        self.rotate_board_clockwise()
        self.rotate_board_clockwise()
        moved, score_gain = self.move_left()
        self.rotate_board_clockwise()
        return moved, score_gain
    
    def move_down(self):
        """Move all tiles down"""
        self.rotate_board_clockwise()
        moved, score_gain = self.move_left()
        self.rotate_board_clockwise()
        self.rotate_board_clockwise()
        self.rotate_board_clockwise()
        return moved, score_gain
    
    def can_move(self):
        """Check if any move is possible"""
        # Check for empty cells
        if any(0 in row for row in self.board):
            return True
        
        # Check for possible horizontal merges
        for row in range(4):
            for col in range(3):
                if self.board[row][col] == self.board[row][col + 1]:
                    return True
        
        # Check for possible vertical merges
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.board[row + 1][col]:
                    return True
        
        return False
    
    def has_won(self):
        """Check if player has reached 2048"""
        return any(2048 in row for row in self.board)
    
    def reset_game(self):
        """Reset the game"""
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.game_over = False
        self.won = False
        self.continue_after_win = False
    
    def draw_board(self):
        """Draw the game board"""
        self.stdscr.erase()  # Use erase instead of clear to reduce flicker
        height, width = self.stdscr.getmaxyx()
        
        # Draw title
        title = "2048 - Number Puzzle Game"
        self.stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)
        
        # Draw border
        border_top = 3
        border_left = (width - 34) // 2
        
        # Draw score
        score_text = f"Score: {self.score}"
        best_text = f"Best: {self.best_score}"
        self.stdscr.addstr(border_top, border_left, score_text)
        self.stdscr.addstr(border_top, border_left + 20, best_text)
        
        # Draw board border
        board_top = border_top + 2
        self.stdscr.addstr(board_top, border_left, "┌────┬────┬────┬────┐")
        
        # Draw tiles
        for row in range(4):
            y = board_top + 1 + row * 2
            self.stdscr.addstr(y, border_left, "│")
            
            for col in range(4):
                value = self.board[row][col]
                x = border_left + 1 + col * 5
                
                if value == 0:
                    tile_str = "    "
                else:
                    tile_str = f"{value:^4}"
                
                try:
                    self.stdscr.addstr(y, x, tile_str, self.get_color(value))
                except:
                    self.stdscr.addstr(y, x, tile_str)
                
                self.stdscr.addstr(y, x + 4, "│")
            
            # Draw horizontal separator
            if row < 3:
                self.stdscr.addstr(y + 1, border_left, "├────┼────┼────┼────┤")
        
        # Draw bottom border
        self.stdscr.addstr(board_top + 8, border_left, "└────┴────┴────┴────┘")
        
        # Draw instructions
        instructions_y = board_top + 10
        self.stdscr.addstr(instructions_y, border_left, "↑↓←→: Move tiles")
        self.stdscr.addstr(instructions_y + 1, border_left, "R: Restart    Q: Quit")
        
        # Draw game status
        if self.won and not self.continue_after_win:
            msg = "You Won! Press C to continue or Q to quit"
            msg_y = board_top + 4
            msg_x = border_left + (34 - len(msg)) // 2
            self.stdscr.addstr(msg_y, msg_x, msg, curses.A_BOLD | curses.A_REVERSE)
        elif self.game_over:
            msg = "Game Over! Press R to restart"
            msg_y = board_top + 4
            msg_x = border_left + (34 - len(msg)) // 2
            self.stdscr.addstr(msg_y, msg_x, msg, curses.A_BOLD | curses.A_REVERSE)
        
        self.stdscr.refresh()
    
    def run(self):
        """Main game loop"""
        while True:
            self.draw_board()
            
            # Get input
            try:
                key = self.stdscr.getch()
            except:
                continue
            
            # Handle quit
            if key in [ord('q'), ord('Q')]:
                break
            
            # Handle restart
            if key in [ord('r'), ord('R')]:
                self.reset_game()
                continue
            
            # Handle continue after win
            if self.won and not self.continue_after_win:
                if key in [ord('c'), ord('C')]:
                    self.continue_after_win = True
                continue
            
            # Don't allow moves if game is over
            if self.game_over:
                continue
            
            # Handle movement
            moved = False
            score_gain = 0
            
            if key == curses.KEY_UP:
                moved, score_gain = self.move_up()
            elif key == curses.KEY_DOWN:
                moved, score_gain = self.move_down()
            elif key == curses.KEY_LEFT:
                moved, score_gain = self.move_left()
            elif key == curses.KEY_RIGHT:
                moved, score_gain = self.move_right()
            
            # If moved, add new tile and update score
            if moved:
                self.score += score_gain
                if self.score > self.best_score:
                    self.best_score = self.score
                
                self.add_new_tile()
                
                # Check win condition
                if self.has_won() and not self.won:
                    self.won = True
                
                # Check game over
                if not self.can_move():
                    self.game_over = True

def main(stdscr=None):
    """Entry point for the game"""
    if stdscr is None:
        wrapper(main)
    else:
        game = Game2048(stdscr)
        game.run()

if __name__ == "__main__":
    main()
