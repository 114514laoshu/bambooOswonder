# ============================================================================
# Module: userland/libs/libc/stdlib.py
# 模块：userland/libs/libc/stdlib.py
# Description: Standard library functions
# 描述：标准库函数
# ============================================================================

"""
Standard library for Bamboo OS.
Bamboo OS 标准库。

Provides malloc, free, atoi, random, and other stdlib functions.
提供 malloc、free、atoi、随机数和其他 stdlib 函数。
"""

import random as _random
import sys


class stdlib:
    """
    Standard library functions.
    标准库函数。
    """

    # Memory allocation / 内存分配
    @staticmethod
    def malloc(size: int) -> bytearray:
        """
        Allocate memory.
        分配内存。

        Args:
            参数：
            size (int): Size in bytes / 字节大小

        Returns:
            返回：
            bytearray: Allocated memory / 分配的内存
        """
        return bytearray(size)

    @staticmethod
    def free(ptr):
        """
        Free memory.
        释放内存。

        Args:
            参数：
            ptr: Pointer to free / 要释放的指针
        """
        pass

    @staticmethod
    def calloc(count: int, size: int) -> bytearray:
        """
        Allocate zero-initialized memory.
        分配零初始化内存。

        Args:
            参数：
            count (int): Number of elements / 元素数量
            size (int): Element size / 元素大小

        Returns:
            返回：
            bytearray: Allocated memory / 分配的内存
        """
        return bytearray(count * size)

    @staticmethod
    def realloc(ptr, new_size: int) -> bytearray:
        """
        Reallocate memory.
        重新分配内存。

        Args:
            参数：
            ptr: Old pointer / 旧指针
            new_size (int): New size / 新大小

        Returns:
            返回：
            bytearray: Reallocated memory / 重新分配的内存
        """
        if ptr is None:
            return stdlib.malloc(new_size)
        if new_size == 0:
            stdlib.free(ptr)
            return bytearray()
        return bytearray(new_size)

    # String conversion / 字符串转换
    @staticmethod
    def atoi(s: str) -> int:
        """
        Convert string to integer.
        字符串转整数。

        Args:
            参数：
            s (str): String to convert / 要转换的字符串

        Returns:
            返回：
            int: Integer value / 整数值
        """
        try:
            return int(s)
        except ValueError:
            return 0

    @staticmethod
    def atol(s: str) -> int:
        """
        Convert string to long integer.
        字符串转长整数。

        Args:
            参数：
            s (str): String to convert / 要转换的字符串

        Returns:
            返回：
            int: Long integer value / 长整数值
        """
        try:
            return int(s)
        except ValueError:
            return 0

    @staticmethod
    def atof(s: str) -> float:
        """
        Convert string to float.
        字符串转浮点数。

        Args:
            参数：
            s (str): String to convert / 要转换的字符串

        Returns:
            返回：
            float: Float value / 浮点值
        """
        try:
            return float(s)
        except ValueError:
            return 0.0

    @staticmethod
    def strtol(s: str, base: int = 10) -> int:
        """
        Convert string to long integer with base.
        按进制将字符串转换为长整数。

        Args:
            参数：
            s (str): String to convert / 要转换的字符串
            base (int): Base (2-36) / 进制 (2-36)

        Returns:
            返回：
            int: Long integer value / 长整数值
        """
        try:
            return int(s, base)
        except ValueError:
            return 0

    @staticmethod
    def strtoul(s: str, base: int = 10) -> int:
        """
        Convert string to unsigned long integer with base.
        按进制将字符串转换为无符号长整数。

        Args:
            参数：
            s (str): String to convert / 要转换的字符串
            base (int): Base (2-36) / 进制 (2-36)

        Returns:
            返回：
            int: Unsigned long integer value / 无符号长整数值
        """
        try:
            return int(s, base) & 0xFFFFFFFF
        except ValueError:
            return 0

    # Random numbers / 随机数
    @staticmethod
    def rand() -> int:
        """
        Generate random integer.
        生成随机整数。

        Returns:
            返回：
            int: Random integer (0 to RAND_MAX) / 随机整数 (0 到 RAND_MAX)
        """
        return _random.randint(0, stdlib.RAND_MAX())

    @staticmethod
    def srand(seed: int):
        """
        Seed random number generator.
        设置随机数种子。

        Args:
            参数：
            seed (int): Seed value / 种子值
        """
        _random.seed(seed)

    @staticmethod
    def RAND_MAX() -> int:
        """
        Maximum random value.
        最大随机值。

        Returns:
            返回：
            int: RAND_MAX value / RAND_MAX 值
        """
        return 2147483647

    # Process control / 进程控制
    @staticmethod
    def abort():
        """Abort process / 终止进程"""
        sys.exit(1)

    @staticmethod
    def exit(code: int):
        """Exit process / 退出进程"""
        sys.exit(code)

    @staticmethod
    def system(cmd: str) -> int:
        """
        Execute shell command.
        执行 shell 命令。

        Args:
            参数：
            cmd (str): Command to execute / 要执行的命令

        Returns:
            返回：
            int: Command exit status / 命令退出状态
        """
        import subprocess
        try:
            return subprocess.call(cmd, shell=True)
        except Exception:
            return -1

    # Environment / 环境变量
    @staticmethod
    def getenv(name: str) -> str:
        """
        Get environment variable.
        获取环境变量。

        Args:
            参数：
            name (str): Variable name / 变量名

        Returns:
            返回：
            str: Value or empty string / 值或空字符串
        """
        import os
        return os.environ.get(name, '')

    @staticmethod
    def setenv(name: str, value: str, overwrite: bool = True):
        """
        Set environment variable.
        设置环境变量。

        Args:
            参数：
            name (str): Variable name / 变量名
            value (str): Variable value / 变量值
            overwrite (bool): Overwrite if exists / 如果存在则覆盖
        """
        import os
        if overwrite or name not in os.environ:
            os.environ[name] = value

    # Sorting / 排序
    @staticmethod
    def qsort(arr: list, key=None):
        """
        Sort array.
        排序数组。

        Args:
            参数：
            arr (list): Array to sort / 要排序的数组
            key (callable): Key function / 键函数
        """
        arr.sort(key=key)

    # Search / 搜索
    @staticmethod
    def bsearch(arr: list, target, key=None):
        """
        Binary search.
        二分查找。

        Args:
            参数：
            arr (list): Sorted array / 已排序数组
            target: Target value / 目标值
            key (callable): Key function / 键函数

        Returns:
            返回：
            object: Found value or None / 找到的值或 None
        """
        try:
            if key:
                for item in arr:
                    if key(item) == target:
                        return item
            else:
                for item in arr:
                    if item == target:
                        return item
            return None
        except Exception:
            return None