# Day 7: Asteroids (小行星射擊遊戲)

## 遊戲概述
經典的小行星射擊遊戲。玩家控制一艘太空船在星空中飛行，射擊小行星並避免碰撞。小行星會分裂成更小的碎片，越小的行星速度越快，難度隨時間增加。

## 遊戲機制

### 核心玩法
1. **太空船控制**
   - 旋轉：左右箭頭
   - 推進：上箭頭（向前加速）
   - 射擊：空白鍵
   - 緊急傳送：下箭頭（隨機傳送，有風險）

2. **物理系統**
   - 慣性移動：太空船保持速度和方向
   - 邊界環繞：從螢幕一側出去會從另一側進來
   - 旋轉角度：360度旋轉
   - 推進效果：增加朝向方向的速度

3. **小行星系統**
   - 大型小行星：移動慢，耐撞擊 3 次，分裂成 2-3 個中型
   - 中型小行星：移動中等，耐撞擊 2 次，分裂成 2-3 個小型
   - 小型小行星：移動快，一擊毀滅
   - 隨機初始速度和方向
   - 碰撞檢測

4. **子彈系統**
   - 有限射速（冷卻時間）
   - 子彈存活時間（飛行距離限制）
   - 多發子彈同時存在

5. **計分系統**
   - 大型小行星：100 分
   - 中型小行星：50 分
   - 小型小行星：25 分
   - 連擊獎勵：快速擊毀多個目標加倍
   - 生命值：3 條
   - 額外生命：每 10,000 分獲得 1 條

6. **關卡進展**
   - 清除所有小行星進入下一關
   - 每關小行星數量增加
   - 難度逐漸提升
   - 顯示關卡數

## 視覺設計

### 遊戲元素顯示
```
太空船：  △ (指向方向)
          推進時：△' (火焰尾巴)
大小行星： ●●
          ●●
中小行星： ●
小小行星： •
子彈：     ·
星空背景： . . · . (隨機星點)
```

### 畫面佈局
```
┌────────────────────────────────────────────────────────────┐
│  ASTEROIDS                    SCORE: 12500    LIVES: ███   │
│                                LEVEL: 3      HI-SCORE: 5000│
├────────────────────────────────────────────────────────────┤
│                                                            │
│         ●●    ·           ●                               │
│         ●●              △'        ●                       │
│                                                            │
│   ●                                    ●●                 │
│                                        ●●                 │
│              .    ·    .    ·    .                        │
│                                                            │
│    ·         ●                             •              │
│                                                            │
│                   .    ·    .    ·                        │
└────────────────────────────────────────────────────────────┘
│ ◀ ▶ Rotate  │  ▲ Thrust  │  SPACE Fire  │  ▼ Hyperspace │
│  ESC Pause  │  Q Quit                                     │
└────────────────────────────────────────────────────────────┘
```

### 特效
- 爆炸效果：小行星被擊中顯示 * ※ * 動畫
- 推進火焰：太空船加速時顯示 `'`
- 碰撞閃爍：太空船被撞時閃爍
- 關卡清除：ALL CLEAR! 文字閃爍

## 技術實作

### 類別設計

```python
class Vector2D:
    """2D 向量類別"""
    def __init__(self, x, y)
    def __add__(self, other)
    def __mul__(self, scalar)
    def magnitude(self)
    def normalize(self)
    def rotate(self, angle)

class GameObject:
    """遊戲物體基類"""
    def __init__(self, x, y, vx, vy)
    def update(self, dt)
    def wrap_position(self, width, height)  # 邊界環繞

class Ship(GameObject):
    """太空船"""
    def __init__(self, x, y)
    def rotate(self, direction)  # -1 左轉，1 右轉
    def thrust(self)
    def shoot(self)
    def hyperspace(self)  # 隨機傳送
    def get_vertices(self)  # 取得三角形頂點

class Asteroid(GameObject):
    """小行星"""
    def __init__(self, x, y, size)  # size: 'large', 'medium', 'small'
    def split(self)  # 分裂成小行星
    def get_vertices(self)  # 多邊形頂點

class Bullet(GameObject):
    """子彈"""
    def __init__(self, x, y, angle, speed)
    def is_expired(self)  # 檢查是否超時

class AsteroidsGame:
    """主遊戲類別"""
    def __init__(self)
    def init_level(self, level)
    def spawn_asteroids(self, count)
    def update(self, dt)
    def check_collisions(self)
    def render(self, screen)
    def run(self)
```

