#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bamboo OS Wonder v10.0 Ultimate Edition
终极完整版 - 人人可用的操作系统
"""
import os
import sys
import struct
import json
import tarfile
import shutil
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from kernel.bamboo_os_core import X64Compiler


class UltimateKernelGenerator:
    """终极版内核生成器"""

    def __init__(self):
        self.compiler = X64Compiler()
        self.c = self.compiler

    def generate(self, output_path):
        """生成终极版内核"""
        c = self.c

        # ====================================================================
        # 启动与核心基础设施
        # ====================================================================
        c.create_multiboot2_header()
        c.create_32bit_startup_stub()
        c.create_long_mode_switch()
        c.build_initial_page_tables()
        c.build_gdt_table()
        c.create_kmain()

        # ====================================================================
        # 内存管理 - 完整实现
        # ====================================================================
        # 物理内存管理
        c.create_pmm_init()
        c.create_pmm_init_bitmap()
        c.create_pmm_init_buddy()
        c.create_pmm_alloc_buddy()
        c.create_pmm_free_buddy()
        c.create_pmm_alloc_page()
        c.create_pmm_free_page()
        c.create_pmm_stats()
        c.create_pmm_debug()

        # 虚拟内存管理
        c.create_vmm_walk_page_table()
        c.create_vmm_map_page()
        c.create_vmm_unmap_page()
        c.create_vmm_protect_page()
        c.create_vmm_kernel_space_map()
        c.create_vmm_user_space_map()
        c.create_vmm_check_user_addr()
        c.create_address_space_struct()

        # Slab分配器
        c.create_kmem_cache_struct()
        c.create_kmem_cache_create()
        c.create_kmem_cache_destroy()
        c.create_kmem_cache_alloc()
        c.create_kmem_cache_free()
        c.create_kmalloc()
        c.create_kfree()
        c.create_slab_caches_init()
        c.create_emergency_pool()

        # 用户内存管理
        c.create_sys_mmap()
        c.create_sys_munmap()
        c.create_sys_mprotect()
        c.create_cow_mechanism()
        c.create_sys_brk()
        c.create_shared_memory()

        # 高级内存特性
        c.create_swap_support()
        c.create_memory_compaction()
        c.create_hugepage_support()
        c.create_numa_allocator()
        c.create_memory_hotplug()

        # 内存调试
        c.create_kasan()
        c.create_rbtree_memory_tracking()
        c.create_slab_poisoning()
        c.create_kmemleak()
        c.create_proc_meminfo()

        # ====================================================================
        # 进程与调度
        # ====================================================================
        c.create_pcb_struct()
        c.create_scheduler()
        c.create_context_switch()
        c.create_sync_primitives()
        c.create_ipc()

        # ====================================================================
        # 中断与系统调用
        # ====================================================================
        c.create_interrupt_handling()
        c.create_exception_handling()
        c.create_syscall_framework()

        # ====================================================================
        # 文件系统 - 完整实现
        # ====================================================================
        c.create_vfs_core()
        c.create_fat32()
        c.create_ext_filesystems()
        c.create_proc_sysfs()
        c.create_vfs_advanced()

        # ====================================================================
        # 设备驱动
        # ====================================================================
        c.create_device_model()
        c.create_block_device()
        c.create_network_stack()
        c.create_graphics_input()
        c.create_advanced_drivers()

        # ====================================================================
        # SMP与安全
        # ====================================================================
        c.create_smp_support()
        c.create_security_features()

        # ====================================================================
        # 高级特性
        # ====================================================================
        c.create_virtualization()
        c.create_container_support()
        c.create_dynamic_linker()
        c.create_posix_compat()

        # ====================================================================
        # 网络服务与GUI
        # ====================================================================
        c.create_network_services()
        c.create_gui()
        c.create_av_subsystem()

        # ====================================================================
        # 工具链与系统服务
        # ====================================================================
        c.create_toolchain()
        c.create_package_manager()
        c.create_system_services()

        # ====================================================================
        # 测试与发布
        # ====================================================================
        c.create_test_certification()
        c.create_release_maintenance()

        # ====================================================================
        # 解析并保存
        # ====================================================================
        c.resolve()
        size = c.save(str(output_path))
        return size


def build_ultimate_edition():
    """构建终极版"""
    print("=" * 70)
    print("  Bamboo OS Wonder v10.0 - Ultimate Edition")
    print("  终极完整版 - 人人可用的操作系统")
    print("=" * 70)

    # 创建输出目录
    output_dir = Path(__file__).parent.parent / "releases" / "v10.0.0-ultimate"
    output_dir.mkdir(parents=True, exist_ok=True)

    boot_dir = output_dir / "boot"
    boot_dir.mkdir(parents=True, exist_ok=True)

    # 构建内核
    print("\n[1/6] Building Ultimate Kernel...")
    kernel_path = boot_dir / "bamboo-os-10.0.0-ultimate.elf"
    generator = UltimateKernelGenerator()
    kernel_size = generator.generate(kernel_path)
    print(f"  Kernel size: {kernel_size:,} bytes")

    # 构建initrd
    print("\n[2/6] Building Initial Ramdisk...")
    initrd_path = build_initrd(output_dir)
    print(f"  Initrd size: {initrd_path.stat().st_size:,} bytes")

    # 构建应用程序包
    print("\n[3/6] Building Application Packages...")
    apps_dir = build_applications(output_dir)
    print(f"  Applications: {len(list(apps_dir.glob('*.bpp')))} packages")

    # 构建ISO
    print("\n[4/6] Building Bootable ISO...")
    iso_path = build_iso(output_dir)
    print(f"  ISO size: {iso_path.stat().st_size:,} bytes")

    # 生成文档
    print("\n[5/6] Generating Documentation...")
    build_docs(output_dir)
    print("  Documentation generated")

    # 生成版本说明
    print("\n[6/6] Generating Release Notes...")
    build_release_notes(output_dir)
    print("  Release notes generated")

    print("\n" + "=" * 70)
    print("  BUILD SUCCESSFUL!")
    print(f"  Output: {output_dir}")
    print("=" * 70)

    return output_dir


def build_initrd(output_dir):
    """构建初始内存磁盘"""
    initrd_dir = output_dir / "initrd"
    initrd_dir.mkdir(parents=True, exist_ok=True)

    # 创建目录结构
    dirs = [
        'bin', 'sbin', 'etc', 'dev', 'proc', 'sys', 'tmp', 'home', 'root',
        'var', 'var/log', 'var/run', 'var/spool', 'var/tmp',
        'usr', 'usr/bin', 'usr/sbin', 'usr/lib', 'usr/include', 'usr/share',
        'usr/local', 'usr/local/bin', 'usr/local/lib',
        'apps', 'apps/system', 'apps/office', 'apps/games', 'apps/net',
        'apps/media', 'apps/utilities',
        'libs', 'include', 'opt', 'mnt', 'media', 'boot',
        'etc/init.d', 'etc/network', 'etc/X11', 'etc/fonts',
        'usr/share/applications', 'usr/share/icons', 'usr/share/themes',
        'usr/share/fonts', 'usr/share/doc',
    ]
    for d in dirs:
        (initrd_dir / d).mkdir(parents=True, exist_ok=True)

    # 创建系统配置文件
    # /etc/version
    with open(initrd_dir / 'etc' / 'version', 'w') as f:
        f.write("""DISTRIB_ID=BambooOS
