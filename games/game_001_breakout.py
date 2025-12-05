"""
Game 001: Breakout (打磚塊) - Version 3
Ultra smooth with minimal redraw
"""
import curses
import time
import random

class Breakout:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.width = 60
        self.height = 25
        self.paddle_width = 8
        self.paddle_pos = self.width // 2 - self.paddle_width // 2
        self.ball_x = float(self.width // 2)
        self.ball_y = float(self.height - 5)
        self.ball_dx = random.choice([-1, 1]) * 0.5
        self.ball_dy = -1.0
        self.score = 0
        self.lives = 3
        self.bricks = []
        self.game_over = False
        self.won = False
        self.running = True
        
        # Store previous positions
        self.prev_ball_x = int(self.ball_x)
        self.prev_ball_y = int(self.ball_y)
        self.prev_paddle_pos = self.paddle_pos
        self.prev_score = 0
        self.prev_lives = 3
        
        self.init_curses()
        self.init_bricks()
        self.draw_static()
    
    def init_curses(self):
        """Initialize curses settings"""
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(50)
        
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    def init_bricks(self):
        """Initialize bricks"""
        # Game width: 60, borders: 2, usable width: 58
        # Use 9 bricks per row to fit nicely: 9 * 6 = 54, leaving margin
        brick_width = 5
        brick_spacing = 1
        total_bricks_per_row = 9
        
        # Center the bricks
        total_width = total_bricks_per_row * brick_width + (total_bricks_per_row - 1) * brick_spacing
        start_x = (self.width - total_width) // 2
        
        for row in range(5):
            brick_row = []
            for col in range(total_bricks_per_row):
                x = start_x + col * (brick_width + brick_spacing)
                brick = {
                    'x': x,
                    'y': row * 2 + 2,
                    'width': brick_width,
                    'color': row + 1,
                    'active': True
                }
                brick_row.append(brick)
            self.bricks.append(brick_row)
    
    def draw_static(self):
        """Draw static elements once"""
        try:
            self.stdscr.clear()
            
            # Borders
            self.stdscr.addstr(0, 0, '╔' + '═' * (self.width - 2) + '╗')
            for y in range(1, self.height - 1):
                self.stdscr.addstr(y, 0, '║')
                self.stdscr.addstr(y, self.width - 1, '║')
            self.stdscr.addstr(self.height - 1, 0, '╚' + '═' * (self.width - 2) + '╝')
            
            # Draw all bricks initially
            for row in self.bricks:
                for brick in row:
                    if brick['active']:
                        brick_str = '█' * brick['width']
                        self.stdscr.addstr(brick['y'], brick['x'], brick_str, 
                                         curses.color_pair(brick['color']))
            
            self.stdscr.noutrefresh()
        except curses.error:
            pass
    
    def draw(self):
        """Only redraw moving elements"""
        try:
            # Erase old paddle
            if self.prev_paddle_pos != self.paddle_pos:
                self.stdscr.addstr(self.height - 2, self.prev_paddle_pos, ' ' * self.paddle_width)
            
            # Draw new paddle
            self.stdscr.addstr(self.height - 2, self.paddle_pos, '▬' * self.paddle_width, 
                             curses.color_pair(6))
            self.prev_paddle_pos = self.paddle_pos
            
            # Erase old ball
            ball_y = int(self.ball_y)
            ball_x = int(self.ball_x)
            
            if (self.prev_ball_x != ball_x or self.prev_ball_y != ball_y):
                if 0 < self.prev_ball_x < self.width - 1 and 0 < self.prev_ball_y < self.height - 1:
                    self.stdscr.addstr(self.prev_ball_y, self.prev_ball_x, ' ')
            
            # Draw new ball
            if 0 < ball_x < self.width - 1 and 0 < ball_y < self.height - 1:
                self.stdscr.addstr(ball_y, ball_x, '●', 
                                 curses.color_pair(6) | curses.A_BOLD)
            
            self.prev_ball_x = ball_x
            self.prev_ball_y = ball_y
            
            # Update status only if changed
            if self.prev_score != self.score or self.prev_lives != self.lives:
                status = f" Score: {self.score}  Lives: {'♥' * self.lives}  (← → or AD, Q=quit) "
                self.stdscr.addstr(self.height + 1, 0, status.ljust(self.width))
                self.prev_score = self.score
                self.prev_lives = self.lives
            
            # Use noutrefresh + doupdate for better performance
            self.stdscr.noutrefresh()
            curses.doupdate()
            
        except curses.error:
            pass
    
    def update(self):
        """Update game state"""
        if self.game_over or self.won:
            return
        
        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Wall collisions
        if self.ball_x <= 1:
            self.ball_x = 1
            self.ball_dx = abs(self.ball_dx)
        if self.ball_x >= self.width - 2:
            self.ball_x = self.width - 2
            self.ball_dx = -abs(self.ball_dx)
        if self.ball_y <= 1:
            self.ball_y = 1
            self.ball_dy = abs(self.ball_dy)
        
        # Paddle collision
        if int(self.ball_y) == self.height - 3:
            if self.paddle_pos <= self.ball_x <= self.paddle_pos + self.paddle_width:
                self.ball_dy = -abs(self.ball_dy)
                hit_pos = (self.ball_x - self.paddle_pos) / self.paddle_width
                self.ball_dx = (hit_pos - 0.5) * 1.5
        
        # Ball falls
        if self.ball_y >= self.height - 2:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball_x = float(self.width // 2)
                self.ball_y = float(self.height - 5)
                self.ball_dx = random.choice([-1, 1]) * 0.5
                self.ball_dy = -1.0
                time.sleep(0.5)
        
        # Brick collision
        for row in self.bricks:
            for brick in row:
                if brick['active']:
                    if (brick['y'] - 1 <= self.ball_y <= brick['y'] + 1 and
                        brick['x'] <= self.ball_x <= brick['x'] + brick['width']):
                        brick['active'] = False
                        self.ball_dy = -self.ball_dy
                        self.score += 10
                        # Erase brick
                        try:
                            self.stdscr.addstr(brick['y'], brick['x'], ' ' * brick['width'])
                        except curses.error:
                            pass
                        break
        
        # Check win
        if all(not brick['active'] for row in self.bricks for brick in row):
            self.won = True
    
    def handle_input(self):
        """Handle input"""
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            self.running = False
        elif key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
            self.paddle_pos = max(1, self.paddle_pos - 3)
        elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
            self.paddle_pos = min(self.width - self.paddle_width - 1, self.paddle_pos + 3)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.draw()
            
            if self.game_over:
                try:
                    msg_y = self.height // 2
                    self.stdscr.addstr(msg_y, self.width // 2 - 10, 
                                     "💥 GAME OVER! 💥", curses.color_pair(1) | curses.A_BOLD)
                    self.stdscr.addstr(msg_y + 2, self.width // 2 - 10, 
                                     f"Final Score: {self.score}", curses.color_pair(6))
                    self.stdscr.addstr(msg_y + 4, self.width // 2 - 15, 
                                     "Press any key...", curses.color_pair(6))
                    self.stdscr.refresh()
                except curses.error:
                    pass
                self.stdscr.nodelay(0)
                self.stdscr.getch()
                break
            
            if self.won:
                try:
                    msg_y = self.height // 2
                    self.stdscr.addstr(msg_y, self.width // 2 - 8, 
                                     "🎉 YOU WIN! 🎉", curses.color_pair(3) | curses.A_BOLD)
                    self.stdscr.addstr(msg_y + 2, self.width // 2 - 10, 
                                     f"Final Score: {self.score}", curses.color_pair(6))
                    self.stdscr.addstr(msg_y + 4, self.width // 2 - 15, 
                                     "Press any key...", curses.color_pair(6))
                    self.stdscr.refresh()
                except curses.error:
                    pass
                self.stdscr.nodelay(0)
                self.stdscr.getch()
                break
            
            self.handle_input()
            self.update()
            time.sleep(0.03)  # ~33 FPS

def game_main(stdscr):
    """Main game function"""
    game = Breakout(stdscr)
    game.run()

def main():
    """Entry point"""
    try:
        curses.wrapper(game_main)
    except KeyboardInterrupt:
        pass
    
    print("\n🎮 BREAKOUT (打磚塊) 🎮")
    print("Press Enter to return to menu...")
    input()

if __name__ == "__main__":
    main()
