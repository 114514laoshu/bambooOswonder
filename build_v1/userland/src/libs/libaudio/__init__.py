# ============================================================================
# Module: userland/libs/libaudio/__init__.py
# 模块：userland/libs/libaudio/__init__.py
# Description: Audio library package
# 描述：音频库包
# ============================================================================

from userland.libs.libaudio.audio import AudioPlayer, AudioRecorder, AudioDevice

__all__ = [
    'AudioPlayer',
    'AudioRecorder',
    'AudioDevice',
]

__version__ = "1.0.0"