# ============================================================================
# Module: userland/libs/libbamboo/bamboo.py
# 模块：userland/libs/libbamboo/bamboo.py
# Description: Bamboo OS core API
# 描述：Bamboo OS 核心 API
# ============================================================================

"""
Bamboo OS Core API.
Bamboo OS 核心 API。

This module provides the core system API for user-space applications.
该模块为用户空间应用提供核心系统 API。
"""

import os
import sys
import ctypes
import ctypes.util
from typing import Optional, List, Union, BinaryIO

from userland.libs.libbamboo.syscall import Syscall
from userland.libs.libbamboo.error import BambooError, ErrorCode


class BambooAPI:
    """
    Bamboo OS core API.
    Bamboo OS 核心 API。

    Provides methods for system calls, file operations, process management,
    and memory management.
    提供系统调用、文件操作、进程管理和内存管理的方法。
    """

    # System call numbers / 系统调用号
    SYS_READ = 0
    SYS_WRITE = 1
    SYS_OPEN = 2
    SYS_CLOSE = 3
    SYS_STAT = 4
    SYS_FSTAT = 5
    SYS_LSEEK = 6
    SYS_POLL = 7
    SYS_MMAP = 8
    SYS_MPROTECT = 9
    SYS_MUNMAP = 10
    SYS_BRK = 11
    SYS_SIGACTION = 12
    SYS_SIGPROCMASK = 13
    SYS_IOCTL = 14
    SYS_PREAD64 = 15
    SYS_PWRITE64 = 16
    SYS_READV = 17
    SYS_WRITEV = 18
    SYS_ACCESS = 19
    SYS_PIPE = 20
    SYS_SELECT = 21
    SYS_SCHED_YIELD = 22
    SYS_MREMAP = 23
    SYS_MSYNC = 24
    SYS_MINCORE = 25
    SYS_MADVISE = 26
    SYS_SHMGET = 27
    SYS_SHMAT = 28
    SYS_SHMCTL = 29
    SYS_DUP = 30
    SYS_DUP2 = 31
    SYS_PAUSE = 32
    SYS_NANOSLEEP = 33
    SYS_GETITIMER = 34
    SYS_ALARM = 35
    SYS_SETITIMER = 36
    SYS_GETPID = 37
    SYS_SENDFILE = 38
    SYS_SOCKET = 39
    SYS_CONNECT = 40
    SYS_ACCEPT = 41
    SYS_SENDTO = 42
    SYS_RECVFROM = 43
    SYS_SENDMSG = 44
    SYS_RECVMSG = 45
    SYS_SHUTDOWN = 46
    SYS_BIND = 47
    SYS_LISTEN = 48
    SYS_GETSOCKNAME = 49
    SYS_GETPEERNAME = 50
    SYS_SOCKETPAIR = 51
    SYS_SETSOCKOPT = 52
    SYS_GETSOCKOPT = 53
    SYS_CLONE = 54
    SYS_FORK = 55
    SYS_EXECVE = 56
    SYS_EXIT = 57
    SYS_WAIT4 = 58
    SYS_KILL = 59
    SYS_UNAME = 60
    SYS_SEMGET = 61
    SYS_SEMOP = 62
    SYS_SEMCTL = 63
    SYS_SHMDT = 64
    SYS_MSGGET = 65
    SYS_MSGSND = 66
    SYS_MSGRCV = 67
    SYS_MSGCTL = 68

    # File open flags / 文件打开标志
    O_RDONLY = 0
    O_WRONLY = 1
    O_RDWR = 2
    O_CREAT = 0x40
    O_TRUNC = 0x200
    O_APPEND = 0x400
    O_EXCL = 0x80

    # File seek flags / 文件定位标志
    SEEK_SET = 0
    SEEK_CUR = 1
    SEEK_END = 2

    # Memory protection flags / 内存保护标志
    PROT_READ = 0x1
    PROT_WRITE = 0x2
    PROT_EXEC = 0x4
    PROT_NONE = 0x0

    # Memory mapping flags / 内存映射标志
    MAP_SHARED = 0x01
    MAP_PRIVATE = 0x02
    MAP_ANONYMOUS = 0x20
    MAP_FIXED = 0x10

    # File descriptor numbers / 文件描述符编号
    STDIN_FILENO = 0
    STDOUT_FILENO = 1
    STDERR_FILENO = 2

    # Signal numbers / 信号编号
    SIGHUP = 1
    SIGINT = 2
    SIGQUIT = 3
    SIGILL = 4
    SIGTRAP = 5
    SIGABRT = 6
    SIGKILL = 9
    SIGSEGV = 11
    SIGPIPE = 13
    SIGALRM = 14
    SIGTERM = 15
    SIGUSR1 = 10
    SIGUSR2 = 12
    SIGCHLD = 17
    SIGCONT = 18
    SIGSTOP = 19

    @staticmethod
    def syscall(number: int, *args) -> int:
        """
        Make a system call.
        发起系统调用。

        Args:
            参数：
            number (int): System call number / 系统调用号
            *args: Arguments / 参数

        Returns:
            返回：
            int: Return value / 返回值
        """
        return Syscall.invoke(number, *args)

    # =========================================================================
    # File operations / 文件操作
    # =========================================================================

    @staticmethod
    def open(path: str, flags: int, mode: int = 0o644) -> int:
        """
        Open a file.
        打开文件。

        Args:
            参数：
            path (str): File path / 文件路径
            flags (int): Open flags / 打开标志
            mode (int): File mode / 文件模式

        Returns:
            返回：
            int: File descriptor or -1 on error / 文件描述符或 -1
        """
        return BambooAPI.syscall(BambooAPI.SYS_OPEN, path, flags, mode)

    @staticmethod
    def close(fd: int) -> int:
        """
        Close a file descriptor.
        关闭文件描述符。

        Args:
            参数：
            fd (int): File descriptor / 文件描述符

        Returns:
            返回：
            int: 0 on success, -1 on error / 成功返回 0，错误返回 -1
        """
        return BambooAPI.syscall(BambooAPI.SYS_CLOSE, fd)

    @staticmethod
    def read(fd: int, size: int) -> bytes:
        """
        Read from a file descriptor.
        从文件描述符读取。

        Args:
            参数：
            fd (int): File descriptor / 文件描述符
            size (int): Number of bytes to read / 要读取的字节数

        Returns:
            返回：
            bytes: Read data / 读取的数据
        """
        buf = ctypes.create_string_buffer(size)
        result = BambooAPI.syscall(BambooAPI.SYS_READ, fd, buf, size)
        if result > 0:
            return buf.raw[:result]
        return b''

    @staticmethod
    def write(fd: int, data: Union[bytes, str]) -> int:
        """
        Write to a file descriptor.
        写入文件描述符。

        Args:
            参数：
            fd (int): File descriptor / 文件描述符
            data (bytes/str): Data to write / 要写入的数据

        Returns:
            返回：
            int: Number of bytes written / 写入的字节数
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return BambooAPI.syscall(BambooAPI.SYS_WRITE, fd, data, len(data))

    @staticmethod
    def lseek(fd: int, offset: int, whence: int) -> int:
        """
        Seek in a file.
        在文件中定位。

        Args:
            参数：
            fd (int): File descriptor / 文件描述符
            offset (int): Offset / 偏移量
            whence (int): Seek flag / 定位标志

        Returns:
            返回：
            int: New file offset / 新的文件偏移
        """
        return BambooAPI.syscall(BambooAPI.SYS_LSEEK, fd, offset, whence)

    @staticmethod
    def stat(path: str) -> dict:
        """
        Get file status.
        获取文件状态。

        Args:
            参数：
            path (str): File path / 文件路径

        Returns:
            返回：
            dict: File status / 文件状态
        """
        # Simplified - returns dummy data / 简化 - 返回虚拟数据
        return {
            'size': 0,
            'mode': 0,
            'uid': 0,
            'gid': 0,
            'atime': 0,
            'mtime': 0,
            'ctime': 0,
        }

    # =========================================================================
    # Process management / 进程管理
    # =========================================================================

    @staticmethod
    def getpid() -> int:
        """Get process ID / 获取进程 ID"""
        return BambooAPI.syscall(BambooAPI.SYS_GETPID)

    @staticmethod
    def fork() -> int:
        """
        Fork process.
        进程分叉。

        Returns:
            返回：
            int: Child PID in parent, 0 in child, -1 on error /
                父进程返回子进程 PID，子进程返回 0，错误返回 -1
        """
        return BambooAPI.syscall(BambooAPI.SYS_FORK)

    @staticmethod
    def execve(path: str, args: List[str], env: Optional[dict] = None) -> int:
        """
        Execute a program.
        执行程序。

        Args:
            参数：
            path (str): Program path / 程序路径
            args (list): Arguments / 参数
            env (dict): Environment / 环境变量

        Returns:
            返回：
            int: -1 on error / 错误返回 -1
        """
        if env is None:
            env = dict(os.environ)
        env_list = [f"{k}={v}" for k, v in env.items()]
        return BambooAPI.syscall(BambooAPI.SYS_EXECVE, path, args, env_list)

    @staticmethod
    def exit(code: int):
        """
        Exit process.
        退出进程。

        Args:
            参数：
            code (int): Exit code / 退出码
        """
        BambooAPI.syscall(BambooAPI.SYS_EXIT, code)

    @staticmethod
    def wait4(pid: int, options: int = 0) -> tuple:
        """
        Wait for process.
        等待进程。

        Args:
            参数：
            pid (int): Process ID / 进程 ID
            options (int): Wait options / 等待选项

        Returns:
            返回：
            tuple: (pid, status) / (进程 ID, 状态)
        """
        status = ctypes.c_int()
        result = BambooAPI.syscall(BambooAPI.SYS_WAIT4, pid, status, options, 0)
        return result, status.value

    @staticmethod
    def kill(pid: int, signal: int) -> int:
        """
        Send signal to process.
        向进程发送信号。

        Args:
            参数：
            pid (int): Process ID / 进程 ID
            signal (int): Signal number / 信号编号

        Returns:
            返回：
            int: 0 on success, -1 on error / 成功返回 0，错误返回 -1
        """
        return BambooAPI.syscall(BambooAPI.SYS_KILL, pid, signal)

    # =========================================================================
    # Memory management / 内存管理
    # =========================================================================

    @staticmethod
    def mmap(addr: int, length: int, prot: int, flags: int, fd: int, offset: int) -> int:
        """
        Map memory.
        映射内存。

        Args:
            参数：
            addr (int): Suggested address / 建议地址
            length (int): Length / 长度
            prot (int): Protection flags / 保护标志
            flags (int): Mapping flags / 映射标志
            fd (int): File descriptor / 文件描述符
            offset (int): File offset / 文件偏移

        Returns:
            返回：
            int: Mapped address / 映射地址
        """
        return BambooAPI.syscall(BambooAPI.SYS_MMAP, addr, length, prot, flags, fd, offset)

    @staticmethod
    def munmap(addr: int, length: int) -> int:
        """
        Unmap memory.
        取消内存映射。

        Args:
            参数：
            addr (int): Address / 地址
            length (int): Length / 长度

        Returns:
            返回：
            int: 0 on success, -1 on error / 成功返回 0，错误返回 -1
        """
        return BambooAPI.syscall(BambooAPI.SYS_MUNMAP, addr, length)

    @staticmethod
    def mprotect(addr: int, length: int, prot: int) -> int:
        """
        Change memory protection.
        修改内存保护。

        Args:
            参数：
            addr (int): Address / 地址
            length (int): Length / 长度
            prot (int): Protection flags / 保护标志

        Returns:
            返回：
            int: 0 on success, -1 on error / 成功返回 0，错误返回 -1
        """
        return BambooAPI.syscall(BambooAPI.SYS_MPROTECT, addr, length, prot)

    @staticmethod
    def brk(addr: int) -> int:
        """
        Change program break.
        修改程序间断点。

        Args:
            参数：
            addr (int): New break address / 新的间断点地址

        Returns:
            返回：
            int: New break address / 新的间断点地址
        """
        return BambooAPI.syscall(BambooAPI.SYS_BRK, addr)

    # =========================================================================
    # Network operations / 网络操作
    # =========================================================================

    @staticmethod
    def socket(domain: int, type_: int, protocol: int) -> int:
        """Create socket / 创建套接字"""
        return BambooAPI.syscall(BambooAPI.SYS_SOCKET, domain, type_, protocol)

    @staticmethod
    def connect(fd: int, addr: bytes, addrlen: int) -> int:
        """Connect socket / 连接套接字"""
        return BambooAPI.syscall(BambooAPI.SYS_CONNECT, fd, addr, addrlen)

    # =========================================================================
    # Time / 时间
    # =========================================================================

    @staticmethod
    def sleep(seconds: int) -> int:
        """
        Sleep for seconds.
        睡眠秒数。

        Args:
            参数：
            seconds (int): Seconds to sleep / 要睡眠的秒数

        Returns:
            返回：
            int: 0 on success / 成功返回 0
        """
        return BambooAPI.syscall(BambooAPI.SYS_NANOSLEEP, seconds, 0)

    @staticmethod
    def gettimeofday() -> tuple:
        """
        Get time of day.
        获取当天时间。

        Returns:
            返回：
            tuple: (seconds, microseconds) / (秒, 微秒)
        """
        import time
        return time.time(), 0

    # =========================================================================
    # Utility functions / 工具函数
    # =========================================================================

    @staticmethod
    def print_stdout(text: str):
        """Print to stdout / 打印到标准输出"""
        BambooAPI.write(BambooAPI.STDOUT_FILENO, text)

    @staticmethod
    def print_stderr(text: str):
        """Print to stderr / 打印到标准错误"""
        BambooAPI.write(BambooAPI.STDERR_FILENO, text)

    @staticmethod
    def getenv(key: str) -> Optional[str]:
        """Get environment variable / 获取环境变量"""
        return os.environ.get(key)

    @staticmethod
    def setenv(key: str, value: str):
        """Set environment variable / 设置环境变量"""
        os.environ[key] = value