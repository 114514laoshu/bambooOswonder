# ============================================================================
# Module: userland/games/snake.py
# 模块：userland/games/snake.py
# Description: Snake game for Bamboo OS
# 描述：Bamboo OS 贪吃蛇游戏
# ============================================================================

"""
Snake game implementation.
贪吃蛇游戏实现。

Classic snake game with score tracking and increasing difficulty.
经典贪吃蛇游戏，带分数追踪和难度递增。
"""

import random
import time
from typing import List, Tuple, Optional


class SnakeGame:
    """
    Snake game.
    贪吃蛇游戏。
    """

    def __init__(self, width: int = 20, height: int = 20):
        """
        Initialize snake game.
        初始化贪吃蛇游戏。

        Args:
            参数：
            width (int): Game width / 游戏宽度
            height (int): Game height / 游戏高度
        """
        self.width = width
        self.height = height
        self.snake: List[Tuple[int, int]] = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food: Optional[Tuple[int, int]] = None
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        self.speed = 0.15  # Seconds per move / 每步秒数
        self.move_timer = 0.0

        self._init_game()

    def _init_game(self):
        """Initialize game state / 初始化游戏状态"""
        mid_x = self.width // 2
        mid_y = self.height // 2
        self.snake = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = 0.15
        self.move_timer = 0.0
        self._spawn_food()

    def _spawn_food(self):
        """Spawn food at random position / 在随机位置生成食物"""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def set_direction(self, dx: int, dy: int):
        """
        Set snake direction.
        设置蛇的方向。

        Args:
            参数：
            dx (int): X direction / X 方向
            dy (int): Y direction / Y 方向
        """
        # Prevent reversing / 防止反向
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)

    def update(self, dt: float) -> bool:
        """
        Update game state.
        更新游戏状态。

        Args:
            参数：
            dt (float): Delta time / 增量时间

        Returns:
            返回：
            bool: True if game is still running / 游戏仍在运行返回 True
        """
        if self.game_over or self.paused:
            return not self.game_over

        self.move_timer += dt
        if self.move_timer < self.speed:
            return True

        self.move_timer = 0.0
        self.direction = self.next_direction

        # Calculate new head position / 计算新的蛇头位置
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Check wall collision / 检查墙壁碰撞
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return False

        # Check self collision / 检查自身碰撞
        if new_head in self.snake:
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return False

        # Move snake / 移动蛇
        self.snake.insert(0, new_head)

        # Check food collision / 检查食物碰撞
        if new_head == self.food:
            self.score += 1
            self._spawn_food()
            # Increase speed / 增加速度
            self.speed = max(0.05, self.speed - 0.005)
        else:
            self.snake.pop()

        return True

    def render(self, renderer, cell_size: int = 20, offset_x: int = 0, offset_y: int = 0):
        """
        Render game.
        渲染游戏。

        Args:
            参数：
            renderer: Renderer instance / 渲染器实例
            cell_size (int): Cell size in pixels / 单元格像素大小
            offset_x (int): X offset / X 偏移
            offset_y (int): Y offset / Y 偏移
        """
        # Draw grid / 绘制网格
        for y in range(self.height):
            for x in range(self.width):
                px = offset_x + x * cell_size
                py = offset_y + y * cell_size
                color = 0x222222 if (x + y) % 2 == 0 else 0x1A1A1A
                renderer.fill_rect(px, py, cell_size, cell_size, color)

        # Draw food / 绘制食物
        if self.food:
            fx = offset_x + self.food[0] * cell_size
            fy = offset_y + self.food[1] * cell_size
            renderer.draw_circle(fx + cell_size // 2, fy + cell_size // 2,
                                cell_size // 2 - 2, 0xFF0000, True)

        # Draw snake / 绘制蛇
        for i, (sx, sy) in enumerate(self.snake):
            px = offset_x + sx * cell_size
            py = offset_y + sy * cell_size
            color = 0x44CC44 if i == 0 else 0x33AA33
            renderer.fill_rect(px + 1, py + 1, cell_size - 2, cell_size - 2, color)

            # Head eyes / 蛇头眼睛
            if i == 0:
                eye_size = cell_size // 6
                eye_offset = cell_size // 4
                # Direction-based eyes / 基于方向的眼睛
                dx, dy = self.direction
                if dx == 1:  # Right / 右
                    ex1, ey1 = px + cell_size - eye_offset - eye_size, py + eye_offset
                    ex2, ey2 = px + cell_size - eye_offset - eye_size, py + cell_size - eye_offset - eye_size
                elif dx == -1:  # Left / 左
                    ex1, ey1 = px + eye_offset, py + eye_offset
                    ex2, ey2 = px + eye_offset, py + cell_size - eye_offset - eye_size
                elif dy == 1:  # Down / 下
                    ex1, ey1 = px + eye_offset, py + cell_size - eye_offset - eye_size
                    ex2, ey2 = px + cell_size - eye_offset - eye_size, py + cell_size - eye_offset - eye_size
                else:  # Up / 上
                    ex1, ey1 = px + eye_offset, py + eye_offset
                    ex2, ey2 = px + cell_size - eye_offset - eye_size, py + eye_offset

                renderer.fill_rect(ex1, ey1, eye_size, eye_size, 0x000000)
                renderer.fill_rect(ex2, ey2, eye_size, eye_size, 0x000000)

    def get_score(self) -> int:
        """Get current score / 获取当前分数"""
        return self.score

    def get_high_score(self) -> int:
        """Get high score / 获取最高分"""
        return self.high_score

    def toggle_pause(self):
        """Toggle pause state / 切换暂停状态"""
        self.paused = not self.paused


def main():
    """Main entry point / 主入口"""
    game = SnakeGame()
    print("Snake Game started!")
    print("Use arrow keys to move, P to pause")
    print(f"Score: {game.get_score()} | High Score: {game.get_high_score()}")


if __name__ == '__main__':
    main()