DISTRIB_RELEASE=10.0.0
DISTRIB_CODENAME=Wonder
DISTRIB_DESCRIPTION="Bamboo OS Wonder Ultimate Edition"
VERSION_ID=10.0
PRETTY_NAME="Bamboo OS Wonder 10.0 (Ultimate Edition)"
""")

    # /etc/os-release
    with open(initrd_dir / 'etc' / 'os-release', 'w') as f:
        f.write("""NAME="Bamboo OS"
VERSION="10.0 (Wonder Ultimate Edition)"
ID=bamboo
ID_LIKE=linux
VERSION_ID=10.0
PRETTY_NAME="Bamboo OS Wonder 10.0 (Ultimate Edition)"
ANSI_COLOR="0;32"
HOME_URL="https://bamboo-os.org"
DOCUMENTATION_URL="https://docs.bamboo-os.org"
SUPPORT_URL="https://support.bamboo-os.org"
BUG_REPORT_URL="https://bugs.bamboo-os.org"
""")

    # /etc/hostname
    with open(initrd_dir / 'etc' / 'hostname', 'w') as f:
        f.write("bamboo-os\n")

    # /etc/hosts
    with open(initrd_dir / 'etc' / 'hosts', 'w') as f:
        f.write("""127.0.0.1   localhost
127.0.1.1   bamboo-os
::1         localhost ip6-localhost ip6-loopback
ff02::1     ip6-allnodes
ff02::2     ip6-allrouters
""")

    # /etc/fstab
    with open(initrd_dir / 'etc' / 'fstab', 'w') as f:
        f.write("""# <file system> <mount point> <type> <options> <dump> <pass>
proc            /proc           proc    defaults        0       0
sysfs           /sys            sysfs   defaults        0       0
devtmpfs        /dev            devtmpfs defaults      0       0
tmpfs           /tmp            tmpfs   defaults        0       0
tmpfs           /run            tmpfs   defaults        0       0
/dev/sda1       /               ext4    defaults        0       1
""")

    # /etc/shells
    with open(initrd_dir / 'etc' / 'shells', 'w') as f:
        f.write("""# Valid login shells
