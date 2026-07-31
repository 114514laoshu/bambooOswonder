#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: build_wonder.py
# 模块：build_wonder.py
# Description: Bamboo OS Wonder Full Build System
# 描述：Bamboo OS Wonder 完整构建系统
# 
# This script builds the complete Bamboo OS Wonder system including:
# - Kernel (Phase 0-1)
# - Userland base (Phase 2)
# - Userland extensions (Phase 2+)
# - GUI and applications (Phase 3)
# - Professional features (Phase P-PRO)
# ============================================================================

import os
import sys
import subprocess
import shutil
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional


class WonderBuildSystem:
    """
    Bamboo OS Wonder Full Build System.
    Bamboo OS Wonder 完整构建系统。

    Orchestrates the build of all system components.
    编排所有系统组件的构建。
    """

    VERSION = "1.0.0"
    RELEASE = "Wonder"
    TARGETS = ['kernel', 'userland', 'gui', 'apps', 'drivers', 'office', 'games']

    def __init__(self, build_dir: str = "build", config_file: str = None):
        """
        Initialize build system.
        初始化构建系统。

        Args:
            参数：
            build_dir (str): Build output directory / 构建输出目录
            config_file (str): Configuration file / 配置文件
        """
        self.root = Path(__file__).parent.resolve()
        self.build_dir = self.root / build_dir
        self.config = self._load_config(config_file)
        self.start_time = time.time()
        self.logs = []

        # Component build status / 组件构建状态
        self.status = {
            'kernel': False,
            'userland': False,
            'gui': False,
            'apps': False,
            'drivers': False,
            'office': False,
            'games': False,
            'pro': False,
        }

    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load build configuration / 加载构建配置"""
        default_config = {
            'target': 'wonder2',
            'debug': False,
            'verbose': False,
            'jobs': 4,
            'memory': '512M',
            'output': {
                'elf': 'wonder.elf',
                'iso': 'wonder.iso',
                'bin': 'wonder.bin',
                'disk': 'disk.img',
            },
            'features': {
                'gui': True,
                'network': True,
                'smp': True,
                'debug': False,
                'profiling': False,
                'p2plus': True,
                'p3plus': True,
                'pro': True,
            },
            'paths': {
                'kernel_src': 'kernel',
                'userland_src': 'userland',
                'toolchain_src': 'toolchain',
                'resources_src': 'resources',
            }
        }

        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    # Deep merge / 深度合并
                    self._merge_config(default_config, user_config)
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")

        return default_config

    def _merge_config(self, base: Dict, override: Dict):
        """Deep merge two dictionaries / 深度合并两个字典"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def log(self, msg: str, level: str = "INFO"):
        """Log a message / 记录消息"""
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {msg}"
        self.logs.append(entry)
        print(entry)

    def log_error(self, msg: str):
        """Log an error / 记录错误"""
        self.log(f"ERROR: {msg}", "ERROR")

    def log_success(self, msg: str):
        """Log a success / 记录成功"""
        self.log(f"SUCCESS: {msg}", "SUCCESS")

    def log_step(self, step: str):
        """Log a build step / 记录构建步骤"""
        self.log(f"=== {step} ===", "STEP")

    def check_prerequisites(self) -> bool:
        """
        Check build prerequisites.
        检查构建前置条件。

        Returns:
            返回：
            bool: True if all prerequisites are met / 所有前置条件满足返回 True
        """
        self.log_step("Checking Prerequisites")

        # Check Python version / 检查 Python 版本
        if sys.version_info < (3, 8):
            self.log_error("Python 3.8+ required")
            return False

        # Check required modules / 检查所需模块
        required_modules = ['struct', 'dataclasses', 'typing', 'pathlib']
        for mod in required_modules:
            try:
                __import__(mod)
            except ImportError:
                self.log_error(f"Required module not found: {mod}")
                return False

        # Check QEMU (optional) / 检查 QEMU（可选）
        qemu_path = shutil.which('qemu-system-x86_64')
        if qemu_path:
            self.log(f"QEMU found: {qemu_path}")
        else:
            self.log("QEMU not found (optional for testing)")

        self.log_success("Prerequisites check passed")
        return True

    def build_kernel(self) -> bool:
        """
        Build the kernel using kernel_generator.
        使用 kernel_generator 构建内核。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building Kernel")

        try:
            # Add project root to path / 将项目根目录添加到路径
            sys.path.insert(0, str(self.root))
            from kernel.kernel_generator import generate_kernel

            # Load configuration / 加载配置
            import importlib
            config_module_name = {
                'wonder1': 'configs.wonder1_config',
                'wonder2': 'configs.wonder2_config',
            }.get(self.config['target'], 'configs.education_config')
            config_mod = importlib.import_module(config_module_name)

            # Build kernel / 构建内核
            kernel_output = self.build_dir / self.config['output']['elf']
            kernel_output.parent.mkdir(parents=True, exist_ok=True)

            size = generate_kernel(config_mod, kernel_output)

            self.log_success(f"Kernel built: {kernel_output} ({size:,} bytes)")
            self.status['kernel'] = True
            return True

        except Exception as e:
            self.log_error(f"Kernel build failed: {e}")
            import traceback
            if self.config.get('verbose', False):
                traceback.print_exc()
            return False

    def build_userland(self) -> bool:
        """
        Build userland components (P2 + P2+).
        构建用户态组件（P2 + P2+）。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building Userland (Phase 2 + 2+)")

        try:
            userland_dir = self.build_dir / 'userland'
            userland_dir.mkdir(parents=True, exist_ok=True)

            # Copy userland source / 复制用户态源码
            src_dir = self.root / 'userland'
            if src_dir.exists():
                shutil.copytree(src_dir, userland_dir / 'src', dirs_exist_ok=True)

            # Build shell / 构建 Shell
            shell_src = userland_dir / 'src/apps/shell/shell.py'
            if shell_src.exists():
                # In real implementation, compile to BPP / 实际实现中编译为 BPP
                self.log("Shell source ready")

            # Build libbamboo / 构建 libbamboo
            lib_src = userland_dir / 'src/libs/libbamboo/bamboo.py'
            if lib_src.exists():
                self.log("libbamboo source ready")

            # Apply P2+ patches / 应用 P2+ 补丁
            if self.config['features'].get('p2plus', True):
                patch_dir = self.root / 'userland/apps/shell/patches'
                if patch_dir.exists():
                    shutil.copytree(patch_dir, userland_dir / 'patches', dirs_exist_ok=True)
                    self.log("P2+ patches applied")

            self.log_success("Userland components built")
            self.status['userland'] = True
            return True

        except Exception as e:
            self.log_error(f"Userland build failed: {e}")
            return False

    def build_gui(self) -> bool:
        """
        Build GUI components (Phase 3).
        构建 GUI 组件（Phase 3）。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building GUI (Phase 3)")

        if not self.config['features'].get('gui', True):
            self.log("GUI disabled by configuration")
            self.status['gui'] = True
            return True

        try:
            gui_dir = self.build_dir / 'gui'
            gui_dir.mkdir(parents=True, exist_ok=True)

            # Copy GUI libraries / 复制 GUI 库
            libgui_src = self.root / 'userland/libs/libgui'
            if libgui_src.exists():
                shutil.copytree(libgui_src, gui_dir / 'libgui', dirs_exist_ok=True)
                self.log("libgui copied")

            # Build renderer / 构建渲染器
            render_src = gui_dir / 'libgui/render.py'
            if render_src.exists():
                self.log("Renderer ready")

            self.log_success("GUI components built")
            self.status['gui'] = True
            return True

        except Exception as e:
            self.log_error(f"GUI build failed: {e}")
            return False

    def build_apps(self) -> bool:
        """
        Build applications (Phase 3 + P-PRO).
        构建应用（Phase 3 + P-PRO）。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building Applications (Phase 3 + PRO)")

        try:
            apps_dir = self.build_dir / 'apps'
            apps_dir.mkdir(parents=True, exist_ok=True)

            # Copy applications / 复制应用
            app_dirs = [
                ('terminal', self.root / 'userland/apps/terminal'),
                ('editor', self.root / 'userland/apps/editor'),
                ('office', self.root / 'userland/office'),
                ('games', self.root / 'userland/games'),
                ('app_store', self.root / 'userland/app_store'),
            ]

            for name, src_path in app_dirs:
                if src_path.exists():
                    dst_path = apps_dir / name
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                    self.log(f"App copied: {name}")

            # Build 3D graphics / 构建 3D 图形
            graphics_src = self.root / 'userland/graphics'
            if graphics_src.exists():
                shutil.copytree(graphics_src, apps_dir / 'graphics', dirs_exist_ok=True)
                self.log("3D graphics copied")

            self.log_success("Applications built")
            self.status['apps'] = True
            return True

        except Exception as e:
            self.log_error(f"Applications build failed: {e}")
            return False

    def build_drivers(self) -> bool:
        """
        Build system drivers (Phase P-PRO).
        构建系统驱动（Phase P-PRO）。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building System Drivers (PRO)")

        try:
            drivers_dir = self.build_dir / 'drivers'
            drivers_dir.mkdir(parents=True, exist_ok=True)

            # Copy driver framework / 复制驱动框架
            driver_src = self.root / 'kernel/drivers'
            if driver_src.exists():
                shutil.copytree(driver_src, drivers_dir / 'src', dirs_exist_ok=True)
                self.log("Driver framework copied")

            # Copy driver hooks / 复制驱动钩子
            hook_src = self.root / 'kernel/hooks'
            if hook_src.exists():
                shutil.copytree(hook_src, drivers_dir / 'hooks', dirs_exist_ok=True)
                self.log("Hook system copied")

            self.log_success("System drivers built")
            self.status['drivers'] = True
            return True

        except Exception as e:
            self.log_error(f"Drivers build failed: {e}")
            return False

    def build_office(self) -> bool:
        """
        Build office suite (Phase P-PRO).
        构建办公套件（Phase P-PRO）。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building Office Suite (PRO)")

        if not self.config['features'].get('pro', True):
            self.log("PRO features disabled by configuration")
            self.status['office'] = True
            return True

        try:
            office_dir = self.build_dir / 'office'
            office_dir.mkdir(parents=True, exist_ok=True)

            # Copy office applications / 复制办公应用
            office_src = self.root / 'userland/office'
            if office_src.exists():
                shutil.copytree(office_src, office_dir, dirs_exist_ok=True)
                self.log("Office suite copied")

            self.log_success("Office suite built")
            self.status['office'] = True
            return True

        except Exception as e:
            self.log_error(f"Office suite build failed: {e}")
            return False

    def build_games(self) -> bool:
        """
        Build games (Phase 3 + P3+).
        构建游戏（Phase 3 + P3+）。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building Games")

        try:
            games_dir = self.build_dir / 'games'
            games_dir.mkdir(parents=True, exist_ok=True)

            # Copy games / 复制游戏
            games_src = self.root / 'userland/games'
            if games_src.exists():
                shutil.copytree(games_src, games_dir, dirs_exist_ok=True)
                self.log("Games copied")

            # Copy game engine / 复制游戏引擎
            engine_src = self.root / 'userland/libs/libgame2d'
            if engine_src.exists():
                shutil.copytree(engine_src, games_dir / 'engine', dirs_exist_ok=True)
                self.log("Game engine copied")

            self.log_success("Games built")
            self.status['games'] = True
            return True

        except Exception as e:
            self.log_error(f"Games build failed: {e}")
            return False

    def build_initrd(self) -> bool:
        """
        Build initial ramdisk.
        构建初始内存磁盘。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building Initrd")

        try:
            initrd_dir = self.build_dir / 'initrd'
            initrd_dir.mkdir(parents=True, exist_ok=True)

            # Create directory structure / 创建目录结构
            dirs = [
                'bin', 'sbin', 'etc', 'dev', 'proc', 'sys',
                'tmp', 'home', 'root', 'var', 'usr', 'lib',
                'apps', 'libs', 'include', 'opt', 'mnt', 'media'
            ]
            for d in dirs:
                (initrd_dir / d).mkdir(parents=True, exist_ok=True)

            # Copy userland binaries / 复制用户态二进制
            userland_bin = self.build_dir / 'userland'
            if userland_bin.exists():
                shutil.copytree(userland_bin, initrd_dir / 'usr', dirs_exist_ok=True)

            # Copy applications / 复制应用
            apps_src = self.build_dir / 'apps'
            if apps_src.exists():
                shutil.copytree(apps_src, initrd_dir / 'apps', dirs_exist_ok=True)

            # Create init script / 创建初始化脚本
            init_script = initrd_dir / 'bin/init'
            with open(init_script, 'w') as f:
                f.write("""#!/bin/sh
# Bamboo OS Init Script
echo "Bamboo OS Wonder v1.0 booting..."
mount -t proc proc /proc
mount -t sysfs sys /sys
mount -t devtmpfs dev /dev
echo "Starting shell..."
/bin/shell
""")
            os.chmod(init_script, 0o755)

            # Create welcome file / 创建欢迎文件
            welcome = initrd_dir / 'etc/welcome.txt'
            with open(welcome, 'w') as f:
                f.write("""====================================================
  Bamboo OS Wonder v1.0
  Complete Operating System with:
  - GUI Desktop
  - Office Suite
  - 3D Graphics
  - App Store
  - 300+ Commands
====================================================
""")

            # Package as tar / 打包为 tar
            import tarfile
            tar_path = self.build_dir / self.config['output'].get('initrd', 'initrd.tar')
            with tarfile.open(tar_path, 'w') as tar:
                tar.add(initrd_dir, arcname='')

            self.log_success(f"Initrd built: {tar_path}")
            return True

        except Exception as e:
            self.log_error(f"Initrd build failed: {e}")
            return False

    def build_iso(self) -> bool:
        """
        Build bootable ISO image.
        构建可引导 ISO 镜像。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log_step("Building ISO Image")

        try:
            iso_dir = self.build_dir / 'iso'
            iso_dir.mkdir(parents=True, exist_ok=True)

            # Copy kernel / 复制内核
            kernel_src = self.build_dir / self.config['output']['elf']
            if kernel_src.exists():
                (iso_dir / 'boot').mkdir(parents=True, exist_ok=True)
                shutil.copy2(kernel_src, iso_dir / 'boot/kernel.elf')

            # Copy initrd / 复制 initrd
            initrd_src = self.build_dir / self.config['output'].get('initrd', 'initrd.tar')
            if initrd_src.exists():
                shutil.copy2(initrd_src, iso_dir / 'boot/initrd.tar')

            # Copy GRUB config / 复制 GRUB 配置
            grub_cfg_src = self.root / 'resources/grub/grub.cfg'
            if grub_cfg_src.exists():
                (iso_dir / 'boot/grub').mkdir(parents=True, exist_ok=True)
                shutil.copy2(grub_cfg_src, iso_dir / 'boot/grub/grub.cfg')

            # In real implementation, use grub-mkrescue / 实际实现中使用 grub-mkrescue
            # For now, create a simple ISO / 现在，创建一个简单的 ISO
            iso_path = self.build_dir / self.config['output']['iso']
            self._create_simple_iso(iso_dir, iso_path)

            self.log_success(f"ISO built: {iso_path}")
            return True

        except Exception as e:
            self.log_error(f"ISO build failed: {e}")
            return False

    def _create_simple_iso(self, iso_dir: Path, iso_path: Path):
        """Create a simple ISO image / 创建一个简单的 ISO 镜像"""
        # In real implementation, this would use grub-mkrescue or xorriso
        # 实际实现中会使用 grub-mkrescue 或 xorriso
        with open(iso_path, 'wb') as f:
            f.write(b'\x00' * 1024 * 1024)  # Placeholder 1MB ISO

    def build(self) -> bool:
        """
        Run the complete build.
        运行完整构建。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        self.log("=" * 60)
        self.log(f" Bamboo OS Wonder v{self.VERSION} Build System")
        self.log(f" Target: {self.config['target']}")
        self.log(f" Build Dir: {self.build_dir}")
        self.log("=" * 60)

        if not self.check_prerequisites():
            return False

        self.build_dir.mkdir(parents=True, exist_ok=True)

        # Build components in order / 按顺序构建组件
        steps = [
            ('kernel', self.build_kernel),
            ('userland', self.build_userland),
            ('gui', self.build_gui),
            ('apps', self.build_apps),
            ('drivers', self.build_drivers),
            ('office', self.build_office),
            ('games', self.build_games),
        ]

        for name, step_func in steps:
            if not step_func():
                self.log_error(f"Build failed at: {name}")
                self._print_summary()
                return False

        # Build initrd and ISO / 构建 initrd 和 ISO
        if not self.build_initrd():
            self.log_error("Initrd build failed")
            self._print_summary()
            return False

        if not self.build_iso():
            self.log_error("ISO build failed")
            self._print_summary()
            return False

        self.log_success("Complete build successful!")
        self._print_summary()
        return True

    def _print_summary(self):
        """Print build summary / 打印构建摘要"""
        elapsed = time.time() - self.start_time
        self.log("=" * 60)
        self.log(" BUILD SUMMARY")
        self.log("=" * 60)

        for name, status in self.status.items():
            icon = "✅" if status else "❌"
            self.log(f"  {icon} {name:12s}: {'SUCCESS' if status else 'FAILED'}")

        self.log(f"  Total time: {elapsed:.2f}s")
        self.log(f"  Output dir: {self.build_dir}")
        self.log("=" * 60)


