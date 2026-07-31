# ============================================================================
# Module: userland/libs/libbamboo/__init__.py
# 模块：userland/libs/libbamboo/__init__.py
# Description: Bamboo OS core library package
# 描述：Bamboo OS 核心库包
# ============================================================================

from userland.libs.libbamboo.bamboo import BambooAPI
from userland.libs.libbamboo.syscall import Syscall
from userland.libs.libbamboo.error import BambooError, ErrorCode

__all__ = [
    'BambooAPI',
    'Syscall',
    'BambooError',
    'ErrorCode',
]

__version__ = "1.0.0"