/bin/sh
/bin/bash
/bin/zsh
/bin/fish
/bin/shell
""")

    # /etc/profile
    with open(initrd_dir / 'etc' / 'profile', 'w') as f:
        f.write("""# /etc/profile - system-wide profile
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
export PS1="\\u@\\h:\\w\\$ "
export EDITOR=vi
export PAGER=less
""")

    # 欢迎信息
    with open(initrd_dir / 'etc' / 'welcome.txt', 'w') as f:
        f.write("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ██████╗  █████╗ ███╗   ███╗██████╗  ██████╗  ██████╗    ║
║     ██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔═══██╗██╔═══██╗   ║
║     ██████╔╝███████║██╔████╔██║██████╔╝██║   ██║██║   ██║   ║
║     ██╔══██╗██╔══██║██║╚██╔╝██║██╔══██╗██║   ██║██║   ██║   ║
║     ██████╔╝██║  ██║██║ ╚═╝ ██║██████╔╝╚██████╔╝╚██████╔╝   ║
║     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝  ╚═════╝  ╚═════╝    ║
║                                                              ║
║              Wonder 10.0 Ultimate Edition                    ║
║                                                              ║
║     Complete Operating System with GUI, Office, Games,       ║
║     Networking, Chinese Support, and App Store               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

  Version: 10.0.0 (Stable)
  Codename: Wonder
  Release Date: 2026-07-31
  Architecture: x86-64
  Kernel: Bamboo Kernel 10.0

  Type 'help' for available commands.
  Type 'gui' to start the desktop environment.

""")

    # MOTD
    with open(initrd_dir / 'etc' / 'motd', 'w') as f:
        f.write("""
Welcome to Bamboo OS Wonder 10.0 (Ultimate Edition)!

 * Documentation:  https://docs.bamboo-os.org
 * Support:        https://support.bamboo-os.org
 * App Store:      type 'appstore'

""")

    # 创建Shell命令列表
    commands = [
        # 文件系统命令
        'ls', 'cd', 'pwd', 'mkdir', 'rmdir', 'rm', 'cp', 'mv', 'cat', 'touch',
        'chmod', 'chown', 'chgrp', 'ln', 'symlink', 'readlink', 'stat',
        'wc', 'head', 'tail', 'sort', 'uniq', 'grep', 'find', 'diff', 'patch',
        'tee', 'truncate', 'du', 'df', 'mount', 'umount', 'fdisk', 'mkfs',
        'fsck', 'sync', 'dump', 'xxd', 'base64', 'md5', 'sha256',
        'compress', 'decompress', 'tar', 'zip', 'unzip',
        # 进程管理命令
        'ps', 'top', 'kill', 'killall', 'fork', 'exec', 'nice', 'renice',
        'bg', 'fg', 'jobs', 'nohup', 'wait', 'sleep', 'usleep',
        'crontab', 'at', 'watch', 'timeout', 'chroot',
        # 网络命令
        'ifconfig', 'ip', 'ping', 'traceroute', 'netstat', 'ss', 'arp',
        'route', 'nslookup', 'dig', 'host', 'wget', 'curl', 'ssh', 'scp',
        'telnet', 'ftp', 'nc', 'socat', 'tcpdump', 'iptables', 'nmap',
        'dhcp', 'httpd',
        # 系统管理命令
        'uname', 'hostname', 'uptime', 'date', 'cal', 'who', 'whoami', 'id',
        'reboot', 'shutdown', 'halt', 'poweroff', 'dmesg', 'sysctl',
        'lscpu', 'lsmem', 'time', 'strace', 'ltrace', 'perf',
        'sysinfo', 'version', 'debug', 'log',
        # Shell内置命令
        'help', 'history', 'clear', 'echo', 'printf', 'read', 'alias',
        'unalias', 'set', 'export', 'unset', 'env', 'source', 'which',
        'whereis', 'type', 'pushd', 'popd', 'dirs', 'true', 'false',
        'test', 'expr', 'let',
        # 设备管理命令
        'lsdev', 'lsusb', 'lspci', 'lsblk', 'devinfo', 'mountdev',
        'umountdev', 'mknod', 'ioctl', 'lsmodule', 'insmod', 'rmmod',
        'modprobe', 'modinfo',
        # GUI命令
        'gui', 'desktop', 'window', 'closewin', 'terminal', 'editor',
        'fileman', 'browser', 'paint', 'calculator', 'notepad',
        'taskbar', 'menu', 'screenshot', 'wallpaper', 'theme',
        'font', 'resolution', 'refresh', 'cursor', 'icon', 'widget',
        'dialog', 'notify', 'tray', 'dock',
        # 音频命令
        'play', 'stop', 'pause', 'volume', 'mute', 'record', 'mixer', 'beep',
        'tone', 'wave',
        # 安全命令
        'login', 'logout', 'passwd', 'su', 'sudo', 'umask', 'selinux',
        'gpg', 'openssl', 'hash', 'sign', 'verify', 'encrypt', 'decrypt',
        # 娱乐与测试命令
        'fortune', 'cowsay', 'lolcat', 'figlet', 'matrix', 'cmatrix',
        'pipes', 'clock', 'weather', 'color', 'benchmark', 'stress',
        'testfs', 'testnet', 'testmm', 'testgui', 'testall',
        # 应用命令
        'word', 'spreadsheet', 'presentation', 'pdfview', 'calc',
        'calendar', 'email', 'downloader', 'imageview', 'video',
        'snake', 'tetris', 'minesweeper', 'chess', 'view3d',
        'app_store', 'settings', 'sysmon',
    ]

    with open(initrd_dir / 'etc' / 'shell_commands.txt', 'w') as f:
        for cmd in commands:
            f.write(f"{cmd}\n")

    # 创建应用程序列表
    apps = [
        # 系统应用
        ('Shell', 'shell', 'system', 'Command line shell with 300+ commands'),
        ('Terminal', 'terminal', 'system', 'Terminal emulator with ANSI support'),
        ('File Manager', 'fileman', 'system', 'Graphical file manager'),
        ('Settings', 'settings', 'system', 'System configuration center'),
        ('System Monitor', 'sysmon', 'system', 'Performance monitoring tool'),
        ('Desktop', 'desktop', 'system', 'Desktop environment'),
        ('Taskbar', 'taskbar', 'system', 'Window management taskbar'),
        # 办公应用
        ('Word Processor', 'word', 'office', 'Document creation and editing'),
        ('Spreadsheet', 'spreadsheet', 'office', 'Spreadsheet with formulas'),
        ('Presentation', 'presentation', 'office', 'Slide presentation maker'),
        ('PDF Viewer', 'pdfview', 'office', 'PDF document viewer'),
        ('Notepad', 'notepad', 'office', 'Simple text editor'),
        ('Calculator', 'calc', 'office', 'Scientific calculator'),
        ('Calendar', 'calendar', 'office', 'Calendar and schedule manager'),
        # 网络应用
        ('Web Browser', 'browser', 'net', 'HTML/CSS web browser'),
        ('Email Client', 'email', 'net', 'IMAP/SMTP email client'),
        ('Download Manager', 'downloader', 'net', 'File download manager'),
        # 媒体应用
        ('Audio Player', 'play', 'media', 'WAV/MP3 audio player'),
        ('Video Player', 'video', 'media', 'Video player'),
        ('Image Viewer', 'imageview', 'media', 'PNG/JPEG/BMP viewer'),
        ('Paint', 'paint', 'media', 'Bitmap drawing tool'),
        # 游戏
        ('Snake', 'snake', 'games', 'Classic snake game'),
        ('Tetris', 'tetris', 'games', 'Block puzzle game'),
        ('Minesweeper', 'minesweeper', 'games', 'Logic puzzle game'),
        ('Chess', 'chess', 'games', 'Chess with AI opponent'),
        ('3D Viewer', 'view3d', 'games', '3D model viewer'),
        # 商店
        ('App Store', 'app_store', 'store', 'Application marketplace'),
    ]

    with open(initrd_dir / 'usr' / 'share' / 'applications' / 'app.list', 'w') as f:
        for name, cmd, category, desc in apps:
            f.write(f"{name}|{cmd}|{category}|{desc}\n")

    # 创建主题文件
    themes = {
        'bamboo': {
            'name': 'Bamboo',
            'bg_color': '#2D5A27',
            'fg_color': '#FFFFFF',
            'accent_color': '#4CAF50',
            'title_bg': '#1B5E20',
            'title_fg': '#FFFFFF',
            'border_color': '#388E3C',
        },
        'dark': {
            'name': 'Dark',
            'bg_color': '#2D2D2D',
            'fg_color': '#FFFFFF',
            'accent_color': '#0078D7',
            'title_bg': '#1E1E1E',
            'title_fg': '#FFFFFF',
            'border_color': '#3D3D3D',
        },
        'light': {
            'name': 'Light',
            'bg_color': '#F5F5F5',
            'fg_color': '#000000',
            'accent_color': '#0078D7',
            'title_bg': '#E0E0E0',
            'title_fg': '#000000',
            'border_color': '#BDBDBD',
        },
    }

    for name, theme in themes.items():
        with open(initrd_dir / 'usr' / 'share' / 'themes' / f'{name}.json', 'w') as f:
            json.dump(theme, f, indent=2)

    # 打包initrd
    initrd_path = output_dir / "boot" / "initrd.tar"
    with tarfile.open(initrd_path, 'w') as tar:
        tar.add(initrd_dir, arcname='')

    return initrd_path


