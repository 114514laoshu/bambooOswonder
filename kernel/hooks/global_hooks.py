# ============================================================================
# Module: kernel/hooks/global_hooks.py
# 模块：kernel/hooks/global_hooks.py
# Description: Global hook system for Bamboo OS
# 描述：Bamboo OS 全局钩子系统
# ============================================================================

"""
Global hook system for Bamboo OS.
Bamboo OS 全局钩子系统。

Provides system-wide hooks for intercepting and extending
kernel and userland functionality.
提供系统级钩子，用于拦截和扩展内核及用户态功能。
"""

from typing import Dict, List, Callable, Any, Optional
from enum import Enum, auto
from dataclasses import dataclass, field
import time


class HookType(Enum):
    """Hook types / 钩子类型"""
    # System hooks / 系统钩子
    SYSTEM_BOOT = auto()
    SYSTEM_SHUTDOWN = auto()
    SYSTEM_PANIC = auto()
    SYSTEM_SUSPEND = auto()
    SYSTEM_RESUME = auto()

    # Process hooks / 进程钩子
    PROCESS_CREATE = auto()
    PROCESS_EXIT = auto()
    PROCESS_SCHEDULE = auto()
    PROCESS_SIGNAL = auto()

    # File system hooks / 文件系统钩子
    FS_OPEN = auto()
    FS_CLOSE = auto()
    FS_READ = auto()
    FS_WRITE = auto()
    FS_MOUNT = auto()
    FS_UMOUNT = auto()

    # Network hooks / 网络钩子
    NET_SOCKET = auto()
    NET_CONNECT = auto()
    NET_ACCEPT = auto()
    NET_SEND = auto()
    NET_RECV = auto()

    # Security hooks / 安全钩子
    SECURITY_CHECK = auto()
    SECURITY_AUTH = auto()
    SECURITY_AUDIT = auto()

    # Driver hooks / 驱动钩子
    DRIVER_LOAD = auto()
    DRIVER_UNLOAD = auto()
    DRIVER_IOCTL = auto()

    # User hooks / 用户钩子
    USER_LOGIN = auto()
    USER_LOGOUT = auto()
    USER_COMMAND = auto()


@dataclass
class HookContext:
    """
    Hook context passed to handlers.
    传递给处理函数的钩子上下文。
    """
    hook_type: HookType
    timestamp: float = field(default_factory=time.time)
    data: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    error: Optional[Exception] = None
    handled: bool = False
    cancelled: bool = False

    def get(self, key: str, default: Any = None) -> Any:
        """Get data value / 获取数据值"""
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        """Set data value / 设置数据值"""
        self.data[key] = value

    def cancel(self):
        """Cancel the operation / 取消操作"""
        self.cancelled = True

    def mark_handled(self):
        """Mark as handled / 标记为已处理"""
        self.handled = True


class HookHandler:
    """
    Hook handler with priority.
    带优先级的钩子处理函数。
    """

    def __init__(self, handler: Callable, priority: int = 0, name: str = ""):
        """
        Initialize hook handler.
        初始化钩子处理函数。

        Args:
            参数：
            handler (callable): Handler function / 处理函数
            priority (int): Priority (higher = first) / 优先级
            name (str): Handler name / 处理函数名称
        """
        self.handler = handler
        self.priority = priority
        self.name = name or handler.__name__

    def __call__(self, context: HookContext) -> HookContext:
        """Execute handler / 执行处理函数"""
        return self.handler(context)


