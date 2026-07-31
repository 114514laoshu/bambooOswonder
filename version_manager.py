#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bamboo OS Wonder Version Manager
10版本迭代发布系统
"""
import os
import sys
import json
import shutil
import time
from pathlib import Path
from datetime import datetime

VERSION_DEFS = [
    {
        "version": "1.0.0",
        "codename": "Foundation",
        "name": "Bamboo OS Wonder v1.0 - 基础内核版",
        "description": "内核基础功能，启动到命令行Shell",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "gui": False,
            "network": False,
            "apps": False,
            "games": False,
            "office": False,
            "chinese": False,
        },
        "phase": "Alpha",
        "release_date": "2026-01-15",
    },
    {
        "version": "2.0.0",
        "codename": "Persistence",
        "name": "Bamboo OS Wonder v2.0 - 磁盘持久化版",
        "description": "添加磁盘驱动和文件系统持久化支持",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "disk_driver": True,
            "data_persistence": True,
            "gui": False,
            "network": False,
            "apps": False,
            "games": False,
            "office": False,
            "chinese": False,
        },
        "phase": "Alpha",
        "release_date": "2026-02-20",
    },
    {
        "version": "3.0.0",
        "codename": "Network",
        "name": "Bamboo OS Wonder v3.0 - 网络通信版",
        "description": "完整TCP/IP协议栈和网络应用",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "disk_driver": True,
            "data_persistence": True,
            "network_stack": True,
            "network_drivers": True,
            "tcp_ip": True,
            "http_client": True,
            "gui": False,
            "apps": False,
            "games": False,
            "office": False,
            "chinese": False,
        },
        "phase": "Alpha",
        "release_date": "2026-03-25",
    },
    {
        "version": "4.0.0",
        "codename": "Desktop",
        "name": "Bamboo OS Wonder v4.0 - 图形桌面版",
        "description": "GUI桌面环境和窗口系统",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "disk_driver": True,
            "data_persistence": True,
            "network_stack": True,
            "network_drivers": True,
            "tcp_ip": True,
            "http_client": True,
            "gui_core": True,
            "window_system": True,
            "desktop_env": True,
            "widgets": True,
            "apps": False,
            "games": False,
            "office": False,
            "chinese": False,
        },
        "phase": "Beta",
        "release_date": "2026-04-30",
    },
    {
        "version": "5.0.0",
        "codename": "Applications",
        "name": "Bamboo OS Wonder v5.0 - 应用生态版",
        "description": "内置应用程序和工具集",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "disk_driver": True,
            "data_persistence": True,
            "network_stack": True,
            "network_drivers": True,
            "tcp_ip": True,
            "http_client": True,
            "gui_core": True,
            "window_system": True,
            "desktop_env": True,
            "widgets": True,
            "apps_basic": True,
            "file_manager": True,
            "terminal": True,
            "text_editor": True,
            "settings": True,
            "games": False,
            "office": False,
            "chinese": False,
        },
        "phase": "Beta",
        "release_date": "2026-05-15",
    },
    {
        "version": "6.0.0",
        "codename": "Multimedia",
        "name": "Bamboo OS Wonder v6.0 - 多媒体娱乐版",
        "description": "2D游戏引擎和多媒体应用",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "disk_driver": True,
            "data_persistence": True,
            "network_stack": True,
            "network_drivers": True,
            "tcp_ip": True,
            "http_client": True,
            "gui_core": True,
            "window_system": True,
            "desktop_env": True,
            "widgets": True,
            "apps_basic": True,
            "file_manager": True,
            "terminal": True,
            "text_editor": True,
            "settings": True,
            "game_engine_2d": True,
            "games_2d": True,
            "audio": True,
            "image_viewer": True,
            "paint": True,
            "office": False,
            "chinese": False,
        },
        "phase": "Beta",
        "release_date": "2026-06-01",
    },
    {
        "version": "7.0.0",
        "codename": "Productivity",
        "name": "Bamboo OS Wonder v7.0 - 办公生产力版",
        "description": "完整办公套件和生产力工具",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "disk_driver": True,
            "data_persistence": True,
            "network_stack": True,
            "network_drivers": True,
            "tcp_ip": True,
            "http_client": True,
            "gui_core": True,
            "window_system": True,
            "desktop_env": True,
            "widgets": True,
            "apps_basic": True,
            "file_manager": True,
            "terminal": True,
            "text_editor": True,
            "settings": True,
            "game_engine_2d": True,
            "games_2d": True,
            "audio": True,
            "image_viewer": True,
            "paint": True,
            "office_suite": True,
            "word_processor": True,
            "spreadsheet": True,
            "presentation": True,
            "calculator": True,
            "calendar": True,
            "chinese": False,
        },
        "phase": "RC",
        "release_date": "2026-06-20",
    },
    {
        "version": "8.0.0",
        "codename": "Sinica",
        "name": "Bamboo OS Wonder v8.0 - 中文化版",
        "description": "完整中文支持和本地化",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "disk_driver": True,
            "data_persistence": True,
            "network_stack": True,
            "network_drivers": True,
            "tcp_ip": True,
            "http_client": True,
            "gui_core": True,
            "window_system": True,
            "desktop_env": True,
            "widgets": True,
            "apps_basic": True,
            "file_manager": True,
            "terminal": True,
            "text_editor": True,
            "settings": True,
            "game_engine_2d": True,
            "games_2d": True,
            "audio": True,
            "image_viewer": True,
            "paint": True,
            "office_suite": True,
            "word_processor": True,
            "spreadsheet": True,
            "presentation": True,
            "calculator": True,
            "calendar": True,
            "chinese_support": True,
            "chinese_fonts": True,
            "chinese_input": True,
            "chinese_ui": True,
        },
        "phase": "RC",
        "release_date": "2026-07-05",
    },
    {
        "version": "9.0.0",
        "codename": "Acceleration",
        "name": "Bamboo OS Wonder v9.0 - 硬件加速版",
        "description": "3D图形加速和性能优化",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "shell_basic": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "disk_driver": True,
            "data_persistence": True,
            "network_stack": True,
            "network_drivers": True,
            "tcp_ip": True,
            "http_client": True,
            "gui_core": True,
            "window_system": True,
            "desktop_env": True,
            "widgets": True,
            "apps_basic": True,
            "file_manager": True,
            "terminal": True,
            "text_editor": True,
            "settings": True,
            "game_engine_2d": True,
            "games_2d": True,
            "audio": True,
            "image_viewer": True,
            "paint": True,
            "office_suite": True,
            "word_processor": True,
            "spreadsheet": True,
            "presentation": True,
            "calculator": True,
            "calendar": True,
            "chinese_support": True,
            "chinese_fonts": True,
            "chinese_input": True,
            "chinese_ui": True,
            "graphics_3d": True,
            "hardware_accel": True,
            "performance_opt": True,
            "boot_optimization": True,
        },
        "phase": "RC",
        "release_date": "2026-07-20",
    },
    {
        "version": "10.0.0",
        "codename": "Wonder",
        "name": "Bamboo OS Wonder v10.0 - 终极完整版",
        "description": "完整操作系统，人人可用的最终发行版",
        "features": {
            "kernel_boot": True,
            "memory_basic": True,
            "memory_advanced": True,
            "shell_basic": True,
            "shell_advanced": True,
            "fs_fat32": True,
            "fs_ext4": True,
            "fs_all": True,
            "disk_driver": True,
            "nvme_driver": True,
            "data_persistence": True,
            "network_stack": True,
            "network_drivers": True,
            "tcp_ip": True,
            "http_client": True,
            "web_browser": True,
            "network_manager": True,
            "gui_core": True,
            "window_system": True,
            "desktop_env": True,
            "widgets": True,
            "themes": True,
            "apps_basic": True,
            "file_manager": True,
            "terminal": True,
            "text_editor": True,
            "settings": True,
            "system_monitor": True,
            "game_engine_2d": True,
            "games_2d": True,
            "game_engine_3d": True,
            "games_3d": True,
            "audio": True,
            "audio_mixer": True,
            "image_viewer": True,
            "paint": True,
            "video_player": True,
            "office_suite": True,
            "word_processor": True,
            "spreadsheet": True,
            "presentation": True,
            "pdf_viewer": True,
            "calculator": True,
            "calendar": True,
            "chinese_support": True,
            "chinese_fonts": True,
            "chinese_input": True,
            "chinese_ui": True,
            "graphics_3d": True,
            "hardware_accel": True,
            "performance_opt": True,
            "boot_optimization": True,
            "app_store": True,
            "package_manager": True,
            "system_update": True,
            "user_accounts": True,
            "security": True,
            "installer": True,
            "hardware_compat": True,
        },
        "phase": "Stable",
        "release_date": "2026-07-31",
    },
]


class VersionManager:
    """版本管理器"""

    def __init__(self, root_dir=None):
        self.root = Path(root_dir or Path(__file__).parent)
        self.releases_dir = self.root.parent / "releases"
        self.releases_dir.mkdir(parents=True, exist_ok=True)

    def get_version(self, version_str):
        """获取指定版本的定义"""
        for v in VERSION_DEFS:
            if v["version"] == version_str:
                return v
        return None

    def list_versions(self):
        """列出所有版本"""
        return VERSION_DEFS

    def build_version(self, version_str, output_dir=None):
        """构建指定版本"""
        version_def = self.get_version(version_str)
        if not version_def:
            print(f"Error: Version {version_str} not found")
            return False

        print(f"=" * 60)
        print(f" Building {version_def['name']}")
        print(f" Phase: {version_def['phase']}")
        print(f" Release Date: {version_def['release_date']}")
        print(f"=" * 60)

        # 创建版本目录
        version_dir = self.releases_dir / f"v{version_str}"
        version_dir.mkdir(parents=True, exist_ok=True)

        # 构建内核
        success = self._build_kernel(version_def, version_dir)
        if not success:
            print(f"Kernel build failed for v{version_str}")
            return False

        # 构建initrd
        self._build_initrd(version_def, version_dir)

        # 构建ISO
        self._build_iso(version_def, version_dir)

        # 生成版本说明
        self._generate_release_notes(version_def, version_dir)

        print(f"\nSUCCESS: Version {version_str} built successfully!")
        print(f"Output: {version_dir}")
        return True

    def _build_kernel(self, version_def, version_dir):
        """构建内核"""
        try:
            sys.path.insert(0, str(self.root))
            from kernel.kernel_generator import generate_kernel
            import importlib

            # 创建版本特定的配置
            config_mod = self._create_version_config(version_def)

            # 构建内核
            kernel_path = version_dir / "boot" / f"bamboo-os-{version_def['version']}.elf"
            kernel_path.parent.mkdir(parents=True, exist_ok=True)

            size = generate_kernel(config_mod, kernel_path)
            print(f"Kernel built: {kernel_path} ({size:,} bytes)")
            return True
        except Exception as e:
            print(f"Kernel build error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _create_version_config(self, version_def):
        """创建版本特定的配置模块"""
        import types

        config = types.ModuleType(f"config_v{version_def['version']}")
        config.VERSION = version_def["version"]
        config.RELEASE = version_def["release_date"]
        config.TARGET_NAME = version_def["name"]

        config.KERNEL_CONFIG = {
            "name": version_def["name"],
            "arch": "x86_64",
            "multiboot": 2,
            "direct_boot": version_def["version"] >= "2.0.0",
            "kernel_base": 0x100000,
            "stack_size": 0x10000,
            "heap_size": 0x4000000,
            "max_processes": 128,
            "max_files": 256,
            "ticks_per_second": 100,
        }

        config.MEMORY_CONFIG = {
            "total_mb": 512,
            "kernel_mb": 64,
            "user_mb": 448,
            "swap_mb": 128 if version_def["version"] >= "3.0.0" else 0,
        }

        config.FS_CONFIG = {
            "root_fs": "fat32",
            "supported_fs": ["fat32"],
            "fat32_sectors_per_cluster": 8,
            "enable_lfn": True,
            "disk_image": "disk.img",
            "disk_size_mb": 256,
        }

        if version_def["features"].get("fs_ext4"):
            config.FS_CONFIG["supported_fs"].extend(["ext2", "ext3", "ext4"])

        config.NET_CONFIG = {
            "enabled": version_def["features"].get("network_stack", False),
            "driver": "rtl8139",
            "ip": "10.0.2.15",
            "netmask": "255.255.255.0",
            "gateway": "10.0.2.2",
            "dns": ["8.8.8.8", "1.1.1.1"],
            "enable_dhcp": version_def["features"].get("network_stack", False),
        }

        config.GUI_CONFIG = {
            "enabled": version_def["features"].get("gui_core", False),
            "width": 1024,
            "height": 768,
            "bpp": 32,
            "theme": "bamboo",
            "font": "terminus",
            "desktop_icons": version_def["features"].get("desktop_env", False),
            "taskbar": version_def["features"].get("desktop_env", False),
            "start_menu": version_def["features"].get("desktop_env", False),
            "animation": version_def["features"].get("desktop_env", False),
            "transparency": version_def["version"] >= "9.0.0",
        }

        config.APPS_CONFIG = {
            "include": [],
            "games_2d": [],
            "games_3d": [],
            "preinstall": False,
        }

        if version_def["features"].get("apps_basic"):
            config.APPS_CONFIG["include"].extend([
                "Shell", "Terminal", "FileManager", "Settings",
            ])

        if version_def["features"].get("office_suite"):
            config.APPS_CONFIG["include"].extend([
                "WordProcessor", "Spreadsheet", "Presentation",
                "Calculator", "Calendar",
            ])

        if version_def["features"].get("games_2d"):
            config.APPS_CONFIG["games_2d"].extend([
                "Snake", "Tetris", "Minesweeper",
            ])

        return config

    def _build_initrd(self, version_def, version_dir):
        """构建初始内存磁盘"""
        initrd_dir = version_dir / "initrd"
        initrd_dir.mkdir(parents=True, exist_ok=True)

        # 创建目录结构
        dirs = [
            'bin', 'sbin', 'etc', 'dev', 'proc', 'sys',
            'tmp', 'home', 'root', 'var', 'usr', 'lib',
            'apps', 'libs', 'include', 'opt', 'mnt', 'media'
        ]
        for d in dirs:
            (initrd_dir / d).mkdir(parents=True, exist_ok=True)

        # 创建欢迎文件
        welcome = initrd_dir / 'etc' / 'welcome.txt'
        with open(welcome, 'w') as f:
            f.write(f"""====================================================
  {version_def['name']}
  Codename: {version_def['codename']}
  Phase: {version_def['phase']}
  Release: {version_def['release_date']}

  {version_def['description']}