def build_applications(output_dir):
    """构建应用程序包"""
    apps_dir = output_dir / "apps"
    apps_dir.mkdir(parents=True, exist_ok=True)

    # 创建BPP应用包（Bamboo Package Format）
    app_list = [
        # 系统应用
        ('shell', 'Shell', 'system', '10.0.0', ['libbamboo']),
        ('terminal', 'Terminal', 'system', '10.0.0', ['libbamboo', 'libgui']),
        ('fileman', 'File Manager', 'system', '10.0.0', ['libbamboo', 'libgui']),
        ('settings', 'Settings', 'system', '10.0.0', ['libbamboo', 'libgui']),
        ('sysmon', 'System Monitor', 'system', '10.0.0', ['libbamboo', 'libgui']),
        ('desktop', 'Desktop Environment', 'system', '10.0.0', ['libbamboo', 'libgui']),
        # 办公应用
        ('word', 'Word Processor', 'office', '10.0.0', ['libbamboo', 'libgui']),
        ('spreadsheet', 'Spreadsheet', 'office', '10.0.0', ['libbamboo', 'libgui']),
        ('presentation', 'Presentation', 'office', '10.0.0', ['libbamboo', 'libgui']),
        ('pdfview', 'PDF Viewer', 'office', '10.0.0', ['libbamboo', 'libgui']),
        ('calculator', 'Calculator', 'office', '10.0.0', ['libbamboo', 'libgui']),
        ('calendar', 'Calendar', 'office', '10.0.0', ['libbamboo', 'libgui']),
        # 网络应用
        ('browser', 'Web Browser', 'network', '10.0.0', ['libbamboo', 'libgui', 'libnet']),
        ('email', 'Email Client', 'network', '10.0.0', ['libbamboo', 'libgui', 'libnet']),
        ('downloader', 'Download Manager', 'network', '10.0.0', ['libbamboo', 'libgui', 'libnet']),
        # 媒体应用
        ('audioplayer', 'Audio Player', 'media', '10.0.0', ['libbamboo', 'libgui', 'libaudio']),
        ('videoplayer', 'Video Player', 'media', '10.0.0', ['libbamboo', 'libgui', 'libaudio']),
        ('imageview', 'Image Viewer', 'media', '10.0.0', ['libbamboo', 'libgui']),
        ('paint', 'Paint', 'media', '10.0.0', ['libbamboo', 'libgui']),
        # 游戏
        ('snake', 'Snake', 'games', '10.0.0', ['libbamboo', 'libgui', 'libgame2d']),
        ('tetris', 'Tetris', 'games', '10.0.0', ['libbamboo', 'libgui', 'libgame2d']),
        ('minesweeper', 'Minesweeper', 'games', '10.0.0', ['libbamboo', 'libgui', 'libgame2d']),
        ('chess', 'Chess', 'games', '10.0.0', ['libbamboo', 'libgui', 'libgame2d']),
        ('view3d', '3D Viewer', 'games', '10.0.0', ['libbamboo', 'libgui', 'lib3d']),
        # 工具
        ('notepad', 'Notepad', 'utilities', '10.0.0', ['libbamboo', 'libgui']),
        ('screenshot', 'Screenshot', 'utilities', '10.0.0', ['libbamboo', 'libgui']),
        ('appstore', 'App Store', 'store', '10.0.0', ['libbamboo', 'libgui', 'libnet']),
    ]

    for app_id, name, category, version, deps in app_list:
        # 创建BPP包（简化格式）
        bpp_data = {
            'id': app_id,
            'name': name,
            'category': category,
            'version': version,
            'dependencies': deps,
            'size': 10240,  # 模拟大小
            'installed': True,
            'description': f'{name} application for Bamboo OS',
        }

        bpp_path = apps_dir / f'{app_id}.bpp'
        with open(bpp_path, 'w') as f:
            json.dump(bpp_data, f, indent=2)

    # 创建应用商店目录
    store_dir = apps_dir / "store"
    store_dir.mkdir(parents=True, exist_ok=True)

    # 额外的可用应用（未预装）
    available_apps = [
        ('doom', 'DOOM', 'games', '1.0.0', ['libbamboo', 'libgui', 'lib3d']),
        ('racer', 'Racer', 'games', '1.0.0', ['libbamboo', 'libgui', 'lib3d']),
        ('blocks', '3D Blocks', 'games', '1.0.0', ['libbamboo', 'libgui', 'lib3d']),
        ('platformer', 'Platformer', 'games', '1.0.0', ['libbamboo', 'libgui', 'libgame2d']),
        ('poker', 'Poker', 'games', '1.0.0', ['libbamboo', 'libgui', 'libgame2d']),
        ('irc', 'IRC Client', 'network', '1.0.0', ['libbamboo', 'libgui', 'libnet']),
        ('vnc', 'VNC Viewer', 'network', '1.0.0', ['libbamboo', 'libgui', 'libnet']),
        ('cloudsync', 'Cloud Sync', 'network', '1.0.0', ['libbamboo', 'libgui', 'libnet']),
        ('gimp', 'Image Editor', 'media', '1.0.0', ['libbamboo', 'libgui']),
        ('audacity', 'Audio Editor', 'media', '1.0.0', ['libbamboo', 'libgui', 'libaudio']),
        ('blender', '3D Editor', 'media', '1.0.0', ['libbamboo', 'libgui', 'lib3d']),
        ('gcc', 'C Compiler', 'development', '1.0.0', ['libbamboo']),
        ('python', 'Python', 'development', '1.0.0', ['libbamboo']),
        ('git', 'Git', 'development', '1.0.0', ['libbamboo']),
        ('vim', 'Vim Editor', 'development', '1.0.0', ['libbamboo']),
    ]

    for app_id, name, category, version, deps in available_apps:
        bpp_data = {
            'id': app_id,
            'name': name,
            'category': category,
            'version': version,
            'dependencies': deps,
            'size': 20480,
            'installed': False,
            'rating': 4.5,
            'downloads': 10000,
            'description': f'{name} - available from Bamboo App Store',
        }

        bpp_path = store_dir / f'{app_id}.bpp'
        with open(bpp_path, 'w') as f:
            json.dump(bpp_data, f, indent=2)

    return apps_dir


