# ============================================================================
# Module: userland/libs/libc/stdio.py
# 模块：userland/libs/libc/stdio.py
# Description: Standard I/O library
# 描述：标准 I/O 库
# ============================================================================

"""
Standard I/O library for Bamboo OS.
Bamboo OS 标准 I/O 库。

Provides printf, scanf, file I/O, and other stdio functions.
提供 printf、scanf、文件 I/O 和其他 stdio 函数。
"""

import sys
from typing import Optional, BinaryIO, TextIO


class stdio:
    """
    Standard I/O functions.
    标准 I/O 函数。
    """

    # File modes / 文件模式
    MODE_READ = 'r'
    MODE_WRITE = 'w'
    MODE_APPEND = 'a'
    MODE_READ_BINARY = 'rb'
    MODE_WRITE_BINARY = 'wb'

    @staticmethod
    def printf(fmt: str, *args) -> int:
        """
        Print formatted output.
        格式化输出。

        Args:
            参数：
            fmt (str): Format string / 格式字符串
            *args: Arguments / 参数

        Returns:
            返回：
            int: Number of characters printed / 打印的字符数
        """
        try:
            result = fmt % args
            sys.stdout.write(result)
            return len(result)
        except Exception:
            return -1

    @staticmethod
    def fprintf(file, fmt: str, *args) -> int:
        """
        Print formatted output to file.
        格式化输出到文件。

        Args:
            参数：
            file: File object / 文件对象
            fmt (str): Format string / 格式字符串
            *args: Arguments / 参数

        Returns:
            返回：
            int: Number of characters printed / 打印的字符数
        """
        try:
            result = fmt % args
            file.write(result)
            return len(result)
        except Exception:
            return -1

    @staticmethod
    def sprintf(buf: bytearray, fmt: str, *args) -> int:
        """
        Print formatted output to buffer.
        格式化输出到缓冲区。

        Args:
            参数：
            buf (bytearray): Output buffer / 输出缓冲区
            fmt (str): Format string / 格式字符串
            *args: Arguments / 参数

        Returns:
            返回：
            int: Number of characters written / 写入的字符数
        """
        try:
            result = fmt % args
            buf.extend(result.encode('utf-8'))
            return len(result)
        except Exception:
            return -1

    @staticmethod
    def vprintf(fmt: str, args: tuple) -> int:
        """
        Print formatted output with va_list.
        使用可变参数列表格式化输出。

        Args:
            参数：
            fmt (str): Format string / 格式字符串
            args (tuple): Arguments tuple / 参数元组

        Returns:
            返回：
            int: Number of characters printed / 打印的字符数
        """
        return stdio.printf(fmt, *args)

    @staticmethod
    def scanf(fmt: str) -> list:
        """
        Read formatted input.
        读取格式化输入。

        Args:
            参数：
            fmt (str): Format string / 格式字符串

        Returns:
            返回：
            list: Parsed values / 解析的值
        """
        try:
            line = sys.stdin.readline()
            if not line:
                return []
            # Simple implementation / 简单实现
            result = []
            for part in fmt.split():
                if part == '%d':
                    import re
                    match = re.search(r'-?\d+', line)
                    if match:
                        result.append(int(match.group()))
                elif part == '%s':
                    result.append(line.strip())
            return result
        except Exception:
            return []

    @staticmethod
    def fopen(path: str, mode: str = MODE_READ) -> Optional[BinaryIO]:
        """
        Open a file.
        打开文件。

        Args:
            参数：
            path (str): File path / 文件路径
            mode (str): Open mode / 打开模式

        Returns:
            返回：
            file: File object or None / 文件对象或 None
        """
        try:
            return open(path, mode)
        except Exception:
            return None

    @staticmethod
    def fclose(file) -> int:
        """
        Close a file.
        关闭文件。

        Args:
            参数：
            file: File object / 文件对象

        Returns:
            返回：
            int: 0 on success, -1 on error / 成功返回 0，错误返回 -1
        """
        try:
            file.close()
            return 0
        except Exception:
            return -1

    @staticmethod
    def fread(size: int, count: int, file) -> bytes:
        """
        Read from file.
        从文件读取。

        Args:
            参数：
            size (int): Element size / 元素大小
            count (int): Number of elements / 元素数量
            file: File object / 文件对象

        Returns:
            返回：
            bytes: Read data / 读取的数据
        """
        try:
            return file.read(size * count)
        except Exception:
            return b''

    @staticmethod
    def fwrite(data: bytes, size: int, count: int, file) -> int:
        """
        Write to file.
        写入文件。

        Args:
            参数：
            data (bytes): Data to write / 要写入的数据
            size (int): Element size / 元素大小
            count (int): Number of elements / 元素数量
            file: File object / 文件对象

        Returns:
            返回：
            int: Number of elements written / 写入的元素数
        """
        try:
            file.write(data)
            return count
        except Exception:
            return 0

    @staticmethod
    def fgetc(file) -> int:
        """
        Get a character from file.
        从文件获取一个字符。

        Args:
            参数：
            file: File object / 文件对象

        Returns:
            返回：
            int: Character code or -1 on EOF / 字符代码或 -1
        """
        c = file.read(1)
        if c:
            return c[0]
        return -1

    @staticmethod
    def fputc(c: int, file) -> int:
        """
        Write a character to file.
        写入一个字符到文件。

        Args:
            参数：
            c (int): Character code / 字符代码
            file: File object / 文件对象

        Returns:
            返回：
            int: Character code on success, -1 on error / 成功返回字符代码，错误返回 -1
        """
        try:
            file.write(bytes([c]))
            return c
        except Exception:
            return -1

    @staticmethod
    def fgets(size: int, file) -> str:
        """
        Get a string from file.
        从文件获取字符串。

        Args:
            参数：
            size (int): Maximum size / 最大大小
            file: File object / 文件对象

        Returns:
            返回：
            str: String or empty on EOF / 字符串或空字符串
        """
        try:
            return file.readline(size)
        except Exception:
            return ''