====================================================
""")

        # 创建版本信息文件
        version_file = initrd_dir / 'etc' / 'version'
        with open(version_file, 'w') as f:
            f.write(f"VERSION={version_def['version']}\n")
            f.write(f"CODENAME={version_def['codename']}\n")
            f.write(f"PHASE={version_def['phase']}\n")
            f.write(f"RELEASE_DATE={version_def['release_date']}\n")
            f.write(f"BUILD_TIME={datetime.now().isoformat()}\n")

        # 打包
        import tarfile
        tar_path = version_dir / "boot" / "initrd.tar"
        with tarfile.open(tar_path, 'w') as tar:
            tar.add(initrd_dir, arcname='')

        print(f"Initrd built: {tar_path}")

    def _build_iso(self, version_def, version_dir):
        """构建ISO镜像"""
        iso_dir = version_dir / "iso"
        iso_dir.mkdir(parents=True, exist_ok=True)

        # 创建ISO目录结构
        boot_dir = iso_dir / "boot"
        boot_dir.mkdir(parents=True, exist_ok=True)

        grub_dir = boot_dir / "grub"
        grub_dir.mkdir(parents=True, exist_ok=True)

        # 复制内核
        kernel_src = version_dir / "boot" / f"bamboo-os-{version_def['version']}.elf"
        if kernel_src.exists():
            shutil.copy2(kernel_src, boot_dir / "kernel.elf")

        # 复制initrd
        initrd_src = version_dir / "boot" / "initrd.tar"
        if initrd_src.exists():
            shutil.copy2(initrd_src, boot_dir / "initrd.tar")

        # 创建GRUB配置
        grub_cfg = grub_dir / "grub.cfg"
        with open(grub_cfg, 'w') as f:
            f.write(f"""set timeout=3