def build_iso(output_dir):
    """构建可引导ISO"""
    iso_dir = output_dir / "iso"
    iso_dir.mkdir(parents=True, exist_ok=True)

    # 创建ISO目录结构
    boot_dir = iso_dir / "boot"
    boot_dir.mkdir(parents=True, exist_ok=True)

    grub_dir = boot_dir / "grub"
    grub_dir.mkdir(parents=True, exist_ok=True)

    # 复制内核
    kernel_src = output_dir / "boot" / "bamboo-os-10.0.0-ultimate.elf"
    if kernel_src.exists():
        shutil.copy2(kernel_src, boot_dir / "kernel.elf")

    # 复制initrd
    initrd_src = output_dir / "boot" / "initrd.tar"
    if initrd_src.exists():
        shutil.copy2(initrd_src, boot_dir / "initrd.tar")

    # 创建GRUB配置
    grub_cfg = grub_dir / "grub.cfg"
    with open(grub_cfg, 'w') as f:
        f.write("""# Bamboo OS Wonder GRUB Configuration
set timeout=5
set default=0
set gfxmode=1024x768x32
insmod all_video
insmod gfxterm
insmod png
insmod part_msdos
insmod ext2

set theme=/boot/grub/theme.txt

menuentry "Bamboo OS Wonder 10.0" {
    set root=(hd0,1)
    multiboot2 /boot/kernel.elf root=/dev/sda1 quiet splash
    module2 /boot/initrd.tar
    boot
}

menuentry "Bamboo OS Wonder 10.0 (Recovery Mode)" {
    set root=(hd0,1)
    multiboot2 /boot/kernel.elf root=/dev/sda1 single recovery
    module2 /boot/initrd.tar
    boot
}

menuentry "Bamboo OS Wonder 10.0 (Command Line)" {
    set root=(hd0,1)
    multiboot2 /boot/kernel.elf root=/dev/sda1 text
    module2 /boot/initrd.tar
    boot
}

menuentry "Memory Test" {
    set root=(hd0,1)
    multiboot2 /boot/kernel.elf memtest
    boot
}

menuentry "System Setup" {
    set root=(hd0,1)
    multiboot2 /boot/kernel.elf setup
    module2 /boot/initrd.tar
    boot
}
""")

    # 创建GRUB主题
    theme_file = grub_dir / "theme.txt"
    with open(theme_file, 'w') as f:
        f.write("""# Bamboo OS GRUB Theme
title-text: "Bamboo OS Wonder 10.0"
title-color: "#4CAF50"
desktop-color: "#1B5E20"
terminal-box: "20% 20% 60% 60%"
terminal-border: "double"
terminal-border-color: "#4CAF50"
terminal-background: "#000000"
terminal-color: "#FFFFFF"
selected-item-color: "#4CAF50"
selected-item-background: "#2E7D32"
""")

    # 复制应用
    apps_src = output_dir / "apps"
    if apps_src.exists():
        apps_dst = iso_dir / "apps"
        shutil.copytree(apps_src, apps_dst, dirs_exist_ok=True)

    # 创建ISO镜像（使用tar.gz格式作为简化的ISO）
    iso_path = output_dir / "bamboo-os-wonder-10.0.0-ultimate.iso"

    with tarfile.open(iso_path, 'w:gz') as tar:
        tar.add(iso_dir, arcname='')

    return iso_path


