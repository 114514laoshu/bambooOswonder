# ============================================================================
# Module: userland/p2plus_config.py
# 模块：userland/p2plus_config.py
# Description: P2+ configuration for optional features
# 描述：P2+ 可选功能配置
# ============================================================================

"""
P2+ configuration module.
P2+ 配置模块。

Controls which patches and extensions are enabled at build time.
控制在构建时启用哪些补丁和扩展。
"""

from typing import Dict, List, Any


# P2+ Configuration / P2+ 配置
P2PLUS_CONFIG: Dict[str, Any] = {

    # ========================================================================
    # Shell Patches / Shell 补丁
    # ========================================================================
    'shell': {

        # Enable shell patches / 启用 Shell 补丁
        'enabled': True,

        # Patch level / 补丁级别
        'patch_level': 1,

        # Command patches / 命令补丁
        'commands': {
            'ls': True,      # Enhanced ls / 增强 ls
            'ps': True,      # Enhanced ps / 增强 ps
            'help': True,    # Enhanced help / 增强 help
            'which': True,   # Add which command / 添加 which 命令
            'type': True,    # Add type command / 添加 type 命令
            'pushd': True,   # Add pushd/popd/dirs / 添加 pushd/popd/dirs
            'export': True,  # Enhanced export / 增强 export
            'source': True,  # Enhanced source / 增强 source
            'exec': True,    # Enhanced exec / 增强 exec
            'time': True,    # Add time command / 添加 time 命令
            'uptime': True,  # Enhanced uptime / 增强 uptime
            'uname': True,   # Enhanced uname / 增强 uname
            'printf': True,  # Add printf / 添加 printf
            'test': True,    # Add test command / 添加 test 命令
            'sleep': True,   # Add sleep command / 添加 sleep 命令
        },

        # Extension modules / 扩展模块
        'extensions': {
            'job_control': True,      # Job control (bg/fg/jobs) / 作业控制
            'plugin_system': True,    # Plugin system / 插件系统
            'advanced_completion': True,  # Advanced tab completion / 高级 Tab 补全
            'history_search': True,   # History search (Ctrl+R) / 历史搜索
            'vi_mode': True,          # Vi editing mode / Vi 编辑模式
        },

        # Hook points / 钩子点
        'hooks': {
            'pre_execute': True,
            'post_execute': True,
            'pre_prompt': True,
            'post_prompt': True,
            'pre_history': True,
            'post_history': True,
            'command_not_found': True,
            'shell_start': True,
            'shell_exit': True,
        },
    },

    # ========================================================================
    # libc Patches / libc 补丁
    # ========================================================================
    'libc': {
        'enabled': True,
        'patch_level': 1,

        # Additions / 新增
        'additions': {
            'locale': True,           # Locale support / 区域设置支持
            'wide_char': True,        # Wide character support / 宽字符支持
            'thread_local': True,     # Thread-local storage / 线程本地存储
            'timezone': True,         # Timezone support / 时区支持
        },
    },

    # ========================================================================
    # libbamboo Patches / libbamboo 补丁
    # ========================================================================
    'libbamboo': {
        'enabled': True,
        'patch_level': 1,

        # Additions / 新增
        'additions': {
            'async_io': True,         # Asynchronous I/O / 异步 I/O
            'event_loop': True,       # Event loop / 事件循环
            'signal_handling': True,  # Enhanced signal handling / 增强信号处理
            'futex': True,            # Futex support / Futex 支持
        },
    },

    # ========================================================================
    # Build-time options / 构建时选项
    # ========================================================================
    'build': {
        # Apply patches during build / 构建时应用补丁
        'apply_patches': True,

        # Generate patch manifest / 生成补丁清单
        'generate_manifest': True,

        # Include patch documentation / 包含补丁文档
        'include_docs': True,

        # Verbose output during patching / 补丁时详细输出
        'verbose': False,
    },

    # ========================================================================
    # Runtime options / 运行时选项
    # ========================================================================
    'runtime': {
        # Load extensions at startup / 启动时加载扩展
        'load_extensions': True,

        # Enable plugin auto-discovery / 启用插件自动发现
        'auto_discover_plugins': True,

        # Plugin directories / 插件目录
        'plugin_dirs': [
            '/apps/plugins',
            '/usr/lib/bamboo/plugins',
        ],
    },
}


def get_p2plus_config(section: str = None) -> Dict[str, Any]:
    """
    Get P2+ configuration.
    获取 P2+ 配置。

    Args:
        参数：
        section (str): Configuration section / 配置节

    Returns:
        返回：
        dict: Configuration / 配置
    """
    if section is None:
        return P2PLUS_CONFIG
    return P2PLUS_CONFIG.get(section, {})


def is_feature_enabled(section: str, feature: str) -> bool:
    """
    Check if a feature is enabled.
    检查功能是否启用。

    Args:
        参数：
        section (str): Configuration section / 配置节
        feature (str): Feature name / 功能名

    Returns:
        返回：
        bool: True if enabled / 启用返回 True
    """
    config = get_p2plus_config(section)
    return config.get(feature, False)