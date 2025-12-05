"""
Game 001: Breakout (打磚塊)
Classic brick breaking game with paddle and ball
Using curses for flicker-free rendering
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
        self.init_curses()
        self.init_bricks()
    
    def init_curses(self):
        """Initialize curses settings"""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(1)  # Non-blocking input
        self.stdscr.timeout(50)  # 50ms timeout for getch()
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
        # Store previous ball position to erase
        self.prev_ball_x = int(self.ball_x)
        self.prev_ball_y = int(self.ball_y)
        self.prev_paddle_pos = self.paddle_pos
        
        # Draw static elements once
        self.draw_static_elements()
    
    def init_bricks(self):
        """Initialize bricks in rows"""
        for row in range(5):
            brick_row = []
            for col in range(10):
                x = col * 6 + 2
                y = row * 2 + 2
                brick = {
                    'x': x,
                    'y': y,
                    'width': 5,
                    'color': row + 1,  # Color pair number
                    'active': True
                }
                brick_row.append(brick)
            self.bricks.append(brick_row)
    
    def draw_static_elements(self):
        """Draw elements that don't change (borders and initial bricks)"""
        try:
            # Draw top border
            self.stdscr.addstr(0, 0, '╔' + '═' * (self.width - 2) + '╗')
            
            # Draw side borders
            for y in range(1, self.height - 1):
                self.stdscr.addstr(y, 0, '║')
                self.stdscr.addstr(y, self.width - 1, '║')
            
            # Draw bottom border
            self.stdscr.addstr(self.height - 1, 0, '╚' + '═' * (self.width - 2) + '╝')
            
            self.stdscr.refresh()
        except curses.error:
            pass
    
    def draw(self):
        """Draw only dynamic elements (no clear, just update changed parts)"""
        try:
            # Erase old paddle position
            if self.prev_paddle_pos != self.paddle_pos:
                erase_str = ' ' * self.paddle_width
                self.stdscr.addstr(self.height - 2, self.prev_paddle_pos, erase_str)
                self.prev_paddle_pos = self.paddle_pos
            
            # Draw paddle at new position
            paddle_str = '▬' * self.paddle_width
            self.stdscr.addstr(self.height - 2, self.paddle_pos, paddle_str, 
                             curses.color_pair(6))
            
            # Erase old ball position
            if 0 < self.prev_ball_x < self.width - 1 and 0 < self.prev_ball_y < self.height - 1:
                self.stdscr.addstr(self.prev_ball_y, self.prev_ball_x, ' ')
            
            # Draw ball at new position
            ball_y = int(self.ball_y)
            ball_x = int(self.ball_x)
            if 0 < ball_x < self.width - 1 and 0 < ball_y < self.height - 1:
                self.stdscr.addstr(ball_y, ball_x, '●', 
                                 curses.color_pair(6) | curses.A_BOLD)
            
            # Update previous positions
            self.prev_ball_x = ball_x
            self.prev_ball_y = ball_y
            
            # Draw bricks (only active ones)
            for row in self.bricks:
                for brick in row:
                    if brick['active']:
                        y = brick['y']
                        if 0 < y < self.height - 1:
                            brick_str = '█' * brick['width']
                            self.stdscr.addstr(y, brick['x'], brick_str, 
                                             curses.color_pair(brick['color']))
            
            # Draw status (always update)
            status = f" Score: {self.score}  Lives: {'♥' * self.lives}  Controls: ← →  (q to quit) "
            self.stdscr.addstr(self.height + 1, 0, status[:self.width])
            
            self.stdscr.refresh()
        except curses.error:
            pass  # Ignore errors from drawing outside screen
    
    def update(self):
        """Update game state"""
        if self.game_over or self.won:
            return
        
        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Ball collision with walls
        if self.ball_x <= 1:
            self.ball_x = 1
            self.ball_dx = abs(self.ball_dx)
        
        if self.ball_x >= self.width - 2:
            self.ball_x = self.width - 2
            self.ball_dx = -abs(self.ball_dx)
        
        if self.ball_y <= 1:
            self.ball_y = 1
            self.ball_dy = abs(self.ball_dy)
        
        # Ball collision with paddle
        if int(self.ball_y) == self.height - 3:
            if self.paddle_pos <= self.ball_x <= self.paddle_pos + self.paddle_width:
                self.ball_dy = -abs(self.ball_dy)
                # Add spin based on where ball hits paddle
                hit_pos = (self.ball_x - self.paddle_pos) / self.paddle_width
                self.ball_dx = (hit_pos - 0.5) * 1.5
        
        # Ball falls off bottom
        if self.ball_y >= self.height - 2:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # Reset ball
                self.ball_x = float(self.width // 2)
                self.ball_y = float(self.height - 5)
                self.ball_dx = random.choice([-1, 1]) * 0.5
                self.ball_dy = -1.0
                time.sleep(0.5)
        
        # Ball collision with bricks
        for row in self.bricks:
            for brick in row:
                if brick['active']:
                    if (brick['y'] - 1 <= self.ball_y <= brick['y'] + 1 and
                        brick['x'] <= self.ball_x <= brick['x'] + brick['width']):
                        brick['active'] = False
                        self.ball_dy = -self.ball_dy
                        self.score += 10
                        # Erase the brick immediately
                        try:
                            erase_str = ' ' * brick['width']
                            self.stdscr.addstr(brick['y'], brick['x'], erase_str)
                        except curses.error:
                            pass
                        break
        
        # Check win condition
        all_destroyed = all(not brick['active'] for row in self.bricks for brick in row)
        if all_destroyed:
            self.won = True
    
    def handle_input(self):
        """Handle user input using curses"""
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            self.running = False
        elif key == curses.KEY_LEFT:
            self.paddle_pos = max(1, self.paddle_pos - 3)
        elif key == curses.KEY_RIGHT:
            self.paddle_pos = min(self.width - self.paddle_width - 1, self.paddle_pos + 3)
        elif key == ord('a') or key == ord('A'):
            self.paddle_pos = max(1, self.paddle_pos - 3)
        elif key == ord('d') or key == ord('D'):
            self.paddle_pos = min(self.width - self.paddle_width - 1, self.paddle_pos + 3)
    
    def run(self):
        """Main game loop using curses"""
        while self.running:
            self.draw()
            
            if self.game_over:
                try:
                    self.stdscr.addstr(self.height // 2, self.width // 2 - 10, 
                                     "💥 GAME OVER! 💥", curses.color_pair(1) | curses.A_BOLD)
                    self.stdscr.addstr(self.height // 2 + 1, self.width // 2 - 10, 
                                     f"Final Score: {self.score}", curses.color_pair(6))
                    self.stdscr.addstr(self.height // 2 + 3, self.width // 2 - 15, 
                                     "Press any key to return...", curses.color_pair(6))
                    self.stdscr.refresh()
                except curses.error:
                    pass
                self.stdscr.nodelay(0)
                self.stdscr.getch()
                break
            
            if self.won:
                try:
                    self.stdscr.addstr(self.height // 2, self.width // 2 - 8, 
                                     "🎉 YOU WIN! 🎉", curses.color_pair(3) | curses.A_BOLD)
                    self.stdscr.addstr(self.height // 2 + 1, self.width // 2 - 10, 
                                     f"Final Score: {self.score}", curses.color_pair(6))
                    self.stdscr.addstr(self.height // 2 + 3, self.width // 2 - 15, 
                                     "Press any key to return...", curses.color_pair(6))
                    self.stdscr.refresh()
                except curses.error:
                    pass
                self.stdscr.nodelay(0)
                self.stdscr.getch()
                break
            
            self.handle_input()
            self.update()
            time.sleep(0.05)

def game_main(stdscr):
    """Main game function for curses wrapper"""
    game = Breakout(stdscr)
    game.run()

def main():
    """Run the Breakout game with curses"""
    try:
        curses.wrapper(game_main)
    except KeyboardInterrupt:
        pass
    
    print("\n🎮 BREAKOUT (打磚塊) 🎮")
    print("Press Enter to return to menu...")
    input()

if __name__ == "__main__":
    main()
