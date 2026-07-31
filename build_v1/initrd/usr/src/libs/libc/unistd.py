# ============================================================================
# Module: userland/libs/libc/unistd.py
# 模块：userland/libs/libc/unistd.py
# Description: POSIX system call wrapper
# 描述：POSIX 系统调用包装器
# ============================================================================

"""
POSIX system call wrapper for Bamboo OS.
Bamboo OS POSIX 系统调用包装器。

Provides POSIX-compatible system call functions.
提供 POSIX 兼容的系统调用函数。
"""

import os
import sys
from typing import Optional, List, Union, BinaryIO

from userland.libs.libbamboo.bamboo import BambooAPI


class unistd:
    """
    POSIX system call wrapper.
    POSIX 系统调用包装器。
    """

    # Standard file descriptors / 标准文件描述符
    STDIN_FILENO = 0
    STDOUT_FILENO = 1
    STDERR_FILENO = 2

    # File open flags / 文件打开标志
    O_RDONLY = 0
    O_WRONLY = 1
    O_RDWR = 2
    O_CREAT = 0x40
    O_TRUNC = 0x200
    O_APPEND = 0x400
    O_EXCL = 0x80
    O_NONBLOCK = 0x800

    # File seek flags / 文件定位标志
    SEEK_SET = 0
    SEEK_CUR = 1
    SEEK_END = 2

    # Memory protection / 内存保护
    PROT_READ = 0x1
    PROT_WRITE = 0x2
    PROT_EXEC = 0x4

    # Memory mapping / 内存映射
    MAP_SHARED = 0x01
    MAP_PRIVATE = 0x02
    MAP_ANONYMOUS = 0x20
    MAP_FIXED = 0x10

    # =========================================================================
    # File operations / 文件操作
    # =========================================================================

    @staticmethod
    def open(path: str, flags: int, mode: int = 0o644) -> int:
        """Open a file / 打开文件"""
        return BambooAPI.open(path, flags, mode)

    @staticmethod
    def close(fd: int) -> int:
        """Close a file descriptor / 关闭文件描述符"""
        return BambooAPI.close(fd)

    @staticmethod
    def read(fd: int, size: int) -> bytes:
        """Read from file descriptor / 从文件描述符读取"""
        return BambooAPI.read(fd, size)

    @staticmethod
    def write(fd: int, data: Union[bytes, str]) -> int:
        """Write to file descriptor / 写入文件描述符"""
        return BambooAPI.write(fd, data)

    @staticmethod
    def lseek(fd: int, offset: int, whence: int) -> int:
        """Seek in file / 在文件中定位"""
        return BambooAPI.lseek(fd, offset, whence)

    @staticmethod
    def stat(path: str) -> dict:
        """Get file status / 获取文件状态"""
        return BambooAPI.stat(path)

    @staticmethod
    def fstat(fd: int) -> dict:
        """Get file status by descriptor / 通过描述符获取文件状态"""
        return BambooAPI.stat(f"/dev/fd/{fd}")

    @staticmethod
    def unlink(path: str) -> int:
        """Delete a file / 删除文件"""
        return BambooAPI.syscall(10, path)  # SYS_UNLINK

    @staticmethod
    def rename(old: str, new: str) -> int:
        """Rename a file / 重命名文件"""
        return BambooAPI.syscall(79, old, new)  # SYS_RENAME

    @staticmethod
    def mkdir(path: str, mode: int = 0o755) -> int:
        """Create a directory / 创建目录"""
        return BambooAPI.syscall(80, path, mode)  # SYS_MKDIR

    @staticmethod
    def rmdir(path: str) -> int:
        """Remove a directory / 删除目录"""
        return BambooAPI.syscall(81, path)  # SYS_RMDIR

    @staticmethod
    def chdir(path: str) -> int:
        """Change directory / 切换目录"""
        return BambooAPI.syscall(77, path)  # SYS_CHDIR

    @staticmethod
    def getcwd() -> str:
        """Get current working directory / 获取当前工作目录"""
        return os.getcwd()

    # =========================================================================
    # Process management / 进程管理
    # =========================================================================

    @staticmethod
    def getpid() -> int:
        """Get process ID / 获取进程 ID"""
        return BambooAPI.getpid()

    @staticmethod
    def getppid() -> int:
        """Get parent process ID / 获取父进程 ID"""
        return BambooAPI.syscall(105)  # SYS_GETPPID

    @staticmethod
    def fork() -> int:
        """Fork a process / 分叉进程"""
        return BambooAPI.fork()

    @staticmethod
    def execve(path: str, args: List[str], env: Optional[dict] = None) -> int:
        """Execute a program / 执行程序"""
        return BambooAPI.execve(path, args, env)

    @staticmethod
    def execvp(file: str, args: List[str]) -> int:
        """Execute a program with PATH search / 使用 PATH 搜索执行程序"""
        import os
        if os.path.exists(file) and os.access(file, os.X_OK):
            return unistd.execve(file, args)

        # Search PATH / 搜索 PATH
        path = os.environ.get('PATH', '/bin:/usr/bin')
        for dir_path in path.split(':'):
            full_path = os.path.join(dir_path, file)
            if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                return unistd.execve(full_path, args)

        return -1

    @staticmethod
    def exit(code: int):
        """Exit process / 退出进程"""
        BambooAPI.exit(code)

    @staticmethod
    def wait(pid: int = -1) -> tuple:
        """Wait for process / 等待进程"""
        return BambooAPI.wait4(pid)

    @staticmethod
    def waitpid(pid: int, options: int = 0) -> tuple:
        """Wait for specific process / 等待特定进程"""
        return BambooAPI.wait4(pid, options)

    @staticmethod
    def kill(pid: int, signal: int) -> int:
        """Send signal to process / 向进程发送信号"""
        return BambooAPI.kill(pid, signal)

    @staticmethod
    def sleep(seconds: int) -> int:
        """Sleep for seconds / 睡眠秒数"""
        return BambooAPI.sleep(seconds)

    @staticmethod
    def usleep(microseconds: int) -> int:
        """Sleep for microseconds / 睡眠微秒数"""
        import time
        time.sleep(microseconds / 1000000.0)
        return 0

    # =========================================================================
    # Memory management / 内存管理
    # =========================================================================

    @staticmethod
    def mmap(addr: int, length: int, prot: int, flags: int, fd: int = -1, offset: int = 0) -> int:
        """Map memory / 映射内存"""
        return BambooAPI.mmap(addr, length, prot, flags, fd, offset)

    @staticmethod
    def munmap(addr: int, length: int) -> int:
        """Unmap memory / 取消内存映射"""
        return BambooAPI.munmap(addr, length)

    @staticmethod
    def mprotect(addr: int, length: int, prot: int) -> int:
        """Change memory protection / 修改内存保护"""
        return BambooAPI.mprotect(addr, length, prot)

    @staticmethod
    def brk(addr: int) -> int:
        """Change program break / 修改程序间断点"""
        return BambooAPI.brk(addr)

    @staticmethod
    def sbrk(increment: int) -> int:
        """Increment program break / 增加程序间断点"""
        current = BambooAPI.brk(0)
        if increment == 0:
            return current
        new_brk = current + increment
        result = BambooAPI.brk(new_brk)
        if result == new_brk:
            return current
        return -1

    # =========================================================================
    # Network / 网络
    # =========================================================================

    @staticmethod
    def socket(domain: int, type_: int, protocol: int) -> int:
        """Create socket / 创建套接字"""
        return BambooAPI.socket(domain, type_, protocol)

    @staticmethod
    def connect(fd: int, addr: bytes, addrlen: int) -> int:
        """Connect socket / 连接套接字"""
        return BambooAPI.connect(fd, addr, addrlen)

    @staticmethod
    def bind(fd: int, addr: bytes, addrlen: int) -> int:
        """Bind socket / 绑定套接字"""
        return BambooAPI.syscall(47, fd, addr, addrlen)  # SYS_BIND

    @staticmethod
    def listen(fd: int, backlog: int) -> int:
        """Listen for connections / 监听连接"""
        return BambooAPI.syscall(48, fd, backlog)  # SYS_LISTEN

    @staticmethod
    def accept(fd: int, addr: bytes, addrlen: int) -> int:
        """Accept connection / 接受连接"""
        return BambooAPI.syscall(41, fd, addr, addrlen)  # SYS_ACCEPT

    @staticmethod
    def send(fd: int, data: bytes, flags: int = 0) -> int:
        """Send data / 发送数据"""
        return BambooAPI.syscall(42, fd, data, len(data), flags)  # SYS_SENDTO

    @staticmethod
    def recv(fd: int, size: int, flags: int = 0) -> bytes:
        """Receive data / 接收数据"""
        return BambooAPI.read(fd, size)

    # =========================================================================
    # Pipe / 管道
    # =========================================================================

    @staticmethod
    def pipe() -> tuple:
        """Create pipe / 创建管道"""
        fds = [0, 0]
        result = BambooAPI.syscall(20, fds)  # SYS_PIPE
        if result == 0:
            return (fds[0], fds[1])
        return (-1, -1)

    @staticmethod
    def dup(fd: int) -> int:
        """Duplicate file descriptor / 复制文件描述符"""
        return BambooAPI.syscall(30, fd)  # SYS_DUP

    @staticmethod
    def dup2(oldfd: int, newfd: int) -> int:
        """Duplicate file descriptor to specific number / 复制到指定文件描述符"""
        return BambooAPI.syscall(31, oldfd, newfd)  # SYS_DUP2

    # =========================================================================
    # Time / 时间
    # =========================================================================

    @staticmethod
    def time() -> int:
        """Get current time in seconds / 获取当前时间（秒）"""
        import time
        return int(time.time())

    @staticmethod
    def gettimeofday() -> tuple:
        """Get time of day / 获取当天时间"""
        return BambooAPI.gettimeofday()

    @staticmethod
    def alarm(seconds: int) -> int:
        """Set alarm / 设置闹钟"""
        return BambooAPI.syscall(35, seconds)  # SYS_ALARM

    # =========================================================================
    # User/Group / 用户/组
    # =========================================================================

    @staticmethod
    def getuid() -> int:
        """Get user ID / 获取用户 ID"""
        return BambooAPI.syscall(99)  # SYS_GETUID

    @staticmethod
    def getgid() -> int:
        """Get group ID / 获取组 ID"""
        return BambooAPI.syscall(100)  # SYS_GETGID

    @staticmethod
    def geteuid() -> int:
        """Get effective user ID / 获取有效用户 ID"""
        return BambooAPI.syscall(103)  # SYS_GETEUID

    @staticmethod
    def getegid() -> int:
        """Get effective group ID / 获取有效组 ID"""
        return BambooAPI.syscall(104)  # SYS_GETEGID

    # =========================================================================
    # System information / 系统信息
    # =========================================================================

    @staticmethod
    def uname() -> dict:
        """Get system information / 获取系统信息"""
        return {
            'sysname': 'BambooOS',
            'nodename': 'bamboo',
            'release': '1.0.0',
            'version': 'Wonder',
            'machine': 'x86_64',
        }

    @staticmethod
    def gethostname() -> str:
        """Get hostname / 获取主机名"""
        return os.environ.get('HOSTNAME', 'bamboo')

    @staticmethod
    def sethostname(name: str) -> int:
        """Set hostname / 设置主机名"""
        os.environ['HOSTNAME'] = name
        return 0