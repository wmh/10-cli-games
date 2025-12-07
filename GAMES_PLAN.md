# 10 CLI Games - Curated Collection

## Project Overview
精選 10 個最適合命令行環境的小遊戲。專注於品質、可玩性和使用者體驗，只選擇真正適合純文字環境的遊戲類型。

## Design Principles 設計原則

### Architecture 架構
- **Modular Design**: 每個遊戲獨立一個檔案，避免單一檔案過大
- **Consistent Interface**: 所有遊戲都有 `main()` 函數作為入口
- **Shared Utilities**: 共用的工具放在 `utils/` 目錄
- **Easy Navigation**: 主選單系統讓玩家輕鬆選擇遊戲

### Technical Stack 技術堆疊
- **Python 3.8+**: 主要開發語言（使用內建模組）
- **rich**: 美化終端輸出
- **colorama**: 跨平台顏色支援

## Complete Game List (10 Games)

### Classic Action (經典動作) - 6 Games
1. ✅ **Breakout** - 打磚塊遊戲，控制板子接球打磚塊
2. ✅ **Snake** - 貪吃蛇，吃食物長大避免撞牆
3. ✅ **Pong** - 雙人乒乓球遊戲
4. ✅ **Space Invaders** - 太空侵略者射擊遊戲
5. ✅ **Tetris** - 俄羅斯方塊
6. ✅ **Pac-Man** - 小精靈迷宮遊戲

### Puzzle & Logic (益智邏輯) - 4 Games
7. ⏳ **2048** - 數字合併益智遊戲（完美適合CLI）
8. ⏳ **Minesweeper** - 踩地雷（經典邏輯遊戲）
9. ⏳ **Wordle** - 猜單字遊戲（文字遊戲最佳代表）
10. ⏳ **Sokoban** - 推箱子（回合制，視覺清晰）

## 為什麼選這 4 個？

### Game 7: 2048
**理由：**
- 完美適合方格顯示
- 數字清晰易讀
- 簡單的方向鍵控制
- 視覺回饋直觀
- 無需即時反應

### Game 8: Minesweeper
**理由：**
- 經典邏輯遊戲
- 回合制，不需要快速反應
- 方格介面適合終端
- 數字提示系統清晰
- 策略性強

### Game 9: Wordle
**理由：**
- 純文字遊戲的最佳代表
- 顏色回饋系統完美
- 每日挑戰模式
- 簡單但有趣
- 目前很流行

### Game 10: Sokoban (推箱子)
**理由：**
- 回合制，可以慢慢思考
- 方格地圖清晰
- 箱子和目標視覺明確
- 經典益智遊戲
- 關卡系統容易擴展

## 放棄的遊戲類型

### 不適合 CLI 的遊戲：
- ❌ **Asteroids** - 需要流暢物理和大小感
- ❌ 大部分射擊遊戲 - 需要精確瞄準
- ❌ 賽車遊戲 - 需要速度感
- ❌ 複雜 RPG - 視覺內容過多
- ❌ 即時戰略 - 需要複雜 UI

### 已完成的遊戲分析：
✅ **成功的**：Snake, Tetris, Pac-Man（簡單、清晰、好玩）
✅ **可以的**：Breakout, Pong, Space Invaders（動作簡單）
❌ **失敗的**：Asteroids（物理和視覺限制）
17. **Crossword** - 填字遊戲
18. **Anagram** - 字母重組
19. **Boggle** - 字母方格找字
20. **Scrabble** - 拼字遊戲
21. **Word Chain** - 文字接龍

### Week 4: Card Games (紙牌遊戲)
22. **Blackjack** - 21點
23. **Poker** - 撲克牌
24. **Solitaire** - 接龍
25. **Uno** - Uno 卡牌遊戲
26. **Memory** - 記憶配對
27. **Go Fish** - 釣魚遊戲
28. **War** - 比大小

### Week 5: Board Games (棋盤遊戲)
29. **Chess** - 西洋棋
30. **Checkers** - 西洋跳棋
31. **Reversi/Othello** - 黑白棋
32. **Connect Four** - 四子棋
33. **Tic-Tac-Toe** - 井字遊戲
34. **Go** - 圍棋（簡化版）
35. **Battleship** - 海戰棋

### Week 6: Adventure & RPG (冒險與角色扮演)
36. **Dungeon Crawler** - 地牢探索
37. **Text Adventure** - 文字冒險
38. **Rogue** - Roguelike 地牢
39. **Turn-based Battle** - 回合制戰鬥
40. **Treasure Hunt** - 尋寶遊戲
41. **Quest Manager** - 任務系統
42. **Character Builder** - 角色創建系統

### Week 7: Strategy Games (策略遊戲)
43. **Tower Defense** - 塔防遊戲
44. **Resource Manager** - 資源管理
45. **City Builder** - 城市建造
46. **Farm Simulator** - 農場經營
47. **Stock Trader** - 股票交易
48. **War Strategy** - 戰爭策略
49. **Civilization Lite** - 文明建造（簡化版）

