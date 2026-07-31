# ============================================================================
# Module: userland/libs/libgui/widget.py
# 模块：userland/libs/libgui/widget.py
# Description: GUI widgets library
# 描述：GUI 控件库
# ============================================================================

"""
Widget library for Bamboo OS GUI.
Bamboo OS GUI 控件库。

Provides buttons, labels, text boxes, and other UI widgets.
提供按钮、标签、文本框和其他 UI 控件。
"""

from typing import List, Optional, Callable, Any
from dataclasses import dataclass, field


@dataclass
class Widget:
    """
    Base widget class.
    基础控件类。
    """

    x: int = 0
    y: int = 0
    width: int = 100
    height: int = 30
    visible: bool = True
    enabled: bool = True

    # Parent window / 父窗口
    window: Any = None

    # Event handlers / 事件处理函数
    on_click: Optional[Callable] = None
    on_hover: Optional[Callable] = None

    def render(self, renderer):
        """Render widget / 渲染控件"""
        pass

    def contains(self, x: int, y: int) -> bool:
        """Check if point is inside widget / 检查点是否在控件内"""
        return (self.x <= x < self.x + self.width and
                self.y <= y < self.y + self.height)


@dataclass
class Button(Widget):
    """
    Button widget.
    按钮控件。
    """

    text: str = "Button"
    bg_color: int = 0xDDDDDD
    fg_color: int = 0x000000
    hover_color: int = 0xCCCCCC
    press_color: int = 0xAAAAAA

    def render(self, renderer):
        """Render button / 渲染按钮"""
        if not self.visible:
            return

        color = self.bg_color
        if hasattr(self, '_hover') and self._hover:
            color = self.hover_color
        if hasattr(self, '_press') and self._press:
            color = self.press_color

        # Draw background / 绘制背景
        renderer.fill_rect(self.x, self.y, self.width, self.height, color)

        # Draw border / 绘制边框
        renderer.draw_rect(self.x, self.y, self.width, self.height, 0x888888)

        # Draw text / 绘制文本
        text_x = self.x + (self.width - len(self.text) * 8) // 2
        text_y = self.y + (self.height - 16) // 2
        renderer.draw_text(text_x, text_y, self.text, self.fg_color)


@dataclass
class Label(Widget):
    """
    Label widget.
    标签控件。
    """

    text: str = "Label"
    fg_color: int = 0x000000
    bg_color: Optional[int] = None
    font_size: int = 14

    def render(self, renderer):
        """Render label / 渲染标签"""
        if not self.visible:
            return

        if self.bg_color is not None:
            renderer.fill_rect(self.x, self.y, self.width, self.height, self.bg_color)

        renderer.draw_text(self.x, self.y, self.text, self.fg_color)


@dataclass
class TextBox(Widget):
    """
    Text box widget.
    文本框控件。
    """

    text: str = ""
    placeholder: str = ""
    fg_color: int = 0x000000
    bg_color: int = 0xFFFFFF
    border_color: int = 0x888888
    focus_color: int = 0x4488FF
    cursor_pos: int = 0
    max_length: int = 100

    def render(self, renderer):
        """Render text box / 渲染文本框"""
        if not self.visible:
            return

        # Draw background / 绘制背景
        renderer.fill_rect(self.x, self.y, self.width, self.height, self.bg_color)

        # Draw border / 绘制边框
        color = self.focus_color if hasattr(self, '_focus') and self._focus else self.border_color
        renderer.draw_rect(self.x, self.y, self.width, self.height, color)

        # Draw text / 绘制文本
        display_text = self.text if self.text else self.placeholder
        if not self.text and self.placeholder:
            renderer.draw_text(self.x + 4, self.y + 4, self.placeholder, 0x888888)
        else:
            renderer.draw_text(self.x + 4, self.y + 4, self.text, self.fg_color)

        # Draw cursor / 绘制光标
        if hasattr(self, '_focus') and self._focus:
            cursor_x = self.x + 4 + self.cursor_pos * 8
            renderer.fill_rect(cursor_x, self.y + 4, 1, self.height - 8, self.fg_color)


@dataclass
class ListBox(Widget):
    """
    List box widget.
    列表框控件。
    """

    items: List[str] = field(default_factory=list)
    selected_index: int = -1
    fg_color: int = 0x000000
    bg_color: int = 0xFFFFFF
    selected_color: int = 0x4488FF
    selected_fg_color: int = 0xFFFFFF
    hover_color: int = 0xEEEEEE

    def render(self, renderer):
        """Render list box / 渲染列表框"""
        if not self.visible:
            return

        # Draw background / 绘制背景
        renderer.fill_rect(self.x, self.y, self.width, self.height, self.bg_color)

        # Draw border / 绘制边框
        renderer.draw_rect(self.x, self.y, self.width, self.height, 0x888888)

        # Draw items / 绘制项目
        item_height = 20
        for i, item in enumerate(self.items):
            if i * item_height >= self.height:
                break

            y = self.y + 2 + i * item_height

            # Highlight selected / 高亮选中的项目
            if i == self.selected_index:
                renderer.fill_rect(self.x + 2, y, self.width - 4, item_height - 2,
                                   self.selected_color)
                renderer.draw_text(self.x + 6, y + 2, item, self.selected_fg_color)
            else:
                renderer.draw_text(self.x + 6, y + 2, item, self.fg_color)


@dataclass
class Menu(Widget):
    """
    Menu widget.
    菜单控件。
    """

    items: List[str] = field(default_factory=list)
    selected_index: int = -1
    expanded: bool = False
    fg_color: int = 0x000000
    bg_color: int = 0xFFFFFF
    hover_color: int = 0x4488FF
    hover_fg_color: int = 0xFFFFFF

    def render(self, renderer):
        """Render menu / 渲染菜单"""
        if not self.visible:
            return

        # Draw background / 绘制背景
        renderer.fill_rect(self.x, self.y, self.width, self.height, self.bg_color)

        # Draw border / 绘制边框
        renderer.draw_rect(self.x, self.y, self.width, self.height, 0x888888)

        # Draw items / 绘制项目
        if self.expanded:
            item_height = 24
            for i, item in enumerate(self.items):
                y = self.y + 2 + i * item_height

                if i == self.selected_index:
                    renderer.fill_rect(self.x + 2, y, self.width - 4, item_height - 2,
                                       self.hover_color)
                    renderer.draw_text(self.x + 6, y + 4, item, self.hover_fg_color)
                else:
                    renderer.draw_text(self.x + 6, y + 4, item, self.fg_color)