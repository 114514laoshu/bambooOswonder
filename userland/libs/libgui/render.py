# ============================================================================
# Module: userland/libs/libgui/render.py
# 模块：userland/libs/libgui/render.py
# Description: GUI rendering engine
# 描述：GUI 渲染引擎
# ============================================================================

"""
Rendering engine for Bamboo OS GUI.
Bamboo OS GUI 渲染引擎。

Provides 2D rendering primitives for GUI applications.
为 GUI 应用提供 2D 渲染基元。
"""

from typing import Optional, Tuple, List


class Renderer:
    """
    GUI rendering engine.
    GUI 渲染引擎。

    Provides methods for drawing primitives and text.
    提供绘制基元和文本的方法。
    """

    def __init__(self, fb_base: int, width: int, height: int, bpp: int = 32):
        """
        Initialize renderer.
        初始化渲染器。

        Args:
            参数：
            fb_base (int): Framebuffer base address / 帧缓冲基址
            width (int): Screen width / 屏幕宽度
            height (int): Screen height / 屏幕高度
            bpp (int): Bits per pixel / 每像素位数
        """
        self.fb_base = fb_base
        self.width = width
        self.height = height
        self.bpp = bpp
        self.pitch = width * (bpp // 8)
        self.fb = memoryview(bytearray(self.pitch * height))

    def put_pixel(self, x: int, y: int, color: int):
        """
        Draw a pixel.
        绘制一个像素。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标
            color (int): Color value / 颜色值
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        offset = y * self.pitch + x * 4
        self.fb[offset:offset + 4] = color.to_bytes(4, 'little')

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int):
        """
        Draw a line using Bresenham's algorithm.
        使用 Bresenham 算法绘制直线。

        Args:
            参数：
            x1 (int): Start X / 起始 X
            y1 (int): Start Y / 起始 Y
            x2 (int): End X / 结束 X
            y2 (int): End Y / 结束 Y
            color (int): Color value / 颜色值
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.put_pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def fill_rect(self, x: int, y: int, width: int, height: int, color: int):
        """
        Fill a rectangle.
        填充矩形。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标
            width (int): Rectangle width / 矩形宽度
            height (int): Rectangle height / 矩形高度
            color (int): Color value / 颜色值
        """
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(self.width, x + width)
        y2 = min(self.height, y + height)

        for row in range(y1, y2):
            offset = row * self.pitch + x1 * 4
            for col in range(x1, x2):
                self.fb[offset:offset + 4] = color.to_bytes(4, 'little')
                offset += 4

    def draw_rect(self, x: int, y: int, width: int, height: int, color: int,
                  fill: bool = False):
        """
        Draw a rectangle.
        绘制矩形。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标
            width (int): Rectangle width / 矩形宽度
            height (int): Rectangle height / 矩形高度
            color (int): Color value / 颜色值
            fill (bool): Fill rectangle / 填充矩形
        """
        if fill:
            self.fill_rect(x, y, width, height, color)
            return

        # Top edge / 上边
        self.draw_line(x, y, x + width - 1, y, color)
        # Bottom edge / 下边
        self.draw_line(x, y + height - 1, x + width - 1, y + height - 1, color)
        # Left edge / 左边
        self.draw_line(x, y, x, y + height - 1, color)
        # Right edge / 右边
        self.draw_line(x + width - 1, y, x + width - 1, y + height - 1, color)

    def draw_circle(self, cx: int, cy: int, radius: int, color: int,
                    fill: bool = False):
        """
        Draw a circle using midpoint algorithm.
        使用中点算法绘制圆。

        Args:
            参数：
            cx (int): Center X / 圆心 X
            cy (int): Center Y / 圆心 Y
            radius (int): Radius / 半径
            color (int): Color value / 颜色值
            fill (bool): Fill circle / 填充圆形
        """
        x = 0
        y = radius
        d = 3 - 2 * radius

        while x <= y:
            if fill:
                self.draw_line(cx - x, cy + y, cx + x, cy + y, color)
                self.draw_line(cx - y, cy + x, cx + y, cy + x, color)
                self.draw_line(cx - y, cy - x, cx + y, cy - x, color)
                self.draw_line(cx - x, cy - y, cx + x, cy - y, color)
            else:
                self.put_pixel(cx + x, cy + y, color)
                self.put_pixel(cx - x, cy + y, color)
                self.put_pixel(cx + x, cy - y, color)
                self.put_pixel(cx - x, cy - y, color)
                self.put_pixel(cx + y, cy + x, color)
                self.put_pixel(cx - y, cy + x, color)
                self.put_pixel(cx + y, cy - x, color)
                self.put_pixel(cx - y, cy - x, color)

            if d < 0:
                d = d + 4 * x + 6
            else:
                d = d + 4 * (x - y) + 10
                y -= 1
            x += 1

    def draw_text(self, x: int, y: int, text: str, color: int,
                  font_data: Optional[bytes] = None):
        """
        Draw text using bitmap font.
        使用位图字体绘制文本。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标
            text (str): Text to draw / 要绘制的文本
            color (int): Color value / 颜色值
            font_data (bytes): Font bitmap data / 字体位图数据
        """
        # Simple 8x16 font / 简单 8x16 字体
        for i, ch in enumerate(text):
            char_x = x + i * 8
            self.draw_char(char_x, y, ord(ch), color, font_data)

    def draw_char(self, x: int, y: int, char: int, color: int,
                  font_data: Optional[bytes] = None):
        """
        Draw a character using bitmap font.
        使用位图字体绘制一个字符。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标
            char (int): Character code / 字符代码
            color (int): Color value / 颜色值
            font_data (bytes): Font bitmap data / 字体位图数据
        """
        if font_data is None:
            # Use default font / 使用默认字体
            return

        char_offset = char * 16
        for row in range(16):
            if y + row >= self.height:
                break
            row_data = font_data[char_offset + row] if char_offset + row < len(font_data) else 0

            for col in range(8):
                if x + col >= self.width:
                    break
                if row_data & (0x80 >> col):
                    self.put_pixel(x + col, y + row, color)

    def clear(self, color: int = 0x000000):
        """
        Clear screen with color.
        用颜色清屏。

        Args:
            参数：
            color (int): Color value / 颜色值
        """
        self.fill_rect(0, 0, self.width, self.height, color)

    def get_framebuffer(self) -> memoryview:
        """
        Get framebuffer memory view.
        获取帧缓冲内存视图。

        Returns:
            返回：
            memoryview: Framebuffer / 帧缓冲
        """
        return self.fb