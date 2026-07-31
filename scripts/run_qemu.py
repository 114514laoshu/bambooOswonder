#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: scripts/run_qemu.py
# 模块：scripts/run_qemu.py
# Description: QEMU runner for Bamboo OS
# 描述：Bamboo OS 的 QEMU 启动脚本
# ============================================================================

import os
import sys
import subprocess
import argparse
import platform
from pathlib import Path


def get_qemu_command():
    """
    Get QEMU command for current platform.
    获取当前平台的 QEMU 命令。

    Returns:
        返回：
        str: QEMU command name / QEMU 命令名
    """
    system = platform.system().lower()
    if system == 'windows':
        return 'qemu-system-x86_64.exe'
    else:
        return 'qemu-system-x86_64'


def run_qemu(kernel_path, memory='512M', gui=False, debug=False,
             extra_args=None, initrd_path=None, disk_path=None):
    """
    Run Bamboo OS in QEMU.
    在 QEMU 中运行 Bamboo OS。

    Args:
        参数：
        kernel_path (str): Path to kernel ELF / 内核 ELF 路径
        memory (str): Memory size / 内存大小
        gui (bool): Show GUI window / 显示 GUI 窗口
        debug (bool): Enable debug mode / 启用调试模式
        extra_args (list): Extra QEMU arguments / 额外的 QEMU 参数
        initrd_path (str): Path to initrd / initrd 路径
        disk_path (str): Path to disk image / 磁盘镜像路径

    Returns:
        返回：
        int: QEMU exit code / QEMU 退出码
    """
    qemu_cmd = get_qemu_command()

    cmd = [qemu_cmd]

    # Kernel / 内核
    cmd.extend(['-kernel', kernel_path])

    # Initrd / 初始内存磁盘
    if initrd_path and os.path.exists(initrd_path):
        cmd.extend(['-initrd', initrd_path])

    # Memory / 内存
    cmd.extend(['-m', memory])

    # Display / 显示
    if not gui:
        cmd.extend(['-nographic'])
        cmd.extend(['-serial', 'stdio'])
    else:
        cmd.extend(['-vga', 'std'])

    # Disk / 磁盘
    if disk_path and os.path.exists(disk_path):
        cmd.extend(['-hda', disk_path])

    # Network / 网络
    cmd.extend(['-net', 'nic,model=rtl8139'])
    cmd.extend(['-net', 'user'])

    # Debug / 调试
    if debug:
        cmd.extend(['-s', '-S'])  # GDB server, wait for connection

    # No reboot on triple fault / 三重故障时不重启
    cmd.append('-no-reboot')

    # Extra args / 额外参数
    if extra_args:
        cmd.extend(extra_args)

    print(f"Running QEMU: {' '.join(cmd)}")
    print("Press Ctrl+A then X to exit QEMU")
    print("-" * 60)

    try:
        result = subprocess.run(cmd)
        return result.returncode
    except KeyboardInterrupt:
        print("\nQEMU interrupted by user")
        return 0
    except FileNotFoundError:
        print(f"Error: QEMU not found ({qemu_cmd})")
        print("Please install QEMU to run Bamboo OS")
        return 1


def main():
    """Main entry point / 主入口"""
    parser = argparse.ArgumentParser(
        description='Run Bamboo OS in QEMU / 在 QEMU 中运行 Bamboo OS'
    )
    parser.add_argument(
        '--kernel', '-k',
        default='build/wonder2/wonder2.elf',
        help='Path to kernel ELF file / 内核 ELF 文件路径'
    )
    parser.add_argument(
        '--initrd', '-i',
        default=None,
        help='Path to initrd / initrd 路径'
    )
    parser.add_argument(
        '--disk', '-d',
        default=None,
        help='Path to disk image / 磁盘镜像路径'
    )
    parser.add_argument(
        '--memory', '-m',
        default='512M',
        help='Memory size / 内存大小 (default: 512M)'
    )
    parser.add_argument(
        '--gui', '-g',
        action='store_true',
        help='Show GUI window / 显示 GUI 窗口'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable GDB debug mode / 启用 GDB 调试模式'
    )
    parser.add_argument(
        '--target', '-t',
        choices=['wonder1', 'wonder2', 'edu'],
        default='wonder2',
        help='Target version / 目标版本'
    )

    args = parser.parse_args()

    # Find kernel based on target / 根据目标查找内核
    if args.target:
        target_map = {
            'wonder1': ('build/wonder1/wonder1.elf', 'build/wonder1/initrd.tar'),
            'wonder2': ('build/wonder2/wonder2.elf', 'build/wonder2/initrd.tar'),
            'edu': ('build/education/education.elf', 'build/education/initrd.tar'),
        }
        if args.target in target_map:
            kernel, initrd = target_map[args.target]
            if os.path.exists(kernel):
                args.kernel = kernel
            if not args.initrd and os.path.exists(initrd):
                args.initrd = initrd

    if not os.path.exists(args.kernel):
        print(f"Error: Kernel not found: {args.kernel}")
        print("Please build the kernel first with buildmain.py")
        sys.exit(1)

    return run_qemu(
        args.kernel,
        memory=args.memory,
        gui=args.gui,
        debug=args.debug,
        initrd_path=args.initrd,
        disk_path=args.disk
    )


if __name__ == '__main__':
    sys.exit(main())
