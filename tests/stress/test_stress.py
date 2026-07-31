#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: tests/stress/test_stress.py
# 模块：tests/stress/test_stress.py
# Description: Stress tests for Bamboo OS components
# 描述：Bamboo OS 组件压力测试
# ============================================================================

import sys
import os
import unittest
import time
import tempfile

# Add project root to path / 将项目根目录添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestAssemblerStress(unittest.TestCase):
    """Stress tests for assembler / 汇编器压力测试"""

    def test_many_instructions(self):
        """Test generating many instructions / 测试生成大量指令"""
        from core.assembler import X64Assembler

        asm = X64Assembler()
        count = 10000

        start = time.time()
        for i in range(count):
            asm.nop()
        elapsed = time.time() - start

        self.assertEqual(len(asm.code), count)
        print(f"  Generated {count} NOPs in {elapsed:.3f}s ({count/elapsed:.0f} ops/s)")

    def test_many_labels(self):
        """Test many labels / 测试大量标签"""
        from core.assembler import X64Assembler

        asm = X64Assembler()
        count = 1000

        start = time.time()
        for i in range(count):
            asm.label(f"label_{i}")
            asm.nop()
        asm.resolve()
        elapsed = time.time() - start

        self.assertEqual(len(asm.labels), count)
        print(f"  Created {count} labels in {elapsed:.3f}s")

    def test_large_code_generation(self):
        """Test large code generation / 测试大型代码生成"""
        from core.assembler import X64Assembler

        asm = X64Assembler()
        target_size = 100 * 1024  # 100KB

        start = time.time()
        while len(asm.code) < target_size:
            asm.mov_r64_imm(asm.REG64["rax"], len(asm.code))
            asm.add_rr(asm.REG64["rax"], asm.REG64["rbx"])
            asm.push_r64(asm.REG64["rax"])
            asm.pop_r64(asm.REG64["rax"])
        elapsed = time.time() - start

        self.assertGreaterEqual(len(asm.code), target_size)
        print(f"  Generated {len(asm.code):,} bytes in {elapsed:.3f}s "
              f"({len(asm.code)/elapsed/1024:.1f} KB/s)")

    def test_label_resolution_performance(self):
        """Test label resolution performance / 测试标签解析性能"""
        from core.assembler import X64Assembler

        asm = X64Assembler()
        count = 500

        # Create many forward references / 创建许多前向引用
        for i in range(count):
            asm.jmp_near(f"label_{i}")

        for i in range(count):
            asm.label(f"label_{i}")
            asm.nop()

        start = time.time()
        asm.resolve()
        elapsed = time.time() - start

        print(f"  Resolved {count} labels in {elapsed:.3f}s")

    def test_memory_usage(self):
        """Test memory usage / 测试内存使用"""
        import sys
        from core.assembler import X64Assembler

        asm = X64Assembler()

        # Generate 1MB of code / 生成 1MB 代码
        target_size = 1024 * 1024  # 1MB
        while len(asm.code) < target_size:
            asm.nop()

        code_size = len(asm.code)
        labels_size = sys.getsizeof(asm.labels)

        print(f"  Code size: {code_size:,} bytes ({code_size/1024/1024:.2f} MB)")
        print(f"  Labels dict: {labels_size:,} bytes")

        self.assertGreaterEqual(code_size, target_size)


