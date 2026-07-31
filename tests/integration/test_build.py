#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: tests/integration/test_build.py
# 模块：tests/integration/test_build.py
# Description: Integration tests for build system
# 描述：构建系统集成测试
# ============================================================================

import sys
import os
import unittest
import tempfile
import shutil

# Add project root to path / 将项目根目录添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestBuildSystem(unittest.TestCase):
    """Test build system / 构建系统测试"""

    def setUp(self):
        """Set up test / 设置测试"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test / 清理测试"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_platform_detector(self):
        """Test platform detection / 测试平台检测"""
        from buildmain import PlatformDetector
        platform = PlatformDetector.get_platform()
        self.assertIn(platform, ['windows', 'linux', 'darwin'])

    def test_build_logger(self):
        """Test build logger / 测试构建日志"""
        from buildmain import BuildLogger
        logger = BuildLogger(verbose=False)
        logger.info("Test info")
        logger.success("Test success")
        logger.warning("Test warning")
        logger.error("Test error")
        # Should not raise / 不应抛出异常

    def test_config_loading(self):
        """Test config loading in build context / 测试构建上下文中的配置加载"""
        from configs import load_config
        config = load_config('wonder1')
        self.assertIsNotNone(config)
        self.assertTrue(hasattr(config, 'KERNEL_CONFIG'))
        self.assertTrue(hasattr(config, 'OUTPUT_CONFIG'))

    def test_bpp_roundtrip(self):
        """Test BPP create and verify roundtrip / 测试 BPP 创建和验证往返"""
        from toolchain.bamboo_pack import create_simple_bpp, verify_bpp

        bpp_path = os.path.join(self.test_dir, 'test.bpp')
        create_simple_bpp(
            'test_app',
            b'\x90' * 1024,
            bpp_path,
            executable=True,
            gui=True
        )

        self.assertTrue(os.path.exists(bpp_path))

        valid, info = verify_bpp(bpp_path)
        self.assertTrue(valid)
        self.assertTrue(info['flags']['executable'])
        self.assertTrue(info['flags']['gui'])

    def test_kernel_generator_import(self):
        """Test kernel generator can be imported / 测试内核生成器可导入"""
        from kernel.kernel_generator import generate_kernel, generate_minimal_kernel
        self.assertTrue(callable(generate_kernel))
        self.assertTrue(callable(generate_minimal_kernel))

    def test_assembler_instantiation(self):
        """Test assembler can be instantiated / 测试汇编器可实例化"""
        from core.assembler import X64Assembler
        asm = X64Assembler()
        self.assertIsNotNone(asm)

    def test_toolchain_imports(self):
        """Test toolchain modules can be imported / 测试工具链模块可导入"""
        from toolchain.bamboo_pack import BPPPackager, BPPLoader
        self.assertTrue(callable(BPPPackager))
        self.assertTrue(callable(BPPLoader))


class TestKernelGeneration(unittest.TestCase):
    """Test kernel generation / 内核生成测试"""

    def test_generate_minimal_kernel(self):
        """Test generating minimal kernel / 测试生成最小内核"""
        from configs import load_config
        from kernel.kernel_generator import generate_minimal_kernel

        config = load_config('edu')

        with tempfile.NamedTemporaryFile(suffix='.elf', delete=False) as f:
            output_path = f.name

        try:
            size = generate_minimal_kernel(config, output_path)
            self.assertGreater(size, 0)
            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(os.path.getsize(output_path), 0)
        finally:
            os.unlink(output_path)

    def test_generate_full_kernel(self):
        """Test generating full kernel / 测试生成完整内核"""
        from configs import load_config
        from kernel.kernel_generator import generate_kernel

        config = load_config('wonder2')

        with tempfile.NamedTemporaryFile(suffix='.elf', delete=False) as f:
            output_path = f.name

        try:
            size = generate_kernel(config, output_path)
            self.assertGreater(size, 0)
            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(os.path.getsize(output_path), 0)
        finally:
            os.unlink(output_path)


class TestBuildValidation(unittest.TestCase):
    """Test build validation / 构建验证测试"""

    def test_validator_creation(self):
        """Test validator creation / 测试验证器创建"""
        from scripts.validate import BuildValidator
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = BuildValidator(tmpdir)
            self.assertIsNotNone(validator)

    def test_validation_methods(self):
        """Test validation methods exist / 测试验证方法存在"""
        from scripts.validate import BuildValidator
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = BuildValidator(tmpdir)
            self.assertTrue(hasattr(validator, 'check_file_exists'))
            self.assertTrue(hasattr(validator, 'check_elf_file'))
            self.assertTrue(hasattr(validator, 'check_min_size'))
            self.assertTrue(hasattr(validator, 'validate_wonder'))
            self.assertTrue(hasattr(validator, 'validate_education'))
            self.assertTrue(hasattr(validator, 'print_summary'))


class TestQEMUScript(unittest.TestCase):
    """Test QEMU runner script / QEMU 启动脚本测试"""

    def test_qemu_command_detection(self):
        """Test QEMU command detection / 测试 QEMU 命令检测"""
        from scripts.run_qemu import get_qemu_command
        cmd = get_qemu_command()
        self.assertIsInstance(cmd, str)
        self.assertIn('qemu', cmd.lower())

    def test_run_qemu_function_exists(self):
        """Test run_qemu function exists / 测试 run_qemu 函数存在"""
        from scripts.run_qemu import run_qemu
        self.assertTrue(callable(run_qemu))


if __name__ == '__main__':
    unittest.main(verbosity=2)
