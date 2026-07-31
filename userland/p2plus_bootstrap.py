# ============================================================================
# Module: userland/p2plus_bootstrap.py
# 模块：userland/p2plus_bootstrap.py
# Description: P2+ bootstrap for applying patches at runtime
# 描述：P2+ 运行时补丁引导
# ============================================================================

"""
P2+ bootstrap module.
P2+ 引导模块。

Applies patches and loads extensions when the shell starts.
在 Shell 启动时应用补丁并加载扩展。
"""

import os
import sys
from typing import Optional, Any

from userland.p2plus_config import get_p2plus_config, is_feature_enabled


class P2PlusBootstrapper:
    """
    P2+ bootstrapper.
    P2+ 引导程序。

    Applies patches and initializes extensions for the shell.
    为 Shell 应用补丁并初始化扩展。
    """

    def __init__(self, shell_instance):
        """
        Initialize bootstrapper.
        初始化引导程序。

        Args:
            参数：
            shell_instance: ShellApp instance / ShellApp 实例
        """
        self.shell = shell_instance
        self._patched = False

        # Load configuration / 加载配置
        self.config = get_p2plus_config('shell')

    def bootstrap(self) -> bool:
        """
        Bootstrap P2+ features.
        引导 P2+ 功能。

        Returns:
            返回：
            bool: True if successful / 成功返回 True
        """
        if not self.config.get('enabled', True):
            return True

        try:
            # Apply patches / 应用补丁
            self._apply_patches()

            # Load extensions / 加载扩展
            self._load_extensions()

            # Initialize hooks / 初始化钩子
            self._init_hooks()

            self._patched = True
            return True

        except Exception as e:
            print(f"P2+ bootstrap failed: {e}")
            return False

    def _apply_patches(self):
        """Apply patches to shell / 对 Shell 应用补丁"""
        # Import patchers / 导入修补器
        from userland.apps.shell.patches.shell_patches import ShellPatcher
        from userland.apps.shell.patches.command_patches import CommandPatcher

        # Apply shell patches / 应用 Shell 补丁
        shell_patcher = ShellPatcher(self.shell)
        shell_patcher.apply()

        # Apply command patches / 应用命令补丁
        command_patcher = CommandPatcher(self.shell)
        command_patcher.apply()

        # Apply command patches / 应用命令补丁
        command_patcher = CommandPatcher(self.shell)
        command_patcher.apply()

    def _load_extensions(self):
        """Load shell extensions / 加载 Shell 扩展"""
        extensions = self.config.get('extensions', {})

        if extensions.get('plugin_system', True):
            from userland.apps.shell.extensions.plugin_system import PluginManager
            self.shell._plugin_manager = PluginManager(self.shell)

            # Auto-discover plugins / 自动发现插件
            if self.config.get('auto_discover_plugins', True):
                plugins = self.shell._plugin_manager.discover_plugins()
                for plugin in plugins:
                    self.shell._plugin_manager.load_plugin(plugin)

        if extensions.get('job_control', True):
            from userland.apps.shell.extensions.job_control import (
                JobControl, cmd_bg, cmd_fg, cmd_jobs
            )
            self.shell._job_control = JobControl(self.shell)

            # Register job control commands / 注册作业控制命令
            self.shell.commands.register('bg', lambda a: cmd_bg(a, self.shell._job_control))
            self.shell.commands.register('fg', lambda a: cmd_fg(a, self.shell._job_control))
            self.shell.commands.register('jobs', lambda a: cmd_jobs(a, self.shell._job_control))

        if extensions.get('advanced_completion', True):
            from userland.apps.shell.extensions.completion import AdvancedCompleter
            self.shell._completer = AdvancedCompleter(self.shell)

    def _init_hooks(self):
        """Initialize hook system / 初始化钩子系统"""
        from userland.apps.shell.patches.hooks import get_global_hooks
        hooks = get_global_hooks()

        # Enable/disable hooks based on config / 根据配置启用/禁用钩子
        hook_config = self.config.get('hooks', {})
        for point, enabled in hook_config.items():
            from userland.apps.shell.patches.hooks import HookPoint
            try:
                hp = getattr(HookPoint, point.upper())
                hooks.enable(hp, enabled)
            except AttributeError:
                pass


def bootstrap_shell(shell_instance) -> bool:
    """
    Bootstrap a shell instance with P2+ patches.
    使用 P2+ 补丁引导 Shell 实例。

    Args:
        参数：
        shell_instance: ShellApp instance / ShellApp 实例

    Returns:
        返回：
        bool: True if successful / 成功返回 True
    """
    bootstrapper = P2PlusBootstrapper(shell_instance)
    return bootstrapper.bootstrap()