### Week 8: Racing & Sports (競速與運動)
50. **ASCII Racing** - ASCII 賽車
51. **Horse Racing** - 賽馬
52. **Basketball** - 籃球投籃
53. **Golf** - 迷你高爾夫
54. **Bowling** - 保齡球
55. **Dice Racing** - 骰子賽跑
56. **Marathon** - 馬拉松耐力賽

### Week 9: Quiz & Trivia (問答與知識)
57. **Trivia Quiz** - 綜合知識問答
58. **Math Quiz** - 數學測驗
59. **Geography Quiz** - 地理知識
60. **History Quiz** - 歷史知識
61. **Science Quiz** - 科學知識
62. **Movie Quiz** - 電影知識
63. **Music Quiz** - 音樂知識

### Week 10: Reaction Games (反應遊戲)
64. **Whack-a-Mole** - 打地鼠
65. **Quick Draw** - 快速反應測試
66. **Simon Says** - 記憶序列
67. **Type Racer** - 打字競速
68. **Reflex Test** - 反射神經測試
69. **Rhythm Game** - 節奏遊戲
70. **Dance Dance** - 跳舞機

### Week 11: Math & Logic (數學與邏輯)
71. **Calculator Game** - 計算機謎題
72. **Number Guess** - 猜數字
73. **Math Duel** - 數學對決
74. **Logic Gates** - 邏輯閘謎題
75. **Pattern Recognition** - 圖案識別
76. **Equation Solver** - 方程式求解
77. **Prime Finder** - 質數尋找

### Week 12: Simulation (模擬)
78. **Life Simulator** - 康威生命遊戲
79. **Ant Colony** - 螞蟻群落模擬
80. **Ecosystem** - 生態系統
81. **Weather Sim** - 天氣模擬
82. **Traffic Sim** - 交通流量模擬
83. **Economy Sim** - 經濟模擬
84. **Evolution Sim** - 演化模擬

### Week 13: Artistic (藝術創作)
85. **ASCII Art Creator** - ASCII 藝術創作
86. **Pixel Editor** - 像素編輯器
87. **Animation Player** - 動畫播放器
88. **Color Mixer** - 顏色混合
89. **Pattern Generator** - 圖案生成器
90. **Mandelbrot** - 碎形查看器
91. **Music Composer** - 音樂作曲器

### Week 14: Multiplayer (多人遊戲)
92. **Chat & Play** - 聊天遊戲
93. **Turn-Based Duel** - 雙人對決
94. **Cooperative Quest** - 合作任務
95. **Auction Game** - 拍賣遊戲
96. **Trading Game** - 交易遊戲
97. **Team Quiz** - 團隊問答
98. **Relay Race** - 接力賽

### Week 15: Unique & Creative (獨特創意)
99. **Time Machine** - 時間旅行遊戲
100. **Game of Life+** - 強化版生命遊戲

## Development Schedule 開發時程

### Day 1 (2025-12-05) ✅
- [x] 專案架構建立
- [x] 主選單系統
- [x] Game 001: Breakout (打磚塊)
- [x] README 文檔
- [x] Git 準備

### Day 2-100 (Coming Soon)
每天完成一個遊戲，按照上述列表順序進行。

## File Structure 檔案結構
```
100-cli-games/
├── main.py                          # 主程式入口
├── requirements.txt                 # Python 依賴
├── README.md                        # 專案說明
├── GAMES_PLAN.md                   # 本檔案：遊戲計畫
├── LICENSE                          # MIT 授權
├── .gitignore                       # Git 忽略檔案
├── games/                           # 遊戲目錄
│   ├── __init__.py
│   ├── game_001_breakout.py        # 第一個遊戲
│   ├── game_002_snake.py           # 第二個遊戲
│   └── ...                          # 其他遊戲
└── utils/                           # 工具模組
    ├── __init__.py
    ├── menu.py                      # 選單系統
    └── renderer.py                  # 渲染工具（未來）
```

## Coding Standards 編碼標準

### Game Module Template
每個遊戲檔案應遵循以下結構：

```python
"""
Game XXX: [Game Name]
[Brief description]
"""

class GameName:
    def __init__(self):
        # Initialize game state
        pass
    
    def run(self):
        # Main game loop
        pass

def main():
    """Entry point for the game"""
    # Setup and run the game
    game = GameName()
    game.run()

if __name__ == "__main__":
    main()
```

### Best Practices
1. 每個遊戲獨立可執行
2. 提供清晰的操作說明
3. 優雅的錯誤處理
4. 適當的遊戲難度
5. 有趣的遊戲體驗

## Future Enhancements 未來改進
- [ ] 遊戲存檔系統
- [ ] 排行榜功能
- [ ] 成就系統
- [ ] 多語言支援
- [ ] 音效支援（終端機 beep）
- [ ] 遊戲統計數據
- [ ] 社群分享功能

## Contributing 貢獻
歡迎提交 Pull Request 或提出建議！

## Progress Tracking 進度追蹤
- Completed: 6/10 ✅ (60%)
- In Progress: 0/10 🚧
- Planned: 4/10 ⏳ (40%)

**Total**: 10 精選遊戲（專注品質勝過數量）

---
**Last Updated**: 2025-12-07 (Restructured to 10 curated games)
