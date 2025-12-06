"""
Game 004: Space Invaders
經典的太空侵略者射擊遊戲
控制: ← → 移動, 空白鍵射擊, q 退出
"""

import curses
import time
import random
from typing import List, Tuple, Optional

# 遊戲常數
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 30
FPS = 30
FRAME_TIME = 1.0 / FPS

# 遊戲區域（扣除邊框和 UI）
GAME_LEFT = 2
GAME_RIGHT = SCREEN_WIDTH - 3
GAME_TOP = 3
GAME_BOTTOM = SCREEN_HEIGHT - 3

# 外星人設定
ALIEN_ROWS = 5
ALIEN_COLS = 10
ALIEN_START_Y = 5
ALIEN_SPACING_X = 4
ALIEN_SPACING_Y = 2
ALIEN_MOVE_DELAY = 0.5  # 初始移動延遲（秒）

# 玩家設定
PLAYER_Y = GAME_BOTTOM - 2
PLAYER_START_X = SCREEN_WIDTH // 2
PLAYER_LIVES = 3

# 掩體設定
SHIELD_COUNT = 4
SHIELD_WIDTH = 5
SHIELD_HEIGHT = 2
SHIELD_Y = PLAYER_Y - 4

# 得分
ALIEN_SCORES = {0: 30, 1: 20, 2: 20, 3: 10, 4: 10}
UFO_SCORE_MIN = 50
UFO_SCORE_MAX = 300


class Bullet:
    """子彈類別"""
    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.direction = direction  # -1 向上, +1 向下
        self.active = True
    
    def move(self):
        """移動子彈"""
        self.y += self.direction
        if self.y < GAME_TOP or self.y > GAME_BOTTOM:
            self.active = False
    
    def get_char(self) -> str:
        """取得顯示字元"""
        return "|" if self.direction == -1 else "!"


class Alien:
    """外星人類別"""
    def __init__(self, x: int, y: int, alien_type: int):
        self.x = x
        self.y = y
        self.type = alien_type
        self.alive = True
        self.frame = 0  # 動畫幀
    
    def get_char(self) -> str:
        """取得顯示字元（帶動畫）"""
        chars = {
            0: ["<o>", "<O>"],  # 頂層
            1: ["/M\\", "\\M/"],  # 中層上
            2: ["/W\\", "\\W/"],  # 中層下
            3: [")o(", "(o)"],  # 底層上
            4: [">o<", "<o>"],  # 底層下
        }
        return chars[self.type][self.frame % 2]
    
    def get_score(self) -> int:
        """取得擊殺得分"""
        return ALIEN_SCORES[self.type]


