#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: tests/unit/test_bpp.py
# 模块：tests/unit/test_bpp.py
# Description: Unit tests for BPP (Bamboo Package) format
# 描述：BPP 包格式单元测试
# ============================================================================

import sys
import os
import unittest
import tempfile

# Add project root to path / 将项目根目录添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestBPPHeader(unittest.TestCase):
    """Test BPP header / BPP 头部测试"""

    def test_header_magic(self):
        """Test BPP magic number / 测试 BPP 魔数"""
        from toolchain.bamboo_pack import BPPHeader, BPP_MAGIC
        header = BPPHeader()
        self.assertEqual(header.magic, BPP_MAGIC)

    def test_header_version(self):
        """Test BPP version / 测试 BPP 版本"""
        from toolchain.bamboo_pack import BPPHeader
        header = BPPHeader()
        self.assertGreater(header.version, 0)

    def test_header_size(self):
        """Test header size / 测试头部大小"""
        from toolchain.bamboo_pack import BPPHeader
        header = BPPHeader()
        self.assertEqual(header.header_size, 128)

    def test_header_default_flags(self):
        """Test default flags / 测试默认标志"""
        from toolchain.bamboo_pack import BPPHeader
        header = BPPHeader()
        self.assertEqual(header.flags, 0)

    def test_header_pack_unpack(self):
        """Test header pack/unpack roundtrip / 测试头部打包/解包往返"""
        from toolchain.bamboo_pack import BPPHeader
        header = BPPHeader()
        header.entry_point = 0x1000
        header.image_size = 0x10000
        header.stack_size = 0x8000
        header.heap_size = 0x100000

        packed = header.pack()
        self.assertEqual(len(packed), BPPHeader.SIZE)

        unpacked = BPPHeader.unpack(packed)
        self.assertEqual(unpacked.magic, header.magic)
        self.assertEqual(unpacked.version, header.version)
        self.assertEqual(unpacked.entry_point, header.entry_point)
        self.assertEqual(unpacked.image_size, header.image_size)
        self.assertEqual(unpacked.stack_size, header.stack_size)
        self.assertEqual(unpacked.heap_size, header.heap_size)

    def test_header_is_valid(self):
        """Test header validation / 测试头部验证"""
        from toolchain.bamboo_pack import BPPHeader
        header = BPPHeader()
        self.assertTrue(header.is_valid())

        header.magic = 0x12345678
        self.assertFalse(header.is_valid())


class TestBPPPackager(unittest.TestCase):
    """Test BPP packager / BPP 打包器测试"""

    def test_create_packager(self):
        """Test creating packager / 测试创建打包器"""
        from toolchain.bamboo_pack import BPPPackager
        packager = BPPPackager()
        self.assertIsNotNone(packager)
        self.assertEqual(len(packager.code), 0)
        self.assertEqual(len(packager.data), 0)

    def test_add_code(self):
        """Test adding code / 测试添加代码"""
        from toolchain.bamboo_pack import BPPPackager
        packager = BPPPackager()
        packager.add_code(b'\x90\x90\x90')
        self.assertEqual(len(packager.code), 3)

    def test_add_data(self):
        """Test adding data / 测试添加数据"""
        from toolchain.bamboo_pack import BPPPackager
        packager = BPPPackager()
        packager.add_data(b'\x00' * 100)
        self.assertEqual(len(packager.data), 100)

    def test_add_rodata(self):
        """Test adding rodata / 测试添加只读数据"""
        from toolchain.bamboo_pack import BPPPackager
        packager = BPPPackager()
        packager.add_rodata(b'Hello')
        self.assertEqual(len(packager.rodata), 5)

    def test_add_library(self):
        """Test adding library / 测试添加库"""
        from toolchain.bamboo_pack import BPPPackager
        packager = BPPPackager()
        packager.add_library('libc.so')
        packager.add_library('libgui.so')
        self.assertEqual(len(packager.libraries), 2)
        self.assertIn('libc.so', packager.libraries)
        self.assertIn('libgui.so', packager.libraries)

    def test_add_library_duplicate(self):
        """Test adding duplicate library / 测试添加重复库"""
        from toolchain.bamboo_pack import BPPPackager
        packager = BPPPackager()
        packager.add_library('libc.so')
        packager.add_library('libc.so')  # duplicate / 重复
        self.assertEqual(len(packager.libraries), 1)

    def test_add_symbol(self):
        """Test adding symbol / 测试添加符号"""
        from toolchain.bamboo_pack import BPPPackager
        packager = BPPPackager()
        packager.add_symbol('main', 0x1000)
        packager.add_symbol('printf', 0x2000)
        self.assertEqual(len(packager.symbols), 2)
        self.assertIn('main', packager.symbols)

    def test_set_flags(self):
        """Test setting flags / 测试设置标志"""
        from toolchain.bamboo_pack import BPPPackager, BPP_FLAG_EXECUTABLE, BPP_FLAG_GUI
        packager = BPPPackager()
        packager.set_flags(executable=True, gui=True)
        self.assertTrue(packager.header.flags & BPP_FLAG_EXECUTABLE)
        self.assertTrue(packager.header.flags & BPP_FLAG_GUI)

    def test_build(self):
        """Test building BPP package / 测试构建 BPP 包"""
        from toolchain.bamboo_pack import BPPPackager
        packager = BPPPackager()
        packager.add_code(b'\x90' * 100)
        packager.add_data(b'\x00' * 50)
        packager.set_flags(executable=True)

        result = packager.build(entry_point=0)
        self.assertGreater(len(result), 128)  # At least header size / 至少头部大小

    def test_save_and_load(self):
        """Test save and load roundtrip / 测试保存和加载往返"""
        from toolchain.bamboo_pack import BPPPackager, BPPLoader
        packager = BPPPackager()
        packager.add_code(b'\x90' * 256)
        packager.add_library('libc.so')
        packager.set_flags(executable=True, gui=True)

        with tempfile.NamedTemporaryFile(suffix='.bpp', delete=False) as f:
            temp_path = f.name

        try:
            size = packager.save(temp_path)
            self.assertGreater(size, 0)

            loader = BPPLoader(temp_path)
            self.assertTrue(loader.is_valid())

            info = loader.get_info()
            self.assertIn('flags', info)
            self.assertTrue(info['flags']['executable'])
            self.assertTrue(info['flags']['gui'])

            libs = loader.get_libraries()
            self.assertIn('libc.so', libs)
        finally:
            os.unlink(temp_path)


