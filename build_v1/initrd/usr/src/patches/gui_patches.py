# ============================================================================
# Module: userland/patches/gui_patches.py
# 模块：userland/patches/gui_patches.py
# Description: GUI patches for P3+
# 描述：P3+ GUI 补丁
# ============================================================================

"""
GUI patches for P3+.
P3+ GUI 补丁。

Extends GUI library with additional widgets and effects.
使用额外的控件和效果扩展 GUI 库。
"""

from typing import List, Optional, Tuple, Dict, Any


class ProgressBar:
    """
    Progress bar widget.
    进度条控件。
    """

    def __init__(self, x: int = 0, y: int = 0, width: int = 200, height: int = 20,
                 min_value: float = 0, max_value: float = 100):
        """
        Initialize progress bar.
        初始化进度条。

        Args:
            参数：
            x (int): X position / X 位置
            y (int): Y position / Y 位置
            width (int): Width / 宽度
            height (int): Height / 高度
            min_value (float): Minimum value / 最小值
            max_value (float): Maximum value / 最大值
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        self.bg_color = 0x333333
        self.fg_color = 0x44CC44
        self.border_color = 0x666666
        self.show_text = True
        self.text_color = 0xFFFFFF

    def set_value(self, value: float):
        """Set progress value / 设置进度值"""
        self.value = max(self.min_value, min(self.max_value, value))

    def get_percentage(self) -> float:
        """Get percentage / 获取百分比"""
        if self.max_value == self.min_value:
            return 0.0
        return (self.value - self.min_value) / (self.max_value - self.min_value) * 100

    def render(self, renderer):
        """Render progress bar / 渲染进度条"""
        # Background / 背景
        renderer.fill_rect(self.x, self.y, self.width, self.height, self.bg_color)

        # Progress / 进度
        progress_width = int(self.width * self.get_percentage() / 100)
        if progress_width > 0:
            renderer.fill_rect(self.x + 2, self.y + 2,
                              progress_width - 4, self.height - 4,
                              self.fg_color)

        # Border / 边框
        renderer.draw_rect(self.x, self.y, self.width, self.height, self.border_color)

        # Text / 文本
        if self.show_text:
            text = f"{int(self.get_percentage())}%"
            text_x = self.x + (self.width - len(text) * 8) // 2
            text_y = self.y + (self.height - 14) // 2
            renderer.draw_text(text_x, text_y, text, self.text_color)


class Slider:
    """
    Slider widget.
    滑块控件。
    """

    def __init__(self, x: int = 0, y: int = 0, width: int = 200,
                 min_value: float = 0, max_value: float = 100,
                 value: float = 50, orientation: str = 'horizontal'):
        """
        Initialize slider.
        初始化滑块。

        Args:
            参数：
            x (int): X position / X 位置
            y (int): Y position / Y 位置
            width (int): Width / 宽度
            min_value (float): Minimum value / 最小值
            max_value (float): Maximum value / 最大值
            value (float): Current value / 当前值
            orientation (str): Orientation / 方向
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = 20 if orientation == 'horizontal' else 200
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.orientation = orientation
        self.bg_color = 0x333333
        self.fg_color = 0x4488CC
        self.handle_color = 0x66AAEE
        self.handle_radius = 8
        self.on_change = None
        self._dragging = False

    def get_position(self) -> float:
        """Get handle position / 获取滑块位置"""
        if self.orientation == 'horizontal':
            return (self.value - self.min_value) / (self.max_value - self.min_value) * (self.width - 20) + 10
        else:
            return (self.value - self.min_value) / (self.max_value - self.min_value) * (self.height - 20) + 10

    def set_value_from_position(self, pos: float):
        """Set value from handle position / 从滑块位置设置值"""
        if self.orientation == 'horizontal':
            pos = max(10, min(self.width - 10, pos))
            ratio = (pos - 10) / (self.width - 20)
            self.value = self.min_value + ratio * (self.max_value - self.min_value)
        else:
            pos = max(10, min(self.height - 10, pos))
            ratio = (pos - 10) / (self.height - 20)
            self.value = self.min_value + ratio * (self.max_value - self.min_value)

        if self.on_change:
            self.on_change(self.value)

    def render(self, renderer):
        """Render slider / 渲染滑块"""
        # Track / 轨道
        if self.orientation == 'horizontal':
            track_y = self.y + self.height // 2 - 2
            renderer.fill_rect(self.x + 10, track_y, self.width - 20, 4, self.bg_color)
            # Filled portion / 已填充部分
            handle_pos = self.get_position()
            renderer.fill_rect(self.x + 10, track_y, handle_pos - 10, 4, self.fg_color)
            # Handle / 滑块
            renderer.draw_circle(int(self.x + handle_pos), int(track_y + 2), self.handle_radius, self.handle_color, True)
        else:
            track_x = self.x + self.width // 2 - 2
            renderer.fill_rect(track_x, self.y + 10, 4, self.height - 20, self.bg_color)
            handle_pos = self.get_position()
            renderer.fill_rect(track_x, self.y + 10, 4, handle_pos - 10, self.fg_color)
            renderer.draw_circle(int(track_x + 2), int(self.y + handle_pos), self.handle_radius, self.handle_color, True)


class Toggle:
    """
    Toggle switch widget.
    开关控件。
    """

    def __init__(self, x: int = 0, y: int = 0, width: int = 60, height: int = 30,
                 checked: bool = False):
        """
        Initialize toggle switch.
        初始化开关。

        Args:
            参数：
            x (int): X position / X 位置
            y (int): Y position / Y 位置
            width (int): Width / 宽度
            height (int): Height / 高度
            checked (bool): Initial state / 初始状态
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.checked = checked
        self.off_color = 0x666666
        self.on_color = 0x44CC44
        self.handle_color = 0xFFFFFF
        self.on_change = None

    def toggle(self):
        """Toggle state / 切换状态"""
        self.checked = not self.checked
        if self.on_change:
            self.on_change(self.checked)

    def render(self, renderer):
        """Render toggle switch / 渲染开关"""
        # Background / 背景
        color = self.on_color if self.checked else self.off_color
        radius = self.height // 2

        # Rounded rect / 圆角矩形
        renderer.fill_rect(self.x + radius, self.y, self.width - radius * 2, self.height, color)
        renderer.draw_circle(self.x + radius, self.y + radius, radius, color, True)
        renderer.draw_circle(self.x + self.width - radius, self.y + radius, radius, color, True)

        # Handle / 滑块
        handle_x = self.x + self.width - self.height if self.checked else self.x
        renderer.draw_circle(handle_x + self.height // 2,
                            self.y + self.height // 2,
                            self.height // 2 - 4,
                            self.handle_color, True)