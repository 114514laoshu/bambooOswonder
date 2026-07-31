#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: tests/unit/test_config.py
# 模块：tests/unit/test_config.py
# Description: Unit tests for configuration system
# 描述：配置系统单元测试
# ============================================================================

import sys
import os
import unittest

# Add project root to path / 将项目根目录添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestConfigLoader(unittest.TestCase):
    """Test configuration loader / 配置加载器测试"""

    def test_load_wonder1_config(self):
        """Test loading Wonder 1.0 config / 测试加载 Wonder 1.0 配置"""
        from configs import load_config
        config = load_config('wonder1')
        self.assertIsNotNone(config)
        self.assertEqual(config.VERSION, "1.0.0")
        self.assertIn('name', config.KERNEL_CONFIG)

    def test_load_wonder2_config(self):
        """Test loading Wonder 2.0 config / 测试加载 Wonder 2.0 配置"""
        from configs import load_config
        config = load_config('wonder2')
        self.assertIsNotNone(config)
        self.assertEqual(config.VERSION, "2.0.0")
        self.assertTrue(config.KERNEL_CONFIG.get('direct_boot', False))

    def test_load_education_config(self):
        """Test loading Education config / 测试加载教学版配置"""
        from configs import load_config
        config = load_config('edu')
        self.assertIsNotNone(config)
        self.assertFalse(config.GUI_CONFIG.get('enabled', True))
        self.assertFalse(config.NET_CONFIG.get('enabled', True))

    def test_load_invalid_target(self):
        """Test loading invalid target / 测试加载无效目标"""
        from configs import load_config
        with self.assertRaises(ValueError):
            load_config('invalid_target')

    def test_load_education_alias(self):
        """Test education alias / 测试 education 别名"""
        from configs import load_config
        config1 = load_config('edu')
        config2 = load_config('education')
        self.assertEqual(config1.VERSION, config2.VERSION)


class TestWonder1Config(unittest.TestCase):
    """Test Wonder 1.0 configuration / Wonder 1.0 配置测试"""

    def setUp(self):
        """Set up test / 设置测试"""
        from configs import load_config
        self.config = load_config('wonder1')

    def test_version(self):
        """Test version / 测试版本"""
        self.assertEqual(self.config.VERSION, "1.0.0")

    def test_kernel_config(self):
        """Test kernel config / 测试内核配置"""
        self.assertIn('name', self.config.KERNEL_CONFIG)
        self.assertEqual(self.config.KERNEL_CONFIG['arch'], 'x86_64')

    def test_memory_config(self):
        """Test memory config / 测试内存配置"""
        self.assertIn('total_mb', self.config.MEMORY_CONFIG)
        self.assertGreater(self.config.MEMORY_CONFIG['total_mb'], 0)

    def test_fs_config(self):
        """Test filesystem config / 测试文件系统配置"""
        self.assertIn('root_fs', self.config.FS_CONFIG)
        self.assertEqual(self.config.FS_CONFIG['root_fs'], 'fat32')

    def test_gui_enabled(self):
        """Test GUI is enabled / 测试 GUI 已启用"""
        self.assertTrue(self.config.GUI_CONFIG.get('enabled', False))

    def test_no_direct_boot(self):
        """Test no direct boot / 测试无直接启动"""
        self.assertFalse(self.config.KERNEL_CONFIG.get('direct_boot', False))


class TestWonder2Config(unittest.TestCase):
    """Test Wonder 2.0 configuration / Wonder 2.0 配置测试"""

    def setUp(self):
        """Set up test / 设置测试"""
        from configs import load_config
        self.config = load_config('wonder2')

    def test_version(self):
        """Test version / 测试版本"""
        self.assertEqual(self.config.VERSION, "2.0.0")

    def test_direct_boot(self):
        """Test direct boot is enabled / 测试直接启动已启用"""
        self.assertTrue(self.config.KERNEL_CONFIG.get('direct_boot', False))

    def test_gui_enabled(self):
        """Test GUI is enabled / 测试 GUI 已启用"""
        self.assertTrue(self.config.GUI_CONFIG.get('enabled', False))

    def test_network_enabled(self):
        """Test network is enabled / 测试网络已启用"""
        self.assertTrue(self.config.NET_CONFIG.get('enabled', False))

    def test_games_enabled(self):
        """Test games are included / 测试包含游戏"""
        self.assertGreater(len(self.config.APPS_CONFIG.get('games_2d', [])), 0)
        self.assertGreater(len(self.config.APPS_CONFIG.get('games_3d', [])), 0)


class TestEducationConfig(unittest.TestCase):
    """Test Education configuration / 教学版配置测试"""

    def setUp(self):
        """Set up test / 设置测试"""
        from configs import load_config
        self.config = load_config('edu')

    def test_gui_disabled(self):
        """Test GUI is disabled / 测试 GUI 已禁用"""
        self.assertFalse(self.config.GUI_CONFIG.get('enabled', True))

    def test_network_disabled(self):
        """Test network is disabled / 测试网络已禁用"""
        self.assertFalse(self.config.NET_CONFIG.get('enabled', True))

    def test_minimal_apps(self):
        """Test minimal apps / 测试最小应用"""
        apps = self.config.APPS_CONFIG.get('include', [])
        self.assertLessEqual(len(apps), 5)

    def test_no_games(self):
        """Test no games / 测试无游戏"""
        self.assertEqual(len(self.config.APPS_CONFIG.get('games_2d', [])), 0)
        self.assertEqual(len(self.config.APPS_CONFIG.get('games_3d', [])), 0)

    def test_education_specific(self):
        """Test education specific config / 测试教学版特定配置"""
        self.assertTrue(self.config.EDUCATION_CONFIG.get('detailed_comments', False))
        self.assertTrue(self.config.EDUCATION_CONFIG.get('lab_exercises', False))


class TestOutputConfig(unittest.TestCase):
    """Test output configuration / 输出配置测试"""

    def test_wonder1_output(self):
        """Test Wonder 1.0 output config / 测试 Wonder 1.0 输出配置"""
        from configs import load_config
        config = load_config('wonder1')
        self.assertIn('elf', config.OUTPUT_CONFIG)
        self.assertIn('iso', config.OUTPUT_CONFIG)
        self.assertIn('output_dir', config.OUTPUT_CONFIG)

    def test_wonder2_output(self):
        """Test Wonder 2.0 output config / 测试 Wonder 2.0 输出配置"""
        from configs import load_config
        config = load_config('wonder2')
        self.assertIn('bin', config.OUTPUT_CONFIG)  # Direct boot binary

    def test_education_output(self):
        """Test Education output config / 测试教学版输出配置"""
        from configs import load_config
        config = load_config('edu')
        self.assertIn('elf', config.OUTPUT_CONFIG)


if __name__ == '__main__':
    unittest.main(verbosity=2)
