# ============================================================================
# Module: userland/pro_config.py
# 模块：userland/pro_config.py
# Description: Phase Pro configuration
# 描述：专业版配置
# ============================================================================

"""
Phase Pro configuration module.
专业版配置模块。

Controls professional features including office suite, 3D acceleration,
app store, and system drivers.
控制办公套件、3D加速、应用市场和系统驱动等专业功能。
"""

from typing import Dict, List, Any

PRO_CONFIG: Dict[str, Any] = {

    # ========================================================================
    # Office Suite / 办公套件
    # ========================================================================
    'office': {
        'enabled': True,
        'word_processor': True,       # 文字处理器
        'spreadsheet': True,           # 电子表格
        'presentation': True,          # 演示文稿
        'pdf_viewer': True,            # PDF 查看器
        'note_taker': True,            # 笔记应用
        'calendar': True,              # 日历
        'contacts': True,              # 联系人
    },

    # ========================================================================
    # 3D Graphics Acceleration / 3D 图形加速
    # ========================================================================
    'graphics': {
        'enabled': True,
        'opengl_compat': True,         # OpenGL 兼容层
        'software_renderer': True,     # 软件渲染器
        'hardware_accel': False,       # 硬件加速 (需驱动)
        'shader_support': True,        # 着色器支持
        'texture_mapping': True,       # 纹理映射
        'lighting': True,              # 光照
        'z_buffer': True,              # Z 缓冲
    },

    # ========================================================================
    # App Store / 应用市场
    # ========================================================================
    'app_store': {
        'enabled': True,
        'repository_url': 'https://apps.bamboo-os.org/repo',
        'local_cache': '/var/cache/bamboo/apps',
        'categories': [
            'system', 'office', 'graphics', 'network',
            'games', 'development', 'multimedia', 'utilities'
        ],
        'auto_update': True,
    },

    # ========================================================================
    # Userland Software / 用户态软件
    # ========================================================================
    'userland': {
        'enabled': True,
        'file_manager': True,          # 文件管理器
        'system_monitor': True,        # 系统监视器
        'settings': True,              # 设置中心
        'terminal': True,              # 终端
        'calculator': True,            # 计算器
        'notepad': True,               # 记事本
        'paint': True,                 # 画图
        'archive_manager': True,       # 压缩管理器
    },

    # ========================================================================
    # System Drivers / 系统驱动
    # ========================================================================
    'drivers': {
        'enabled': True,
        'usb': True,                   # USB 驱动
        'audio': True,                 # 音频驱动
        'network': True,               # 网络驱动
        'graphics': True,              # 显卡驱动
        'storage': True,               # 存储驱动
        'input': True,                 # 输入设备驱动
    },

    # ========================================================================
    # Build options / 构建选项
    # ========================================================================
    'build': {
        'apply_patches': True,
        'generate_manifest': True,
        'verbose': False,
        'install_deps': True,
    },
}


def get_pro_config(section: str = None) -> Dict[str, Any]:
    """Get Phase Pro configuration / 获取专业版配置"""
    if section is None:
        return PRO_CONFIG
    return PRO_CONFIG.get(section, {})


def is_feature_enabled(section: str, feature: str) -> bool:
    """Check if a feature is enabled / 检查功能是否启用"""
    config = get_pro_config(section)
    return config.get(feature, False)