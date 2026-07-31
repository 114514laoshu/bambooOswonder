# ============================================================================
# Module: userland/libs/libgame2d/sprite.py
# 模块：userland/libs/libgame2d/sprite.py
# Description: Sprite system for 2D games
# 描述：2D 游戏精灵系统
# ============================================================================

"""
Sprite system for 2D games.
2D 游戏精灵系统。

Provides sprite creation, manipulation, and rendering.
提供精灵的创建、操作和渲染。
"""

from typing import Optional, List, Tuple, Any


class Sprite:
    """
    2D game sprite.
    2D 游戏精灵。
    """

    def __init__(self, x: float = 0, y: float = 0, width: int = 32, height: int = 32,
                 image_data: Optional[bytes] = None):
        """
        Initialize sprite.
        初始化精灵。

        Args:
            参数：
            x (float): X position / X 位置
            y (float): Y position / Y 位置
            width (int): Sprite width / 精灵宽度
            height (int): Sprite height / 精灵高度
            image_data (bytes): Sprite image / 精灵图像
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_data = image_data
        self.visible = True
        self.rotation = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.origin_x = width // 2
        self.origin_y = height // 2
        self.opacity = 1.0
        self.color = (255, 255, 255)
        self.z_index = 0

        # Physics / 物理
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0

    def move(self, dx: float, dy: float):
        """Move sprite / 移动精灵"""
        self.x += dx
        self.y += dy

    def set_position(self, x: float, y: float):
        """Set sprite position / 设置精灵位置"""
        self.x = x
        self.y = y

    def set_scale(self, scale_x: float, scale_y: Optional[float] = None):
        """Set sprite scale / 设置精灵缩放"""
        self.scale_x = scale_x
        self.scale_y = scale_y if scale_y is not None else scale_x

    def set_rotation(self, angle: float):
        """Set sprite rotation (degrees) / 设置精灵旋转（角度）"""
        self.rotation = angle

    def get_rect(self) -> Tuple[float, float, float, float]:
        """
        Get bounding rectangle.
        获取边界矩形。

        Returns:
            返回：
            tuple: (x, y, width, height) / (x, y, 宽度, 高度)
        """
        return (self.x - self.width // 2, self.y - self.height // 2,
                self.width, self.height)

    def collides_with(self, other: 'Sprite') -> bool:
        """
        Check collision with another sprite.
        检查与另一个精灵的碰撞。

        Args:
            参数：
            other (Sprite): Other sprite / 另一个精灵

        Returns:
            返回：
            bool: True if colliding / 碰撞返回 True
        """
        x1, y1, w1, h1 = self.get_rect()
        x2, y2, w2, h2 = other.get_rect()

        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)

    def render(self, renderer):
        """Render sprite / 渲染精灵"""
        if not self.visible:
            return

        # In real implementation, draw sprite image / 实际实现中绘制精灵图像
        renderer.fill_rect(int(self.x - self.width // 2),
                          int(self.y - self.height // 2),
                          self.width, self.height, 0xFF4488)


class SpriteSheet:
    """
    Sprite sheet for animations.
    用于动画的精灵表。
    """

    def __init__(self, image_data: bytes, sprite_width: int, sprite_height: int,
                 columns: int, rows: int):
        """
        Initialize sprite sheet.
        初始化精灵表。

        Args:
            参数：
            image_data (bytes): Sprite sheet image / 精灵表图像
            sprite_width (int): Sprite width / 精灵宽度
            sprite_height (int): Sprite height / 精灵高度
            columns (int): Number of columns / 列数
            rows (int): Number of rows / 行数
        """
        self.image_data = image_data
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.columns = columns
        self.rows = rows
        self.total_sprites = columns * rows

    def get_sprite(self, index: int) -> Sprite:
        """
        Get sprite at index.
        获取索引处的精灵。

        Args:
            参数：
            index (int): Sprite index / 精灵索引

        Returns:
            返回：
            Sprite: Sprite instance / 精灵实例
        """
        if index >= self.total_sprites:
            index = 0

        col = index % self.columns
        row = index // self.columns

        # Extract sprite from sheet / 从表中提取精灵
        # In real implementation, extract image data / 实际实现中提取图像数据
        sprite = Sprite(0, 0, self.sprite_width, self.sprite_height)
        return sprite