# ============================================================================
# Module: userland/app_store/app_store.py
# 模块：userland/app_store/app_store.py
# Description: Bamboo OS App Store
# 描述：Bamboo OS 应用市场
# ============================================================================

"""
App Store for Bamboo OS.
Bamboo OS 应用市场。

Provides application discovery, installation, and updates.
提供应用发现、安装和更新。
"""

import os
import json
import hashlib
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import time


@dataclass
class AppInfo:
    """Application information / 应用信息"""
    name: str
    version: str
    description: str
    author: str
    category: str
    size: int
    download_url: str
    checksum: str
    icon: Optional[str] = None
    screenshots: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    requires: Dict[str, str] = field(default_factory=dict)
    rating: float = 0.0
    downloads: int = 0
    release_date: int = 0
    source_url: Optional[str] = None
    license: str = "Proprietary"


@dataclass
class AppInstallation:
    """Installed application / 已安装应用"""
    app_info: AppInfo
    install_path: str
    install_time: int
    size_on_disk: int
    update_available: bool = False
    enabled: bool = True


class AppStore:
    """
    Bamboo OS App Store.
    Bamboo OS 应用市场。
    """

    def __init__(self, repo_url: str = "https://apps.bamboo-os.org/repo",
                 cache_dir: str = "/var/cache/bamboo/apps"):
        """
        Initialize app store.
        初始化应用市场。

        Args:
            参数：
            repo_url (str): Repository URL / 仓库 URL
            cache_dir (str): Cache directory / 缓存目录
        """
        self.repo_url = repo_url
        self.cache_dir = cache_dir
        self.apps: Dict[str, AppInfo] = {}
        self.installed: Dict[str, AppInstallation] = {}
        self._initialized = False

        self._init_cache()

    def _init_cache(self):
        """Initialize cache directory / 初始化缓存目录"""
        os.makedirs(self.cache_dir, exist_ok=True)

    def refresh(self) -> bool:
        """
        Refresh app catalog from repository.
        从仓库刷新应用目录。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        # In real implementation, fetch from repo / 实际实现中从仓库获取
        # For now, use built-in catalog / 现在，使用内置目录
        self._load_builtin_catalog()
        self._initialized = True
        return True

    def _load_builtin_catalog(self):
        """Load built-in application catalog / 加载内置应用目录"""
        builtin_apps = [
            AppInfo(
                name="Text Editor",
                version="1.0.0",
                description="Simple text editor with syntax highlighting",
                author="Bamboo OS Team",
                category="Development",
                size=102400,
                download_url="https://apps.bamboo-os.org/editor.bpp",
                checksum="abc123",
                license="GPLv3"
            ),
            AppInfo(
                name="Terminal",
                version="1.0.0",
                description="Terminal emulator with ANSI support",
                author="Bamboo OS Team",
                category="System",
                size=204800,
                download_url="https://apps.bamboo-os.org/terminal.bpp",
                checksum="def456",
                license="MIT"
            ),
            AppInfo(
                name="Snake Game",
                version="1.0.0",
                description="Classic snake game",
                author="Bamboo OS Team",
                category="Games",
                size=51200,
                download_url="https://apps.bamboo-os.org/snake.bpp",
                checksum="ghi789",
                license="MIT"
            ),
            AppInfo(
                name="Word Processor",
                version="1.0.0",
                description="Full-featured word processor",
                author="Bamboo OS Team",
                category="Office",
                size=512000,
                download_url="https://apps.bamboo-os.org/word.bpp",
                checksum="jkl012",
                license="GPLv3"
            ),
            AppInfo(
                name="Web Browser",
                version="1.0.0",
                description="Lightweight web browser",
                author="Bamboo OS Team",
                category="Internet",
                size=204800,
                download_url="https://apps.bamboo-os.org/browser.bpp",
                checksum="mno345",
                license="MIT"
            ),
            AppInfo(
                name="Calculator",
                version="1.0.0",
                description="Scientific calculator",
                author="Bamboo OS Team",
                category="Utilities",
                size=40960,
                download_url="https://apps.bamboo-os.org/calc.bpp",
                checksum="pqr678",
                license="MIT"
            ),
            AppInfo(
                name="3D Viewer",
                version="1.0.0",
                description="3D model viewer with hardware acceleration",
                author="Bamboo OS Team",
                category="Graphics",
                size=307200,
                download_url="https://apps.bamboo-os.org/3dview.bpp",
                checksum="stu901",
                requires={"opengl": "1.0"},
                license="MIT"
            ),
            AppInfo(
                name="System Monitor",
                version="1.0.0",
                description="System performance monitoring",
                author="Bamboo OS Team",
                category="System",
                size=81920,
                download_url="https://apps.bamboo-os.org/sysmon.bpp",
                checksum="vwx234",
                license="GPLv3"
            ),
        ]

        for app in builtin_apps:
            self.apps[app.name] = app

    def search(self, query: str, category: str = None) -> List[AppInfo]:
        """
        Search for applications.
        搜索应用。

        Args:
            参数：
            query (str): Search query / 搜索查询
            category (str): Category filter / 分类过滤

        Returns:
            返回：
            list: Matching applications / 匹配的应用列表
        """
        results = []
        query_lower = query.lower()

        for name, app in self.apps.items():
            if category and app.category != category:
                continue

            if (query_lower in name.lower() or
                query_lower in app.description.lower() or
                query_lower in app.author.lower()):
                results.append(app)

        return results

    def get_app(self, name: str) -> Optional[AppInfo]:
        """Get application by name / 按名称获取应用"""
        return self.apps.get(name)

    def get_categories(self) -> List[str]:
        """Get all categories / 获取所有分类"""
        categories = set()
        for app in self.apps.values():
            categories.add(app.category)
        return sorted(categories)

    def install(self, app_name: str) -> bool:
        """
        Install an application.
        安装应用。

        Args:
            参数：
            app_name (str): Application name / 应用名称

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        if app_name not in self.apps:
            print(f"App not found: {app_name}")
            return False

        if app_name in self.installed:
            print(f"App already installed: {app_name}")
            return False

        app = self.apps[app_name]

        # Check dependencies / 检查依赖
        if app.dependencies:
            for dep in app.dependencies:
                if dep not in self.apps:
                    print(f"Missing dependency: {dep}")
                    return False
                if dep not in self.installed:
                    print(f"Dependency not installed: {dep}")
                    return False

        # Download app / 下载应用
        install_path = os.path.join(self.cache_dir, f"{app_name}.bpp")
        # In real implementation, download from URL / 实际实现中从 URL 下载
        # For now, create empty file / 现在，创建空文件
        with open(install_path, 'w') as f:
            f.write(f"# {app_name} v{app.version}\n")
            f.write(f"# Description: {app.description}\n")

        # Verify checksum / 验证校验和
        # In real implementation, verify checksum / 实际实现中验证校验和

        # Install to system / 安装到系统
        install = AppInstallation(
            app_info=app,
            install_path=install_path,
            install_time=int(time.time()),
            size_on_disk=app.size,
            enabled=True
        )
        self.installed[app_name] = install

        print(f"Installed: {app_name} v{app.version}")
        return True

    def uninstall(self, app_name: str) -> bool:
        """
        Uninstall an application.
        卸载应用。

        Args:
            参数：
            app_name (str): Application name / 应用名称

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        if app_name not in self.installed:
            print(f"App not installed: {app_name}")
            return False

        install = self.installed[app_name]

        # Remove files / 移除文件
        if os.path.exists(install.install_path):
            os.remove(install.install_path)

        del self.installed[app_name]
        print(f"Uninstalled: {app_name}")
        return True

    def update(self, app_name: str = None) -> bool:
        """
        Update applications.
        更新应用。

        Args:
            参数：
            app_name (str): Specific app or None for all / 特定应用或全部

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        if app_name:
            return self._update_single(app_name)

        success = True
        for name in list(self.installed.keys()):
            if not self._update_single(name):
                success = False
        return success

    def _update_single(self, app_name: str) -> bool:
        """
        Update a single application.
        更新单个应用。

        Args:
            参数：
            app_name (str): Application name / 应用名称

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        if app_name not in self.apps:
            return False

        if app_name not in self.installed:
            return False

        current = self.installed[app_name]
        latest = self.apps[app_name]

        if current.app_info.version == latest.version:
            return True

        # Uninstall old version / 卸载旧版本
        old_path = current.install_path
        if os.path.exists(old_path):
            os.remove(old_path)

        # Install new version / 安装新版本
        return self.install(app_name)

    def list_installed(self) -> List[AppInstallation]:
        """List installed applications / 列出已安装应用"""
        return list(self.installed.values())

    def get_app_stats(self) -> Dict[str, Any]:
        """Get app store statistics / 获取应用市场统计"""
        return {
            'total_apps': len(self.apps),
            'installed_apps': len(self.installed),
            'categories': len(self.get_categories()),
            'total_downloads': sum(a.downloads for a in self.apps.values()),
            'cache_size': self._get_cache_size(),
        }

    def _get_cache_size(self) -> int:
        """Get cache directory size / 获取缓存目录大小"""
        total = 0
        for root, dirs, files in os.walk(self.cache_dir):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except Exception:
                    pass
        return total


def main():
    """Main entry point / 主入口"""
    store = AppStore()
    store.refresh()

    print("=== Bamboo OS App Store ===")
    print(f"Total apps: {len(store.apps)}")
    print(f"Categories: {store.get_categories()}")
    print()

    print("Searching for 'editor':")
    results = store.search("editor")
    for app in results:
        print(f"  {app.name} v{app.version} - {app.description[:50]}...")

    print()
    print("Installing Text Editor...")
    store.install("Text Editor")

    print()
    print("Installed apps:")
    for app in store.list_installed():
        print(f"  {app.app_info.name} v{app.app_info.version}")


if __name__ == '__main__':
    main()