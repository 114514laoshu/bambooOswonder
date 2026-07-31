# ============================================================================
# Module: configs/__init__.py
# 模块：configs/__init__.py
# Description: Configuration package for Bamboo OS Wonder Series
# 描述：Bamboo OS Wonder 系列配置包
# ============================================================================

import importlib
import os


def load_config(target):
    """
    Load configuration for a specific target / 加载指定目标的配置

    Args:
        参数：
        target (str): Target name (wonder1, wonder2, edu) / 目标名称

    Returns:
        返回：
        module: Configuration module / 配置模块
    """
    config_map = {
        'wonder1': 'wonder1_config',
        'wonder2': 'wonder2_config',
        'edu': 'education_config',
        'education': 'education_config',
    }

    config_name = config_map.get(target.lower())
    if not config_name:
        raise ValueError(f"Unknown target: {target}. Available: wonder1, wonder2, edu")

    module = importlib.import_module(f'configs.{config_name}')
    return module


__all__ = ['load_config']
