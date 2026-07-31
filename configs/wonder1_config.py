# ============================================================================
# Module: configs/wonder1_config.py
# 模块：configs/wonder1_config.py
# Description: Bamboo OS Wonder 1.0 Configuration
# 描述：Bamboo OS Wonder 1.0 配置文件
# ============================================================================

# ============================================================================
# Version Information / 版本信息
# ============================================================================
VERSION = "1.0.0"
RELEASE = "2026.07"
TARGET_NAME = "Bamboo OS Wonder 1.0"

# ============================================================================
# Kernel Configuration / 内核配置
# ============================================================================
KERNEL_CONFIG = {
    "name": "Bamboo OS Wonder 1.0",
    "arch": "x86_64",
    "multiboot": 2,                     # Multiboot2
    "direct_boot": False,               # GRUB2 only
    "kernel_base": 0x100000,
    "stack_size": 0x10000,
    "heap_size": 0x4000000,             # 64MB
    "max_processes": 128,
    "max_files": 256,
    "ticks_per_second": 100,
}

# ============================================================================
# Memory Configuration / 内存配置
# ============================================================================
MEMORY_CONFIG = {
    "total_mb": 512,
    "kernel_mb": 64,
    "user_mb": 448,
    "swap_mb": 128,
}

# ============================================================================
# Filesystem Configuration / 文件系统配置
# ============================================================================
FS_CONFIG = {
    "root_fs": "fat32",
    "supported_fs": ["fat32", "ext2", "ext4", "ntfs", "iso9660"],
    "fat32_sectors_per_cluster": 8,
    "enable_lfn": True,
    "disk_image": "disk.img",
    "disk_size_mb": 256,
}

# ============================================================================
# Network Configuration / 网络配置
# ============================================================================
NET_CONFIG = {
    "enabled": True,
    "driver": "rtl8139",
    "ip": "10.0.2.15",
    "netmask": "255.255.255.0",
    "gateway": "10.0.2.2",
    "dns": ["8.8.8.8", "1.1.1.1"],
    "enable_dhcp": True,
}

# ============================================================================
# GUI Configuration / 图形界面配置
# ============================================================================
GUI_CONFIG = {
    "enabled": True,
    "width": 1024,
    "height": 768,
    "bpp": 32,
    "theme": "bamboo",
    "font": "terminus",
    "desktop_icons": True,
    "taskbar": True,
    "start_menu": True,
    "animation": True,
    "transparency": True,
}

# ============================================================================
# Application Configuration / 应用配置
# ============================================================================
APPS_CONFIG = {
    "include": [
        "Shell", "Terminal", "FileManager", "Settings",
        "WordProcessor", "Spreadsheet", "Presentation", "PDFViewer",
        "Browser", "Email", "Downloader",
        "AudioPlayer", "VideoPlayer", "ImageViewer",
        "Calculator", "Paint", "Calendar", "SystemMonitor",
    ],
    "games_2d": [
        "Snake", "Tetris", "Platformer", "Chess", "Minesweeper"
    ],
    "games_3d": [
        "Doom", "Racer", "Blocks"
    ],
    "preinstall": True,
}

# ============================================================================
# Game Engine Configuration / 游戏引擎配置
# ============================================================================
GAME_CONFIG = {
    "enable_2d": True,
    "enable_3d": True,
    "physics": True,
    "particles": True,
    "max_sprites": 1024,
    "max_particles": 10000,
}

# ============================================================================
# Boot Configuration / 启动配置
# ============================================================================
BOOT_CONFIG = {
    "timeout": 3,
    "default": "bamboo-os",
    "menu_entries": [
        {"title": "Bamboo OS Wonder 1.0", "kernel": "wonder1.elf", "args": ""},
        {"title": "Wonder 1.0 (Safe Mode)", "kernel": "wonder1.elf", "args": "safemode"},
        {"title": "Memory Test", "kernel": "wonder1.elf", "args": "memtest"},
    ]
}

# ============================================================================
# Output Configuration / 输出配置
# ============================================================================
OUTPUT_CONFIG = {
    "elf": "wonder1.elf",
    "iso": "bamboo-wonder1.iso",
    "initrd": "initrd.tar",
    "disk_image": "disk.img",
    "output_dir": "build/wonder1/",
}
