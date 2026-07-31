# ============================================================================
# Module: userland/apps/shell/patches/__init__.py
# 模块：userland/apps/shell/patches/__init__.py
# Description: Shell patches package for P2+
# 描述：P2+ Shell 补丁包
# ============================================================================

from userland.apps.shell.patches.hooks import ShellHooks
from userland.apps.shell.patches.shell_patches import ShellPatcher
from userland.apps.shell.patches.command_patches import CommandPatcher

__all__ = [
    'ShellHooks',
    'ShellPatcher',
    'CommandPatcher',
]

__version__ = "1.1.0"
__patch_level__ = 1