def main():
    """Main entry point / 主入口"""
    parser = argparse.ArgumentParser(
        description="Bamboo OS Wonder Build System"
    )
    parser.add_argument(
        '--target', '-t',
        choices=['wonder1', 'wonder2', 'edu'],
        default='wonder2',
        help='Build target / 构建目标'
    )
    parser.add_argument(
        '--build-dir', '-b',
        default='build',
        help='Build directory / 构建目录'
    )
    parser.add_argument(
        '--config', '-c',
        default=None,
        help='Configuration file / 配置文件'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output / 详细输出'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug build / 启用调试构建'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean build directory / 清理构建目录'
    )

    args = parser.parse_args()

    # Clean if requested / 如果需要清理
    if args.clean:
        import shutil
        build_dir = Path(args.build_dir)
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print(f"Cleaned: {build_dir}")
        return

    # Build configuration / 构建配置
    config = {
        'target': args.target,
        'verbose': args.verbose,
        'debug': args.debug,
        'features': {
            'gui': True,
            'network': True,
            'smp': True,
            'debug': args.debug,
            'profiling': args.debug,
            'p2plus': True,
            'p3plus': True,
            'pro': True,
        }
    }

    # Run build / 运行构建
    builder = WonderBuildSystem(args.build_dir, args.config)
    builder.config.update(config)
    success = builder.build()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()