# ============================================================================
# Module: scripts/build_patches.py
# 模块：scripts/build_patches.py
# Description: Build script for P2+ patches
# 描述：P2+ 补丁构建脚本
# ============================================================================

"""
P2+ patch build script.
P2+ 补丁构建脚本。

Builds and validates P2+ patches for optional inclusion.
构建并验证可选的 P2+ 补丁。
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any

from userland.p2plus_config import P2PLUS_CONFIG


class PatchBuilder:
    """
    P2+ patch builder.
    P2+ 补丁构建器。

    Builds patch manifests and optionally applies patches
    to the source tree.
    构建补丁清单，并可选择将补丁应用到源码树。
    """

    def __init__(self, source_dir: str, build_dir: str):
        """
        Initialize patch builder.
        初始化补丁构建器。

        Args:
            参数：
            source_dir (str): Source directory / 源码目录
            build_dir (str): Build directory / 构建目录
        """
        self.source_dir = Path(source_dir)
        self.build_dir = Path(build_dir)
        self.patch_manifest: Dict[str, Any] = {}
        self.patches_applied: List[str] = []

    def build_manifest(self) -> Dict[str, Any]:
        """
        Build patch manifest.
        构建补丁清单。

        Returns:
            返回：
            dict: Patch manifest / 补丁清单
        """
        manifest = {
            'version': '1.1.0',
            'patch_level': P2PLUS_CONFIG.get('shell', {}).get('patch_level', 1),
            'sections': {},
        }

        # Shell patches / Shell 补丁
        shell_config = P2PLUS_CONFIG.get('shell', {})
        manifest['sections']['shell'] = {
            'enabled': shell_config.get('enabled', True),
            'commands': shell_config.get('commands', {}),
            'extensions': shell_config.get('extensions', {}),
            'hooks': shell_config.get('hooks', {}),
        }

        # libc patches / libc 补丁
        libc_config = P2PLUS_CONFIG.get('libc', {})
        manifest['sections']['libc'] = {
            'enabled': libc_config.get('enabled', True),
            'patch_level': libc_config.get('patch_level', 1),
            'additions': libc_config.get('additions', {}),
        }

        # libbamboo patches / libbamboo 补丁
        bamboo_config = P2PLUS_CONFIG.get('libbamboo', {})
        manifest['sections']['libbamboo'] = {
            'enabled': bamboo_config.get('enabled', True),
            'patch_level': bamboo_config.get('patch_level', 1),
            'additions': bamboo_config.get('additions', {}),
        }

        self.patch_manifest = manifest
        return manifest

    def apply_patches(self) -> List[str]:
        """
        Apply patches to source tree.
        将补丁应用到源码树。

        Returns:
            返回：
            list: List of applied patches / 已应用的补丁列表
        """
        applied = []

        # Copy patch files / 复制补丁文件
        patch_dirs = [
            ('shell', 'userland/apps/shell/patches'),
            ('shell', 'userland/apps/shell/extensions'),
            ('libc', 'userland/libs/libc/patches'),
            ('libc', 'userland/libs/libc/extensions'),
            ('libbamboo', 'userland/libs/libbamboo/patches'),
            ('libbamboo', 'userland/libs/libbamboo/extensions'),
        ]

        for section, patch_path in patch_dirs:
            config = P2PLUS_CONFIG.get(section, {})
            if config.get('enabled', True):
                src_path = self.source_dir / patch_path
                dst_path = self.build_dir / patch_path

                if src_path.exists():
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                    applied.append(patch_path)

        self.patches_applied = applied
        return applied

    def generate_patch_info(self, output_path: str):
        """
        Generate patch information file.
        生成补丁信息文件。

        Args:
            参数：
            output_path (str): Output file path / 输出文件路径
        """
        info = {
            'version': '1.1.0',
            'build_time': str(__import__('time').time()),
            'patches_applied': self.patches_applied,
            'manifest': self.patch_manifest,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

        print(f"Patch info written to: {output_path}")

    def get_applied_patches(self) -> List[str]:
        """Get list of applied patches / 获取已应用的补丁列表"""
        return self.patches_applied


def main():
    """Main entry point / 主入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='P2+ Patch Builder / P2+ 补丁构建器'
    )
    parser.add_argument(
        '--source', '-s',
        default='.',
        help='Source directory / 源码目录'
    )
    parser.add_argument(
        '--build', '-b',
        default='build',
        help='Build directory / 构建目录'
    )
    parser.add_argument(
        '--manifest', '-m',
        action='store_true',
        help='Generate manifest only / 仅生成清单'
    )
    parser.add_argument(
        '--apply', '-a',
        action='store_true',
        help='Apply patches / 应用补丁'
    )
    parser.add_argument(
        '--output', '-o',
        default='build/patch_info.json',
        help='Output patch info file / 输出补丁信息文件'
    )

    args = parser.parse_args()

    builder = PatchBuilder(args.source, args.build)

    if args.manifest:
        manifest = builder.build_manifest()
        print(json.dumps(manifest, indent=2))
        return

    if args.apply:
        builder.build_manifest()
        applied = builder.apply_patches()
        print(f"Applied {len(applied)} patches:")
        for p in applied:
            print(f"  - {p}")

    builder.generate_patch_info(args.output)


if __name__ == '__main__':
    main()