set default=0

menuentry "{version_def['name']}" {{
    multiboot2 /boot/kernel.elf
    module2 /boot/initrd.tar
    boot
}}

menuentry "{version_def['name']} (Safe Mode)" {{
    multiboot2 /boot/kernel.elf safemode
    module2 /boot/initrd.tar
    boot
}}

menuentry "Memory Test" {{
    multiboot2 /boot/kernel.elf memtest
    boot
}}
""")

        # 创建ISO文件（使用Python创建简单的ISO镜像）
        iso_path = version_dir / f"bamboo-os-wonder-{version_def['version']}.iso"

        # 简单的ISO创建 - 在实际中会使用grub-mkrescue
        # 这里创建一个包含所有文件的tar包作为ISO替代
        import tarfile
        with tarfile.open(iso_path, 'w:gz') as tar:
            tar.add(iso_dir, arcname='')

        print(f"ISO built: {iso_path}")

    def _generate_release_notes(self, version_def, version_dir):
        """生成版本说明"""
        notes_path = version_dir / "RELEASE_NOTES.md"

        features_list = []
        for key, value in version_def["features"].items():
            if value:
                features_list.append(key.replace("_", " ").title())

        with open(notes_path, 'w') as f:
            f.write(f"# {version_def['name']}\n\n")
            f.write(f"**Codename:** {version_def['codename']}\n")
            f.write(f"**Phase:** {version_def['phase']}\n")
            f.write(f"**Release Date:** {version_def['release_date']}\n\n")

            f.write(f"## Description\n\n")
            f.write(f"{version_def['description']}\n\n")

            f.write(f"## Features\n\n")
            for feature in features_list:
                f.write(f"- {feature}\n")
            f.write("\n")

            f.write(f"## System Requirements\n\n")
            f.write(f"- CPU: x86-64 compatible\n")
            f.write(f"- RAM: 512MB minimum, 1GB recommended\n")
            f.write(f"- Storage: 256MB free space\n")
            f.write(f"- Boot: Multiboot2 compatible bootloader\n\n")

            f.write(f"## Files\n\n")
            f.write(f"- `bamboo-os-wonder-{version_def['version']}.iso` - Installation ISO\n")
            f.write(f"- `boot/kernel.elf` - Kernel binary\n")
            f.write(f"- `boot/initrd.tar` - Initial ramdisk\n")

        print(f"Release notes: {notes_path}")

    def build_all(self):
        """构建所有版本"""
        results = {}
        for v in VERSION_DEFS:
            print(f"\n{'='*60}")
            print(f" Building version {v['version']}...")
            print(f"{'='*60}\n")
            success = self.build_version(v["version"])
            results[v["version"]] = success

        # 打印总结
        print("\n" + "=" * 60)
        print(" BUILD SUMMARY")
        print("=" * 60)
        for version, success in results.items():
            status = "SUCCESS" if success else "FAILED"
            print(f"  v{version}: {status}")
        print("=" * 60)

        return all(results.values())


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bamboo OS Version Manager")
    parser.add_argument('--list', '-l', action='store_true', help='List all versions')
    parser.add_argument('--version', '-v', type=str, help='Build specific version')
    parser.add_argument('--all', '-a', action='store_true', help='Build all versions')
    parser.add_argument('--output', '-o', type=str, help='Output directory')

    args = parser.parse_args()

    vm = VersionManager()

    if args.list:
        versions = vm.list_versions()
        print(f"{'Version':<12} {'Codename':<15} {'Phase':<10} {'Date':<12} Description")
        print("-" * 80)
        for v in versions:
            print(f"{v['version']:<12} {v['codename']:<15} {v['phase']:<10} {v['release_date']:<12} {v['description']}")
    elif args.version:
        vm.build_version(args.version, args.output)
    elif args.all:
        vm.build_all()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
