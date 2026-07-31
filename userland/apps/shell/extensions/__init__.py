# ============================================================================
# Module: userland/apps/shell/extensions/__init__.py
# 模块：userland/apps/shell/extensions/__init__.py
# Description: Shell extensions package for P2+
# 描述：P2+ Shell 扩展包
# ============================================================================

from userland.apps.shell.extensions.plugin_system import PluginManager, Plugin
from userland.apps.shell.extensions.job_control import JobControl
from userland.apps.shell.extensions.completion import AdvancedCompleter

__all__ = [
    'PluginManager',
    'Plugin',
    'JobControl',
    'AdvancedCompleter',
]

__version__ = "1.1.0"