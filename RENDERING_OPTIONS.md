# CLI 遊戲渲染方案比較

## 問題：畫面閃爍
當前使用 `os.system('clear')` 會導致：
- 整個螢幕清空再重繪，造成閃爍
- 終端機需要完整重新渲染

## 解決方案比較

### 方案 1: curses (推薦 ⭐⭐⭐⭐⭐)
**優點：**
- Python 內建，無需額外安裝
- 專門為終端遊戲設計
- 雙緩衝機制，完全無閃爍
- 可以控制單個字元位置
- 支援顏色、鍵盤事件
- 效能最好

**缺點：**
- Windows 需要安裝 windows-curses
- API 稍微複雜一點

**適用：** 所有動作類遊戲（打磚塊、貪吃蛇、Tetris等）

### 方案 2: Rich Live Display (推薦 ⭐⭐⭐⭐)
**優點：**
- 已經在依賴中（rich）
- 自動處理更新，減少閃爍
- 支援漂亮的格式和顏色
- 跨平台無問題

**缺點：**
- 不如 curses 即時
- 較適合刷新頻率較低的遊戲

**適用：** 回合制遊戲、策略遊戲

### 方案 3: ANSI Escape Codes (推薦 ⭐⭐⭐)
**優點：**
- 無需額外依賴
- 可以定位游標到任意位置
- 不需要完整清屏

**缺點：**
- 需要手動處理
- Windows 支援較差（需 colorama）

**適用：** 簡單動畫、文字特效

### 方案 4: 雙緩衝 + ANSI (推薦 ⭐⭐⭐⭐)
**優點：**
- 只更新變化的部分
- 大幅減少閃爍
- 較簡單實現

**缺點：**
- 需要追蹤前一幀狀態

## 建議

### 立即改進（簡單）：
使用 **ANSI Escape Codes** 替換 clear：
- 游標移動而非清屏
- 只重繪需要的部分
- 約 10 行程式碼改動

### 最佳方案（推薦）：
使用 **curses** 重寫：
- 完全無閃爍
- 更好的效能
- 更專業的遊戲體驗
- 約 30-50 行程式碼改動

### 折衷方案：
使用 **Rich Live Display**：
- 利用現有依賴
- 程式碼改動中等
- 適合部分遊戲類型

## 實作範例

### 方案 A: ANSI Codes（快速修正）
```python
def clear_screen():
    print('\033[2J\033[H', end='')  # 清屏並移動游標到左上角

def move_cursor(x, y):
    print(f'\033[{y};{x}H', end='')

# 隱藏游標減少閃爍
print('\033[?25l', end='')  # 隱藏
# ... 遊戲 ...
print('\033[?25h', end='')  # 顯示
```

### 方案 B: curses（最佳方案）
```python
import curses

def main(stdscr):
    curses.curs_set(0)  # 隱藏游標
    stdscr.nodelay(1)   # 非阻塞輸入
    
    while running:
        stdscr.clear()
        # 繪製遊戲
        stdscr.addstr(y, x, "●")
        stdscr.refresh()  # 雙緩衝刷新

curses.wrapper(main)
```

### 方案 C: Rich Live
```python
from rich.live import Live
from rich.panel import Panel

with Live(Panel("Game"), refresh_per_second=30) as live:
    while running:
        # 更新遊戲狀態
        live.update(Panel(render_game()))
```

## 建議實作順序

1. **今天（Day 1）**: 使用 ANSI 快速修正打磚塊
2. **Day 2-3**: 使用 curses 重寫打磚塊和貪吃蛇
3. **後續遊戲**: 根據類型選擇合適方案
   - 動作遊戲 → curses
   - 回合制 → Rich Live
   - 簡單遊戲 → ANSI

