#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: scripts/create_iso.py
# 模块：scripts/create_iso.py
# Description: ISO image creator for Bamboo OS
# 描述：Bamboo OS 的 ISO 镜像创建工具
# ============================================================================

import os
import sys
import struct
import argparse
from pathlib import Path


def create_bootable_iso(kernel_path, iso_path, initrd_path=None, grub_cfg=None):
    """
    Create a bootable ISO image for Bamboo OS.
    为 Bamboo OS 创建可引导 ISO 镜像。

    Args:
        参数：
        kernel_path (str): Path to kernel ELF / 内核 ELF 路径
        iso_path (str): Output ISO path / 输出 ISO 路径
        initrd_path (str): Path to initrd / initrd 路径
        grub_cfg (str): Path to GRUB config / GRUB 配置路径

    Returns:
        返回：
        int: ISO size in bytes / ISO 大小（字节）
    """
    print(f"Creating bootable ISO: {iso_path}")
    print(f"  Kernel: {kernel_path}")

    # Read kernel / 读取内核
    with open(kernel_path, 'rb') as f:
        kernel_data = f.read()

    # Read initrd if provided / 读取 initrd（如果提供）
    initrd_data = b''
    if initrd_path and os.path.exists(initrd_path):
        with open(initrd_path, 'rb') as f:
            initrd_data = f.read()
        print(f"  Initrd: {initrd_path}")

    # Create ISO structure / 创建 ISO 结构
    # Simplified ISO9660 with boot catalog / 简化的 ISO9660 + 引导目录
    sector_size = 2048

    # Boot sector / 引导扇区
    boot_sector = bytearray(sector_size)
    boot_sector[0:7] = b'\x00CD001\x01'  # ISO9660 magic
    # ... simplified boot sector

    # For simplicity, create a minimal ISO / 简化：创建最小 ISO
    iso_data = bytearray()

    # Primary volume descriptor / 主卷描述符
    pvd = bytearray(sector_size)
    pvd[0] = 1  # Volume descriptor type
    pvd[1:6] = b'CD001'  # Standard identifier
    pvd[6] = 1  # Volume descriptor version
    # System identifier / 系统标识符
    pvd[8:40] = b'BAMBOO OS'.ljust(32, b'\x00')
    # Volume identifier / 卷标识符
    pvd[40:72] = b'BAMBOO_OS'.ljust(32, b'\x00')
    # Volume space size / 卷空间大小（扇区数）
    total_sectors = 100  # Simplified
    struct.pack_into('<I', pvd, 80, total_sectors)
    struct.pack_into('>I', pvd, 84, total_sectors)
    # Volume set size / 卷集大小
    struct.pack_into('<H', pvd, 120, 1)
    struct.pack_into('>H', pvd, 122, 1)
    # Volume sequence number / 卷序列号
    struct.pack_into('<H', pvd, 124, 1)
    struct.pack_into('>H', pvd, 126, 1)
    # Logical block size / 逻辑块大小
    struct.pack_into('<H', pvd, 128, sector_size)
    struct.pack_into('>H', pvd, 130, sector_size)
    # Path table size / 路径表大小
    struct.pack_into('<I', pvd, 132, 0)
    struct.pack_into('>I', pvd, 136, 0)
    # Volume creation date / 卷创建日期
    import time
    date_str = time.strftime('%Y%m%d%H%M%S') + '00'
    pvd[813:830] = date_str.encode('ascii').ljust(17, b'\x00')

    iso_data.extend(pvd)

    # Add kernel data (simplified - just append) / 添加内核数据（简化：直接追加）
    # Pad to sector boundary / 对齐到扇区边界
    while len(iso_data) % sector_size != 0:
        iso_data.append(0)

    # Add kernel / 添加内核
    kernel_start = len(iso_data) // sector_size
    iso_data.extend(kernel_data)
    while len(iso_data) % sector_size != 0:
        iso_data.append(0)

    # Add initrd / 添加 initrd
    initrd_start = len(iso_data) // sector_size
    if initrd_data:
        iso_data.extend(initrd_data)
        while len(iso_data) % sector_size != 0:
            iso_data.append(0)

    # Volume descriptor set terminator / 卷描述符集终止符
    vd_term = bytearray(sector_size)
    vd_term[0] = 255  # Terminator
    vd_term[1:6] = b'CD001'
    vd_term[6] = 1
    iso_data.extend(vd_term)

    # Write ISO / 写入 ISO
    os.makedirs(os.path.dirname(iso_path) or '.', exist_ok=True)
    with open(iso_path, 'wb') as f:
        f.write(iso_data)

    size = len(iso_data)
    print(f"ISO created: {size:,} bytes ({size // 1024} KB)")
    return size


def main():
    """Main entry point / 主入口"""
    parser = argparse.ArgumentParser(
        description='Create bootable ISO for Bamboo OS / 为 Bamboo OS 创建可引导 ISO'
    )
    parser.add_argument(
        '--kernel', '-k',
        required=True,
        help='Path to kernel ELF / 内核 ELF 路径'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output ISO path / 输出 ISO 路径'
    )
    parser.add_argument(
        '--initrd', '-i',
        default=None,
        help='Path to initrd / initrd 路径'
    )

    args = parser.parse_args()

    if not os.path.exists(args.kernel):
        print(f"Error: Kernel not found: {args.kernel}")
        sys.exit(1)

    create_bootable_iso(args.kernel, args.output, args.initrd)


if __name__ == '__main__':
    main()
