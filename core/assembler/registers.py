# ============================================================================
# Module: core/assembler/registers.py
# 模块：core/assembler/registers.py
# Description: x86-64 register definitions for Bamboo OS assembler
# 描述：Bamboo OS 汇编器 x86-64 寄存器定义
# ============================================================================

# 64-bit general purpose registers / 64位通用寄存器
REG64 = {
    "rax": 0, "rcx": 1, "rdx": 2, "rbx": 3,
    "rsp": 4, "rbp": 5, "rsi": 6, "rdi": 7,
    "r8": 8, "r9": 9, "r10": 10, "r11": 11,
    "r12": 12, "r13": 13, "r14": 14, "r15": 15
}

# 32-bit general purpose registers / 32位通用寄存器
REG32 = {
    "eax": 0, "ecx": 1, "edx": 2, "ebx": 3,
    "esp": 4, "ebp": 5, "esi": 6, "edi": 7,
    "r8d": 8, "r9d": 9, "r10d": 10, "r11d": 11,
    "r12d": 12, "r13d": 13, "r14d": 14, "r15d": 15
}

# 16-bit general purpose registers / 16位通用寄存器
REG16 = {
    "ax": 0, "cx": 1, "dx": 2, "bx": 3,
    "sp": 4, "bp": 5, "si": 6, "di": 7,
    "r8w": 8, "r9w": 9, "r10w": 10, "r11w": 11,
    "r12w": 12, "r13w": 13, "r14w": 14, "r15w": 15
}

# 8-bit general purpose registers / 8位通用寄存器
REG8 = {
    "al": 0, "cl": 1, "dl": 2, "bl": 3,
    "ah": 4, "ch": 5, "dh": 6, "bh": 7,
    "r8b": 8, "r9b": 9, "r10b": 10, "r11b": 11,
    "r12b": 12, "r13b": 13, "r14b": 14, "r15b": 15
}

# Segment registers / 段寄存器
SEGMENT_REGS = {
    "es": 0, "cs": 1, "ss": 2, "ds": 3,
    "fs": 4, "gs": 5
}

# Control registers / 控制寄存器
CR_REGS = {
    "cr0": 0, "cr2": 2, "cr3": 3, "cr4": 4
}

# Debug registers / 调试寄存器
DR_REGS = {
    "dr0": 0, "dr1": 1, "dr2": 2, "dr3": 3,
    "dr6": 6, "dr7": 7
}

# REX prefix bits / REX前缀位
REX_W = 0x48  # 64-bit operand size / 64位操作数大小
REX_R = 0x44  # Extension of MODRM.reg field / MODRM.reg字段扩展
REX_X = 0x42  # Extension of SIB.index field / SIB.index字段扩展
REX_B = 0x41  # Extension of MODRM.rm or SIB.base field / MODRM.rm或SIB.base字段扩展

# ModRM byte fields / ModRM字节字段
MODRM_MOD_MASK = 0xC0  # Mode field (bits 7-6) / 模式字段
MODRM_REG_MASK = 0x38  # Register field (bits 5-3) / 寄存器字段
MODRM_RM_MASK = 0x07   # R/M field (bits 2-0) / R/M字段

# SIB byte fields / SIB字节字段
SIB_SCALE_MASK = 0xC0  # Scale field (bits 7-6) / 比例字段
SIB_INDEX_MASK = 0x38  # Index field (bits 5-3) / 索引字段
SIB_BASE_MASK = 0x07   # Base field (bits 2-0) / 基址字段
