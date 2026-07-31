# ============================================================================
# Module: userland/p3plus_bootstrap.py
# 模块：userland/p3plus_bootstrap.py
# Description: P3+ bootstrap for applying patches at runtime
# 描述：P3+ 运行时补丁引导
# ============================================================================

"""
P3+ bootstrap module.
P3+ 引导模块。

Applies patches and loads extensions when the application starts.
在应用启动时应用补丁并加载扩展。
"""

import os
import sys
from typing import Optional, Any

from userland.p3plus_config import get_p3plus_config, is_feature_enabled


class P3PlusBootstrapper:
    """
    P3+ bootstrapper.
    P3+ 引导程序。

    Applies patches and initializes extensions for P3 applications.
    为 P3 应用应用补丁并初始化扩展。
    """

    def __init__(self, app_instance):
        """
        Initialize bootstrapper.
        初始化引导程序。

        Args:
            参数：
            app_instance: Application instance / 应用实例
        """
        self.app = app_instance
        self._patched = False
        self.config = get_p3plus_config()

    def bootstrap(self) -> bool:
        """Bootstrap P3+ features / 引导 P3+ 功能"""
        if not self.config.get('enabled', True):
            return True

        try:
            # Apply game engine patches / 应用游戏引擎补丁
            if is_feature_enabled('game_engine', 'enabled'):
                self._apply_game_engine_patches()

            # Apply GUI patches / 应用 GUI 补丁
            if is_feature_enabled('gui', 'enabled'):
                self._apply_gui_patches()

            # Apply network patches / 应用网络补丁
            if is_feature_enabled('network', 'enabled'):
                self._apply_network_patches()

            # Apply multimedia patches / 应用多媒体补丁
            if is_feature_enabled('multimedia', 'enabled'):
                self._apply_multimedia_patches()

            self._patched = True
            return True

        except Exception as e:
            print(f"P3+ bootstrap failed: {e}")
            return False

    def _apply_game_engine_patches(self):
        """Apply game engine patches / 应用游戏引擎补丁"""
        from userland.patches.game_engine_patches import GameEnginePatcher
        patcher = GameEnginePatcher(self.app)
        patcher.apply()

    def _apply_gui_patches(self):
        """Apply GUI patches / 应用 GUI 补丁"""
        from userland.patches.gui_patches import GUIPatcher
        patcher = GUIPatcher(self.app)
        patcher.apply()

    def _apply_network_patches(self):
        """Apply network patches / 应用网络补丁"""
        from userland.patches.network_patches import NetworkPatcher
        patcher = NetworkPatcher(self.app)
        patcher.apply()

    def _apply_multimedia_patches(self):
        """Apply multimedia patches / 应用多媒体补丁"""
        from userland.patches.multimedia_patches import MultimediaPatcher
        patcher = MultimediaPatcher(self.app)
        patcher.apply()


def bootstrap_p3(app_instance) -> bool:
    """Bootstrap an application with P3+ patches / 使用 P3+ 补丁引导应用"""
    bootstrapper = P3PlusBootstrapper(app_instance)
    return bootstrapper.bootstrap()