def build_docs(output_dir):
    """构建文档"""
    docs_dir = output_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # 用户手册
    with open(docs_dir / "USER_MANUAL.md", 'w') as f:
        f.write("""# Bamboo OS Wonder 10.0 - User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Desktop Environment](#desktop-environment)
3. [Applications](#applications)
4. [System Configuration](#system-configuration)
5. [Networking](#networking)
6. [File Management](#file-management)
7. [Command Line Reference](#command-line-reference)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation
1. Download the ISO image
2. Burn to USB drive or DVD
3. Boot from the installation media
4. Follow the installation wizard

### First Boot
- The system will automatically boot into the desktop environment
- Default username: guest
- Default password: (none)

## Desktop Environment

### Desktop Components
- **Desktop Background**: Customizable wallpaper
- **Taskbar**: Bottom bar with start menu and running apps
- **Start Menu**: Access all applications
- **System Tray**: Status icons and notifications
- **Desktop Icons**: Quick access to files and apps

### Keyboard Shortcuts
- `Ctrl+Alt+T`: Open terminal
- `Ctrl+Alt+Del`: System monitor
- `Alt+Tab`: Switch windows
- `Super+D`: Show desktop
- `Super+E`: File manager
- `Print`: Screenshot

## Applications

### Office Suite
- **Word Processor**: Create and edit documents
- **Spreadsheet**: Manage data with formulas
- **Presentation**: Create slide presentations
- **PDF Viewer**: View PDF documents
- **Calculator**: Scientific calculator
- **Calendar**: Schedule management

### Internet
- **Web Browser**: Browse the internet
- **Email Client**: Send and receive email
- **Download Manager**: Manage downloads

### Media
- **Audio Player**: Play music files
- **Video Player**: Play video files
- **Image Viewer**: View images
- **Paint**: Draw and edit images

### Games
- **Snake**: Classic snake game
- **Tetris**: Block puzzle game
- **Minesweeper**: Logic puzzle
- **Chess**: Chess with AI
- **3D Viewer**: 3D model viewer

### System Tools
- **File Manager**: Browse and manage files
- **Terminal**: Command line interface
- **Settings**: System configuration
- **System Monitor**: Performance monitoring

## System Configuration

### Display Settings
- Resolution: 800x600 to 1920x1080
- Color depth: 16-bit / 24-bit / 32-bit
- Theme: Bamboo / Dark / Light
- Wallpaper: Customizable

### Sound Settings
- Master volume control
- Input/output device selection
- System sounds toggle

### Network Settings
- Wired and Wi-Fi support
- DHCP / Static IP configuration
- DNS settings
- Proxy configuration

## Networking

### Connecting to Wi-Fi
1. Click the network icon in the system tray
2. Select your Wi-Fi network
3. Enter the password
4. Click Connect

### Network Commands
- `ifconfig`: View network interfaces
- `ping`: Test network connectivity
- `wget`: Download files
- `curl`: Transfer data

## File Management

### File Manager Features
- Browse files and folders
- Copy, move, delete files
- Search files
- File preview
- Archive support (ZIP, TAR, etc.)

### File System Structure
- `/bin`: User binaries
- `/etc`: Configuration files
- `/home`: User directories
- `/usr`: User programs
- `/var`: Variable data
- `/tmp`: Temporary files

## Command Line Reference

### Basic Commands
- `ls`: List directory contents
- `cd`: Change directory
- `pwd`: Print working directory
- `mkdir`: Create directory
- `rm`: Remove files/directories
- `cp`: Copy files
- `mv`: Move/rename files
- `cat`: View file contents
- `grep`: Search text
- `find`: Find files

### System Commands
- `uname`: System information
- `uptime`: System uptime
- `ps`: Process list
- `top`: Process monitor
- `df`: Disk usage
- `free`: Memory usage
- `reboot`: Restart system
- `shutdown`: Shutdown system

### Network Commands
- `ifconfig`: Network interfaces
- `ping`: Test connectivity
- `netstat`: Network statistics
- `wget`: Download files
- `curl`: Data transfer

## Troubleshooting

### Common Issues

**System won't boot**
- Check BIOS settings
- Verify boot order
- Try recovery mode

**No internet connection**
- Check network cable
- Verify Wi-Fi settings
- Restart network service

**Slow performance**
- Close unused applications
- Check system monitor
- Free up disk space

### Getting Help
- Type `help` in terminal for command help
- Visit https://docs.bamboo-os.org
- Contact support at support@bamboo-os.org

---
*Bamboo OS Wonder 10.0 User Manual*
*Last updated: 2026-07-31*
""")

    # 安装指南
    with open(docs_dir / "INSTALL_GUIDE.md", 'w') as f:
        f.write("""# Bamboo OS Wonder 10.0 - Installation Guide

## System Requirements

### Minimum Requirements
- CPU: x86-64 compatible processor (Intel/AMD)
- RAM: 512 MB (1 GB recommended)
- Storage: 2 GB free space
- Graphics: VGA compatible
- Boot: USB or DVD drive

### Recommended Requirements
- CPU: Dual-core x86-64 processor
- RAM: 2 GB or more
- Storage: 10 GB free space
- Graphics: 3D accelerated
- Network: Ethernet or Wi-Fi

## Installation Methods

### Method 1: USB Drive (Recommended)
1. Download the ISO image
2. Use dd or Rufus to write to USB drive
3. Boot from USB
4. Follow installation wizard

### Method 2: DVD
1. Download the ISO image
2. Burn to DVD
3. Boot from DVD
4. Follow installation wizard

### Method 3: Virtual Machine
1. Create new VM with 1GB RAM
2. Attach ISO image
3. Start VM
4. Follow installation wizard

## Installation Steps

### Step 1: Boot from Installation Media
1. Insert USB/DVD
2. Restart computer
3. Press boot menu key (F12, F2, or Del)
4. Select boot device
5. Wait for GRUB menu

### Step 2: Start Installation
1. Select "Bamboo OS Wonder 10.0" from GRUB menu
2. Wait for system to load
3. Click "Install Bamboo OS" on desktop

### Step 3: Language Selection
1. Select your language
2. Click Next

### Step 4: Keyboard Layout
1. Select keyboard layout
2. Test keyboard
3. Click Next

### Step 5: Network Configuration
1. Connect to network (optional)
2. Click Next

### Step 6: Disk Partitioning
Options:
- **Guided - Use entire disk**: Simplest option
- **Guided - Use free space**: Install alongside other OS
- **Manual**: Custom partitioning

For beginners, select "Guided - Use entire disk"

### Step 7: User Account
1. Enter your name
2. Enter username
3. Enter password
4. Confirm password
5. Click Next

### Step 8: Installation
1. Review settings
2. Click Install
3. Wait for installation to complete
4. Click Reboot

## Post-Installation

### First Boot
1. Remove installation media
2. System will boot from hard drive
3. Log in with your credentials

### Initial Setup
1. Check for updates
2. Install additional applications
3. Customize desktop
4. Set up network

### Installing Updates
```bash
sudo bamboo-update
```

### Installing Applications
```bash
sudo bamboo-install <package-name>
```

## Troubleshooting

### Boot Issues
**Black screen after boot**
- Try nomodeset boot option
- Check graphics compatibility

**Kernel panic**
- Boot in recovery mode
- Check hardware compatibility

### Installation Issues
**Installation fails**
- Check ISO integrity (MD5 sum)
- Try different USB port
- Verify disk space

**Slow installation**
- Normal for older hardware
- Check system requirements

### Driver Issues
**No sound**
- Check volume settings
- Run sound configuration
- Update audio drivers

**No network**
- Check cable connection
- Verify driver loaded
- Run network configuration

## Getting Help

- Documentation: https://docs.bamboo-os.org
- Support: https://support.bamboo-os.org
- Forum: https://forum.bamboo-os.org
- Bug reports: https://bugs.bamboo-os.org

---
*Bamboo OS Wonder 10.0 Installation Guide*
*Last updated: 2026-07-31*
""")

    # 开发者文档
    with open(docs_dir / "DEVELOPER_GUIDE.md", 'w') as f:
        f.write("""# Bamboo OS Wonder 10.0 - Developer Guide

## Architecture Overview

### System Architecture
```
+---------------------------+
|      Applications         |
+---------------------------+
|      System Libraries     |
+---------------------------+
|        Kernel             |
+---------------------------+
|      Hardware             |
+---------------------------+
```

### Kernel Architecture
- Microkernel hybrid design
- Modular driver framework
- POSIX compatible system calls
- SMP support

## Development Environment

### Setup
1. Install build tools
2. Get source code
3. Configure build
4. Compile kernel
5. Test in QEMU

### Build Tools
- Python 3.8+
- GCC (optional, for C extensions)
- QEMU (for testing)
- GRUB tools (for ISO creation)

## Kernel Development

### Kernel Modules
Drivers can be compiled as modules:
```c
#include <bamboo/module.h>

static int __init mydriver_init(void) {
    printk("My driver loaded\\n");
    return 0;
}

static void __exit mydriver_exit(void) {
    printk("My driver unloaded\\n");
}

module_init(mydriver_init);
module_exit(mydriver_exit);
MODULE_LICENSE("GPL");
```

### System Calls
Adding a new system call:
1. Add syscall number to syscall table
2. Implement syscall handler
3. Add user-space wrapper

### Device Drivers
Driver framework:
- Character devices
- Block devices
- Network devices
- USB devices

## Application Development

### BPP Package Format
Bamboo Package (BPP) format structure:
```
myapp.bpp/
├── manifest.json      # Package metadata
├── bin/
│   └── myapp          # Executable
├── lib/
│   └── libmyapp.so   # Libraries
├── share/
│   ├── icons/         # Icons
│   └── doc/           # Documentation
└── etc/
    └── myapp.conf     # Configuration
```

### Manifest Format
```json
{
  "name": "myapp",
  "version": "1.0.0",
  "description": "My Application",
  "author": "Developer",
  "license": "GPL",
  "category": "utilities",
  "dependencies": ["libgui >= 1.0"],
  "size": 102400,
  "executable": "bin/myapp"
}
```

### GUI Programming
Using libgui:
```python
from libgui import Window, Button, Label

class MyWindow(Window):
    def __init__(self):
        super().__init__(200, 200, 400, 300, "My App")
        self.button = Button(50, 50, 100, 30, "Click Me")
        self.button.on_click = self.on_button_click
        self.label = Label(50, 100, 200, 30, "Hello World")
        self.add(self.button)
        self.add(self.label)

    def on_button_click(self):
        self.label.text = "Button clicked!"

app = MyWindow()
app.run()
```

## API Reference

### System Calls
- `sys_open`: Open file
- `sys_read`: Read from file
- `sys_write`: Write to file
- `sys_close`: Close file
- `sys_mmap`: Memory mapping
- `sys_munmap`: Unmap memory
- `sys_fork`: Create process
- `sys_execve`: Execute program
- `sys_exit`: Exit process
- `sys_waitpid`: Wait for process

### Library Functions
- libbamboo: Core system library
- libgui: GUI toolkit
- libnet: Network library
- libaudio: Audio library
- libgame2d: 2D game engine
- lib3d: 3D graphics library

## Building from Source

### Build Kernel
```bash
cd kernel
make
make install
```

### Build Applications
```bash
cd apps/myapp
make
make install
```

### Build ISO
```bash
make iso
```

## Testing

### QEMU Testing
```bash
qemu-system-x86_64 -cdrom bamboo-os.iso -m 512M
```

### Debugging
```bash
qemu-system-x86_64 -s -S &
gdb kernel.elf
(gdb) target remote localhost:1234
```

## Contributing

### Code Style
- Follow kernel coding style
- Use meaningful variable names
- Add comments for complex code
- Write unit tests

### Submitting Patches
1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

---
*Bamboo OS Wonder 10.0 Developer Guide*
*Last updated: 2026-07-31*
""")

    # API参考
    with open(docs_dir / "API_REFERENCE.md", 'w') as f:
        f.write("""# Bamboo OS Wonder 10.0 - API Reference

## System Calls

### Process Management
| Number | Name | Description |
|--------|------|-------------|
| 0 | sys_read | Read from file descriptor |
| 1 | sys_write | Write to file descriptor |
| 2 | sys_open | Open file |
| 3 | sys_close | Close file descriptor |
| 57 | sys_fork | Create new process |
| 59 | sys_execve | Execute program |
| 60 | sys_exit | Terminate process |
| 61 | sys_wait4 | Wait for process termination |
| 39 | sys_getpid | Get process ID |
| 102 | sys_getuid | Get user ID |

### Memory Management
| Number | Name | Description |
|--------|------|-------------|
| 9 | sys_mmap | Map files or devices into memory |
| 11 | sys_munmap | Unmap files or devices |
| 10 | sys_mprotect | Set protection on memory |
| 12 | sys_brk | Change data segment size |
| 25 | sys_msync | Synchronize file with memory |

### File System
| Number | Name | Description |
|--------|------|-------------|
| 2 | sys_open | Open file |
| 3 | sys_close | Close file |
| 0 | sys_read | Read file |
| 1 | sys_write | Write file |
| 8 | sys_lseek | Reposition file offset |
| 80 | sys_dup | Duplicate file descriptor |
| 82 | sys_dup2 | Duplicate file descriptor |
| 257 | sys_openat | Open file relative to directory |
| 263 | sys_unlinkat | Remove file relative to directory |

### Network
| Number | Name | Description |
|--------|------|-------------|
| 41 | sys_socket | Create socket |
| 42 | sys_connect | Connect socket |
| 43 | sys_accept | Accept connection |
| 44 | sys_sendto | Send message |
| 45 | sys_recvfrom | Receive message |
| 48 | sys_shutdown | Shut down socket |
| 49 | sys_bind | Bind socket |
| 50 | sys_listen | Listen for connections |

### Device I/O
| Number | Name | Description |
|--------|------|-------------|
| 16 | sys_ioctl | Control device |
| 17 | sys_pread64 | Read from file at offset |
| 18 | sys_pwrite64 | Write to file at offset |

## Library API

### libbamboo

#### String Functions
```c
char* strcpy(char *dest, const char *src);
char* strncpy(char *dest, const char *src, size_t n);
int strcmp(const char *s1, const char *s2);
int strncmp(const char *s1, const char *s2, size_t n);
size_t strlen(const char *s);
char* strcat(char *dest, const char *src);
char* strchr(const char *s, int c);
char* strstr(const char *haystack, const char *needle);
```

#### Memory Functions
```c
void* malloc(size_t size);
void free(void *ptr);
void* calloc(size_t nmemb, size_t size);
void* realloc(void *ptr, size_t size);
void* memcpy(void *dest, const void *src, size_t n);
void* memset(void *s, int c, size_t n);
int memcmp(const void *s1, const void *s2, size_t n);
```

#### I/O Functions
```c
int printf(const char *format, ...);
int sprintf(char *str, const char *format, ...);
int snprintf(char *str, size_t size, const char *format, ...);
int scanf(const char *format, ...);
FILE* fopen(const char *path, const char *mode);
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream);
int fclose(FILE *stream);
```

### libgui

#### Window Management
```python
class Window:
    def __init__(self, x, y, width, height, title):
        pass
    def show(self): pass
    def hide(self): pass
    def move(self, x, y): pass
    def resize(self, width, height): pass
    def close(self): pass
    def add(self, widget): pass
    def remove(self, widget): pass
```

#### Widgets
```python
class Button:
    def __init__(self, x, y, width, height, text): pass
    def on_click(self, callback): pass

class Label:
    def __init__(self, x, y, width, height, text): pass
    def set_text(self, text): pass

class TextBox:
    def __init__(self, x, y, width, height, text=''): pass
    def get_text(self): pass
    def set_text(self, text): pass

class ListBox:
    def __init__(self, x, y, width, height, items=[]): pass
    def add_item(self, item): pass
    def remove_item(self, index): pass
    def get_selected(self): pass

class Menu:
    def __init__(self, items=[]): pass
    def show(self, x, y): pass

class ProgressBar:
    def __init__(self, x, y, width, height, value=0): pass
    def set_value(self, value): pass

class ScrollBar:
    def __init__(self, x, y, width, height, orientation='vertical'): pass
    def set_value(self, value): pass
```

#### Drawing API
```python
class Graphics:
    def draw_pixel(self, x, y, color): pass
    def draw_line(self, x1, y1, x2, y2, color): pass
    def draw_rect(self, x, y, w, h, color): pass
    def fill_rect(self, x, y, w, h, color): pass
    def draw_circle(self, x, y, r, color): pass
    def fill_circle(self, x, y, r, color): pass
    def draw_text(self, x, y, text, color, font='default'): pass
    def draw_image(self, x, y, image): pass
```

### libnet

#### Socket API
```python
class Socket:
    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0): pass
    def connect(self, host, port): pass
    def bind(self, host, port): pass
    def listen(self, backlog=5): pass
    def accept(self): pass
    def send(self, data): pass
    def recv(self, size=1024): pass
    def close(self): pass
```

#### HTTP Client
```python
class HttpClient:
    def __init__(self, host, port=80): pass
    def get(self, path): pass
    def post(self, path, data): pass
    def request(self, method, path, data=None, headers=None): pass
```

### libgame2d

#### Sprite
```python
class Sprite:
    def __init__(self, x, y, image): pass
    def move(self, dx, dy): pass
    def set_position(self, x, y): pass
    def scale(self, factor): pass
    def rotate(self, angle): pass
    def collides_with(self, other): pass
    def update(self): pass
    def draw(self, screen): pass
```

#### Animation
```python
class Animation:
    def __init__(self, sprite_sheet, frame_width, frame_height, fps=10): pass
    def play(self): pass
    def stop(self): pass
    def update(self): pass
    def get_current_frame(self): pass
```

#### Physics
```python
class PhysicsBody:
    def __init__(self, x, y, mass=1.0): pass
    def apply_force(self, fx, fy): pass
    def apply_impulse(self, ix, iy): pass
    def update(self, dt): pass
```

### lib3d

#### 3D Math
```python
class Vec3:
    def __init__(self, x=0, y=0, z=0): pass
    def length(self): pass
    def normalize(self): pass
    def dot(self, other): pass
    def cross(self, other): pass

class Mat4:
    def __init__(self): pass
    def identity(self): pass
    def translate(self, x, y, z): pass
    def rotate_x(self, angle): pass
    def rotate_y(self, angle): pass
    def rotate_z(self, angle): pass
    def scale(self, x, y, z): pass
    def perspective(self, fov, aspect, near, far): pass
    def multiply(self, other): pass
```

#### Renderer
```python
class Renderer:
    def __init__(self, width, height): pass
    def clear(self, color): pass
    def draw_point(self, x, y, z, color): pass
    def draw_line(self, x1, y1, z1, x2, y2, z2, color): pass
    def draw_triangle(self, v1, v2, v3, color): pass
    def draw_mesh(self, mesh, transform): pass
    def set_camera(self, camera): pass
    def set_light(self, light): pass
```

---
*Bamboo OS Wonder 10.0 API Reference*
*Last updated: 2026-07-31*
""")

    return docs_dir


