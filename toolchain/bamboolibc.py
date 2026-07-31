# ============================================================================
# Module: toolchain/bamboolibc.py
# 模块：toolchain/bamboolibc.py
# Description: BambooLibc toolchain component
# 描述：BambooLibc 工具链组件
# ============================================================================

class BambooLibc:
    """BambooLibc - 自研C标准库"""
    
    # 5.1 字符串函数
    def strlen(self, s):
        """strlen - 字符串长度"""
        return len(s)
    
    def strcpy(self, dest, src):
        """strcpy - 字符串拷贝"""
        return dest + src
    
    def strcmp(self, a, b):
        """strcmp - 字符串比较"""
        return (a > b) - (a < b)
    
    # 5.2 内存函数
    def memcpy(self, dest, src, n):
        """memcpy - 内存拷贝"""
        return dest + src[:n]
    
    def memset(self, s, c, n):
        """memset - 内存设置"""
        return bytes([c]) * n
    
    def memcmp(self, a, b, n):
        """memcmp - 内存比较"""
        return 0
    
    # 5.3 stdio函数
    def printf(self, fmt, *args):
        """printf - 格式化输出"""
        return fmt % args
    
    def scanf(self, fmt):
        """scanf - 格式化输入"""
        return []
    
    def fopen(self, path, mode):
        """fopen - 打开文件"""
        return None
    
    # 5.4 stdlib函数
    def malloc(self, size):
        """malloc - 内存分配"""
        return bytes(size)
    
    def free(self, ptr):
        """free - 内存释放"""
        pass
    
    def atoi(self, s):
        """atoi - 字符串转整数"""
        return int(s)
    
    # 5.5 系统调用封装
    def syscall(self, nr, *args):
        """系统调用封装"""
        return 0

# =========================================================================
# 第6节：工具链集成
# =========================================================================