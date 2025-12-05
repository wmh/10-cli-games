"""
Game 003: Pong (乒乓球)
Classic two-player paddle game with smooth curses rendering
"""
import curses
import time
import random

class Pong:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.width = 60
        self.height = 25
        
        # Paddles
        self.paddle_height = 5
        self.paddle1_y = self.height // 2 - self.paddle_height // 2
        self.paddle2_y = self.height // 2 - self.paddle_height // 2
        self.paddle1_x = 2
        self.paddle2_x = self.width - 3
        
        # Ball
        self.ball_x = float(self.width // 2)
        self.ball_y = float(self.height // 2)
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.uniform(-0.5, 0.5)
        
        # Game state
        self.score1 = 0
        self.score2 = 0
        self.winning_score = 11
        self.game_over = False
        self.winner = None
        self.paused = False
        self.running = True
        
        # Speed
        self.ball_speed = 0.05
        
        # Previous positions for erasing
        self.prev_ball_x = int(self.ball_x)
        self.prev_ball_y = int(self.ball_y)
        self.prev_paddle1_y = self.paddle1_y
        self.prev_paddle2_y = self.paddle2_y
        
        self.init_curses()
        self.draw_static()
    
    def init_curses(self):
        """Initialize curses settings"""
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(0)
        
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Paddles
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Ball
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Border
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Text
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)     # Winner
    
    def draw_static(self):
        """Draw static elements (border and center line)"""
        try:
            self.stdscr.clear()
            
            # Draw border
            self.stdscr.addstr(0, 0, '╔' + '═' * (self.width - 2) + '╗', 
                             curses.color_pair(3))
            for y in range(1, self.height - 1):
                self.stdscr.addstr(y, 0, '║', curses.color_pair(3))
                self.stdscr.addstr(y, self.width - 1, '║', curses.color_pair(3))
            self.stdscr.addstr(self.height - 1, 0, '╚' + '═' * (self.width - 2) + '╝',
                             curses.color_pair(3))
            
            # Draw center line
            center_x = self.width // 2
            for y in range(1, self.height - 1, 2):
                self.stdscr.addstr(y, center_x, '│', curses.color_pair(3))
            
            self.stdscr.noutrefresh()
        except curses.error:
            pass
    
    def reset_ball(self):
        """Reset ball to center after scoring"""
        self.ball_x = float(self.width // 2)
        self.ball_y = float(self.height // 2)
        # Ball goes toward the player who just lost the point
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.uniform(-0.5, 0.5)
    
    def draw(self):
        """Draw game elements (incremental rendering)"""
        try:
            # Erase old ball position
            if 0 < self.prev_ball_x < self.width - 1 and 0 < self.prev_ball_y < self.height - 1:
                self.stdscr.addstr(self.prev_ball_y, self.prev_ball_x, ' ')
            
            # Always erase old paddle positions (complete erase)
            for i in range(self.paddle_height):
                if 0 < self.prev_paddle1_y + i < self.height - 1:
                    self.stdscr.addstr(self.prev_paddle1_y + i, self.paddle1_x, ' ')
                if 0 < self.prev_paddle2_y + i < self.height - 1:
                    self.stdscr.addstr(self.prev_paddle2_y + i, self.paddle2_x, ' ')
            
            # Update previous positions
            self.prev_paddle1_y = self.paddle1_y
            self.prev_paddle2_y = self.paddle2_y
            
            # Redraw center line (before drawing paddles and ball)
            center_x = self.width // 2
            for y in range(1, self.height - 1, 2):
                self.stdscr.addstr(y, center_x, '│', curses.color_pair(3))
            
            # Draw paddles (will cover center line if needed)
            for i in range(self.paddle_height):
                # Left paddle
                if 0 < self.paddle1_y + i < self.height - 1:
                    self.stdscr.addstr(self.paddle1_y + i, self.paddle1_x, '▓', 
                                     curses.color_pair(1))
                # Right paddle
                if 0 < self.paddle2_y + i < self.height - 1:
                    self.stdscr.addstr(self.paddle2_y + i, self.paddle2_x, '▓',
                                     curses.color_pair(1))
            
            # Draw ball
            ball_y = int(self.ball_y)
            ball_x = int(self.ball_x)
            if 0 < ball_x < self.width - 1 and 0 < ball_y < self.height - 1:
                self.stdscr.addstr(ball_y, ball_x, '●', 
                                 curses.color_pair(2) | curses.A_BOLD)
            
            # Update previous ball position
            self.prev_ball_x = ball_x
            self.prev_ball_y = ball_y
            
            # Draw scores
            status = f"Player 1: {self.score1}    [First to {self.winning_score} wins]    Player 2: {self.score2}"
            status_x = (self.width - len(status)) // 2
            self.stdscr.addstr(self.height + 1, status_x, status, curses.color_pair(4))
            
            # Draw controls
            controls = "W/S: P1   ↑/↓: P2   Space: Pause   Q: Quit"
            controls_x = (self.width - len(controls)) // 2
            self.stdscr.addstr(self.height + 2, controls_x, controls, curses.color_pair(4))
            
            # Draw pause message
            if self.paused:
                msg = "*** PAUSED - Press Space to continue ***"
                msg_x = (self.width - len(msg)) // 2
                self.stdscr.addstr(self.height // 2, msg_x, msg, 
                                 curses.color_pair(2) | curses.A_BOLD)
            
            self.stdscr.noutrefresh()
            curses.doupdate()
            
        except curses.error:
            pass
    
    def handle_input(self):
        """Handle keyboard input"""
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            self.running = False
            return
        
        if key == ord(' '):
            self.paused = not self.paused
            return
        
        if self.paused:
            return
        
        # Player 1 controls (W/S)
        if key == ord('w') or key == ord('W'):
            self.paddle1_y = max(1, self.paddle1_y - 1)
        elif key == ord('s') or key == ord('S'):
            self.paddle1_y = min(self.height - self.paddle_height - 1, self.paddle1_y + 1)
        
        # Player 2 controls (Arrow keys)
        elif key == curses.KEY_UP:
            self.paddle2_y = max(1, self.paddle2_y - 1)
        elif key == curses.KEY_DOWN:
            self.paddle2_y = min(self.height - self.paddle_height - 1, self.paddle2_y + 1)
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Ball collision with top/bottom walls
        if self.ball_y <= 1:
            self.ball_y = 1
            self.ball_dy = abs(self.ball_dy)
        elif self.ball_y >= self.height - 2:
            self.ball_y = self.height - 2
            self.ball_dy = -abs(self.ball_dy)
        
        # Ball collision with left paddle
        if (self.paddle1_x <= self.ball_x <= self.paddle1_x + 1 and
            self.paddle1_y <= self.ball_y < self.paddle1_y + self.paddle_height):
            self.ball_x = self.paddle1_x + 1
            self.ball_dx = abs(self.ball_dx)
            # Adjust angle based on hit position
            hit_pos = (self.ball_y - self.paddle1_y) / self.paddle_height
            self.ball_dy = (hit_pos - 0.5) * 2
        
        # Ball collision with right paddle
        if (self.paddle2_x - 1 <= self.ball_x <= self.paddle2_x and
            self.paddle2_y <= self.ball_y < self.paddle2_y + self.paddle_height):
            self.ball_x = self.paddle2_x - 1
            self.ball_dx = -abs(self.ball_dx)
            # Adjust angle based on hit position
            hit_pos = (self.ball_y - self.paddle2_y) / self.paddle_height
            self.ball_dy = (hit_pos - 0.5) * 2
        
        # Scoring
        if self.ball_x <= 1:
            # Player 2 scores
            self.score2 += 1
            if self.score2 >= self.winning_score:
                self.game_over = True
                self.winner = 2
            else:
                self.reset_ball()
                time.sleep(0.5)
        elif self.ball_x >= self.width - 2:
            # Player 1 scores
            self.score1 += 1
            if self.score1 >= self.winning_score:
                self.game_over = True
                self.winner = 1
            else:
                self.reset_ball()
                time.sleep(0.5)
    
    def run(self):
        """Main game loop"""
        last_update = time.time()
        
        while self.running:
            current_time = time.time()
            
            self.handle_input()
            
            # Update game at appropriate speed
            if not self.paused and current_time - last_update >= self.ball_speed:
                self.update()
                last_update = current_time
            
            self.draw()
            
            if self.game_over:
                try:
                    msg_y = self.height // 2
                    win_msg = f"🏓 PLAYER {self.winner} WINS! 🏓"
                    self.stdscr.addstr(msg_y, self.width // 2 - len(win_msg) // 2,
                                     win_msg, 
                                     curses.color_pair(5) | curses.A_BOLD)
                    score_msg = f"Final Score: {self.score1} - {self.score2}"
                    self.stdscr.addstr(msg_y + 2, self.width // 2 - len(score_msg) // 2,
                                     score_msg,
                                     curses.color_pair(4))
                    continue_msg = "Press any key..."
                    self.stdscr.addstr(msg_y + 4, self.width // 2 - len(continue_msg) // 2,
                                     continue_msg,
                                     curses.color_pair(4))
                    self.stdscr.refresh()
                except curses.error:
                    pass
                self.stdscr.nodelay(0)
                self.stdscr.getch()
                break
            
            time.sleep(0.01)

def game_main(stdscr):
    """Main game function for curses wrapper"""
    game = Pong(stdscr)
    game.run()

def main():
    """Entry point"""
    try:
        curses.wrapper(game_main)
    except KeyboardInterrupt:
        pass
    
    print("\n🏓 PONG (乒乓球) 🏓")
    print("Press Enter to return to menu...")
    input()

if __name__ == "__main__":
    main()