class Shield:
    """掩體類別"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.blocks = [[3 for _ in range(SHIELD_WIDTH)] for _ in range(SHIELD_HEIGHT)]
    
    def damage(self, x: int, y: int) -> bool:
        """對掩體造成傷害"""
        local_x = x - self.x
        local_y = y - self.y
        
        if 0 <= local_x < SHIELD_WIDTH and 0 <= local_y < SHIELD_HEIGHT:
            if self.blocks[local_y][local_x] > 0:
                self.blocks[local_y][local_x] -= 1
                return True
        return False
    
    def get_char(self, x: int, y: int) -> str:
        """取得該位置的顯示字元"""
        local_x = x - self.x
        local_y = y - self.y
        
        if 0 <= local_x < SHIELD_WIDTH and 0 <= local_y < SHIELD_HEIGHT:
            health = self.blocks[local_y][local_x]
            chars = [" ", "░", "▒", "▓"]
            return chars[health]
        return " "


class UFO:
    """神秘飛船類別"""
    def __init__(self):
        self.x = 0
        self.y = GAME_TOP
        self.direction = 1
        self.active = False
        self.score_value = 0
    
    def spawn(self):
        """生成 UFO"""
        self.active = True
        self.direction = random.choice([-1, 1])
        self.x = GAME_LEFT if self.direction == 1 else GAME_RIGHT
        self.score_value = random.randint(UFO_SCORE_MIN, UFO_SCORE_MAX)
    
    def move(self):
        """移動 UFO"""
        if not self.active:
            return
        
        self.x += self.direction
        if self.x < GAME_LEFT or self.x > GAME_RIGHT:
            self.active = False
    
    def get_char(self) -> str:
        """取得顯示字元"""
        return "<-UFO->"


class SpaceInvaders:
    """太空侵略者遊戲主類別"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_colors()
        
        # 遊戲狀態
        self.player_x = PLAYER_START_X
        self.lives = PLAYER_LIVES
        self.score = 0
        self.high_score = 0
        self.level = 1
        
        # 遊戲物件
        self.aliens: List[List[Optional[Alien]]] = []
        self.player_bullets: List[Bullet] = []
        self.alien_bullets: List[Bullet] = []
        self.shields: List[Shield] = []
        self.ufo = UFO()
        
        # 遊戲邏輯
        self.alien_direction = 1
        self.alien_move_timer = 0
        self.alien_move_delay = ALIEN_MOVE_DELAY
        self.alien_shoot_timer = 0
        self.ufo_spawn_timer = 0
        self.animation_timer = 0
        
        self.game_over = False
        self.paused = False
        
        # 初始化遊戲
        self.init_game()
    
    def setup_colors(self):
        """設定顏色"""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # 玩家
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # 外星人
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # 子彈
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # 掩體
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # UFO
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)   # UI
    
    def init_game(self):
        """初始化遊戲"""
        # 初始化外星人
        self.aliens = []
        start_x = (SCREEN_WIDTH - (ALIEN_COLS * ALIEN_SPACING_X)) // 2
        
        for row in range(ALIEN_ROWS):
            alien_row = []
            for col in range(ALIEN_COLS):
                x = start_x + col * ALIEN_SPACING_X
                y = ALIEN_START_Y + row * ALIEN_SPACING_Y
                alien = Alien(x, y, row)
                alien_row.append(alien)
            self.aliens.append(alien_row)
        
        # 初始化掩體
        self.shields = []
        shield_spacing = (GAME_RIGHT - GAME_LEFT) // (SHIELD_COUNT + 1)
        for i in range(SHIELD_COUNT):
            x = GAME_LEFT + shield_spacing * (i + 1) - SHIELD_WIDTH // 2
            shield = Shield(x, SHIELD_Y)
            self.shields.append(shield)
        
        # 重置計時器
        self.alien_move_timer = 0
        self.alien_shoot_timer = 0
        self.ufo_spawn_timer = 0
        self.animation_timer = 0
        
        # 清空子彈
        self.player_bullets = []
        self.alien_bullets = []
        
        # 重置 UFO
        self.ufo.active = False
    
    def count_aliens(self) -> int:
        """計算存活的外星人數量"""
        count = 0
        for row in self.aliens:
            for alien in row:
                if alien and alien.alive:
                    count += 1
        return count
    
    def adjust_alien_speed(self):
        """根據剩餘外星人數量調整速度"""
        total = ALIEN_ROWS * ALIEN_COLS
        alive = self.count_aliens()
        if alive > 0:
            speed_factor = alive / total
            self.alien_move_delay = ALIEN_MOVE_DELAY * speed_factor
            # 最快速度限制
            if self.alien_move_delay < 0.1:
                self.alien_move_delay = 0.1
    
    def move_aliens(self, dt: float):
        """移動外星人群"""
        self.alien_move_timer += dt
        
        if self.alien_move_timer >= self.alien_move_delay:
            self.alien_move_timer = 0
            
            # 檢查是否碰到邊界
            hit_edge = False
            for row in self.aliens:
                for alien in row:
                    if alien and alien.alive:
                        next_x = alien.x + self.alien_direction
                        if next_x < GAME_LEFT or next_x > GAME_RIGHT:
                            hit_edge = True
                            break
                if hit_edge:
                    break
            
            # 碰到邊界：換方向並下移
            if hit_edge:
                self.alien_direction *= -1
                for row in self.aliens:
                    for alien in row:
                        if alien and alien.alive:
                            alien.y += 1
                            
                            # 外星人到達底部 = 遊戲結束
                            if alien.y >= PLAYER_Y:
                                self.game_over = True
            else:
                # 水平移動
                for row in self.aliens:
                    for alien in row:
                        if alien and alien.alive:
                            alien.x += self.alien_direction
            
            # 調整速度
            self.adjust_alien_speed()
    
    def animate_aliens(self, dt: float):
        """外星人動畫"""
        self.animation_timer += dt
        if self.animation_timer >= 0.5:
            self.animation_timer = 0
            for row in self.aliens:
                for alien in row:
                    if alien and alien.alive:
                        alien.frame += 1
    
    def alien_shoot(self, dt: float):
        """外星人射擊"""
        self.alien_shoot_timer += dt
        
        # 每秒有機會射擊
        if self.alien_shoot_timer >= 1.0:
            self.alien_shoot_timer = 0
            
            # 找出每列最前面的外星人
            front_aliens = []
            for col in range(ALIEN_COLS):
                for row in range(ALIEN_ROWS - 1, -1, -1):
                    if self.aliens[row][col] and self.aliens[row][col].alive:
                        front_aliens.append(self.aliens[row][col])
                        break
            
            # 隨機選擇一個射擊
            if front_aliens and random.random() < 0.3:
                shooter = random.choice(front_aliens)
                bullet = Bullet(shooter.x + 1, shooter.y + 1, 1)
                self.alien_bullets.append(bullet)
    
    def spawn_ufo(self, dt: float):
        """生成 UFO"""
        if self.ufo.active:
            return
        
        self.ufo_spawn_timer += dt
        
        # 每 10-20 秒有機會出現
        if self.ufo_spawn_timer >= 10.0 and random.random() < 0.05:
            self.ufo.spawn()
            self.ufo_spawn_timer = 0
    
    def move_bullets(self):
        """移動所有子彈"""
        # 玩家子彈
        for bullet in self.player_bullets:
            bullet.move()
        self.player_bullets = [b for b in self.player_bullets if b.active]
        
        # 外星人子彈
        for bullet in self.alien_bullets:
            bullet.move()
        self.alien_bullets = [b for b in self.alien_bullets if b.active]
    
    def check_collisions(self):
        """檢查碰撞"""
        # 玩家子彈 vs 外星人
        for bullet in self.player_bullets[:]:
            for row in self.aliens:
                for alien in row:
                    if alien and alien.alive:
                        # 簡單的碰撞檢測
                        if alien.y == bullet.y and abs(alien.x - bullet.x) <= 1:
                            alien.alive = False
                            bullet.active = False
                            self.score += alien.get_score()
                            if self.count_aliens() == 0:
                                self.next_level()
                            break
        
        # 玩家子彈 vs UFO
        for bullet in self.player_bullets[:]:
            if self.ufo.active:
                if self.ufo.y == bullet.y and abs(self.ufo.x - bullet.x) <= 3:
                    self.score += self.ufo.score_value
                    self.ufo.active = False
                    bullet.active = False
        
        # 外星人子彈 vs 玩家
        for bullet in self.alien_bullets[:]:
            if bullet.y == PLAYER_Y and abs(bullet.x - self.player_x) <= 1:
                bullet.active = False
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
        
        # 子彈 vs 掩體
        for bullet in self.player_bullets + self.alien_bullets:
            for shield in self.shields:
                if shield.y <= bullet.y < shield.y + SHIELD_HEIGHT:
                    if shield.damage(bullet.x, bullet.y):
                        bullet.active = False
        
        # 清理失效子彈
        self.player_bullets = [b for b in self.player_bullets if b.active]
        self.alien_bullets = [b for b in self.alien_bullets if b.active]
    
    def next_level(self):
        """進入下一關"""
        self.level += 1
        self.init_game()
    
    def handle_input(self, dt: float) -> bool:
        """處理輸入"""
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            return False
        
        if key == ord('p') or key == ord('P'):
            self.paused = not self.paused
            return True
        
        if self.paused or self.game_over:
            return True
        
        # 處理移動按鍵
        if key == curses.KEY_LEFT:
            self.player_x = max(GAME_LEFT, self.player_x - 1)
        elif key == curses.KEY_RIGHT:
            self.player_x = min(GAME_RIGHT, self.player_x + 1)
        elif key == ord(' '):
            # 射擊（限制同時只能有一發子彈）
            if len(self.player_bullets) == 0:
                bullet = Bullet(self.player_x, PLAYER_Y - 1, -1)
                self.player_bullets.append(bullet)
        
        return True
    
    def update(self, dt: float):
        """更新遊戲狀態"""
        if self.paused or self.game_over:
            return
        
        self.move_aliens(dt)
        self.animate_aliens(dt)
        self.alien_shoot(dt)
        self.spawn_ufo(dt)
        self.move_bullets()
        self.ufo.move()
        self.check_collisions()
        
        # 更新最高分
        if self.score > self.high_score:
            self.high_score = self.score
    
    def render(self):
        """渲染遊戲畫面"""
        # 使用 erase() 而不是 clear() 來減少閃爍
        self.stdscr.erase()
        
        # 繪製邊框
        for y in range(SCREEN_HEIGHT):
            self.stdscr.addstr(y, 0, "│", curses.color_pair(6))
            self.stdscr.addstr(y, SCREEN_WIDTH - 1, "│", curses.color_pair(6))
        
        for x in range(SCREEN_WIDTH):
            self.stdscr.addstr(0, x, "─", curses.color_pair(6))
            self.stdscr.addstr(SCREEN_HEIGHT - 1, x, "─", curses.color_pair(6))
        
        self.stdscr.addstr(0, 0, "┌", curses.color_pair(6))
        self.stdscr.addstr(0, SCREEN_WIDTH - 1, "┐", curses.color_pair(6))
        self.stdscr.addstr(SCREEN_HEIGHT - 1, 0, "└", curses.color_pair(6))
        self.stdscr.addstr(SCREEN_HEIGHT - 1, SCREEN_WIDTH - 1, "┘", curses.color_pair(6))
        
        # 繪製 UI
        score_str = f"SCORE: {self.score:05d}"
        lives_str = f"LIVES: {'❤' * self.lives}"
        hi_str = f"HI: {self.high_score:05d}"
        level_str = f"LEVEL: {self.level}"
        
        self.stdscr.addstr(1, 3, score_str, curses.color_pair(6))
        self.stdscr.addstr(1, 25, lives_str, curses.color_pair(1))
        self.stdscr.addstr(1, 45, hi_str, curses.color_pair(6))
        self.stdscr.addstr(1, 60, level_str, curses.color_pair(6))
        
        # 繪製外星人
        for row in self.aliens:
            for alien in row:
                if alien and alien.alive:
                    char = alien.get_char()
                    self.stdscr.addstr(alien.y, alien.x, char, curses.color_pair(2))
        
        # 繪製 UFO
        if self.ufo.active:
            char = self.ufo.get_char()
            self.stdscr.addstr(self.ufo.y, max(0, self.ufo.x), char[:min(len(char), SCREEN_WIDTH - self.ufo.x)], curses.color_pair(5))
        
        # 繪製掩體
        for shield in self.shields:
            for dy in range(SHIELD_HEIGHT):
                for dx in range(SHIELD_WIDTH):
                    char = shield.get_char(shield.x + dx, shield.y + dy)
                    if char != " ":
                        self.stdscr.addstr(shield.y + dy, shield.x + dx, char, curses.color_pair(4))
        
        # 繪製子彈
        for bullet in self.player_bullets:
            self.stdscr.addstr(bullet.y, bullet.x, bullet.get_char(), curses.color_pair(3))
        
        for bullet in self.alien_bullets:
            self.stdscr.addstr(bullet.y, bullet.x, bullet.get_char(), curses.color_pair(3))
        
        # 繪製玩家
        if not self.game_over:
            self.stdscr.addstr(PLAYER_Y, self.player_x, "▲", curses.color_pair(1))
        
        # 繪製控制說明
        controls = "← → Move | SPACE Shoot | P Pause | Q Quit"
        self.stdscr.addstr(SCREEN_HEIGHT - 2, (SCREEN_WIDTH - len(controls)) // 2, controls, curses.color_pair(6))
        
        # 遊戲狀態訊息
        if self.game_over:
            msg = "GAME OVER! Press Q to quit"
            self.stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - len(msg)) // 2, msg, curses.color_pair(2) | curses.A_BOLD)
        elif self.paused:
            msg = "PAUSED - Press P to continue"
            self.stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - len(msg)) // 2, msg, curses.color_pair(6) | curses.A_BOLD)
        
        self.stdscr.refresh()
    
    def run(self):
        """遊戲主迴圈"""
        curses.curs_set(0)  # 隱藏游標
        self.stdscr.nodelay(True)  # 非阻塞輸入
        self.stdscr.timeout(0)  # 不等待輸入
        
        # 啟用雙緩衝來減少閃爍
        try:
            curses.cbreak()
            self.stdscr.keypad(True)
        except:
            pass
        
        last_time = time.time()
        
        while True:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # 處理輸入
            if not self.handle_input(dt):
                break
            
            # 更新遊戲
            self.update(dt)
            
            # 渲染
            self.render()
            
            # 控制幀率
            elapsed = time.time() - current_time
            sleep_time = FRAME_TIME - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)


def main():
    """遊戲入口"""
    try:
        curses.wrapper(lambda stdscr: SpaceInvaders(stdscr).run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