class TestBPPStress(unittest.TestCase):
    """Stress tests for BPP format / BPP 格式压力测试"""

    def test_large_bpp(self):
        """Test large BPP package / 测试大型 BPP 包"""
        from toolchain.bamboo_pack import BPPPackager, BPPLoader

        packager = BPPPackager()
        code_size = 1024 * 1024  # 1MB

        start = time.time()
        packager.add_code(b'\x90' * code_size)
        packager.set_flags(executable=True, gui=True)
        result = packager.build(entry_point=0)
        elapsed = time.time() - start

        self.assertGreater(len(result), code_size)
        print(f"  Built {len(result):,} byte BPP in {elapsed:.3f}s")

    def test_many_symbols(self):
        """Test BPP with many symbols / 测试带大量符号的 BPP"""
        from toolchain.bamboo_pack import BPPPackager

        packager = BPPPackager()
        packager.add_code(b'\x90' * 1024)

        count = 1000
        start = time.time()
        for i in range(count):
            packager.add_symbol(f"sym_{i}", i * 8)
        result = packager.build()
        elapsed = time.time() - start

        print(f"  Built BPP with {count} symbols in {elapsed:.3f}s")

    def test_many_libraries(self):
        """Test BPP with many libraries / 测试带大量库的 BPP"""
        from toolchain.bamboo_pack import BPPPackager

        packager = BPPPackager()
        packager.add_code(b'\x90' * 1024)

        count = 100
        start = time.time()
        for i in range(count):
            packager.add_library(f"lib{i}.so")
        result = packager.build()
        elapsed = time.time() - start

        print(f"  Built BPP with {count} libraries in {elapsed:.3f}s")

    def test_many_relocations(self):
        """Test BPP with many relocations / 测试带大量重定位的 BPP"""
        from toolchain.bamboo_pack import BPPPackager

        packager = BPPPackager()
        packager.add_code(b'\x00' * 4096)

        count = 1000
        start = time.time()
        for i in range(count):
            packager.add_relocation(i * 4, f"sym_{i}")
        result = packager.build()
        elapsed = time.time() - start

        print(f"  Built BPP with {count} relocations in {elapsed:.3f}s")

    def test_bpp_io_performance(self):
        """Test BPP save/load performance / 测试 BPP 保存/加载性能"""
        from toolchain.bamboo_pack import BPPPackager, BPPLoader
        import tempfile

        packager = BPPPackager()
        packager.add_code(b'\x90' * (512 * 1024))  # 512KB
        packager.set_flags(executable=True)

        with tempfile.NamedTemporaryFile(suffix='.bpp', delete=False) as f:
            temp_path = f.name

        try:
            # Save / 保存
            start = time.time()
            size = packager.save(temp_path)
            save_time = time.time() - start
            print(f"  Saved {size:,} bytes in {save_time:.3f}s "
                  f"({size/save_time/1024/1024:.1f} MB/s)")

            # Load / 加载
            start = time.time()
            loader = BPPLoader(temp_path)
            load_time = time.time() - start
            print(f"  Loaded in {load_time:.3f}s")

            self.assertTrue(loader.is_valid())
        finally:
            os.unlink(temp_path)


class TestKernelGenStress(unittest.TestCase):
    """Stress tests for kernel generation / 内核生成压力测试"""

    def test_wonder1_build_time(self):
        """Test Wonder 1.0 build time / 测试 Wonder 1.0 构建时间"""
        from configs import load_config
        from kernel.kernel_generator import generate_kernel

        config = load_config('wonder1')

        with tempfile.NamedTemporaryFile(suffix='.elf', delete=False) as f:
            output_path = f.name

        try:
            start = time.time()
            size = generate_kernel(config, output_path)
            elapsed = time.time() - start

            print(f"  Wonder 1.0: {size:,} bytes in {elapsed:.3f}s")
            self.assertGreater(size, 0)
        finally:
            os.unlink(output_path)

    def test_wonder2_build_time(self):
        """Test Wonder 2.0 build time / 测试 Wonder 2.0 构建时间"""
        from configs import load_config
        from kernel.kernel_generator import generate_kernel

        config = load_config('wonder2')

        with tempfile.NamedTemporaryFile(suffix='.elf', delete=False) as f:
            output_path = f.name

        try:
            start = time.time()
            size = generate_kernel(config, output_path)
            elapsed = time.time() - start

            print(f"  Wonder 2.0: {size:,} bytes in {elapsed:.3f}s")
            self.assertGreater(size, 0)
        finally:
            os.unlink(output_path)

    def test_education_build_time(self):
        """Test Education build time / 测试教学版构建时间"""
        from configs import load_config
        from kernel.kernel_generator import generate_minimal_kernel

        config = load_config('edu')

        with tempfile.NamedTemporaryFile(suffix='.elf', delete=False) as f:
            output_path = f.name

        try:
            start = time.time()
            size = generate_minimal_kernel(config, output_path)
            elapsed = time.time() - start

            print(f"  Education: {size:,} bytes in {elapsed:.3f}s")
            self.assertGreater(size, 0)
        finally:
            os.unlink(output_path)

    def test_repeated_builds(self):
        """Test repeated builds / 测试重复构建"""
        from configs import load_config
        from kernel.kernel_generator import generate_minimal_kernel

        config = load_config('edu')
        count = 5

        times = []
        for i in range(count):
            with tempfile.NamedTemporaryFile(suffix='.elf', delete=False) as f:
                output_path = f.name

            try:
                start = time.time()
                generate_minimal_kernel(config, output_path)
                elapsed = time.time() - start
                times.append(elapsed)
            finally:
                os.unlink(output_path)

        avg_time = sum(times) / len(times)
        print(f"  Average build time over {count} runs: {avg_time:.3f}s")
        print(f"  Min: {min(times):.3f}s, Max: {max(times):.3f}s")


if __name__ == '__main__':
    unittest.main(verbosity=2)
