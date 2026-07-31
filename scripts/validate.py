#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: scripts/validate.py
# 模块：scripts/validate.py
# Description: Build validation tool for Bamboo OS
# 描述：Bamboo OS 构建验证工具
# ============================================================================

import os
import sys
import struct
import json
import hashlib
from pathlib import Path


class BuildValidator:
    """
    Validate Bamboo OS build output.
    验证 Bamboo OS 构建输出。
    """

    def __init__(self, build_dir):
        """
        Initialize validator / 初始化验证器

        Args:
            参数：
            build_dir (str): Path to build directory / 构建目录路径
        """
        self.build_dir = Path(build_dir)
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check_file_exists(self, filepath, description=""):
        """
        Check if a file exists.
        检查文件是否存在。

        Args:
            参数：
            filepath (str): Relative file path / 相对文件路径
            description (str): File description / 文件描述

        Returns:
            返回：
            bool: True if exists / 存在返回 True
        """
        full_path = self.build_dir / filepath
        exists = full_path.exists() and full_path.is_file()

        if exists:
            size = full_path.stat().st_size
            self._pass(f"{description or filepath}: {size:,} bytes")
        else:
            self._fail(f"{description or filepath}: NOT FOUND")

        return exists

    def check_elf_file(self, filepath, description="ELF file"):
        """
        Check if file is a valid ELF.
        检查文件是否为有效 ELF。

        Args:
            参数：
            filepath (str): Path to ELF file / ELF 文件路径
            description (str): File description / 文件描述

        Returns:
            返回：
            bool: True if valid ELF / 有效 ELF 返回 True
        """
        full_path = self.build_dir / filepath

        if not full_path.exists():
            self._fail(f"{description}: file not found")
            return False

        try:
            with open(full_path, 'rb') as f:
                magic = f.read(4)

            if magic == b'\x7fELF':
                self._pass(f"{description}: valid ELF magic")
                return True
            else:
                self._fail(f"{description}: invalid ELF magic: {magic.hex()}")
                return False
        except Exception as e:
            self._fail(f"{description}: error reading file: {e}")
            return False

    def check_min_size(self, filepath, min_size, description=""):
        """
        Check if file meets minimum size.
        检查文件是否满足最小大小。

        Args:
            参数：
            filepath (str): File path / 文件路径
            min_size (int): Minimum size in bytes / 最小大小（字节）
            description (str): File description / 文件描述

        Returns:
            返回：
            bool: True if meets minimum size / 满足最小大小返回 True
        """
        full_path = self.build_dir / filepath

        if not full_path.exists():
            self._fail(f"{description or filepath}: file not found")
            return False

        size = full_path.stat().st_size
        if size >= min_size:
            self._pass(f"{description or filepath}: size OK ({size:,} >= {min_size:,})")
            return True
        else:
            self._fail(f"{description or filepath}: too small ({size:,} < {min_size:,})")
            return False

    def check_directory(self, dirpath, description=""):
        """
        Check if directory exists.
        检查目录是否存在。

        Args:
            参数：
            dirpath (str): Directory path / 目录路径
            description (str): Directory description / 目录描述

        Returns:
            返回：
            bool: True if exists / 存在返回 True
        """
        full_path = self.build_dir / dirpath
        exists = full_path.exists() and full_path.is_dir()

        if exists:
            file_count = len(list(full_path.iterdir()))
            self._pass(f"{description or dirpath}: {file_count} items")
        else:
            self._fail(f"{description or dirpath}: NOT FOUND")

        return exists

    def _pass(self, msg):
        """Record a pass / 记录通过"""
        self.passed += 1
        self.results.append(('PASS', msg))
        print(f"  [PASS] {msg}")

    def _fail(self, msg):
        """Record a failure / 记录失败"""
        self.failed += 1
        self.results.append(('FAIL', msg))
        print(f"  [FAIL] {msg}")

    def _warn(self, msg):
        """Record a warning / 记录警告"""
        self.warnings += 1
        self.results.append(('WARN', msg))
        print(f"  [WARN] {msg}")

    def validate_wonder(self, target='wonder2'):
        """
        Validate a Wonder version build.
        验证 Wonder 版本构建。

        Args:
            参数：
            target (str): Target name / 目标名称

        Returns:
            返回：
            bool: True if all checks pass / 所有检查通过返回 True
        """
        print(f"\nValidating {target} build...")
        print("=" * 60)

        elf_name = f"{target}.elf"
        iso_name = f"bamboo-{target}.iso"

        # Core files / 核心文件
        self.check_elf_file(elf_name, f"Kernel ELF ({elf_name})")
        self.check_min_size(elf_name, 10000, "Kernel size check")

        # Optional files / 可选文件
        iso_path = self.build_dir / iso_name
        if iso_path.exists():
            self.check_min_size(iso_name, 100000, "ISO image")
        else:
            self._warn(f"ISO image not found (use --output-iso to generate)")

        initrd_path = self.build_dir / 'initrd.tar'
        if initrd_path.exists():
            self.check_min_size('initrd.tar', 1000, "Initrd")
        else:
            self._warn("Initrd not found")

        # Build info / 构建信息
        info_path = self.build_dir / 'build_info.json'
        if info_path.exists():
            self._pass("Build info present")
        else:
            self._warn("Build info not found")

        return self.failed == 0

    def validate_education(self):
        """Validate Education version build / 验证教学版构建"""
        print("\nValidating Education build...")
        print("=" * 60)

        self.check_elf_file('education.elf', "Kernel ELF")
        self.check_min_size('education.elf', 5000, "Kernel size check")

        return self.failed == 0

    def print_summary(self):
        """Print validation summary / 打印验证摘要"""
        print("\n" + "=" * 60)
        print("Validation Summary / 验证摘要")
        print("=" * 60)
        print(f"  Total checks:  {self.passed + self.failed + self.warnings}")
        print(f"  Passed:        {self.passed}")
        print(f"  Failed:        {self.failed}")
        print(f"  Warnings:      {self.warnings}")
        print("=" * 60)

        if self.failed == 0:
            print("\n  Result: ALL CHECKS PASSED ✓")
            return True
        else:
            print(f"\n  Result: {self.failed} CHECKS FAILED ✗")
            return False

    def save_report(self, output_path):
        """
        Save validation report to file.
        保存验证报告到文件。

        Args:
            参数：
            output_path (str): Output file path / 输出文件路径
        """
        report = {
            'total': self.passed + self.failed + self.warnings,
            'passed': self.passed,
            'failed': self.failed,
            'warnings': self.warnings,
            'results': [
                {'status': status, 'message': msg}
                for status, msg in self.results
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\nReport saved to: {output_path}")


def main():
    """Main entry point / 主入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate Bamboo OS build / 验证 Bamboo OS 构建'
    )
    parser.add_argument(
        '--build-dir', '-d',
        default='build/wonder2',
        help='Build directory / 构建目录'
    )
    parser.add_argument(
        '--target', '-t',
        choices=['wonder1', 'wonder2', 'edu', 'all'],
        default='wonder2',
        help='Target to validate / 要验证的目标'
    )
    parser.add_argument(
        '--report', '-r',
        default=None,
        help='Save report to file / 保存报告到文件'
    )

    args = parser.parse_args()

    if not os.path.exists(args.build_dir):
        print(f"Error: Build directory not found: {args.build_dir}")
        sys.exit(1)

    validator = BuildValidator(args.build_dir)

    success = True
    if args.target == 'all':
        for target in ['wonder1', 'wonder2', 'edu']:
            target_dir = Path('build') / target
            if target_dir.exists():
                v = BuildValidator(str(target_dir))
                if target == 'edu':
                    success &= v.validate_education()
                else:
                    success &= v.validate_wonder(target)
                v.print_summary()
    elif args.target == 'edu':
        success = validator.validate_education()
        validator.print_summary()
    else:
        success = validator.validate_wonder(args.target)
        validator.print_summary()

    if args.report:
        validator.save_report(args.report)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