class TestBPPLoader(unittest.TestCase):
    """Test BPP loader / BPP 加载器测试"""

    def test_load_invalid_file(self):
        """Test loading invalid file / 测试加载无效文件"""
        from toolchain.bamboo_pack import BPPLoader
        with tempfile.NamedTemporaryFile(suffix='.bpp', delete=False) as f:
            f.write(b'NOT_A_BPP_FILE')
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                BPPLoader(temp_path)
        finally:
            os.unlink(temp_path)

    def test_load_empty_file(self):
        """Test loading empty file / 测试加载空文件"""
        from toolchain.bamboo_pack import BPPLoader
        with tempfile.NamedTemporaryFile(suffix='.bpp', delete=False) as f:
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                BPPLoader(temp_path)
        finally:
            os.unlink(temp_path)

    def test_verify_bpp(self):
        """Test verify_bpp function / 测试 verify_bpp 函数"""
        from toolchain.bamboo_pack import create_simple_bpp, verify_bpp
        with tempfile.NamedTemporaryFile(suffix='.bpp', delete=False) as f:
            temp_path = f.name

        try:
            create_simple_bpp('test', b'\x90' * 100, temp_path)
            valid, info = verify_bpp(temp_path)
            self.assertTrue(valid)
            self.assertIn('flags', info)
        finally:
            os.unlink(temp_path)


class TestCreateSimpleBPP(unittest.TestCase):
    """Test create_simple_bpp helper / create_simple_bpp 辅助函数测试"""

    def test_create_executable(self):
        """Test creating executable BPP / 测试创建可执行 BPP"""
        from toolchain.bamboo_pack import create_simple_bpp, BPPLoader
        with tempfile.NamedTemporaryFile(suffix='.bpp', delete=False) as f:
            temp_path = f.name

        try:
            size = create_simple_bpp(
                'test_app',
                b'\x90' * 1000,
                temp_path,
                entry_point=0,
                executable=True,
                gui=False
            )
            self.assertGreater(size, 0)

            loader = BPPLoader(temp_path)
            self.assertTrue(loader.is_valid())
            self.assertTrue(loader.get_info()['flags']['executable'])
        finally:
            os.unlink(temp_path)

    def test_create_with_libraries(self):
        """Test creating BPP with libraries / 测试创建带库的 BPP"""
        from toolchain.bamboo_pack import create_simple_bpp, BPPLoader
        with tempfile.NamedTemporaryFile(suffix='.bpp', delete=False) as f:
            temp_path = f.name

        try:
            create_simple_bpp(
                'test_app',
                b'\x90' * 100,
                temp_path,
                libraries=['libc.so', 'libgui.so']
            )

            loader = BPPLoader(temp_path)
            libs = loader.get_libraries()
            self.assertEqual(len(libs), 2)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
