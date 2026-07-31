#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: tests/unit/test_assembler.py
# 模块：tests/unit/test_assembler.py
# Description: Unit tests for x86-64 assembler
# 描述：x86-64 汇编器单元测试
# ============================================================================

import sys
import os
import unittest

# Add project root to path / 将项目根目录添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestX64Assembler(unittest.TestCase):
    """Test cases for X64Assembler / X64Assembler 测试用例"""

    def setUp(self):
        """Set up test / 设置测试"""
        from core.assembler import X64Assembler
        self.asm = X64Assembler()

    def test_initial_state(self):
        """Test initial assembler state / 测试初始汇编器状态"""
        self.assertEqual(len(self.asm.code), 0)
        self.assertEqual(len(self.asm.labels), 0)
        self.assertIsNotNone(self.asm.REG64)

    def test_register_definitions(self):
        """Test register definitions / 测试寄存器定义"""
        self.assertEqual(self.asm.REG64["rax"], 0)
        self.assertEqual(self.asm.REG64["rbx"], 3)
        self.assertEqual(self.asm.REG64["rsp"], 4)
        self.assertEqual(self.asm.REG64["r15"], 15)

    def test_emit_byte(self):
        """Test emitting single byte / 测试发射单字节"""
        self.asm.emit(0x90)  # NOP
        self.assertEqual(len(self.asm.code), 1)
        self.assertEqual(self.asm.code[0], 0x90)

    def test_emit_multiple_bytes(self):
        """Test emitting multiple bytes / 测试发射多字节"""
        self.asm.emit(0x48, 0xC7, 0xC0, 0x2A, 0x00, 0x00, 0x00)
        self.assertEqual(len(self.asm.code), 7)

    def test_label_creation(self):
        """Test label creation / 测试标签创建"""
        self.asm.label("test_label")
        self.assertIn("test_label", self.asm.labels)

    def test_nop_instruction(self):
        """Test NOP instruction / 测试 NOP 指令"""
        self.asm.nop()
        self.assertEqual(len(self.asm.code), 1)
        self.assertEqual(self.asm.code[0], 0x90)

    def test_hlt_instruction(self):
        """Test HLT instruction / 测试 HLT 指令"""
        self.asm.hlt()
        self.assertEqual(len(self.asm.code), 1)
        self.assertEqual(self.asm.code[0], 0xF4)

    def test_cli_instruction(self):
        """Test CLI instruction / 测试 CLI 指令"""
        self.asm.cli()
        self.assertEqual(len(self.asm.code), 1)
        self.assertEqual(self.asm.code[0], 0xFA)

    def test_sti_instruction(self):
        """Test STI instruction / 测试 STI 指令"""
        self.asm.sti()
        self.assertEqual(len(self.asm.code), 1)
        self.assertEqual(self.asm.code[0], 0xFB)

    def test_ret_instruction(self):
        """Test RET instruction / 测试 RET 指令"""
        self.asm.ret()
        self.assertEqual(len(self.asm.code), 1)
        self.assertEqual(self.asm.code[0], 0xC3)

    def test_mov_r64_imm(self):
        """Test MOV r64, imm64 / 测试 MOV 指令"""
        self.asm.mov_r64_imm(self.asm.REG64["rax"], 42)
        # MOV rax, imm64 is 10 bytes (REX.W + opcode + 8-byte imm)
        self.assertEqual(len(self.asm.code), 10)
        # REX.W prefix / REX.W 前缀
        self.assertEqual(self.asm.code[0], 0x48)
        # Opcode / 操作码
        self.assertEqual(self.asm.code[1], 0xB8)

    def test_push_r64(self):
        """Test PUSH r64 / 测试 PUSH 指令"""
        self.asm.push_r64(self.asm.REG64["rax"])
        self.assertEqual(len(self.asm.code), 1)
        # PUSH rax = 0x50
        self.assertEqual(self.asm.code[0], 0x50)

    def test_pop_r64(self):
        """Test POP r64 / 测试 POP 指令"""
        self.asm.pop_r64(self.asm.REG64["rax"])
        self.assertEqual(len(self.asm.code), 1)
        # POP rax = 0x58
        self.assertEqual(self.asm.code[0], 0x58)

    def test_add_rr(self):
        """Test ADD r64, r64 / 测试 ADD 指令"""
        self.asm.add_rr(self.asm.REG64["rax"], self.asm.REG64["rbx"])
        # ADD rax, rbx = REX.W + 0x01 + ModRM
        self.assertEqual(len(self.asm.code), 3)
        self.assertEqual(self.asm.code[0], 0x48)  # REX.W
        self.assertEqual(self.asm.code[1], 0x01)  # ADD r/m64, r64

    def test_sub_rr(self):
        """Test SUB r64, r64 / 测试 SUB 指令"""
        self.asm.sub_rr(self.asm.REG64["rax"], self.asm.REG64["rbx"])
        self.assertEqual(len(self.asm.code), 3)
        self.assertEqual(self.asm.code[0], 0x48)  # REX.W
        self.assertEqual(self.asm.code[1], 0x29)  # SUB r/m64, r64

    def test_and_rr(self):
        """Test AND r64, r64 / 测试 AND 指令"""
        self.asm.and_rr(self.asm.REG64["rax"], self.asm.REG64["rbx"])
        self.assertEqual(len(self.asm.code), 3)
        self.assertEqual(self.asm.code[0], 0x48)  # REX.W
        self.assertEqual(self.asm.code[1], 0x21)  # AND r/m64, r64

    def test_or_rr(self):
        """Test OR r64, r64 / 测试 OR 指令"""
        self.asm.or_rr(self.asm.REG64["rax"], self.asm.REG64["rbx"])
        self.assertEqual(len(self.asm.code), 3)
        self.assertEqual(self.asm.code[0], 0x48)  # REX.W
        self.assertEqual(self.asm.code[1], 0x09)  # OR r/m64, r64

    def test_xor_rr(self):
        """Test XOR r64, r64 / 测试 XOR 指令"""
        self.asm.xor_rr(self.asm.REG64["rax"], self.asm.REG64["rbx"])
        self.assertEqual(len(self.asm.code), 3)
        self.assertEqual(self.asm.code[0], 0x48)  # REX.W
        self.assertEqual(self.asm.code[1], 0x31)  # XOR r/m64, r64

    def test_cmp_rr(self):
        """Test CMP r64, r64 / 测试 CMP 指令"""
        self.asm.cmp_rr(self.asm.REG64["rax"], self.asm.REG64["rbx"])
        self.assertEqual(len(self.asm.code), 3)
        self.assertEqual(self.asm.code[0], 0x48)  # REX.W
        self.assertEqual(self.asm.code[1], 0x39)  # CMP r/m64, r64

    def test_inc_r64(self):
        """Test INC r64 / 测试 INC 指令"""
        self.asm.inc_r64(self.asm.REG64["rax"])
        self.assertGreater(len(self.asm.code), 0)

    def test_dec_r64(self):
        """Test DEC r64 / 测试 DEC 指令"""
        self.asm.dec_r64(self.asm.REG64["rax"])
        self.assertGreater(len(self.asm.code), 0)

    def test_neg_r64(self):
        """Test NEG r64 / 测试 NEG 指令"""
        self.asm.neg_r64(self.asm.REG64["rax"])
        self.assertGreater(len(self.asm.code), 0)

    def test_not_r64(self):
        """Test NOT r64 / 测试 NOT 指令"""
        self.asm.not_r64(self.asm.REG64["rax"])
        self.assertGreater(len(self.asm.code), 0)

    def test_jmp_short(self):
        """Test short JMP / 测试短跳转"""
        self.asm.label("target")
        self.asm.nop()
        self.asm.jmp_short("target")
        self.assertGreater(len(self.asm.code), 0)

    def test_call(self):
        """Test CALL instruction / 测试 CALL 指令"""
        self.asm.label("function")
        self.asm.nop()
        self.asm.call("function")
        self.assertGreater(len(self.asm.code), 0)

    def test_create_gdt_entry(self):
        """Test GDT entry creation / 测试 GDT 条目创建"""
        entry = self.asm.create_gdt_entry(0, 0xFFFFF, 0x9A, 0xA0)
        self.assertIsNotNone(entry)
        self.assertNotEqual(entry, 0)

    def test_create_idt_entry(self):
        """Test IDT entry creation / 测试 IDT 条目创建"""
        low, high = self.asm.create_idt_entry(0x100000, 0x08, 0, 0x8E)
        self.assertIsNotNone(low)
        self.assertIsNotNone(high)

    def test_rodata_string(self):
        """Test rodata string / 测试只读数据字符串"""
        self.asm.rodata_string("hello", "Hello, World!")
        self.assertGreater(len(self.asm.rodata_section), 0)

    def test_data_reserve(self):
        """Test data reservation / 测试数据预留"""
        self.asm.data_reserve("buffer", 1024)
        self.assertGreater(len(self.asm.data_section), 0)

    def test_resolve(self):
        """Test label resolution / 测试标签解析"""
        self.asm.label("start")
        self.asm.nop()
        self.asm.label("end")
        # Should not raise / 不应抛出异常
        self.asm.resolve()


class TestRegisters(unittest.TestCase):
    """Test register definitions / 寄存器定义测试"""

    def test_reg64_count(self):
        """Test 64-bit register count / 测试 64 位寄存器数量"""
        from core.assembler.registers import REG64
        self.assertEqual(len(REG64), 16)

    def test_reg32_count(self):
        """Test 32-bit register count / 测试 32 位寄存器数量"""
        from core.assembler.registers import REG32
        self.assertEqual(len(REG32), 16)

    def test_reg16_count(self):
        """Test 16-bit register count / 测试 16 位寄存器数量"""
        from core.assembler.registers import REG16
        self.assertEqual(len(REG16), 16)

    def test_reg8_count(self):
        """Test 8-bit register count / 测试 8 位寄存器数量"""
        from core.assembler.registers import REG8
        self.assertEqual(len(REG8), 16)


if __name__ == '__main__':
    unittest.main(verbosity=2)