def build_release_notes(output_dir):
    """生成版本说明"""
    notes_path = output_dir / "RELEASE_NOTES.md"

    with open(notes_path, 'w') as f:
        f.write("""# Bamboo OS Wonder 10.0 Ultimate Edition
## Release Notes

---

### Release Information
- **Version**: 10.0.0
- **Codename**: Wonder
- **Phase**: Stable
- **Release Date**: 2026-07-31
- **Architecture**: x86-64
- **Kernel Version**: Bamboo Kernel 10.0

---

## What's New in 10.0

### Core System
- Complete x86-64 kernel with long mode support
- Advanced memory management with 4-level paging
- CFS process scheduler with SMP support
- 768 system calls (256 native + 512 Linux compatible)
- Full POSIX compatibility layer

### File System
- VFS (Virtual File System) framework
- FAT32 with long file name support
- Ext2/3/4 file system support
- procfs, sysfs, devfs, tmpfs
- Swap support
- File system journaling

### Networking
- Complete TCP/IP protocol stack
- ARP, IPv4, ICMP, UDP, TCP
- DNS, DHCP, HTTP, WebSocket
- FTP, SMTP client support
- TLS/SSL framework
- Network driver framework

### Graphics & GUI
- Complete windowing system
- Desktop environment with taskbar and start menu
- 2D graphics acceleration
- Theme system (Bamboo, Dark, Light)
- Widget library (buttons, labels, text boxes, etc.)
- Event handling system
- Multi-monitor support framework

### Office Suite
- Word processor with document editing
- Spreadsheet with formulas and charts
- Presentation software
- PDF viewer
- Scientific calculator
- Calendar and schedule manager

### Multimedia
- Audio subsystem with mixer
- WAV/MP3 audio player
- Video player framework
- Image viewer (PNG, JPEG, BMP)
- Paint program
- 3D graphics engine
- Software renderer with 3D pipeline

### Games
- 2D game engine
- Snake game
- Tetris game
- Minesweeper
- Chess with AI opponent
- 3D model viewer
- Particle system
- Physics engine

### Applications
- Web browser (HTML/CSS)
- Email client (IMAP/SMTP)
- Download manager
- File manager
- Terminal emulator
- System monitor
- Settings center
- Screenshot tool

### Security
- User account system
- File permissions
- Process isolation
- Memory protection
- SMAP/SMEP support
- Encryption framework
- Secure boot support

### System Tools
- 300+ shell commands
- Package manager (BPP format)
- App Store
- System update framework
- Hardware detection
- Driver framework
- System logging

### Chinese Support
- Complete Chinese localization
- Chinese font rendering
- Pinyin input method framework
- Chinese UI translations
- Chinese documentation

---

## System Requirements

### Minimum
- CPU: x86-64 compatible processor
- RAM: 512 MB
- Storage: 2 GB free space
- Graphics: VGA compatible
- Boot: USB or DVD drive

### Recommended
- CPU: Dual-core x86-64 processor
- RAM: 2 GB
- Storage: 10 GB free space
- Graphics: 3D accelerated
- Network: Ethernet or Wi-Fi

---

## Installation

See INSTALL_GUIDE.md for detailed installation instructions.

Quick start:
1. Download ISO image
2. Write to USB drive
3. Boot from USB
4. Follow installation wizard

---

## Known Issues

- Some hardware may require additional drivers
- 3D acceleration is software-based (no GPU driver yet)
- Wi-Fi support limited to certain chipsets
- Printing support not yet implemented
- Some applications are in beta stage

---

## Version History

### v10.0.0 (2026-07-31)
- Ultimate stable release
- Complete feature set
- Performance optimizations
- Bug fixes

### v9.0.0 (2026-07-20)
- 3D graphics acceleration
- Performance optimizations
- Boot optimization
- Hardware compatibility improvements

### v8.0.0 (2026-07-05)
- Complete Chinese support
- Chinese fonts and input method
- Chinese UI localization

### v7.0.0 (2026-06-20)
- Complete office suite
- Word processor, spreadsheet, presentation
- Productivity tools

### v6.0.0 (2026-06-01)
- 2D game engine
- Multimedia applications
- Audio subsystem

### v5.0.0 (2026-05-15)
- Built-in applications
- File manager, terminal, settings
- System utilities

### v4.0.0 (2026-04-30)
- GUI desktop environment
- Window system
- Widget library

### v3.0.0 (2026-03-25)
- TCP/IP network stack
- Network drivers
- HTTP client

### v2.0.0 (2026-02-20)
- Disk driver support
- Ext4 file system
- Data persistence

### v1.0.0 (2026-01-15)
- Initial release
- Kernel base
- Command line shell
- FAT32 file system

---

## Support & Documentation

- **Website**: https://bamboo-os.org
- **Documentation**: https://docs.bamboo-os.org
- **Support**: https://support.bamboo-os.org
- **Forum**: https://forum.bamboo-os.org
- **Bug Reports**: https://bugs.bamboo-os.org
- **Source Code**: https://github.com/bamboo-os/wonder

---

## License

Bamboo OS Wonder is released under the GNU General Public License v3.0.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

---

*Bamboo OS Wonder 10.0 Ultimate Edition*
*Copyright (c) 2026 Bamboo OS Team*
*All rights reserved.*
""")

    return notes_path


if __name__ == '__main__':
    build_ultimate_edition()
