# ============================================================================
# Module: userland/apps/shell/extensions/completion.py
# 模块：userland/apps/shell/extensions/completion.py
# Description: Advanced command completion for Shell
# 描述：Shell 高级命令补全
# ============================================================================

"""
Advanced command completion for Shell application.
Shell 应用的高级命令补全。

Provides intelligent tab completion for commands, paths, and options.
为命令、路径和选项提供智能 Tab 补全。
"""

import os
import sys
from typing import List, Set, Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class CompletionResult:
    """Completion result / 补全结果"""
    matches: List[str] = field(default_factory=list)
    common_prefix: str = ""
    cursor_position: int = 0


class AdvancedCompleter:
    """
    Advanced command completer.
    高级命令补全器。

    Provides intelligent completion for:
    - Command names / 命令名
    - File paths / 文件路径
    - Command options / 命令选项
    - Environment variables / 环境变量
    """

    def __init__(self, shell_instance):
        """
        Initialize completer.
        初始化补全器。

        Args:
            参数：
            shell_instance: ShellApp instance / ShellApp 实例
        """
        self.shell = shell_instance
        self._command_cache: Set[str] = set()
        self._option_cache: Dict[str, Set[str]] = {}
        self._built_cache = False

    def cache_commands(self):
        """Cache available commands / 缓存可用命令"""
        if self._built_cache:
            return

        # Built-in commands / 内置命令
        for cmd in self.shell.commands.list():
            self._command_cache.add(cmd)

        # External commands from PATH / PATH 中的外部命令
        path = self.shell.env.get('PATH', '/bin:/usr/bin')
        for dir_path in path.split(':'):
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                for item in os.listdir(dir_path):
                    full_path = os.path.join(dir_path, item)
                    if os.access(full_path, os.X_OK):
                        self._command_cache.add(item)

        self._built_cache = True

    def complete_command(self, partial: str, line: str = "") -> CompletionResult:
        """
        Complete command names.
        补全命令名。

        Args:
            参数：
            partial (str): Partial command / 部分命令
            line (str): Full command line / 完整命令行

        Returns:
            返回：
            CompletionResult: Completion results / 补全结果
        """
        self.cache_commands()

        matches = []
        partial_lower = partial.lower()

        for cmd in self._command_cache:
            if cmd.lower().startswith(partial_lower):
                matches.append(cmd)

        return self._build_result(matches, partial)

    def complete_path(self, partial: str) -> CompletionResult:
        """
        Complete file paths.
        补全文件路径。

        Args:
            参数：
            partial (str): Partial path / 部分路径

        Returns:
            返回：
            CompletionResult: Completion results / 补全结果
        """
        # Get directory and base / 获取目录和基名
        if '/' in partial:
            dir_path = os.path.dirname(partial)
            base = os.path.basename(partial)
            if not dir_path:
                dir_path = '.'
        else:
            dir_path = '.'
            base = partial

        try:
            items = os.listdir(dir_path)
        except Exception:
            return CompletionResult()

        matches = []
        full_base = base.lower()

        for item in items:
            if item.lower().startswith(full_base):
                # Add trailing slash for directories / 目录添加斜杠
                full_path = os.path.join(dir_path, item)
                if os.path.isdir(full_path):
                    matches.append(item + '/')
                else:
                    matches.append(item)

        return self._build_result(matches, base)

    def complete_variable(self, partial: str) -> CompletionResult:
        """
        Complete environment variables.
        补全环境变量。

        Args:
            参数：
            partial (str): Partial variable name / 部分变量名

        Returns:
            返回：
            CompletionResult: Completion results / 补全结果
        """
        matches = []
        partial_lower = partial.lower()

        for key in self.shell.env:
            if key.lower().startswith(partial_lower):
                matches.append(key)

        return self._build_result(matches, partial)

    def complete_options(self, cmd: str, partial: str) -> CompletionResult:
        """
        Complete command options.
        补全命令选项。

        Args:
            参数：
            cmd (str): Command name / 命令名
            partial (str): Partial option / 部分选项

        Returns:
            返回：
            CompletionResult: Completion results / 补全结果
        """
        # Built-in option cache / 内置选项缓存
        option_map = {
            'ls': ['-l', '-a', '-A', '-R', '-h', '-d', '-t', '-S'],
            'ps': ['-a', '-u', '-x', '-e', '-f', '-l'],
            'rm': ['-r', '-f', '-i', '-v'],
            'cp': ['-r', '-f', '-i', '-v', '-p'],
            'mv': ['-f', '-i', '-v'],
            'mkdir': ['-p', '-v'],
            'grep': ['-r', '-i', '-v', '-c', '-l', '-n', '-H'],
            'find': ['-name', '-type', '-size', '-mtime', '-exec'],
            'tar': ['-c', '-x', '-t', '-f', '-v', '-z', '-j'],
            'uname': ['-a', '-s', '-n', '-r', '-v', '-m'],
        }

        matches = []
        partial_lower = partial.lower()

        for opt in option_map.get(cmd, []):
            if opt.lower().startswith(partial_lower):
                matches.append(opt)

        return self._build_result(matches, partial)

    def complete(self, line: str, pos: int) -> CompletionResult:
        """
        Main completion entry point.
        主补全入口点。

        Args:
            参数：
            line (str): Full command line / 完整命令行
            pos (int): Cursor position / 光标位置

        Returns:
            返回：
            CompletionResult: Completion results / 补全结果
        """
        # Get current token / 获取当前标记
        tokens = line[:pos].split()
        if not tokens:
            return CompletionResult()

        # Get the current token being completed / 获取正在补全的当前标记
        current = tokens[-1]

        # Check if it's a variable / 检查是否为变量
        if current.startswith('$'):
            var_name = current[1:]
            result = self.complete_variable(var_name)
            result.matches = ['$' + m for m in result.matches]
            return result

        # Check if it's a path / 检查是否为路径
        if '/' in current or any(c in current for c in './~'):
            return self.complete_path(current)

        # Check if it's an option (starts with -) / 检查是否为选项（以 - 开头）
        if current.startswith('-'):
            if tokens:
                cmd = tokens[0]
                result = self.complete_options(cmd, current)
                return result

        # Check if it's a command (first token) / 检查是否为命令（第一个标记）
        if len(tokens) == 1 and not current.startswith('-') and not current.startswith('$'):
            return self.complete_command(current, line)

        # Default: command name completion / 默认：命令名补全
        return self.complete_command(current, line)

    def _build_result(self, matches: List[str], partial: str) -> CompletionResult:
        """
        Build completion result from matches.
        从匹配项构建补全结果。

        Args:
            参数：
            matches (list): Match list / 匹配列表
            partial (str): Partial string / 部分字符串

        Returns:
            返回：
            CompletionResult: Completion result / 补全结果
        """
        result = CompletionResult()
        result.matches = matches

        if matches:
            # Find common prefix / 查找公共前缀
            if len(matches) == 1:
                result.common_prefix = matches[0]
            else:
                # Find longest common prefix / 查找最长公共前缀
                prefix = matches[0]
                for m in matches[1:]:
                    while not m.startswith(prefix):
                        prefix = prefix[:-1]
                        if not prefix:
                            break
                result.common_prefix = prefix

            # Advance cursor / 推进光标
            if result.common_prefix:
                result.cursor_position = len(result.common_prefix) - len(partial)

        return result