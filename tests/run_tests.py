#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Module: tests/run_tests.py
# 模块：tests/run_tests.py
# Description: Test runner for Bamboo OS Wonder Series
# 描述：Bamboo OS Wonder 系列测试运行器
# ============================================================================

import sys
import os
import unittest
import argparse
import time

# Add project root to path / 将项目根目录添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_unit_tests(verbose=False):
    """
    Run all unit tests.
    运行所有单元测试。

    Args:
        参数：
        verbose (bool): Verbose output / 详细输出

    Returns:
        返回：
        bool: True if all tests pass / 所有测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("  Running Unit Tests / 运行单元测试")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(os.path.dirname(__file__), 'unit'),
        pattern='test_*.py'
    )

    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_integration_tests(verbose=False):
    """
    Run all integration tests.
    运行所有集成测试。

    Args:
        参数：
        verbose (bool): Verbose output / 详细输出

    Returns:
        返回：
        bool: True if all tests pass / 所有测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("  Running Integration Tests / 运行集成测试")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(os.path.dirname(__file__), 'integration'),
        pattern='test_*.py'
    )

    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_stress_tests(verbose=False):
    """
    Run all stress tests.
    运行所有压力测试。

    Args:
        参数：
        verbose (bool): Verbose output / 详细输出

    Returns:
        返回：
        bool: True if all tests pass / 所有测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("  Running Stress Tests / 运行压力测试")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(os.path.dirname(__file__), 'stress'),
        pattern='test_*.py'
    )

    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_all_tests(verbose=False):
    """
    Run all tests.
    运行所有测试。

    Args:
        参数：
        verbose (bool): Verbose output / 详细输出

    Returns:
        返回：
        bool: True if all tests pass / 所有测试通过返回 True
    """
    start_time = time.time()

    unit_ok = run_unit_tests(verbose)
    integration_ok = run_integration_tests(verbose)
    stress_ok = run_stress_tests(verbose)

    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print("  TEST SUMMARY / 测试摘要")
    print("=" * 60)
    print(f"  Unit Tests:        {'PASS' if unit_ok else 'FAIL'}")
    print(f"  Integration Tests: {'PASS' if integration_ok else 'FAIL'}")
    print(f"  Stress Tests:      {'PASS' if stress_ok else 'FAIL'}")
    print(f"  Total Time:        {elapsed:.2f}s")
    print("=" * 60)

    all_ok = unit_ok and integration_ok and stress_ok
    if all_ok:
        print("\n  ALL TESTS PASSED ✓")
    else:
        print("\n  SOME TESTS FAILED ✗")

    return all_ok


def main():
    """Main entry point / 主入口"""
    parser = argparse.ArgumentParser(
        description='Bamboo OS Test Runner / Bamboo OS 测试运行器'
    )
    parser.add_argument(
        '--unit',
        action='store_true',
        help='Run unit tests only / 仅运行单元测试'
    )
    parser.add_argument(
        '--integration',
        action='store_true',
        help='Run integration tests only / 仅运行集成测试'
    )
    parser.add_argument(
        '--stress',
        action='store_true',
        help='Run stress tests only / 仅运行压力测试'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output / 详细输出'
    )

    args = parser.parse_args()

    if args.unit:
        success = run_unit_tests(args.verbose)
    elif args.integration:
        success = run_integration_tests(args.verbose)
    elif args.stress:
        success = run_stress_tests(args.verbose)
    else:
        success = run_all_tests(args.verbose)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
