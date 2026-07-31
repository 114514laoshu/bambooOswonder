# ============================================================================
# Module: userland/libs/libgui/window.py
# 模块：userland/libs/libgui/window.py
# Description: Window management for GUI
# 描述：GUI 窗口管理
# ============================================================================

"""
Window management for Bamboo OS GUI.
Bamboo OS GUI 窗口管理。

Provides window creation, management, and event handling.
提供窗口创建、管理和事件处理。
"""

from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto


class WindowState(Enum):
    """Window state / 窗口状态"""
    NORMAL = auto()
    MINIMIZED = auto()
    MAXIMIZED = auto()
    FULLSCREEN = auto()


@dataclass
class Window:
    """
    Window class for GUI applications.
    GUI 应用的窗口类。
    """

    title: str = "Window"
    x: int = 0
    y: int = 0
    width: int = 640
    height: int = 480
    state: WindowState = WindowState.NORMAL
    visible: bool = True
    resizable: bool = True
    movable: bool = True
    closeable: bool = True
    z_order: int = 0
    parent: Optional['Window'] = None
    children: List['Window'] = field(default_factory=list)

    # Content / 内容
    bg_color: int = 0xFFFFFF
    fg_color: int = 0x000000

    # Widgets / 控件
    widgets: List[Any] = field(default_factory=list)

    # Event handlers / 事件处理函数
    on_close: Optional[Callable] = None
    on_resize: Optional[Callable] = None
    on_focus: Optional[Callable] = None

    def add_widget(self, widget):
        """Add widget to window / 向窗口添加控件"""
        self.widgets.append(widget)
        widget.window = self

    def remove_widget(self, widget):
        """Remove widget from window / 从窗口移除控件"""
        if widget in self.widgets:
            self.widgets.remove(widget)

    def add_child(self, child: 'Window'):
        """Add child window / 添加子窗口"""
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: 'Window'):
        """Remove child window / 移除子窗口"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def contains(self, x: int, y: int) -> bool:
        """Check if point is inside window / 检查点是否在窗口内"""
        return (self.x <= x < self.x + self.width and
                self.y <= y < self.y + self.height)

    def get_child_at(self, x: int, y: int) -> Optional['Window']:
        """Get child window at point / 获取点处的子窗口"""
        # Check children in reverse order (top first) / 逆序检查子窗口（顶层优先）
        for child in reversed(self.children):
            if child.contains(x, y):
                return child
        return None


class WindowManager:
    """
    Window manager for GUI.
    GUI 窗口管理器。

    Manages all windows, z-order, and event dispatching.
    管理所有窗口、Z 顺序和事件分发。
    """

    def __init__(self, screen_width=1024, screen_height=768):
        """
        Initialize window manager.
        初始化窗口管理器。

        Args:
            参数：
            screen_width (int): Screen width / 屏幕宽度
            screen_height (int): Screen height / 屏幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.windows: List[Window] = []
        self.active_window: Optional[Window] = None
        self.drag_window: Optional[Window] = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def create_window(self, **kwargs) -> Window:
        """
        Create a new window.
        创建一个新窗口。

        Args:
            参数：
            **kwargs: Window attributes / 窗口属性

        Returns:
            返回：
            Window: Created window / 创建的窗口
        """
        window = Window(**kwargs)
        self.add_window(window)
        return window

    def add_window(self, window: Window):
        """
        Add window to manager.
        向管理器添加窗口。

        Args:
            参数：
            window (Window): Window to add / 要添加的窗口
        """
        window.z_order = len(self.windows)
        self.windows.append(window)
        self.active_window = window

        # Call on_focus callback / 调用 on_focus 回调
        if window.on_focus:
            window.on_focus()

    def remove_window(self, window: Window):
        """
        Remove window from manager.
        从管理器移除窗口。

        Args:
            参数：
            window (Window): Window to remove / 要移除的窗口
        """
        if window in self.windows:
            self.windows.remove(window)
            if self.active_window == window:
                self.active_window = self.windows[-1] if self.windows else None

    def bring_to_front(self, window: Window):
        """
        Bring window to front.
        将窗口带到前面。

        Args:
            参数：
            window (Window): Window to bring front / 要带到前面的窗口
        """
        if window in self.windows:
            self.windows.remove(window)
            self.windows.append(window)
            window.z_order = len(self.windows) - 1
            self.active_window = window

    def get_window_at(self, x: int, y: int) -> Optional[Window]:
        """
        Get window at point (top-most).
        获取点处的窗口（最顶层）。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标

        Returns:
            返回：
            Window: Window at point or None / 点处的窗口或 None
        """
        for window in reversed(self.windows):
            if window.contains(x, y):
                return window
        return None

    def handle_mouse_down(self, x: int, y: int, button: int):
        """
        Handle mouse down event.
        处理鼠标按下事件。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标
            button (int): Button number / 按钮编号
        """
        window = self.get_window_at(x, y)

        if window:
            self.bring_to_front(window)

            # Check title bar for dragging / 检查标题栏是否可拖动
            if window.movable and y < window.y + 24:
                self.drag_window = window
                self.drag_offset_x = x - window.x
                self.drag_offset_y = y - window.y

    def handle_mouse_up(self, x: int, y: int, button: int):
        """
        Handle mouse up event.
        处理鼠标释放事件。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标
            button (int): Button number / 按钮编号
        """
        self.drag_window = None

    def handle_mouse_move(self, x: int, y: int):
        """
        Handle mouse move event.
        处理鼠标移动事件。

        Args:
            参数：
            x (int): X coordinate / X 坐标
            y (int): Y coordinate / Y 坐标
        """
        if self.drag_window:
            # Drag window / 拖拽窗口
            new_x = x - self.drag_offset_x
            new_y = y - self.drag_offset_y

            # Clamp to screen / 限制在屏幕内
            new_x = max(0, min(self.screen_width - self.drag_window.width, new_x))
            new_y = max(0, min(self.screen_height - self.drag_window.height, new_y))

            self.drag_window.x = new_x
            self.drag_window.y = new_y

    def handle_key(self, key: str):
        """
        Handle keyboard event.
        处理键盘事件。

        Args:
            参数：
            key (str): Key character / 按键字符
        """
        if self.active_window:
            # Forward to active window / 转发到活动窗口
            pass

    def update(self):
        """Update window manager / 更新窗口管理器"""
        # Resolve z-order conflicts / 解决 Z 顺序冲突
        for i, window in enumerate(self.windows):
            window.z_order = i