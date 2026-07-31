# ============================================================================
# Module: userland/apps/shell/patches/shell_patches.py
# 模块：userland/apps/shell/patches/shell_patches.py
# Description: Shell patches for P2+
# 描述：P2+ Shell 补丁
# ============================================================================

"""
Patches for Shell application.
Shell 应用的补丁。

These patches extend the base ShellApp class with additional functionality.
这些补丁扩展了基础 ShellApp 类的额外功能。
"""

import os
import sys
from typing import List, Dict, Optional, Any

from userland.apps.shell.patches.hooks import (
    ShellHooks, HookPoint, HookContext, get_global_hooks
)


class ShellPatcher:
    """
    Shell application patcher.
    Shell 应用修补器。

    Applies patches to ShellApp at runtime.
    在运行时对 ShellApp 应用补丁。
    """

    def __init__(self, shell_instance):
        """
        Initialize patcher.
        初始化修补器。

        Args:
            参数：
            shell_instance: ShellApp instance / ShellApp 实例
        """
        self.shell = shell_instance
        self.hooks = get_global_hooks()
        self._patched_methods: Dict[str, Any] = {}
        self._patch_applied = False

    def apply(self) -> bool:
        """
        Apply all patches to shell instance.
        对 Shell 实例应用所有补丁。

        Returns:
            返回：
            bool: True if patches applied / 补丁已应用返回 True
        """
        if self._patch_applied:
            return True

        # Apply method patches / 应用方法补丁
        self._patch_read_line()
        self._patch_execute_command()
        self._patch_prompt()

        # Register hooks / 注册钩子
        self._register_hooks()

        self._patch_applied = True
        return True

    def _patch_read_line(self):
        """Patch _read_line_interactive with hook support / 带钩子支持的补丁"""
        original = self.shell._read_line_interactive

        def patched_read_line():
            # Pre-prompt hook / 提示符前钩子
            context = HookContext(shell=self.shell)
            context = self.hooks.execute(HookPoint.PRE_PROMPT, context)

            # Call original / 调用原始方法
            line = original()

            # Post-prompt hook / 提示符后钩子
            context.command = line
            context = self.hooks.execute(HookPoint.POST_PROMPT, context)

            return context.command

        self.shell._read_line_interactive = patched_read_line
        self._patched_methods['_read_line_interactive'] = original

    def _patch_execute_command(self):
        """Patch _execute_line with hook support / 带钩子支持的补丁"""
        original = self.shell._execute_line

        def patched_execute_line(line: str):
            # Pre-execute hook / 执行前钩子
            context = HookContext(shell=self.shell, command=line)
            context = self.hooks.execute(HookPoint.PRE_EXECUTE, context)

            if context.command != line:
                line = context.command

            try:
                # Call original / 调用原始方法
                original(line)
                context.result = 0
            except Exception as e:
                context.error = e
                context.result = -1
                raise

            # Post-execute hook / 执行后钩子
            self.hooks.execute(HookPoint.POST_EXECUTE, context)

        self.shell._execute_line = patched_execute_line
        self._patched_methods['_execute_line'] = original

    def _patch_prompt(self):
        """Patch prompt building / 补丁提示符构建"""
        original = self.shell._print_welcome

        def patched_print_welcome():
            # Shell start hook / Shell 启动钩子
            context = HookContext(shell=self.shell)
            self.hooks.execute(HookPoint.SHELL_START, context)

            # Call original / 调用原始方法
            original()

        self.shell._print_welcome = patched_print_welcome
        self._patched_methods['_print_welcome'] = original

    def _register_hooks(self):
        """Register default hooks / 注册默认钩子"""
        # Hook for command history / 命令历史钩子
        def history_hook(context: HookContext) -> HookContext:
            if context.command and context.command.strip():
                self.shell._add_history(context.command)
            return context

        self.hooks.register(HookPoint.PRE_EXECUTE, history_hook, priority=100)

        # Hook for command not found / 命令未找到钩子
        def not_found_hook(context: HookContext) -> HookContext:
            if context.error and "Command not found" in str(context.error):
                # Try plugin system / 尝试插件系统
                if hasattr(self.shell, '_plugin_manager'):
                    plugin_cmd = self.shell._plugin_manager.find_command(context.command)
                    if plugin_cmd:
                        plugin_cmd(context.args)
                        context.result = 0
                        context.error = None
            return context

        self.hooks.register(HookPoint.COMMAND_NOT_FOUND, not_found_hook, priority=50)

    def revert(self):
        """Revert all patches / 恢复所有补丁"""
        for method_name, original in self._patched_methods.items():
            if hasattr(self.shell, method_name):
                setattr(self.shell, method_name, original)
        self._patch_applied = False