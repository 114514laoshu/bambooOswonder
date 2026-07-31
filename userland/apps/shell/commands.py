# ============================================================================
# Module: userland/apps/shell/commands.py
# 模块：userland/apps/shell/commands.py
# Description: Command registry for Bamboo OS Shell
# 描述：Bamboo OS Shell 命令注册表
# ============================================================================

from typing import Dict, List, Callable, Optional, Any


class CommandRegistry:
    """
    Command registry for shell commands.
    Shell 命令注册表。

    Manages registration, lookup, and help for commands.
    管理命令的注册、查找和帮助。
    """

    def __init__(self):
        """Initialize command registry / 初始化命令注册表"""
        self._commands: Dict[str, Callable] = {}
        self._help: Dict[str, str] = {}
        self._aliases: Dict[str, str] = {}

    def register(self, name: str, handler: Callable, help_text: str = ""):
        """
        Register a command / 注册命令

        Args:
            参数：
            name (str): Command name / 命令名
            handler (callable): Command handler / 命令处理函数
            help_text (str): Help text / 帮助文本
        """
        self._commands[name] = handler
        self._help[name] = help_text

    def register_alias(self, alias: str, target: str):
        """
        Register a command alias / 注册命令别名

        Args:
            参数：
            alias (str): Alias name / 别名
            target (str): Target command / 目标命令
        """
        self._aliases[alias] = target

    def has(self, name: str) -> bool:
        """
        Check if command exists / 检查命令是否存在

        Args:
            参数：
            name (str): Command name / 命令名

        Returns:
            返回：
            bool: True if exists / 存在返回 True
        """
        return name in self._commands or name in self._aliases

    def get(self, name: str) -> Optional[Callable]:
        """
        Get command handler / 获取命令处理函数

        Args:
            参数：
            name (str): Command name / 命令名

        Returns:
            返回：
            callable: Command handler or None / 命令处理函数或 None
        """
        if name in self._commands:
            return self._commands[name]
        if name in self._aliases:
            alias = self._aliases[name]
            return self._commands.get(alias)
        return None

    def get_info(self, name: str) -> Dict[str, Any]:
        """
        Get command information / 获取命令信息

        Args:
            参数：
            name (str): Command name / 命令名

        Returns:
            返回：
            dict: Command info / 命令信息
        """
        info = {
            'name': name,
            'help': self._help.get(name, "No help available"),
            'is_alias': name in self._aliases,
        }
        if name in self._aliases:
            info['target'] = self._aliases[name]
        return info

    def list(self) -> List[str]:
        """
        List all command names / 列出所有命令名

        Returns:
            返回：
            list: List of command names / 命令名列表
        """
        return list(self._commands.keys()) + list(self._aliases.keys())

    def list_commands(self) -> List[str]:
        """
        List only real commands (not aliases) / 仅列出真实命令（非别名）

        Returns:
            返回：
            list: List of command names / 命令名列表
        """
        return list(self._commands.keys())

    def list_aliases(self) -> List[str]:
        """
        List only aliases / 仅列出别名

        Returns:
            返回：
            list: List of alias names / 别名列表
        """
        return list(self._aliases.keys())

    def remove(self, name: str):
        """
        Remove a command / 移除命令

        Args:
            参数：
            name (str): Command name / 命令名
        """
        if name in self._commands:
            del self._commands[name]
        if name in self._help:
            del self._help[name]
        if name in self._aliases:
            del self._aliases[name]