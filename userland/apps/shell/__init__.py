# ============================================================================
# Module: userland/apps/shell/__init__.py
# 模块：userland/apps/shell/__init__.py
# Description: Bamboo OS Shell application package
# 描述：Bamboo OS Shell 应用包
# ============================================================================

from userland.apps.shell.shell import ShellApp
from userland.apps.shell.commands import CommandRegistry

__all__ = [
    'ShellApp',
    'CommandRegistry',
]

__version__ = "1.0.0"