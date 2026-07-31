# ============================================================================
# Module: userland/libs/libc/string.py
# 模块：userland/libs/libc/string.py
# Description: String library functions
# 描述：字符串库函数
# ============================================================================

"""
String library for Bamboo OS.
Bamboo OS 字符串库。

Provides strlen, strcpy, strcmp, memcpy, and other string functions.
提供 strlen、strcpy、strcmp、memcpy 和其他字符串函数。
"""


class string:
    """
    String library functions.
    字符串库函数。
    """

    # =========================================================================
    # String length / 字符串长度
    # =========================================================================

    @staticmethod
    def strlen(s: str) -> int:
        """Get string length / 获取字符串长度"""
        return len(s)

    @staticmethod
    def strnlen(s: str, maxlen: int) -> int:
        """Get string length with limit / 获取带限制的字符串长度"""
        return min(len(s), maxlen)

    # =========================================================================
    # String copy / 字符串复制
    # =========================================================================

    @staticmethod
    def strcpy(dest: str, src: str) -> str:
        """Copy string / 复制字符串"""
        return src

    @staticmethod
    def strncpy(dest: str, src: str, n: int) -> str:
        """Copy string with limit / 带限制复制字符串"""
        return src[:n]

    @staticmethod
    def strdup(s: str) -> str:
        """Duplicate string / 复制字符串"""
        return s

    @staticmethod
    def strndup(s: str, n: int) -> str:
        """Duplicate string with limit / 带限制复制字符串"""
        return s[:n]

    # =========================================================================
    # String concatenation / 字符串连接
    # =========================================================================

    @staticmethod
    def strcat(dest: str, src: str) -> str:
        """Concatenate strings / 连接字符串"""
        return dest + src

    @staticmethod
    def strncat(dest: str, src: str, n: int) -> str:
        """Concatenate strings with limit / 带限制连接字符串"""
        return dest + src[:n]

    # =========================================================================
    # String comparison / 字符串比较
    # =========================================================================

    @staticmethod
    def strcmp(a: str, b: str) -> int:
        """
        Compare strings.
        比较字符串。

        Returns:
            返回：
            int: Negative if a < b, 0 if equal, positive if a > b /
                负数表示 a < b，0 表示相等，正数表示 a > b
        """
        if a < b:
            return -1
        if a > b:
            return 1
        return 0

    @staticmethod
    def strncmp(a: str, b: str, n: int) -> int:
        """Compare strings with limit / 带限制比较字符串"""
        return string.strcmp(a[:n], b[:n])

    @staticmethod
    def strcasecmp(a: str, b: str) -> int:
        """Case-insensitive string compare / 不区分大小写比较字符串"""
        return string.strcmp(a.lower(), b.lower())

    @staticmethod
    def strncasecmp(a: str, b: str, n: int) -> int:
        """Case-insensitive string compare with limit / 带限制不区分大小写比较"""
        return string.strcasecmp(a[:n], b[:n])

    # =========================================================================
    # String search / 字符串搜索
    # =========================================================================

    @staticmethod
    def strchr(s: str, c: str) -> int:
        """Find character in string / 在字符串中查找字符"""
        try:
            return s.index(c)
        except ValueError:
            return -1

    @staticmethod
    def strrchr(s: str, c: str) -> int:
        """Find character from end / 从末尾查找字符"""
        try:
            return s.rindex(c)
        except ValueError:
            return -1

    @staticmethod
    def strstr(s: str, substr: str) -> int:
        """Find substring / 查找子字符串"""
        try:
            return s.index(substr)
        except ValueError:
            return -1

    @staticmethod
    def strcasestr(s: str, substr: str) -> int:
        """Case-insensitive substring search / 不区分大小写查找子字符串"""
        try:
            return s.lower().index(substr.lower())
        except ValueError:
            return -1

    @staticmethod
    def strspn(s: str, accept: str) -> int:
        """Get span of characters in accept / 获取接受字符的跨度"""
        count = 0
        for ch in s:
            if ch in accept:
                count += 1
            else:
                break
        return count

    @staticmethod
    def strcspn(s: str, reject: str) -> int:
        """Get span of characters not in reject / 获取不在拒绝字符中的跨度"""
        count = 0
        for ch in s:
            if ch not in reject:
                count += 1
            else:
                break
        return count

    @staticmethod
    def strpbrk(s: str, accept: str) -> int:
        """Find first character in accept / 查找第一个在 accept 中的字符"""
        for i, ch in enumerate(s):
            if ch in accept:
                return i
        return -1

    # =========================================================================
    # String tokenization / 字符串分词
    # =========================================================================

    @staticmethod
    def strtok(s: str, delim: str, context: list = None) -> str:
        """
        Tokenize string.
        分词字符串。

        Args:
            参数：
            s (str): String to tokenize / 要分词的字符串
            delim (str): Delimiters / 分隔符
            context (list): Context for persistent calls / 持久调用的上下文

        Returns:
            返回：
            str: Token or empty string / 分词或空字符串
        """
        if context is None:
            context = [0, s]
        if s is not None:
            context[1] = s
            context[0] = 0

        if context[0] >= len(context[1]):
            return ''

        # Skip delimiters / 跳过分隔符
        while context[0] < len(context[1]) and context[1][context[0]] in delim:
            context[0] += 1

        if context[0] >= len(context[1]):
            return ''

        start = context[0]
        while context[0] < len(context[1]) and context[1][context[0]] not in delim:
            context[0] += 1

        token = context[1][start:context[0]]

        # Skip delimiter for next call / 为下次调用跳过分隔符
        if context[0] < len(context[1]) and context[1][context[0]] in delim:
            context[0] += 1

        return token

    # =========================================================================
    # Memory functions / 内存函数
    # =========================================================================

    @staticmethod
    def memcpy(dest: bytearray, src: bytes, n: int) -> bytearray:
        """Copy memory / 复制内存"""
        dest[:n] = src[:n]
        return dest

    @staticmethod
    def memmove(dest: bytearray, src: bytes, n: int) -> bytearray:
        """Move memory (handles overlap) / 移动内存（处理重叠）"""
        dest[:n] = src[:n]
        return dest

    @staticmethod
    def memset(s: bytearray, c: int, n: int) -> bytearray:
        """Set memory / 设置内存"""
        s[:n] = bytes([c]) * n
        return s

    @staticmethod
    def memcmp(a: bytes, b: bytes, n: int) -> int:
        """Compare memory / 比较内存"""
        if a[:n] < b[:n]:
            return -1
        if a[:n] > b[:n]:
            return 1
        return 0

    @staticmethod
    def memchr(s: bytes, c: int, n: int) -> int:
        """Find character in memory / 在内存中查找字符"""
        for i in range(min(n, len(s))):
            if s[i] == c:
                return i
        return -1

    @staticmethod
    def memmem(haystack: bytes, needle: bytes) -> int:
        """Find memory block in memory / 在内存中查找内存块"""
        try:
            return haystack.index(needle)
        except ValueError:
            return -1

    # =========================================================================
    # Utility functions / 工具函数
    # =========================================================================

    @staticmethod
    def strerror(errnum: int) -> str:
        """Get error message for error number / 获取错误码对应的错误消息"""
        errors = {
            0: "Success",
            1: "Operation not permitted",
            2: "No such file or directory",
            3: "No such process",
            4: "Interrupted system call",
            5: "I/O error",
            6: "No such device or address",
            7: "Argument list too long",
            8: "Exec format error",
            9: "Bad file number",
            10: "No child processes",
            11: "Try again",
            12: "Out of memory",
            13: "Permission denied",
            14: "Bad address",
            16: "Device or resource busy",
            17: "File exists",
            22: "Invalid argument",
            24: "Too many open files",
            28: "No space left on device",
            38: "Function not implemented",
            39: "Directory not empty",
            61: "Connection refused",
            110: "Connection timed out",
            111: "Connection refused",
            113: "No route to host",
        }
        return errors.get(errnum, f"Unknown error {errnum}")

    @staticmethod
    def strlwr(s: str) -> str:
        """Convert string to lowercase / 将字符串转换为小写"""
        return s.lower()

    @staticmethod
    def strupr(s: str) -> str:
        """Convert string to uppercase / 将字符串转换为大写"""
        return s.upper()