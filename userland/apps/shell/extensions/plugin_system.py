# ============================================================================
# Module: userland/apps/shell/extensions/plugin_system.py
# 模块：userland/apps/shell/extensions/plugin_system.py
# Description: Plugin system for Shell
# 描述：Shell 插件系统
# ============================================================================

"""
Plugin system for Shell application.
Shell 应用的插件系统。

Allows dynamic loading of command plugins.
允许动态加载命令插件。
"""

import os
import sys
import importlib
import inspect
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field


@dataclass
class Plugin:
    """
    Plugin definition.
    插件定义。
    """
    name: str
    version: str = "1.0.0"
    author: str = "Unknown"
    description: str = ""
    commands: Dict[str, Callable] = field(default_factory=dict)
    hooks: Dict[str, Callable] = field(default_factory=dict)
    enabled: bool = True


class PluginManager:
    """
    Plugin manager for Shell.
    Shell 插件管理器。

    Manages loading, enabling, and disabling of plugins.
    管理插件的加载、启用和禁用。
    """

    def __init__(self, shell_instance):
        """
        Initialize plugin manager.
        初始化插件管理器。

        Args:
            参数：
            shell_instance: ShellApp instance / ShellApp 实例
        """
        self.shell = shell_instance
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_paths: List[str] = [
            '/apps/plugins',
            '/usr/lib/bamboo/plugins',
            './plugins',
        ]

    def add_plugin_path(self, path: str):
        """Add plugin search path / 添加插件搜索路径"""
        self.plugin_paths.append(path)

    def discover_plugins(self) -> List[str]:
        """
        Discover available plugins.
        发现可用插件。

        Returns:
            返回：
            list: List of plugin names / 插件名列表
        """
        discovered = []
        for path in self.plugin_paths:
            if os.path.exists(path) and os.path.isdir(path):
                for item in os.listdir(path):
                    if item.endswith('.py') and not item.startswith('_'):
                        name = item[:-3]
                        if name not in discovered:
                            discovered.append(name)
        return discovered

    def load_plugin(self, name: str) -> Optional[Plugin]:
        """
        Load a plugin by name.
        按名称加载插件。

        Args:
            参数：
            name (str): Plugin name / 插件名

        Returns:
            返回：
            Plugin: Loaded plugin or None / 加载的插件或 None
        """
        if name in self.plugins:
            return self.plugins[name]

        # Find plugin file / 查找插件文件
        plugin_path = None
        for path in self.plugin_paths:
            test_path = os.path.join(path, name + '.py')
            if os.path.exists(test_path):
                plugin_path = test_path
                break

        if not plugin_path:
            print(f"Plugin not found: {name}")
            return None

        try:
            # Load module / 加载模块
            spec = importlib.util.spec_from_file_location(name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Create plugin object / 创建插件对象
            plugin = Plugin(name=name)

            # Look for plugin class / 查找插件类
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (inspect.isclass(attr) and
                    hasattr(attr, 'get_plugin_info') and
                    attr.__module__ == name):
                    plugin_instance = attr()
                    info = plugin_instance.get_plugin_info()
                    plugin.version = info.get('version', '1.0.0')
                    plugin.author = info.get('author', 'Unknown')
                    plugin.description = info.get('description', '')

                    # Register commands / 注册命令
                    if hasattr(plugin_instance, 'get_commands'):
                        plugin.commands = plugin_instance.get_commands()
                        for cmd_name, handler in plugin.commands.items():
                            self.shell.commands.register(cmd_name, handler)

                    # Register hooks / 注册钩子
                    if hasattr(plugin_instance, 'get_hooks'):
                        plugin.hooks = plugin_instance.get_hooks()

                    break

            self.plugins[name] = plugin
            print(f"Loaded plugin: {name} v{plugin.version}")
            return plugin

        except Exception as e:
            print(f"Failed to load plugin {name}: {e}")
            return None

    def enable_plugin(self, name: str) -> bool:
        """
        Enable a plugin.
        启用插件。

        Args:
            参数：
            name (str): Plugin name / 插件名

        Returns:
            返回：
            bool: True if enabled / 启用返回 True
        """
        if name not in self.plugins:
            plugin = self.load_plugin(name)
            if not plugin:
                return False

        self.plugins[name].enabled = True
        return True

    def disable_plugin(self, name: str) -> bool:
        """
        Disable a plugin.
        禁用插件。

        Args:
            参数：
            name (str): Plugin name / 插件名

        Returns:
            返回：
            bool: True if disabled / 禁用返回 True
        """
        if name in self.plugins:
            self.plugins[name].enabled = False
            # Remove commands / 移除命令
            for cmd_name in self.plugins[name].commands:
                # Don't remove builtins / 不移除内置命令
                pass
            return True
        return False

    def list_plugins(self) -> List[Dict[str, str]]:
        """
        List all loaded plugins.
        列出所有已加载插件。

        Returns:
            返回：
            list: Plugin info list / 插件信息列表
        """
        return [
            {
                'name': p.name,
                'version': p.version,
                'author': p.author,
                'description': p.description,
                'enabled': p.enabled,
                'commands': len(p.commands),
            }
            for p in self.plugins.values()
        ]

    def find_command(self, cmd: str) -> Optional[Callable]:
        """
        Find command in plugins.
        在插件中查找命令。

        Args:
            参数：
            cmd (str): Command name / 命令名

        Returns:
            返回：
            callable: Command handler or None / 命令处理函数或 None
        """
        for plugin in self.plugins.values():
            if plugin.enabled and cmd in plugin.commands:
                return plugin.commands[cmd]
        return None