### 碰撞檢測
```python
def check_collision(obj1, obj2):
    """圓形碰撞檢測"""
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y
    distance = sqrt(dx*dx + dy*dy)
    return distance < (obj1.radius + obj2.radius)
```

### 物理更新
```python
def update_physics(self, dt):
    """更新物理狀態"""
    # 更新位置
    self.x += self.vx * dt
    self.y += self.vy * dt
    
    # 應用阻力（輕微減速）
    self.vx *= 0.99
    self.vy *= 0.99
    
    # 邊界環繞
    self.wrap_position()
```

## 遊戲流程

### 開始遊戲
1. 顯示標題畫面
2. 等待玩家按任意鍵開始
3. 初始化第一關（3 個大型小行星）

### 遊戲循環
1. 處理玩家輸入
2. 更新所有遊戲物體
3. 檢查碰撞
4. 更新分數和狀態
5. 渲染畫面
6. 檢查遊戲結束條件

### 關卡完成
1. 檢測所有小行星被清除
2. 顯示 "LEVEL CLEAR!" 訊息
3. 短暫停頓（2秒）
4. 增加關卡數
5. 生成更多小行星（+2 per level）
6. 繼續遊戲

### 遊戲結束
1. 玩家生命值歸零
2. 顯示 "GAME OVER"
3. 顯示最終分數
4. 更新最高分（如果突破）
5. 詢問是否重新開始

## 難度設計

### 關卡進程
- Level 1: 3 個大型小行星
- Level 2: 4 個大型小行星
- Level 3: 5 個大型小行星
- Level 4+: 每關 +1 個，最多 10 個

### 速度設定
```python
ASTEROID_SPEEDS = {
    'large': (20, 40),   # 像素/秒
    'medium': (30, 60),
    'small': (50, 100)
}

SHIP_ROTATION_SPEED = 180  # 度/秒
SHIP_THRUST = 150          # 加速度
SHIP_MAX_SPEED = 200       # 最大速度
BULLET_SPEED = 300         # 子彈速度
```

## 音效提示（可選）
- 推進引擎：蜂鳴聲（低頻持續）
- 射擊：嗶嗶聲（短促）
- 爆炸：雜訊（短促爆破）
- 傳送：掃描聲（上升音調）
- 額外生命：音樂（簡短旋律）

## 測試要點

### 功能測試
- [ ] 太空船旋轉流暢
- [ ] 推進加速正確
- [ ] 射擊命中判定準確
- [ ] 小行星分裂正確
- [ ] 邊界環繞運作正常
- [ ] 碰撞檢測準確
- [ ] 計分正確
- [ ] 關卡進展正常

### 邊界情況
- [ ] 快速旋轉不卡頓
- [ ] 多個子彈同時存在
- [ ] 大量小行星不延遲
- [ ] 邊界穿越無閃爍
- [ ] 碰撞瞬間正確處理

### 遊戲體驗
- [ ] 難度曲線合理
- [ ] 操作手感良好
- [ ] 視覺清晰易讀
- [ ] 遊戲平衡性佳
- [ ] 有挑戰性但不過難

## 進階功能（時間允許）
- [ ] UFO 敵人（隨機出現，會射擊）
- [ ] 能量護盾（限時無敵）
- [ ] 武器升級（雙倍射速、三連發）
- [ ] 粒子特效（更華麗的爆炸）
- [ ] 背景音樂（簡單旋律）
- [ ] 成就系統（無傷通關等）
- [ ] 分數排行榜

## 開發時程
- 規劃與設計：30 分鐘 ✅
- 核心物理系統：60 分鐘
- 遊戲物體實作：90 分鐘
- 碰撞與計分：45 分鐘
- 視覺與 UI：45 分鐘
- 測試與調整：45 分鐘
- 文檔整理：15 分鐘

**預計總時間**：5.5 小時

## 成功標準
✅ 遊戲可流暢運行
✅ 物理模擬真實感
✅ 操作反應靈敏
✅ 視覺效果清晰
✅ 難度曲線合理
✅ 無明顯 bug
✅ 符合經典 Asteroids 體驗

---
**創建日期**: 2025-12-07
**狀態**: 規劃中 📋
**優先級**: 高 ⭐⭐⭐
