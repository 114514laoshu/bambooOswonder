# ============================================================================
# Module: userland/libs/libbamboo/error.py
# 模块：userland/libs/libbamboo/error.py
# Description: Error definitions for Bamboo OS
# 描述：Bamboo OS 错误定义
# ============================================================================

"""
Error code definitions for Bamboo OS.
Bamboo OS 错误码定义。

Provides error codes and exception classes for user-space applications.
为用户空间应用提供错误码和异常类。
"""


class ErrorCode:
    """
    Standard error codes.
    标准错误码。

    These match Linux/Unix error codes for compatibility.
    这些错误码与 Linux/Unix 错误码兼容。
    """

    # Success / 成功
    EOK = 0

    # General errors / 通用错误
    EPERM = 1       # Operation not permitted / 操作不允许
    ENOENT = 2      # No such file or directory / 文件或目录不存在
    ESRCH = 3       # No such process / 进程不存在
    EINTR = 4       # Interrupted system call / 系统调用被中断
    EIO = 5         # I/O error / I/O 错误
    ENXIO = 6       # No such device or address / 设备或地址不存在
    E2BIG = 7       # Argument list too long / 参数列表太长
    ENOEXEC = 8     # Exec format error / 执行格式错误
    EBADF = 9       # Bad file number / 错误的文件号
    ECHILD = 10     # No child processes / 没有子进程
    EAGAIN = 11     # Try again / 重试
    ENOMEM = 12     # Out of memory / 内存不足
    EACCES = 13     # Permission denied / 权限被拒绝
    EFAULT = 14     # Bad address / 错误地址
    ENOTBLK = 15    # Block device required / 需要块设备
    EBUSY = 16      # Device or resource busy / 设备或资源忙
    EEXIST = 17     # File exists / 文件已存在
    EXDEV = 18      # Cross-device link / 跨设备链接
    ENODEV = 19     # No such device / 设备不存在
    ENOTDIR = 20    # Not a directory / 不是目录
    EISDIR = 21     # Is a directory / 是目录
    EINVAL = 22     # Invalid argument / 无效参数
    ENFILE = 23     # File table overflow / 文件表溢出
    EMFILE = 24     # Too many open files / 打开文件太多
    ENOTTY = 25     # Not a typewriter / 不是 TTY
    ETXTBSY = 26    # Text file busy / 文本文件忙
    EFBIG = 27      # File too large / 文件太大
    ENOSPC = 28     # No space left on device / 设备空间不足
    ESPIPE = 29     # Illegal seek / 非法定位
    EROFS = 30      # Read-only file system / 只读文件系统
    EMLINK = 31     # Too many links / 链接太多
    EPIPE = 32      # Broken pipe / 管道破裂

    # Math errors / 数学错误
    EDOM = 33       # Math argument out of domain / 数学参数超出定义域
    ERANGE = 34     # Math result not representable / 数学结果无法表示

    # Network errors / 网络错误
    ENETDOWN = 50   # Network is down / 网络已关闭
    ENETUNREACH = 51  # Network is unreachable / 网络不可达
    ENETRESET = 52  # Network dropped connection / 网络连接被重置
    ECONNABORTED = 53  # Software caused connection abort / 软件导致连接中止
    ECONNRESET = 54  # Connection reset by peer / 连接被对方重置
    ENOBUFS = 55    # No buffer space available / 缓冲区空间不足
    EISCONN = 56    # Socket is already connected / 套接字已连接
    ENOTCONN = 57   # Socket is not connected / 套接字未连接
    ESHUTDOWN = 58  # Cannot send after socket shutdown / 套接字关闭后无法发送
    ETOOMANYREFS = 59  # Too many references / 引用太多
    ETIMEDOUT = 60  # Connection timed out / 连接超时
    ECONNREFUSED = 61  # Connection refused / 连接被拒绝

    # Unix domain socket errors / Unix 域套接字错误
    EPROTONOSUPPORT = 62  # Protocol not supported / 协议不支持
    ESOCKTNOSUPPORT = 63  # Socket type not supported / 套接字类型不支持
    ENOPROTOOPT = 64  # Protocol not available / 协议不可用

    # Resource errors / 资源错误
    EDEADLK = 35    # Resource deadlock would occur / 资源死锁
    ENAMETOOLONG = 36  # File name too long / 文件名太长
    ENOLCK = 37     # No record locks available / 没有记录锁
    ENOSYS = 38     # Function not implemented / 功能未实现
    ENOTEMPTY = 39  # Directory not empty / 目录非空
    ELOOP = 40      # Too many symbolic links / 符号链接太多
    ENOMSG = 42     # No message of desired type / 没有所需类型的消息
    EIDRM = 43      # Identifier removed / 标识符已移除
    ECHRNG = 44     # Channel number out of range / 通道号超出范围
    EL2NSYNC = 45   # Level 2 not synchronized / 第二层未同步
    EL3HLT = 46     # Level 3 halted / 第三层停止
    EL3RST = 47     # Level 3 reset / 第三层重置
    ELNRNG = 48     # Link number out of range / 链路号超出范围
    EUNATCH = 49    # Protocol driver not attached / 协议驱动未附加
    ENOCSI = 50     # No CSI structure available / 没有可用的 CSI 结构
    EL2HLT = 51     # Level 2 halted / 第二层停止

    # IPC errors / IPC 错误
    EADDRINUSE = 98   # Address already in use / 地址已在使用
    EADDRNOTAVAIL = 99  # Address not available / 地址不可用
    EAFNOSUPPORT = 97  # Address family not supported / 地址族不支持
    EALREADY = 114   # Operation already in progress / 操作已在进行

    # Quota errors / 配额错误
    EDQUOT = 122   # Disk quota exceeded / 磁盘配额已超

    @classmethod
    def get_name(cls, code: int) -> str:
        """Get error name by code / 根据错误码获取错误名称"""
        for name, value in cls.__dict__.items():
            if isinstance(value, int) and value == code and not name.startswith('_'):
                return name
        return f"UNKNOWN_{code}"

    @classmethod
    def get_message(cls, code: int) -> str:
        """Get error message by code / 根据错误码获取错误消息"""
        messages = {
            cls.EOK: "Success",
            cls.EPERM: "Operation not permitted",
            cls.ENOENT: "No such file or directory",
            cls.ESRCH: "No such process",
            cls.EINTR: "Interrupted system call",
            cls.EIO: "I/O error",
            cls.ENXIO: "No such device or address",
            cls.E2BIG: "Argument list too long",
            cls.ENOEXEC: "Exec format error",
            cls.EBADF: "Bad file number",
            cls.ECHILD: "No child processes",
            cls.EAGAIN: "Try again",
            cls.ENOMEM: "Out of memory",
            cls.EACCES: "Permission denied",
            cls.EFAULT: "Bad address",
            cls.EBUSY: "Device or resource busy",
            cls.EEXIST: "File exists",
            cls.EINVAL: "Invalid argument",
            cls.ENFILE: "File table overflow",
            cls.EMFILE: "Too many open files",
            cls.ENOSPC: "No space left on device",
            cls.ESPIPE: "Illegal seek",
            cls.EROFS: "Read-only file system",
            cls.ENOSYS: "Function not implemented",
            cls.ENOTEMPTY: "Directory not empty",
            cls.ECONNREFUSED: "Connection refused",
            cls.ETIMEDOUT: "Connection timed out",
            cls.ENETUNREACH: "Network is unreachable",
            cls.EADDRINUSE: "Address already in use",
            cls.EDQUOT: "Disk quota exceeded",
        }
        return messages.get(code, f"Unknown error {code}")


class BambooError(Exception):
    """
    Bamboo OS error exception.
    Bamboo OS 错误异常。
    """

    def __init__(self, code: int, message: str = None):
        """
        Initialize error / 初始化错误

        Args:
            参数：
            code (int): Error code / 错误码
            message (str): Error message / 错误消息
        """
        self.code = code
        self.name = ErrorCode.get_name(code)
        self.message = message or ErrorCode.get_message(code)
        super().__init__(f"[{self.name}] {self.message}")

    def is_success(self) -> bool:
        """Check if error is success / 检查是否为成功"""
        return self.code == ErrorCode.EOK