class GlobalHookSystem:
    """
    Global hook system.
    全局钩子系统。

    Singleton pattern for system-wide hook management.
    系统级钩子管理的单例模式。
    """

    _instance = None

    def __new__(cls):
        """Singleton instance / 单例实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize hook system / 初始化钩子系统"""
        if self._initialized:
            return

        self._hooks: Dict[HookType, List[HookHandler]] = {}
        self._enabled: Dict[HookType, bool] = {}
        self._global_enabled = True
        self._hook_history: List[HookContext] = []
        self._max_history = 1000

        # Initialize all hook types / 初始化所有钩子类型
        for hook_type in HookType:
            self._hooks[hook_type] = []
            self._enabled[hook_type] = True

        self._initialized = True

    def register(self, hook_type: HookType, handler: Callable,
                 priority: int = 0, name: str = ""):
        """
        Register a hook handler.
        注册一个钩子处理函数。

        Args:
            参数：
            hook_type (HookType): Hook type / 钩子类型
            handler (callable): Handler function / 处理函数
            priority (int): Priority / 优先级
            name (str): Handler name / 处理函数名称
        """
        if hook_type not in self._hooks:
            self._hooks[hook_type] = []

        hook_handler = HookHandler(handler, priority, name)
        self._hooks[hook_type].append(hook_handler)

        # Sort by priority descending / 按优先级降序排序
        self._hooks[hook_type].sort(key=lambda h: h.priority, reverse=True)

    def unregister(self, hook_type: HookType, handler: Callable):
        """
        Unregister a hook handler.
        取消注册钩子处理函数。

        Args:
            参数：
            hook_type (HookType): Hook type / 钩子类型
            handler (callable): Handler to remove / 要移除的处理函数
        """
        if hook_type in self._hooks:
            self._hooks[hook_type] = [
                h for h in self._hooks[hook_type] if h.handler != handler
            ]

    def enable(self, hook_type: HookType, enabled: bool = True):
        """
        Enable or disable a hook type.
        启用或禁用钩子类型。

        Args:
            参数：
            hook_type (HookType): Hook type / 钩子类型
            enabled (bool): Enable flag / 启用标志
        """
        self._enabled[hook_type] = enabled

    def enable_global(self, enabled: bool = True):
        """Enable or disable all hooks / 启用或禁用所有钩子"""
        self._global_enabled = enabled

    def is_enabled(self, hook_type: HookType) -> bool:
        """Check if hook type is enabled / 检查钩子类型是否启用"""
        return self._global_enabled and self._enabled.get(hook_type, True)

    def execute(self, hook_type: HookType, **kwargs) -> HookContext:
        """
        Execute all handlers for a hook type.
        执行钩子类型的所有处理函数。

        Args:
            参数：
            hook_type (HookType): Hook type / 钩子类型
            **kwargs: Context data / 上下文数据

        Returns:
            返回：
            HookContext: Execution context / 执行上下文
        """
        context = HookContext(hook_type=hook_type, data=kwargs)

        if not self.is_enabled(hook_type):
            return context

        if hook_type not in self._hooks:
            return context

        for handler in self._hooks[hook_type]:
            try:
                result = handler(context)
                if isinstance(result, HookContext):
                    context = result
                if context.cancelled or context.handled:
                    break
            except Exception as e:
                context.error = e
                # Log error but continue / 记录错误但继续
                print(f"[Hook Error] {hook_type}: {e}")

        # Save history / 保存历史
        self._hook_history.append(context)
        if len(self._hook_history) > self._max_history:
            self._hook_history = self._hook_history[-self._max_history:]

        return context

    def get_history(self, hook_type: Optional[HookType] = None,
                    limit: int = 100) -> List[HookContext]:
        """
        Get hook execution history.
        获取钩子执行历史。

        Args:
            参数：
            hook_type (HookType): Filter by hook type / 按钩子类型过滤
            limit (int): Maximum entries / 最大条目数

        Returns:
            返回：
            list: Hook contexts / 钩子上下文列表
        """
        history = self._hook_history
        if hook_type:
            history = [h for h in history if h.hook_type == hook_type]
        return history[-limit:]

    def clear_history(self):
        """Clear hook history / 清除钩子历史"""
        self._hook_history.clear()

    def list_handlers(self, hook_type: Optional[HookType] = None) -> Dict[HookType, List[str]]:
        """
        List registered handlers.
        列出已注册的处理函数。

        Args:
            参数：
            hook_type (HookType): Filter by hook type / 按钩子类型过滤

        Returns:
            返回：
            dict: Handlers by hook type / 按钩子类型分类的处理函数
        """
        result = {}
        types = [hook_type] if hook_type else HookType

        for ht in types:
            if ht in self._hooks:
                result[ht] = [h.name for h in self._hooks[ht]]

        return result


# Global hook system instance / 全局钩子系统实例
_global_hooks: Optional[GlobalHookSystem] = None


def get_global_hooks() -> GlobalHookSystem:
    """Get global hook system / 获取全局钩子系统"""
    global _global_hooks
    if _global_hooks is None:
        _global_hooks = GlobalHookSystem()
    return _global_hooks


# Convenience functions / 便捷函数
def register_hook(hook_type: HookType, handler: Callable,
                  priority: int = 0, name: str = ""):
    """Register a hook / 注册一个钩子"""
    get_global_hooks().register(hook_type, handler, priority, name)


def execute_hook(hook_type: HookType, **kwargs) -> HookContext:
    """Execute a hook / 执行一个钩子"""
    return get_global_hooks().execute(hook_type, **kwargs)