# ============================================================================
# Module: userland/apps/shell/patches/hooks.py
# 模块：userland/apps/shell/patches/hooks.py
# Description: Shell hook system for P2+
# 描述：P2+ Shell 钩子系统
# ============================================================================

"""
Hook system for Shell application.
Shell 应用的钩子系统。

Provides hooks that can be used to inject custom behavior
at specific points in the shell lifecycle.
提供在 Shell 生命周期特定点注入自定义行为的钩子。
"""

from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto


class HookPoint(Enum):
    """
    Hook points in shell lifecycle.
    Shell 生命周期中的钩子点。
    """
    # Before/after command execution / 命令执行前后
    PRE_EXECUTE = auto()
    POST_EXECUTE = auto()

    # Before/after command parsing / 命令解析前后
    PRE_PARSE = auto()
    POST_PARSE = auto()

    # Before/after prompt display / 提示符显示前后
    PRE_PROMPT = auto()
    POST_PROMPT = auto()

    # Before/after history add / 历史记录添加前后
    PRE_HISTORY = auto()
    POST_HISTORY = auto()

    # Before/after directory change / 目录切换前后
    PRE_CHDIR = auto()
    POST_CHDIR = auto()

    # When command not found / 命令未找到时
    COMMAND_NOT_FOUND = auto()

    # When shell starts/exits / Shell 启动/退出时
    SHELL_START = auto()
    SHELL_EXIT = auto()

    # For custom extensions / 自定义扩展
    CUSTOM = auto()


@dataclass
class HookContext:
    """
    Context passed to hook handlers.
    传递给钩子处理函数的上下文。

    Contains information about the current state and environment.
    包含当前状态和环境的信息。
    """
    shell: Any = None
    command: str = ""
    args: List[str] = field(default_factory=list)
    result: Any = None
    error: Optional[Exception] = None
    custom_data: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        """Get custom data / 获取自定义数据"""
        return self.custom_data.get(key, default)

    def set(self, key: str, value: Any):
        """Set custom data / 设置自定义数据"""
        self.custom_data[key] = value


class ShellHooks:
    """
    Hook manager for Shell application.
    Shell 应用的钩子管理器。

    Manages registration and execution of hook handlers.
    管理钩子处理函数的注册和执行。
    """

    def __init__(self):
        """Initialize hook manager / 初始化钩子管理器"""
        self._hooks: Dict[HookPoint, List[Callable]] = {}
        self._enabled: Dict[HookPoint, bool] = {}
        self._priority: Dict[HookPoint, int] = {}

        # Enable all hooks by default / 默认启用所有钩子
        for hp in HookPoint:
            self._hooks[hp] = []
            self._enabled[hp] = True
            self._priority[hp] = 0

    def register(self, point: HookPoint, handler: Callable, priority: int = 0):
        """
        Register a hook handler.
        注册一个钩子处理函数。

        Args:
            参数：
            point (HookPoint): Hook point / 钩子点
            handler (callable): Handler function / 处理函数
            priority (int): Priority (higher = executed first) / 优先级
        """
        if point not in self._hooks:
            self._hooks[point] = []
        self._hooks[point].append((priority, handler))
        # Sort by priority descending / 按优先级降序排序
        self._hooks[point].sort(key=lambda x: x[0], reverse=True)

    def unregister(self, point: HookPoint, handler: Callable):
        """
        Unregister a hook handler.
        取消注册钩子处理函数。

        Args:
            参数：
            point (HookPoint): Hook point / 钩子点
            handler (callable): Handler to remove / 要移除的处理函数
        """
        if point in self._hooks:
            self._hooks[point] = [
                (p, h) for p, h in self._hooks[point] if h != handler
            ]

    def enable(self, point: HookPoint, enabled: bool = True):
        """
        Enable or disable a hook point.
        启用或禁用钩子点。

        Args:
            参数：
            point (HookPoint): Hook point / 钩子点
            enabled (bool): Enable flag / 启用标志
        """
        self._enabled[point] = enabled

    def is_enabled(self, point: HookPoint) -> bool:
        """Check if hook point is enabled / 检查钩子点是否启用"""
        return self._enabled.get(point, True)

    def execute(self, point: HookPoint, context: HookContext) -> HookContext:
        """
        Execute all handlers for a hook point.
        执行钩子点的所有处理函数。

        Args:
            参数：
            point (HookPoint): Hook point / 钩子点
            context (HookContext): Hook context / 钩子上下文

        Returns:
            返回：
            HookContext: Modified context / 修改后的上下文
        """
        if not self.is_enabled(point):
            return context

        if point not in self._hooks:
            return context

        for priority, handler in self._hooks[point]:
            try:
                result = handler(context)
                if result is not None and isinstance(result, HookContext):
                    context = result
            except Exception as e:
                # Log error but continue / 记录错误但继续
                print(f"[Hook Error] {point}: {e}")

        return context

    def clear(self, point: Optional[HookPoint] = None):
        """
        Clear registered hooks.
        清除已注册的钩子。

        Args:
            参数：
            point (HookPoint): Specific point or None for all / 特定点或全部
        """
        if point is None:
            for hp in self._hooks:
                self._hooks[hp] = []
        elif point in self._hooks:
            self._hooks[point] = []


# Global hook registry / 全局钩子注册表
_global_hooks: Optional[ShellHooks] = None


def get_global_hooks() -> ShellHooks:
    """Get global hook registry / 获取全局钩子注册表"""
    global _global_hooks
    if _global_hooks is None:
        _global_hooks = ShellHooks()
    return _global_hooks