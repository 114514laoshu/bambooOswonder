# ============================================================================
# Module: userland/p3plus_config.py
# 模块：userland/p3plus_config.py
# Description: P3+ configuration for optional features
# 描述：P3+ 可选功能配置
# ============================================================================

"""
P3+ configuration module.
P3+ 配置模块。

Controls which patches and extensions are enabled at build time.
控制在构建时启用哪些补丁和扩展。
"""

from typing import Dict, List, Any


# P3+ Configuration / P3+ 配置
P3PLUS_CONFIG: Dict[str, Any] = {

    # ========================================================================
    # Game Engine Patches / 游戏引擎补丁
    # ========================================================================
    'game_engine': {
        'enabled': True,
        'patch_level': 1,

        # 2D Engine enhancements / 2D 引擎增强
        'sprite': {
            'batch_rendering': True,      # 批处理渲染
            'layers': True,               # 分层渲染
            'camera': True,               # 摄像机系统
            'tilemap': True,              # 瓦片地图
        },
        'physics': {
            'advanced_collision': True,   # 高级碰撞检测
            'gravity': True,              # 重力系统
            'friction': True,             # 摩擦力
            'damping': True,              # 阻尼
            'impulse': True,              # 冲量
        },
        'particle': {
            'color_over_life': True,      # 生命周期颜色
            'size_over_life': True,       # 生命周期大小
            'gravity_well': True,         # 引力井
            'turbulence': True,           # 湍流
        },
        'audio': {
            'positional_audio': True,     # 位置音频
            'sound_effects': True,        # 音效
            'music_player': True,         # 音乐播放器
        },
    },

    # ========================================================================
    # GUI Enhancements / GUI 增强
    # ========================================================================
    'gui': {
        'enabled': True,
        'patch_level': 1,

        'widgets': {
            'progress_bar': True,         # 进度条
            'slider': True,               # 滑块
            'toggle': True,               # 开关
            'tabbed_pane': True,          # 标签面板
            'tree_view': True,            # 树形视图
            'table_view': True,           # 表格视图
        },
        'effects': {
            'transparency': True,         # 透明度
            'shadow': True,               # 阴影
            'gradient': True,             # 渐变
            'rounded_corners': True,      # 圆角
            'animation': True,            # 动画效果
        },
        'layout': {
            'grid_layout': True,          # 网格布局
            'flow_layout': True,          # 流式布局
            'dock_layout': True,          # 停靠布局
        },
    },

    # ========================================================================
    # Network Stack Enhancements / 网络栈增强
    # ========================================================================
    'network': {
        'enabled': True,
        'patch_level': 1,

        'protocols': {
            'websocket': True,            # WebSocket 支持
            'tls': True,                  # TLS 加密
            'ftp': True,                  # FTP 客户端
            'smtp': True,                 # SMTP 客户端
        },
        'security': {
            'certificate_validation': True,  # 证书验证
            'hostname_verification': True,   # 主机名验证
        },
    },

    # ========================================================================
    # Multimedia Enhancements / 多媒体增强
    # ========================================================================
    'multimedia': {
        'enabled': True,
        'patch_level': 1,

        'codecs': {
            'mp3_decoder': True,          # MP3 解码
            'ogg_decoder': True,          # OGG 解码
            'png_decoder': True,          # PNG 解码
            'jpeg_decoder': True,         # JPEG 解码
        },
        'video': {
            'frame_processor': True,      # 帧处理
            'timeline': True,             # 时间线
        },
    },

    # ========================================================================
    # Game Applications / 游戏应用
    # ========================================================================
    'games': {
        'enabled': True,
        'snake': True,                    # 贪吃蛇
        'tetris': True,                   # 俄罗斯方块
        'minesweeper': True,              # 扫雷
        'platformer': True,               # 平台跳跃
        'chess': True,                    # 国际象棋
    },

    # ========================================================================
    # Build-time options / 构建时选项
    # ========================================================================
    'build': {
        'apply_patches': True,
        'generate_manifest': True,
        'verbose': False,
    },
}


def get_p3plus_config(section: str = None) -> Dict[str, Any]:
    """Get P3+ configuration / 获取 P3+ 配置"""
    if section is None:
        return P3PLUS_CONFIG
    return P3PLUS_CONFIG.get(section, {})


def is_feature_enabled(section: str, feature: str) -> bool:
    """Check if a feature is enabled / 检查功能是否启用"""
    config = get_p3plus_config(section)
    return config.get(feature, False)