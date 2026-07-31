# ============================================================================
# Module: core/assembler/__init__.py
# 模块：core/assembler/__init__.py
# Description: x86-64 Assembler package for Bamboo OS kernel
# 描述：Bamboo OS 内核 x86-64 汇编器包
# ============================================================================

# Import from core implementation / 从核心实现导入
# The main X64Compiler class is in the kernel core module
# 主 X64Compiler 类位于内核核心模块中
from kernel.bamboo_os_core import X64Compiler as X64Assembler

# Register definitions / 寄存器定义
REG64 = {
    "rax": 0, "rcx": 1, "rdx": 2, "rbx": 3,
    "rsp": 4, "rbp": 5, "rsi": 6, "rdi": 7,
    "r8": 8, "r9": 9, "r10": 10, "r11": 11,
    "r12": 12, "r13": 13, "r14": 14, "r15": 15,
}

REG32 = {
    "eax": 0, "ecx": 1, "edx": 2, "ebx": 3,
    "esp": 4, "ebp": 5, "esi": 6, "edi": 7,
    "r8d": 8, "r9d": 9, "r10d": 10, "r11d": 11,
    "r12d": 12, "r13d": 13, "r14d": 14, "r15d": 15,
}

REG16 = {
    "ax": 0, "cx": 1, "dx": 2, "bx": 3,
    "sp": 4, "bp": 5, "si": 6, "di": 7,
    "r8w": 8, "r9w": 9, "r10w": 10, "r11w": 11,
    "r12w": 12, "r13w": 13, "r14w": 14, "r15w": 15,
}

REG8 = {
    "al": 0, "cl": 1, "dl": 2, "bl": 3,
    "spl": 4, "bpl": 5, "sil": 6, "dil": 7,
    "r8b": 8, "r9b": 9, "r10b": 10, "r11b": 11,
    "r12b": 12, "r13b": 13, "r14b": 14, "r15b": 15,
}

SEGMENT_REGS = {
    "cs": 0, "ds": 1, "es": 2, "fs": 3, "gs": 4, "ss": 5,
}

__all__ = [
    'X64Assembler',
    'REG64', 'REG32', 'REG16', 'REG8', 'SEGMENT_REGS',
]
