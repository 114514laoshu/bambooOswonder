# ============================================================================
# Module: configs/education_config.py
# 模块：configs/education_config.py
# Description: Bamboo OS Education Configuration
# 描述：Bamboo OS 教学版配置文件
# ============================================================================

# ============================================================================
# Version Information / 版本信息
# ============================================================================
VERSION = "1.0.0"
RELEASE = "2026.07"
TARGET_NAME = "Bamboo OS Education"

# ============================================================================
# Kernel Configuration / 内核配置
# ============================================================================
KERNEL_CONFIG = {
    "name": "Bamboo OS Education",
    "arch": "x86_64",
    "multiboot": 2,                     # Multiboot2
    "direct_boot": False,               # GRUB2 only
    "kernel_base": 0x100000,
    "stack_size": 0x8000,
    "heap_size": 0x1000000,             # 16MB
    "max_processes": 32,
    "max_files": 64,
    "ticks_per_second": 100,
}

# ============================================================================
# Memory Configuration / 内存配置
# ============================================================================
MEMORY_CONFIG = {
    "total_mb": 128,
    "kernel_mb": 16,
    "user_mb": 112,
    "swap_mb": 0,
}

# ============================================================================
# Filesystem Configuration / 文件系统配置
# ============================================================================
FS_CONFIG = {
    "root_fs": "fat32",
    "supported_fs": ["fat32"],
    "fat32_sectors_per_cluster": 8,
    "enable_lfn": True,
    "disk_image": "disk.img",
    "disk_size_mb": 64,
}

# ============================================================================
# Network Configuration / 网络配置
# ============================================================================
NET_CONFIG = {
    "enabled": False,                    # No network in education version
    "driver": None,
    "ip": "10.0.2.15",
    "netmask": "255.255.255.0",
    "gateway": "10.0.2.2",
    "dns": ["8.8.8.8"],
    "enable_dhcp": False,
}

# ============================================================================
# GUI Configuration / 图形界面配置
# ============================================================================
GUI_CONFIG = {
    "enabled": False,                    # No GUI in education version
    "width": 800,
    "height": 600,
    "bpp": 32,
    "theme": "default",
    "font": "terminus",
    "desktop_icons": False,
    "taskbar": False,
    "start_menu": False,
    "animation": False,
    "transparency": False,
}

# ============================================================================
# Application Configuration / 应用配置
# ============================================================================
APPS_CONFIG = {
    "include": [
        "Shell",
    ],
    "games_2d": [],
    "games_3d": [],
    "preinstall": False,
}

# ============================================================================
# Game Engine Configuration / 游戏引擎配置
# ============================================================================
GAME_CONFIG = {
    "enable_2d": False,
    "enable_3d": False,
    "physics": False,
    "particles": False,
    "max_sprites": 0,
    "max_particles": 0,
}

# ============================================================================
# Boot Configuration / 启动配置
# ============================================================================
BOOT_CONFIG = {
    "timeout": 5,
    "default": "bamboo-os-edu",
    "menu_entries": [
        {"title": "Bamboo OS Education", "kernel": "education.elf", "args": ""},
        {"title": "Education (Debug Mode)", "kernel": "education.elf", "args": "debug"},
    ]
}

# ============================================================================
# Education Specific Configuration / 教学版特定配置
# ============================================================================
EDUCATION_CONFIG = {
    "detailed_comments": True,           # 详细中文注释
    "lab_exercises": True,               # 包含实验练习
    "step_by_step": True,                # 分步讲解
    "api_docs": True,                    # API文档
    "max_syscalls": 50,                  # 限制系统调用数量
}

# ============================================================================
# Output Configuration / 输出配置
# ============================================================================
OUTPUT_CONFIG = {
    "elf": "education.elf",
    "iso": "bamboo-education.iso",
    "initrd": "initrd.tar",
    "disk_image": "disk.img",
    "output_dir": "build/education/",
}
