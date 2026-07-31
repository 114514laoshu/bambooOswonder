# ============================================================================
# Module: core/assembler/x64_assembler.py
# 模块：core/assembler/x64_assembler.py
# Description: Main x86-64 assembler class (migrated from X64Compiler)
# 描述：主 x86-64 汇编器类（从 X64Compiler 迁移）
# ============================================================================

"""
x86-64 Assembler main class.
x86-64 汇编器主类。

This class is migrated from kernel/bamboo_os_core.py X64Compiler.
All instruction generation methods are preserved.
"""

import struct
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

from core.assembler.registers import REG64, REG32, REG16, REG8
from core.assembler.label import Label


class X64Assembler:
    """
    x86-64 Assembler - generates machine code for Bamboo OS kernel.
    x86-64 汇编器 - 为 Bamboo OS 内核生成机器码。

    This class provides methods to emit x86-64 instructions,
    handle relocations, and manage labels.
    该类提供生成 x86-64 指令、处理重定位和管理标签的方法。
    """

    # Register tables / 寄存器表
    REG64 = REG64
    REG32 = REG32
    REG16 = REG16
    REG8 = REG8

    def __init__(self):
        """Initialize assembler / 初始化汇编器"""
        # Code generation buffers / 代码生成缓冲区
        self.code = bytearray()
        self.rodata_section = bytearray()
        self.data_section = bytearray()
        self.bss_section = bytearray()

        # Labels and relocations / 标签和重定位
        self.labels: Dict[str, Label] = {}
        self.relocations: List[Tuple[int, str, str]] = []

        # RODATA labels / RODATA 标签
        self.rodata_labels: Dict[str, int] = {}
        self.data_labels: Dict[str, int] = {}

        # Code origin (for relocation) / 代码起始地址（用于重定位）
        self.code_start_addr = 0x100000

    # =========================================================================
    # Low-level emit methods / 底层发射方法
    # =========================================================================

    def emit(self, *args):
        """Emit raw bytes to code buffer / 发射原始字节到代码缓冲区"""
        for b in args:
            if isinstance(b, (bytes, bytearray)):
                self.code.extend(b)
            else:
                self.code.append(b & 0xFF)

    def emit64(self, v):
        """Emit 64-bit little-endian value / 发射 64 位小端值"""
        self.code.extend(struct.pack('<Q', v & 0xFFFFFFFFFFFFFFFF))

    def emit32(self, v):
        """Emit 32-bit little-endian value / 发射 32 位小端值"""
        self.code.extend(struct.pack('<I', v & 0xFFFFFFFF))

    def emit16(self, v):
        """Emit 16-bit little-endian value / 发射 16 位小端值"""
        self.code.extend(struct.pack('<H', v & 0xFFFF))

    def emit_bytes(self, bytes_list):
        """Emit list of bytes / 发射字节列表"""
        for b in bytes_list:
            self.emit(b)

    # =========================================================================
    # REX prefix / REX 前缀
    # =========================================================================

    def rex(self, w=1, r=0, x=0, b=0):
        """Generate REX prefix byte / 生成 REX 前缀字节"""
        v = 0x40 | (w << 3) | (r << 2) | (x << 1) | b
        self.emit(v)

    def need_rex_for_reg(self, reg):
        """Check if REX is needed for a register / 检查寄存器是否需要 REX"""
        return reg >= 8

    def rex_prefix(self, reg=0, rm=0, index=0, w=1):
        """Generate REX prefix with full W/R/X/B bits / 生成完整的 REX 前缀"""
        r = 1 if reg >= 8 else 0
        x = 1 if index >= 8 else 0
        b = 1 if rm >= 8 else 0
        self.rex(w=w, r=r, x=x, b=b)

    # =========================================================================
    # ModRM and SIB / ModRM 和 SIB
    # =========================================================================

    def modrm(self, mod, reg, rm):
        """Generate ModR/M byte / 生成 ModR/M 字节"""
        if mod == 0 and rm == 5:
            self.emit(((mod & 3) << 6) | ((reg & 7) << 3) | (rm & 7))
            return
        if rm == 4:
            self.emit(((mod & 3) << 6) | ((reg & 7) << 3) | 4)
            return
        self.emit(((mod & 3) << 6) | ((reg & 7) << 3) | (rm & 7))

    def sib(self, scale, index, base):
        """Generate SIB byte / 生成 SIB 字节"""
        self.emit(((scale & 3) << 6) | ((index & 7) << 3) | (base & 7))

    # =========================================================================
    # Labels / 标签
    # =========================================================================

    def label(self, name):
        """Define a label at current code position / 在当前代码位置定义标签"""
        if name not in self.labels:
            self.labels[name] = Label(name)
        self.labels[name].addr = len(self.code)

    def label_addr(self, name):
        """Get label address / 获取标签地址"""
        if name in self.labels and self.labels[name].addr is not None:
            return self.labels[name].addr
        return None

    # =========================================================================
    # MOV instructions / MOV 指令
    # =========================================================================

    def mov_r64_imm(self, reg, imm):
        """MOV r64, imm64 / MOV r64, 立即数64"""
        if isinstance(imm, str):
            self.rex_prefix(rm=reg, w=1)
            self.emit(0xB8 + (reg & 7))
            self.relocations.append((len(self.code), imm, 'abs64'))
            self.emit64(0)
        else:
            self.rex_prefix(rm=reg, w=1)
            self.emit(0xB8 + (reg & 7))
            self.emit64(imm)

    def mov_r64_label(self, reg, name):
        """MOV r64, label address / MOV r64, 标签地址"""
        self.mov_r64_imm(reg, name)

    def mov_rr(self, dst, src):
        """MOV r64, r64 / MOV r64, r64"""
        self.rex_prefix(reg=src, rm=dst, w=1)
        self.emit(0x89)
        self.modrm(3, src, dst)

    def mov_m_r(self, addr_or_label, src):
        """MOV [addr], r64 / MOV [地址], r64"""
        if isinstance(addr_or_label, str):
            self.rex_prefix(reg=src, w=1)
            self.emit(0x89)
            self.modrm(0, src, 5)
            self.relocations.append((len(self.code), addr_or_label, 'rip32'))
            self.emit32(0)
        elif isinstance(addr_or_label, int):
            self.rex_prefix(reg=src, rm=addr_or_label, w=1)
            self.emit(0x89)
            self.modrm(0, src, addr_or_label)
        else:
            self.rex_prefix(reg=src, rm=addr_or_label, w=1)
            self.emit(0x89)
            self.modrm(0, src, addr_or_label)

    def mov_r_m(self, reg, addr_or_label):
        """MOV r64, [addr] / MOV r64, [地址]"""
        if isinstance(addr_or_label, str):
            self.rex_prefix(reg=reg, w=1)
            self.emit(0x8B)
            self.modrm(0, reg, 5)
            self.relocations.append((len(self.code), addr_or_label, 'rip32'))
            self.emit32(0)
        elif isinstance(addr_or_label, int):
            self.rex_prefix(reg=reg, rm=addr_or_label, w=1)
            self.emit(0x8B)
            self.modrm(0, reg, addr_or_label)
        else:
            self.rex_prefix(reg=reg, rm=addr_or_label, w=1)
            self.emit(0x8B)
            self.modrm(0, reg, addr_or_label)

    def mov_r_m_offset(self, reg, base, offset):
        """MOV r64, [base + offset] / MOV r64, [基址 + 偏移]"""
        self.rex_prefix(reg=reg, rm=base, w=1)
        self.emit(0x8B)
        if -128 <= offset < 128:
            self.modrm(1, reg, base)
            self.emit(offset & 0xFF)
        else:
            self.modrm(2, reg, base)
            self.emit32(offset)

    def mov_m_offset_r(self, base, offset, src):
        """MOV [base + offset], r64 / MOV [基址 + 偏移], r64"""
        self.rex_prefix(reg=src, rm=base, w=1)
        self.emit(0x89)
        if -128 <= offset < 128:
            self.modrm(1, src, base)
            self.emit(offset & 0xFF)
        else:
            self.modrm(2, src, base)
            self.emit32(offset)

    def mov_m_offset_r16(self, base, offset, src):
        """MOV [base + offset], r16 / MOV [基址 + 偏移], r16"""
        self.emit(0x66)
        if src >= 8:
            self.emit(0x41)
        self.emit(0x89)
        if -128 <= offset < 128:
            self.modrm(1, src & 7, base & 7)
            self.emit(offset & 0xFF)
        else:
            self.modrm(2, src & 7, base & 7)
            self.emit32(offset)

    def mov_m_offset_r32(self, base, offset, src):
        """MOV [base + offset], r32 / MOV [基址 + 偏移], r32"""
        if src >= 8:
            self.emit(0x41)
        self.emit(0x89)
        if -128 <= offset < 128:
            self.modrm(1, src & 7, base & 7)
            self.emit(offset & 0xFF)
        else:
            self.modrm(2, src & 7, base & 7)
            self.emit32(offset)

    def mov_m_offset_r8(self, base, offset, src):
        """MOV [base + offset], r8 / MOV [基址 + 偏移], r8"""
        if src >= 4:
            self.emit(0x40)
        self.emit(0x88)
        if -128 <= offset < 128:
            self.modrm(1, src & 7, base & 7)
            self.emit(offset & 0xFF)
        else:
            self.modrm(2, src & 7, base & 7)
            self.emit32(offset)

    def mov_m_offset_imm32(self, base, offset, imm):
        """MOV [base + offset], imm32 / MOV [基址 + 偏移], 立即数32"""
        self.rex_prefix(rm=base, w=1)
        self.emit(0xC7)
        if -128 <= offset < 128:
            self.modrm(1, 0, base)
            self.emit(offset & 0xFF)
        else:
            self.modrm(2, 0, base)
            self.emit32(offset)
        self.emit32(imm)

    def mov_r64_m_offset(self, dst, base, offset):
        """MOV dst, [base + offset] / MOV 目标, [基址 + 偏移]"""
        self.mov_r_m_offset(dst, base, offset)

    # =========================================================================
    # Arithmetic instructions / 算术指令
    # =========================================================================

    def _alu_rr(self, op, dst, src):
        """Internal: ALU operation on registers / 内部：寄存器 ALU 操作"""
        self.rex_prefix(reg=src, rm=dst, w=1)
        self.emit(op)
        self.modrm(3, src, dst)

    def add_rr(self, dst, src):
        self._alu_rr(0x01, dst, src)

    def sub_rr(self, dst, src):
        self._alu_rr(0x29, dst, src)

    def and_rr(self, dst, src):
        self._alu_rr(0x21, dst, src)

    def or_rr(self, dst, src):
        self._alu_rr(0x09, dst, src)

    def xor_rr(self, dst, src):
        self._alu_rr(0x31, dst, src)

    def cmp_rr(self, dst, src):
        self._alu_rr(0x39, dst, src)

    def test_rr(self, dst, src):
        self._alu_rr(0x85, dst, src)

    def _alu_r_imm(self, op1, op2, reg, imm):
        """Internal: ALU operation with immediate / 内部：立即数 ALU 操作"""
        if imm < 0:
            imm = imm & 0xFFFFFFFFFFFFFFFF
        if -0x80000000 <= imm < 0x80000000 and (imm & 0xFFFFFFFF) == imm:
            if reg == 0 and op1 == 0x81:
                self.rex_prefix(w=1)
                self.emit(op2)
                self.emit32(imm & 0xFFFFFFFF)
            else:
                self.rex_prefix(reg=reg, w=1)
                self.emit(op1)
                self.modrm(3, reg, reg)
                self.emit32(imm & 0xFFFFFFFF)
        else:
            self.mov_r64_imm(self.REG64["r10"], imm)
            self._alu_rr(op2 - 4, reg, self.REG64["r10"])

    def add_r64_imm(self, reg, imm):
        self._alu_r_imm(0x81, 0x05, reg, imm)

    def sub_r64_imm(self, reg, imm):
        self._alu_r_imm(0x81, 0x2D, reg, imm)

    def and_r64_imm(self, reg, imm):
        self._alu_r_imm(0x81, 0x25, reg, imm)

    def or_r64_imm(self, reg, imm):
        self._alu_r_imm(0x81, 0x0D, reg, imm)

    def xor_r64_imm(self, reg, imm):
        self._alu_r_imm(0x81, 0x35, reg, imm)

    def cmp_r64_imm(self, reg, imm):
        self._alu_r_imm(0x81, 0x3D, reg, imm)

    def test_r64_imm(self, reg, imm):
        self._alu_r_imm(0xF7, 0xA9, reg, imm)

    def xor_r_m_offset(self, reg, base, offset):
        """XOR reg, [base + offset] / XOR 寄存器, [基址 + 偏移]"""
        self.rex_prefix(reg=reg, rm=base, w=1)
        self.emit(0x31)
        if -128 <= offset < 128:
            self.modrm(1, reg, base)
            self.emit(offset & 0xFF)
        else:
            self.modrm(2, reg, base)
            self.emit32(offset)

    # =========================================================================
    # Shift instructions / 移位指令
    # =========================================================================

    def shl_r64_imm(self, reg, imm):
        self.rex_prefix(reg=reg, w=1)
        self.emit(0xC1)
        self.modrm(3, 4, reg)
        self.emit(imm & 0xFF)

    def shl_rr(self, dst, src):
        self.rex_prefix(reg=dst, w=1)
        self.emit(0xD3)
        self.modrm(3, 4, dst)

    def shr_rr(self, dst, src):
        self.rex_prefix(reg=dst, w=1)
        self.emit(0xD3)
        self.modrm(3, 5, dst)

    def shr_r64_imm(self, reg, imm):
        self.rex_prefix(reg=reg, w=1)
        self.emit(0xC1)
        self.modrm(3, 5, reg)
        self.emit(imm & 0xFF)

    def ror_r64_imm(self, reg, imm):
        self.rex_prefix(reg=reg, w=1)
        self.emit(0xC1)
        self.modrm(3, 1, reg)
        self.emit(imm & 0xFF)

    def rol_r64_imm(self, reg, imm):
        self.rex_prefix(reg=reg, w=1)
        self.emit(0xC1)
        self.modrm(3, 0, reg)
        self.emit(imm & 0xFF)

    # =========================================================================
    # Multiply / Divide / 乘除
    # =========================================================================

    def mul_r64(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xF7)
        self.modrm(3, 4, reg)

    def imul_rr(self, dst, src):
        self.rex_prefix(reg=dst, rm=src, w=1)
        self.emit(0x0F)
        self.emit(0xAF)
        self.modrm(3, dst, src)

    def imul_r64_imm(self, reg, imm):
        self.rex_prefix(reg=reg, rm=reg, w=1)
        if -128 <= imm < 128:
            self.emit(0x6B)
            self.modrm(3, reg, reg)
            self.emit(imm & 0xFF)
        else:
            self.emit(0x69)
            self.modrm(3, reg, reg)
            self.emit32(imm)

    def div_r64(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xF7)
        self.modrm(3, 6, reg)

    def imul_r64(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xF7)
        self.modrm(3, 5, reg)

    def neg_r64(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xF7)
        self.modrm(3, 3, reg)

    def not_r64(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xF7)
        self.modrm(3, 2, reg)

    def inc_r64(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xFF)
        self.modrm(3, 0, reg)

    def dec_r64(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xFF)
        self.modrm(3, 1, reg)

    # =========================================================================
    # Push / Pop / 压栈/弹栈
    # =========================================================================

    def push_r64(self, reg):
        if reg >= 8:
            self.emit(0x41)
        self.emit(0x50 + (reg & 7))

    def pop_r64(self, reg):
        if reg >= 8:
            self.emit(0x41)
        self.emit(0x58 + (reg & 7))

    def push_imm32(self, imm):
        self.emit(0x68)
        self.emit32(imm & 0xFFFFFFFF)

    def push_all_registers(self):
        """Push all general purpose registers / 压入所有通用寄存器"""
        self.push_r64(self.REG64["rax"])
        self.push_r64(self.REG64["rbx"])
        self.push_r64(self.REG64["rcx"])
        self.push_r64(self.REG64["rdx"])
        self.push_r64(self.REG64["rsi"])
        self.push_r64(self.REG64["rdi"])
        self.push_r64(self.REG64["rbp"])
        self.push_r64(self.REG64["r8"])
        self.push_r64(self.REG64["r9"])
        self.push_r64(self.REG64["r10"])
        self.push_r64(self.REG64["r11"])
        self.push_r64(self.REG64["r12"])
        self.push_r64(self.REG64["r13"])
        self.push_r64(self.REG64["r14"])
        self.push_r64(self.REG64["r15"])

    def pop_all_registers(self):
        """Pop all general purpose registers / 弹出所有通用寄存器"""
        self.pop_r64(self.REG64["r15"])
        self.pop_r64(self.REG64["r14"])
        self.pop_r64(self.REG64["r13"])
        self.pop_r64(self.REG64["r12"])
        self.pop_r64(self.REG64["r11"])
        self.pop_r64(self.REG64["r10"])
        self.pop_r64(self.REG64["r9"])
        self.pop_r64(self.REG64["r8"])
        self.pop_r64(self.REG64["rbp"])
        self.pop_r64(self.REG64["rdi"])
        self.pop_r64(self.REG64["rsi"])
        self.pop_r64(self.REG64["rdx"])
        self.pop_r64(self.REG64["rcx"])
        self.pop_r64(self.REG64["rbx"])
        self.pop_r64(self.REG64["rax"])

    # =========================================================================
    # Jumps / 跳转
    # =========================================================================

    def jmp_short(self, label_name):
        self.emit(0xEB)
        target = self.label_addr(label_name)
        if target is not None:
            offset = target - (len(self.code) + 1)
            self.emit(offset & 0xFF)
        else:
            self.relocations.append((len(self.code), label_name, 'jmp8'))
            self.emit(0)

    def jmp_near(self, label_name):
        self.emit(0xE9)
        target = self.label_addr(label_name)
        if target is not None:
            offset = target - (len(self.code) + 4)
            self.emit32(offset & 0xFFFFFFFF)
        else:
            self.relocations.append((len(self.code), label_name, 'jmp32'))
            self.emit32(0)

    def jmp_rr(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xFF)
        self.modrm(3, 4, reg)

    def _jcc(self, opcode, label_name):
        self.emit(0x0F, opcode)
        target = self.label_addr(label_name)
        if target is not None:
            offset = target - (len(self.code) + 4)
            self.emit32(offset & 0xFFFFFFFF)
        else:
            self.relocations.append((len(self.code), label_name, 'jcc32'))
            self.emit32(0)

    def _jcc_short(self, opcode, label_name):
        self.emit(0x70 | opcode)
        target = self.label_addr(label_name)
        if target is not None:
            offset = target - (len(self.code) + 1)
            self.emit(offset & 0xFF)
        else:
            self.relocations.append((len(self.code), label_name, 'jcc8'))
            self.emit(0)

    def jz_short(self, l):
        self._jcc_short(0x4, l)

    def jnz_short(self, l):
        self._jcc_short(0x5, l)

    def jl_short(self, l):
        self._jcc_short(0xC, l)

    def jge_short(self, l):
        self._jcc_short(0xD, l)

    def jle_short(self, l):
        self._jcc_short(0xE, l)

    def jg_short(self, l):
        self._jcc_short(0xF, l)

    def jb_short(self, l):
        self._jcc_short(0x2, l)

    def jae_short(self, l):
        self._jcc_short(0x3, l)

    def js_short(self, l):
        self._jcc_short(0x8, l)

    def jns_short(self, l):
        self._jcc_short(0x9, l)

    def jz(self, l):
        self._jcc(0x84, l)

    def jnz(self, l):
        self._jcc(0x85, l)

    def jl(self, l):
        self._jcc(0x8C, l)

    def jge(self, l):
        self._jcc(0x8D, l)

    def jle(self, l):
        self._jcc(0x8E, l)

    def jg(self, l):
        self._jcc(0x8F, l)

    def js(self, l):
        self._jcc(0x88, l)

    def jns(self, l):
        self._jcc(0x89, l)

    def jb(self, l):
        self._jcc(0x82, l)

    def jc(self, l):
        self._jcc(0x82, l)

    def jae(self, l):
        self._jcc(0x83, l)

    def ja(self, l):
        self._jcc(0x87, l)

    def ja_short(self, l):
        self._jcc_short(0x7, l)

    def jbe_short(self, l):
        self._jcc_short(0x6, l)

    def jnc(self, l):
        self.ja(l)

    # =========================================================================
    # Call / Return / 调用/返回
    # =========================================================================

    def call(self, label_name):
        self.emit(0xE8)
        target = self.label_addr(label_name)
        if target is not None:
            offset = target - (len(self.code) + 4)
            self.emit32(offset & 0xFFFFFFFF)
        else:
            self.relocations.append((len(self.code), label_name, 'call32'))
            self.emit32(0)

    def call_rr(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0xFF)
        self.modrm(3, 2, reg)

    def ret(self):
        self.emit(0xC3)

    def retf(self):
        self.emit(0x48, 0xCB)

    # =========================================================================
    # I/O instructions / I/O 指令
    # =========================================================================

    def inb(self):
        self.emit(0xEC)

    def inw(self):
        self.emit(0x66, 0xED)

    def inl(self):
        self.emit(0xED)

    def outb(self):
        self.emit(0xEE)

    def outw(self):
        self.emit(0x66, 0xEF)

    def outl(self):
        self.emit(0xEF)

    # =========================================================================
    # System instructions / 系统指令
    # =========================================================================

    def cli(self):
        self.emit(0xFA)

    def sti(self):
        self.emit(0xFB)

    def hlt(self):
        self.emit(0xF4)

    def nop(self):
        self.emit(0x90)

    def iretq(self):
        self.emit(0x48, 0xCF)

    def swapgs(self):
        self.emit(0x0F, 0x01, 0xF8)

    def syscall(self):
        self.emit(0x0F, 0x05)

    def sysret(self):
        self.emit(0x0F, 0x07)

    def sysretq(self):
        self.emit(0x48, 0x0F, 0x07)

    def int_n(self, n):
        self.emit(0xCD, n)

    def int0x80(self):
        self.emit(0xCD, 0x80)

    def lidt(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0x0F, 0x01)
        self.modrm(0, 3, reg)

    def lgdt(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0x0F, 0x01)
        self.modrm(0, 2, reg)

    def ltr(self, reg):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0x0F, 0x00)
        self.modrm(3, 3, reg)

    def cpuid(self):
        self.emit(0x0F, 0xA2)

    def rdmsr(self):
        self.emit(0x0F, 0x32)

    def wrmsr(self):
        self.emit(0x0F, 0x30)

    # =========================================================================
    # Control registers / 控制寄存器
    # =========================================================================

    def mov_cr0_r64(self, reg):
        self.emit(0x0F, 0x22)
        self.modrm(3, 0, reg)

    def mov_cr2_r64(self, reg):
        self.emit(0x0F, 0x22)
        self.modrm(3, 2, reg)

    def mov_cr3_r64(self, reg):
        self.emit(0x0F, 0x22)
        self.modrm(3, 3, reg)

    def mov_cr4_r64(self, reg):
        self.emit(0x0F, 0x22)
        self.modrm(3, 4, reg)

    def mov_r64_cr0(self, reg):
        self.emit(0x0F, 0x20)
        self.modrm(3, 0, reg)

    def mov_r64_cr2(self, reg):
        self.emit(0x0F, 0x20)
        self.modrm(3, 2, reg)

    def mov_r64_cr3(self, reg):
        self.emit(0x0F, 0x20)
        self.modrm(3, 3, reg)

    def mov_r64_cr4(self, reg):
        self.emit(0x0F, 0x20)
        self.modrm(3, 4, reg)

    def mov_dr0_r64(self, reg):
        self.emit(0x0F, 0x23)
        self.modrm(3, 0, reg)

    # =========================================================================
    # Segment registers / 段寄存器
    # =========================================================================

    def mov_ds_ax(self):
        self.emit(0x8E, 0xD8)

    def mov_es_ax(self):
        self.emit(0x8E, 0xC0)

    def mov_fs_ax(self):
        self.emit(0x8E, 0xE0)

    def mov_gs_ax(self):
        self.emit(0x8E, 0xE8)

    def mov_ss_ax(self):
        self.emit(0x8E, 0xD0)

    # =========================================================================
    # String operations / 字符串操作
    # =========================================================================

    def rep_movsb(self):
        self.emit(0xF3, 0xA4)

    def rep_movsd(self):
        self.emit(0xF3, 0xA5)

    def rep_movsq(self):
        self.emit(0xF3, 0x48, 0xA5)

    def rep_stosd(self):
        self.emit(0xF3, 0xAB)

    def rep_stosq(self):
        self.emit(0xF3, 0x48, 0xAB)

    def cld(self):
        self.emit(0xFC)

    def std(self):
        self.emit(0xFD)

    # =========================================================================
    # LEA / 取地址
    # =========================================================================

    def lea_r64_label(self, reg, name):
        self.rex_prefix(reg=reg, w=1)
        self.emit(0x8D)
        self.modrm(0, reg, 5)
        self.relocations.append((len(self.code), name, 'rip32'))
        self.emit32(0)

    # =========================================================================
    # Conditional moves / 条件移动
    # =========================================================================

    def cmovz_rr(self, dst, src):
        self.rex_prefix(reg=src, rm=dst, w=1)
        self.emit(0x0F, 0x44)
        self.modrm(3, src, dst)

    def cmovnz_rr(self, dst, src):
        self.rex_prefix(reg=src, rm=dst, w=1)
        self.emit(0x0F, 0x45)
        self.modrm(3, src, dst)

    # =========================================================================
    # Set byte on condition / 条件设置字节
    # =========================================================================

    def sete_r8(self, reg):
        self.emit(0x0F, 0x94)
        self.modrm(3, 0, reg)

    def setne_r8(self, reg):
        self.emit(0x0F, 0x95)
        self.modrm(3, 0, reg)

    def setc_al(self):
        self.emit(0x0F, 0x92, 0xC0)

    # =========================================================================
    # Atomic operations / 原子操作
    # =========================================================================

    def lock(self):
        self.emit(0xF0)

    def xchg_rr(self, dst, src):
        if dst == 0:
            self.rex_prefix(rm=src, w=1)
            self.emit(0x90 + (src & 7))
        else:
            self.rex_prefix(reg=src, rm=dst, w=1)
            self.emit(0x87)
            self.modrm(3, src, dst)

    def xchg_m_r(self, addr_or_label, src):
        if isinstance(addr_or_label, str):
            self.rex_prefix(reg=src, w=1)
            self.emit(0x87)
            self.modrm(0, src, 5)
            self.relocations.append((len(self.code), addr_or_label, 'rip32'))
            self.emit32(0)
        elif isinstance(addr_or_label, int):
            self.rex_prefix(reg=src, rm=addr_or_label, w=1)
            self.emit(0x87)
            self.modrm(0, src, addr_or_label)
        else:
            self.rex_prefix(reg=src, rm=addr_or_label, w=1)
            self.emit(0x87)
            self.modrm(0, src, addr_or_label)

    def cmpxchg_rr(self, dst, src):
        self.rex_prefix(reg=src, rm=dst, w=1)
        self.emit(0x0F, 0xB1)
        self.modrm(3, src, dst)

    def cmpxchg_r64_m(self, reg, mem_reg):
        self.emit(0xF0)
        self.rex_prefix(reg=reg, rm=mem_reg, w=1)
        self.emit(0x0F, 0xB1)
        self.modrm(0, reg, mem_reg)

    def xadd_r64_m(self, reg, mem_reg):
        self.emit(0xF0)
        self.rex_prefix(reg=reg, rm=mem_reg, w=1)
        self.emit(0x0F, 0xC1)
        self.modrm(0, reg, mem_reg)

    # =========================================================================
    # Bit operations / 位操作
    # =========================================================================

    def bts_rr(self, dst, src):
        self.rex_prefix(reg=src, rm=dst, w=0)
        self.emit(0x0F, 0xAB)
        self.modrm(3, src, dst)

    def bt_rr(self, dst, src):
        self.rex_prefix(reg=src, rm=dst, w=0)
        self.emit(0x0F, 0xA3)
        self.modrm(3, src, dst)

    def bts_r64_imm(self, reg, bit):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0x0F, 0xBA)
        self.modrm(3, 5, reg)
        self.emit(bit & 0xFF)

    def btr_r64_imm(self, reg, bit):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0x0F, 0xBA)
        self.modrm(3, 6, reg)
        self.emit(bit & 0xFF)

    def bt_r64_imm(self, reg, bit):
        self.rex_prefix(rm=reg, w=1)
        self.emit(0x0F, 0xBA)
        self.modrm(3, 4, reg)
        self.emit(bit & 0xFF)

    def bt_m_imm(self, mem_reg, bit):
        self.rex_prefix(rm=mem_reg, w=1)
        self.emit(0x0F, 0xBA)
        self.modrm(0, 4, mem_reg)
        self.emit(bit & 0xFF)

    def bts_m_imm(self, mem_reg, bit):
        self.rex_prefix(rm=mem_reg, w=1)
        self.emit(0x0F, 0xBA)
        self.modrm(0, 5, mem_reg)
        self.emit(bit & 0xFF)

    # =========================================================================
    # Memory barriers / 内存屏障
    # =========================================================================

    def mfence(self):
        self.emit(0x0F, 0xAE, 0xF0)

    def lfence(self):
        self.emit(0x0F, 0xAE, 0xE8)

    def sfence(self):
        self.emit(0x0F, 0xAE, 0xF8)

    # =========================================================================
    # FPU / SSE / FPU 和 SSE
    # =========================================================================

    def fxsave_m(self, mem_reg):
        self.emit(0x0F, 0xAE)
        self.modrm(0, 0, mem_reg)

    def fxrstor_m(self, mem_reg):
        self.emit(0x0F, 0xAE)
        self.modrm(0, 1, mem_reg)

    # =========================================================================
    # TLB / TLB 操作
    # =========================================================================

    def invalidate_tlb(self):
        self.mov_r64_cr3(self.REG64["rax"])
        self.mov_cr3_r64(self.REG64["rax"])

    def invlpg(self, addr_reg):
        self.emit(0x0F, 0x01)
        self.modrm(0, 7, addr_reg)

    # =========================================================================
    # Paging / 分页
    # =========================================================================

    def enable_paging(self):
        self.mov_r64_cr0(self.REG64["rax"])
        self.or_r64_imm(self.REG64["rax"], 1 << 31)
        self.mov_cr0_r64(self.REG64["rax"])

    def enable_pae(self):
        self.mov_r64_cr4(self.REG64["rax"])
        self.or_r64_imm(self.REG64["rax"], 1 << 5)
        self.mov_cr4_r64(self.REG64["rax"])

    def enable_long_mode(self):
        self.mov_r64_imm(self.REG64["rcx"], 0xC0000080)
        self.rdmsr()
        self.or_r64_imm(self.REG64["rax"], 1 << 8)
        self.wrmsr()

    def setup_cr3(self, pml4_addr):
        self.mov_r64_imm(self.REG64["rax"], pml4_addr)
        self.mov_cr3_r64(self.REG64["rax"])

    # =========================================================================
    # GDT / IDT 设置
    # =========================================================================

    def setup_gdt_register(self, gdt_addr, gdt_limit):
        self.sub_r64_imm(self.REG64["rsp"], 16)
        self.mov_r64_imm(self.REG64["rax"], gdt_limit)
        self.mov_m_offset_r16(self.REG64["rsp"], 0, self.REG64["rax"])
        self.mov_r64_imm(self.REG64["rax"], gdt_addr)
        self.mov_m_offset_r64(self.REG64["rsp"], 2, self.REG64["rax"])
        self.lgdt(self.REG64["rsp"])
        self.add_r64_imm(self.REG64["rsp"], 16)

    def setup_idt_register(self, idt_addr, idt_limit):
        self.sub_r64_imm(self.REG64["rsp"], 16)
        self.mov_r64_imm(self.REG64["rax"], idt_limit)
        self.mov_m_offset_r16(self.REG64["rsp"], 0, self.REG64["rax"])
        self.mov_r64_imm(self.REG64["rax"], idt_addr)
        self.mov_m_offset_r64(self.REG64["rsp"], 2, self.REG64["rax"])
        self.lidt(self.REG64["rsp"])
        self.add_r64_imm(self.REG64["rsp"], 16)

    # =========================================================================
    # RODATA / DATA sections / RODATA / DATA 段
    # =========================================================================

    def rodata_string(self, name, s):
        """Add string to RODATA section / 添加字符串到 RODATA 段"""
        self.rodata_labels[name] = len(self.rodata_section)
        for ch in s:
            self.rodata_section.append(ord(ch))
        self.rodata_section.append(0)

    def rodata_bytes(self, name, data):
        """Add bytes to RODATA section / 添加字节到 RODATA 段"""
        self.rodata_labels[name] = len(self.rodata_section)
        self.rodata_section.extend(data)

    def rodata_qwords(self, name, values):
        """Add qwords to RODATA section / 添加 qword 到 RODATA 段"""
        self.rodata_labels[name] = len(self.rodata_section)
        for v in values:
            self.rodata_section.extend(struct.pack('<Q', v & 0xFFFFFFFFFFFFFFFF))

    def data_string(self, name, s):
        """Add string to DATA section / 添加字符串到 DATA 段"""
        self.data_labels[name] = len(self.data_section)
        for ch in s:
            self.data_section.append(ord(ch))
        self.data_section.append(0)

    def data_bytes(self, name, data):
        """Add bytes to DATA section / 添加字节到 DATA 段"""
        self.data_labels[name] = len(self.data_section)
        self.data_section.extend(data)

    def data_qwords(self, name, values):
        """Add qwords to DATA section / 添加 qword 到 DATA 段"""
        self.data_labels[name] = len(self.data_section)
        for v in values:
            self.data_section.extend(struct.pack('<Q', v & 0xFFFFFFFFFFFFFFFF))

    def data_reserve(self, name, size):
        """Reserve space in DATA section / 在 DATA 段预留空间"""
        self.data_labels[name] = len(self.data_section)
        self.data_section.extend(b'\x00' * size)

    # =========================================================================
    # Resolve and Save / 解析和保存
    # =========================================================================

    def resolve(self):
        """Resolve all relocations / 解析所有重定位"""
        code_size = len(self.code)
        rodata_size = len(self.rodata_section)

        for offset, label_name, rtype in self.relocations:
            if label_name in self.rodata_labels:
                addr = self.code_start_addr + code_size + self.rodata_labels[label_name]
            elif label_name in self.data_labels:
                addr = self.code_start_addr + code_size + rodata_size + self.data_labels[label_name]
            elif label_name in self.labels and self.labels[label_name].addr is not None:
                addr = self.code_start_addr + self.labels[label_name].addr
            else:
                continue

            if rtype == 'abs64':
                struct.pack_into('<Q', self.code, offset, addr)
            elif rtype == 'rip32':
                rel = addr - (self.code_start_addr + offset + 4)
                if -2147483648 <= rel <= 2147483647:
                    struct.pack_into('<i', self.code, offset, rel)
            elif rtype in ('call32', 'jmp32', 'jcc32'):
                rel = addr - (self.code_start_addr + offset + 4)
                if -2147483648 <= rel <= 2147483647:
                    struct.pack_into('<i', self.code, offset, rel)
            elif rtype == 'abs32':
                struct.pack_into('<I', self.code, offset, addr & 0xFFFFFFFF)
            elif rtype in ('jmp8', 'jcc8'):
                rel = addr - (self.code_start_addr + offset + 1)
                struct.pack_into('<b', self.code, offset, rel)

    def save(self, filename):
        """Save assembled binary to file / 保存汇编后的二进制到文件"""
        self.code_start_addr = 0x100000
        self.resolve()
        with open(filename, 'wb') as f:
            f.write(self.code)
            f.write(self.rodata_section)
            f.write(self.data_section)
        total_size = len(self.code) + len(self.rodata_section) + len(self.data_section)
        return total_size

    # =========================================================================
    # Misc utility methods / 杂项工具方法
    # =========================================================================

    def popfq(self):
        self.emit(0x9D)

    def not_al(self):
        self.emit(0xF6, 0xD0)

    def movzx_rax_al(self):
        self.emit(0x48, 0x0F, 0xB6, 0xC0)

    def pause(self):
        self.emit(0xF3, 0x90)

    def div64(self):
        self.emit(0x48, 0xF7, 0xF1)

    def emit_string(self, s):
        for ch in s:
            self.emit(ord(ch))