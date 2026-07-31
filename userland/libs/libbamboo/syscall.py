# ============================================================================
# Module: userland/libs/libbamboo/syscall.py
# 模块：userland/libs/libbamboo/syscall.py
# Description: System call wrapper
# 描述：系统调用包装器
# ============================================================================

"""
System call interface for Bamboo OS.
Bamboo OS 系统调用接口。

This module provides the low-level syscall invocation mechanism.
该模块提供底层的系统调用调用机制。
"""

import ctypes
import ctypes.util


class Syscall:
    """
    System call wrapper.
    系统调用包装器。

    Provides methods for invoking system calls using the appropriate
    mechanism for the current platform.
    提供使用当前平台适当机制调用系统调用的方法。
    """

    # Library for syscall / 用于系统调用的库
    _libc = None

    @classmethod
    def _get_libc(cls):
        """Get libc library for syscall / 获取用于系统调用的 libc 库"""
        if cls._libc is None:
            libc_name = ctypes.util.find_library("c")
            if libc_name:
                cls._libc = ctypes.CDLL(libc_name, use_errno=True)
            else:
                # Fallback: try common names / 备用：尝试常见名称
                for name in ["libc.so.6", "libc.so", "libc.dylib"]:
                    try:
                        cls._libc = ctypes.CDLL(name, use_errno=True)
                        break
                    except OSError:
                        continue
        return cls._libc

    @classmethod
    def invoke(cls, number: int, *args) -> int:
        """
        Invoke a system call.
        调用系统调用。

        Args:
            参数：
            number (int): System call number / 系统调用号
            *args: Arguments / 参数

        Returns:
            返回：
            int: Return value / 返回值
        """
        # In a real Bamboo OS environment, this would use inline assembly
        # or the syscall instruction directly.
        # 在真实的 Bamboo OS 环境中，这将是内联汇编或直接使用 syscall 指令。

        # For development/testing, use libc syscall / 开发/测试阶段，使用 libc 系统调用
        libc = cls._get_libc()
        if libc:
            try:
                # Use syscall function / 使用 syscall 函数
                result = libc.syscall(number, *args)
                return result
            except AttributeError:
                pass

        # Fallback: simulate with print (for testing only) / 备用：模拟打印（仅用于测试）
        print(f"[SYSCALL] syscall({number}, {', '.join(str(a) for a in args)})")
        return 0