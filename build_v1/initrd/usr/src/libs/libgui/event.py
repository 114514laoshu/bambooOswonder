# ============================================================================
# Module: userland/libs/libgui/event.py
# 模块：userland/libs/libgui/event.py
# Description: GUI event system
# 描述：GUI 事件系统
# ============================================================================

"""
Event system for Bamboo OS GUI.
Bamboo OS GUI 事件系统。

Provides event types, event objects, and event handling.
提供事件类型、事件对象和事件处理。
"""

from enum import Enum, auto
from typing import Optional, Callable, Dict, List, Any
from dataclasses import dataclass, field
import time


class EventType(Enum):
    """
    Event types.
    事件类型。
    """

    # Mouse events / 鼠标事件
    MOUSE_DOWN = auto()
    MOUSE_UP = auto()
    MOUSE_MOVE = auto()
    MOUSE_ENTER = auto()
    MOUSE_LEAVE = auto()
    MOUSE_WHEEL = auto()

    # Keyboard events / 键盘事件
    KEY_DOWN = auto()
    KEY_UP = auto()

    # Window events / 窗口事件
    WINDOW_CREATE = auto()
    WINDOW_DESTROY = auto()
    WINDOW_MOVE = auto()
    WINDOW_RESIZE = auto()
    WINDOW_FOCUS = auto()
    WINDOW_BLUR = auto()
    WINDOW_CLOSE = auto()

    # Widget events / 控件事件
    WIDGET_CLICK = auto()
    WIDGET_CHANGE = auto()
    WIDGET_HOVER = auto()
    WIDGET_LEAVE = auto()

    # System events / 系统事件
    TIMER = auto()
    QUIT = auto()


@dataclass
class Event:
    """
    Event object.
    事件对象。
    """

    type: EventType
    time: float = field(default_factory=time.time)
    handled: bool = False

    # Mouse event fields / 鼠标事件字段
    x: int = 0
    y: int = 0
    button: int = 0
    dx: int = 0
    dy: int = 0
    wheel_delta: int = 0

    # Keyboard event fields / 键盘事件字段
    key: str = ""
    keycode: int = 0
    modifiers: int = 0

    # Window event fields / 窗口事件字段
    window: Any = None
    widget: Any = None

    # Custom data / 自定义数据
    data: Any = None

    def stop_propagation(self):
        """Stop event propagation / 停止事件传播"""
        self.handled = True


class EventHandler:
    """
    Event handler registry.
    事件处理函数注册表。
    """

    def __init__(self):
        """
        Initialize event handler.
        初始化事件处理函数。
        """
        self.handlers: Dict[EventType, List[Callable]] = {}
        self.global_handlers: List[Callable] = []

    def register(self, event_type: EventType, handler: Callable):
        """
        Register event handler.
        注册事件处理函数。

        Args:
            参数：
            event_type (EventType): Event type / 事件类型
            handler (callable): Handler function / 处理函数
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unregister(self, event_type: EventType, handler: Callable):
        """
        Unregister event handler.
        取消注册事件处理函数。

        Args:
            参数：
            event_type (EventType): Event type / 事件类型
            handler (callable): Handler to remove / 要移除的处理函数
        """
        if event_type in self.handlers:
            if handler in self.handlers[event_type]:
                self.handlers[event_type].remove(handler)

    def register_global(self, handler: Callable):
        """
        Register global event handler.
        注册全局事件处理函数。

        Args:
            参数：
            handler (callable): Handler function / 处理函数
        """
        self.global_handlers.append(handler)

    def dispatch(self, event: Event) -> bool:
        """
        Dispatch event to handlers.
        将事件分发到处理函数。

        Args:
            参数：
            event (Event): Event to dispatch / 要分发的事件

        Returns:
            返回：
            bool: True if event was handled / 事件已处理返回 True
        """
        # Global handlers first / 先调用全局处理函数
        for handler in self.global_handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Global event handler error: {e}")

        if event.handled:
            return True

        # Type-specific handlers / 类型特定处理函数
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Event handler error: {e}")
                if event.handled:
                    return True

        return False


class EventQueue:
    """
    Event queue for asynchronous event handling.
    异步事件处理的事件队列。
    """

    def __init__(self, max_size: int = 1024):
        """
        Initialize event queue.
        初始化事件队列。

        Args:
            参数：
            max_size (int): Maximum queue size / 最大队列大小
        """
        self.queue: List[Event] = []
        self.max_size = max_size

    def push(self, event: Event) -> bool:
        """
        Push event to queue.
        将事件推入队列。

        Args:
            参数：
            event (Event): Event to push / 要推入的事件

        Returns:
            返回：
            bool: True if pushed / 推入成功返回 True
        """
        if len(self.queue) >= self.max_size:
            return False

        self.queue.append(event)
        return True

    def pop(self) -> Optional[Event]:
        """
        Pop event from queue.
        从队列弹出事件。

        Returns:
            返回：
            Event: Next event or None / 下一个事件或 None
        """
        if not self.queue:
            return None

        return self.queue.pop(0)

    def peek(self) -> Optional[Event]:
        """
        Peek at next event without removing.
        查看下一个事件而不移除。

        Returns:
            返回：
            Event: Next event or None / 下一个事件或 None
        """
        if not self.queue:
            return None

        return self.queue[0]

    def clear(self):
        """Clear all events / 清空所有事件"""
        self.queue.clear()

    def size(self) -> int:
        """
        Get queue size / 获取队列大小

        Returns:
            返回：
            int: Number of events / 事件数量
        """
        return len(self.queue)

    def is_empty(self) -> bool:
        """
        Check if queue is empty / 检查队列是否为空

        Returns:
            返回：
            bool: True if empty / 为空返回 True
        """
        return len(self.queue) == 0