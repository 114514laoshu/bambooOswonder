# ============================================================================
# Module: userland/apps/shell/patches/command_patches.py
# 模块：userland/apps/shell/patches/command_patches.py
# Description: Command patches for P2+
# 描述：P2+ 命令补丁
# ============================================================================

"""
Command patches for Shell application.
Shell 应用的命令补丁。

Adds additional built-in commands and extends existing ones.
添加额外的内置命令并扩展现有命令。
"""

from typing import List, Dict, Any, Optional
import os
import sys
import time
import importlib


class CommandPatcher:
    """
    Command patcher for Shell.
    Shell 命令修补器。

    Adds extra commands and patches existing command handlers.
    添加额外命令并修补现有命令处理函数。
    """

    def __init__(self, shell_instance):
        """
        Initialize command patcher.
        初始化命令修补器。

        Args:
            参数：
            shell_instance: ShellApp instance / ShellApp 实例
        """
        self.shell = shell_instance
        self._extra_commands: Dict[str, Any] = {}
        self._patched_commands: Dict[str, Any] = {}

    def apply(self) -> bool:
        """
        Apply command patches.
        应用命令补丁。

        Returns:
            返回：
            bool: True if patches applied / 补丁已应用返回 True
        """
        # Add extra commands / 添加额外命令
        self._register_extra_commands()

        # Patch existing commands / 修补现有命令
        self._patch_ls_command()
        self._patch_ps_command()
        self._patch_help_command()

        return True

    def _register_extra_commands(self):
        """Register extra built-in commands / 注册额外的内置命令"""
        extra_commands = {
            'which': self._cmd_which_ext,
            'type': self._cmd_type,
            'pushd': self._cmd_pushd,
            'popd': self._cmd_popd,
            'dirs': self._cmd_dirs,
            'export': self._cmd_export_ext,
            'source': self._cmd_source_ext,
            'exec': self._cmd_exec_ext,
            'time': self._cmd_time,
            'uptime': self._cmd_uptime_ext,
            'uname': self._cmd_uname_ext,
            'true': self._cmd_true,
            'false': self._cmd_false,
            'sleep': self._cmd_sleep,
            'printf': self._cmd_printf,
            'test': self._cmd_test,
            '[': self._cmd_test,
        }

        for name, handler in extra_commands.items():
            self.shell.commands.register(name, handler, self._get_help(name))
            self._extra_commands[name] = handler

    def _get_help(self, name: str) -> str:
        """Get help text for extra command / 获取额外命令的帮助文本"""
        helps = {
            'which': "Locate command in PATH",
            'type': "Display command type",
            'pushd': "Push directory to stack",
            'popd': "Pop directory from stack",
            'dirs': "Display directory stack",
            'export': "Set environment variable",
            'source': "Execute script file",
            'exec': "Execute program (replaces shell)",
            'time': "Time command execution",
            'uptime': "System uptime",
            'uname': "System information",
            'true': "Return true (0)",
            'false': "Return false (1)",
            'sleep': "Delay for specified time",
            'printf': "Format and print data",
            'test': "Evaluate expression",
            '[': "Evaluate expression (alias)",
        }
        return helps.get(name, "Extra command")

    def _patch_ls_command(self):
        """Patch ls command with more options / 带更多选项的补丁"""
        original = self.shell._cmd_ls
        self._patched_commands['ls'] = original

        def patched_ls(args: List[str]):
            """Enhanced ls with -l, -a options / 增强的 ls 命令"""
            show_all = '-a' in args or '-A' in args
            long_format = '-l' in args
            paths = [a for a in args if not a.startswith('-')]

            if not paths:
                paths = ['.']

            for path in paths:
                # In real implementation, use VFS / 实际实现中使用 VFS
                # For now, use os.listdir if available / 现在，使用 os.listdir
                try:
                    if os.path.exists(path) and os.path.isdir(path):
                        items = os.listdir(path)
                        if not show_all:
                            items = [i for i in items if not i.startswith('.')]

                        if long_format:
                            for item in sorted(items):
                                full_path = os.path.join(path, item)
                                try:
                                    st = os.stat(full_path)
                                    size = st.st_size
                                    print(f"{item:20s} {size:8d}")
                                except OSError:
                                    print(item)
                        else:
                            print("  ".join(sorted(items)))
                    else:
                        print(f"ls: {path}: No such file or directory")
                except Exception as e:
                    print(f"ls: {path}: {e}")

        self.shell._cmd_ls = patched_ls

    def _patch_ps_command(self):
        """Patch ps command with more options / 带更多选项的补丁"""
        original = self.shell._cmd_ps
        self._patched_commands['ps'] = original

        def patched_ps(args: List[str]):
            """Enhanced ps with -a, -u, -x options / 增强的 ps 命令"""
            show_all = '-a' in args
            show_user = '-u' in args

            # In real implementation, read from /proc / 实际实现中从 /proc 读取
            print("PID  PPID  STATE    PRIORITY  NAME")
            print("1    0     RUNNING  128       init")
            print("2    1     READY    100       shell")
            print("3    1     SLEEPING 64        idle")

            if show_all:
                print("4    1     RUNNING  120       kthreadd")
                print("5    1     SLEEPING 100       kworker")

        self.shell._cmd_ps = patched_ps

    def _patch_help_command(self):
        """Patch help command with category support / 带分类支持的补丁"""
        original = self.shell._cmd_help
        self._patched_commands['help'] = original

        def patched_help(args: List[str]):
            """Enhanced help with categories / 增强的 help 命令"""
            if args and args[0] == '--categories':
                print("=== Shell Command Categories ===")
                print("  file    - File operations")
                print("  process - Process management")
                print("  system  - System information")
                print("  shell   - Shell builtins")
                print("  network - Network commands")
                print("  memory  - Memory management")
                print("  gui     - GUI commands")
                print("  extra   - Extra commands")
                return

            if args:
                cmd = args[0]
                if self.shell.commands.has(cmd):
                    info = self.shell.commands.get_info(cmd)
                    print(f"{cmd}: {info['help']}")
                    if hasattr(self.shell.commands, '_aliases') and cmd in self.shell.commands._aliases:
                        print(f"  Alias for: {self.shell.commands._aliases[cmd]}")
                    return
                print(f"Command not found: {cmd}")
                return

            # Show all commands / 显示所有命令
            print("=== Bamboo OS Shell Commands ===")
            print("")
            print("File operations:")
            print("  ls  cd  pwd  mkdir  rmdir  rm  cp  mv  cat  touch")
            print("")
            print("Process management:")
            print("  ps  kill  fork  exec  exit  bg  fg  jobs")
            print("")
            print("System information:")
            print("  uname  hostname  uptime  date  reboot  shutdown  clear")
            print("")
            print("Shell builtins:")
            print("  help  history  echo  alias  unalias  export  unset")
            print("  env  source  set  which")
            print("")
            print("Network commands:")
            print("  ifconfig  ping  netstat")
            print("")
            print("Memory commands:")
            print("  free  meminfo")
            print("")
            print("Extra commands:")
            print("  type  pushd  popd  dirs  time  printf  test  sleep")
            print("")
            print("GUI commands:")
            print("  gui  terminal")
            print("")
            print("Type 'help <command>' for more details")

        self.shell._cmd_help = patched_help

    # =========================================================================
    # Extra command implementations / 额外命令实现
    # =========================================================================

    def _cmd_which_ext(self, args: List[str]):
        """Enhanced which command / 增强的 which 命令"""
        if not args:
            print("Usage: which <command>")
            return

        path = self.shell.env.get('PATH', '/bin:/usr/bin')
        for cmd in args:
            found = False
            for dir_path in path.split(':'):
                full_path = os.path.join(dir_path, cmd)
                if os.path.exists(full_path):
                    print(f"{cmd}: {full_path}")
                    found = True
                    break

            if not found:
                print(f"{cmd}: not found")

    def _cmd_type(self, args: List[str]):
        """Type command / 命令类型"""
        if not args:
            print("Usage: type <command>")
            return

        for cmd in args:
            if self.shell.commands.has(cmd):
                info = self.shell.commands.get_info(cmd)
                if info.get('is_alias', False):
                    print(f"{cmd} is an alias for {info.get('target', cmd)}")
                else:
                    print(f"{cmd} is a shell builtin")
            else:
                print(f"{cmd}: not found")

    def _cmd_pushd(self, args: List[str]):
        """Push directory to stack / 将目录压入栈"""
        if not hasattr(self.shell, '_dir_stack'):
            self.shell._dir_stack = []

        if args:
            target = args[0]
            if os.path.isdir(target):
                self.shell._dir_stack.append(self.shell.cwd)
                self.shell._cmd_cd([target])
                print(self.shell.cwd)
            else:
                print(f"pushd: {target}: Not a directory")
        else:
            if self.shell._dir_stack:
                print(self.shell._dir_stack)
            else:
                print("Directory stack empty")

    def _cmd_popd(self, args: List[str]):
        """Pop directory from stack / 从栈弹出目录"""
        if not hasattr(self.shell, '_dir_stack') or not self.shell._dir_stack:
            print("popd: directory stack empty")
            return

        old_dir = self.shell._dir_stack.pop()
        self.shell._cmd_cd([old_dir])
        print(self.shell.cwd)

    def _cmd_dirs(self, args: List[str]):
        """Display directory stack / 显示目录栈"""
        if hasattr(self.shell, '_dir_stack') and self.shell._dir_stack:
            for i, d in enumerate(self.shell._dir_stack):
                print(f"{i}: {d}")
        else:
            print("Directory stack empty")

    def _cmd_export_ext(self, args: List[str]):
        """Enhanced export / 增强的 export"""
        if not args:
            for key, value in sorted(self.shell.env.items()):
                print(f"export {key}={value}")
            return

        for arg in args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                self.shell.env[key] = value
                print(f"export: {key}={value}")
            else:
                print(f"export: {arg} (missing =)")

    def _cmd_source_ext(self, args: List[str]):
        """Enhanced source / 增强的 source"""
        if not args:
            print("Usage: source <script> [args...]")
            return

        for script in args:
            try:
                with open(script, 'r') as f:
                    content = f.read()
                for line in content.split('\n'):
                    if line.strip() and not line.startswith('#'):
                        self.shell._execute_line(line)
            except Exception as e:
                print(f"source: {script}: {e}")

    def _cmd_exec_ext(self, args: List[str]):
        """Enhanced exec / 增强的 exec"""
        if not args:
            print("Usage: exec <program> [args...]")
            return

        # exec replaces the shell / exec 替换 shell
        try:
            os.execvp(args[0], args)
        except Exception as e:
            print(f"exec: {args[0]}: {e}")

    def _cmd_time(self, args: List[str]):
        """Time command execution / 计时命令执行"""
        if not args:
            print("Usage: time <command> [args...]")
            return

        import time
        start = time.time()

        try:
            self.shell._execute_line(" ".join(args))
        except Exception as e:
            print(f"time: {e}")

        elapsed = time.time() - start
        print(f"\nreal {elapsed:.3f}s")

    def _cmd_uptime_ext(self, args: List[str]):
        """Enhanced uptime / 增强的 uptime"""
        # In real implementation, read from /proc/uptime / 实际实现中从 /proc/uptime 读取
        import time
        uptime_seconds = int(time.time()) % 100000
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        print(f"up {days} days, {hours:02d}:{minutes:02d}")

    def _cmd_uname_ext(self, args: List[str]):
        """Enhanced uname / 增强的 uname"""
        options = {
            '-a': "BambooOS Wonder 1.0 x86-64 Bamboo",
            '-s': "BambooOS",
            '-n': "bamboo",
            '-r': "1.0.0",
            '-v': "Wonder",
            '-m': "x86_64",
        }

        if args:
            for arg in args:
                if arg in options:
                    print(options[arg])
                else:
                    print(f"uname: invalid option {arg}")
        else:
            print(options['-s'])

    def _cmd_true(self, args: List[str]):
        """Always return true / 总是返回真"""
        pass

    def _cmd_false(self, args: List[str]):
        """Always return false / 总是返回假"""
        sys.exit(1)

    def _cmd_sleep(self, args: List[str]):
        """Delay for specified time / 延迟指定时间"""
        if not args:
            print("Usage: sleep <seconds>")
            return
        try:
            seconds = float(args[0])
            time.sleep(seconds)
        except ValueError:
            print(f"sleep: invalid time: {args[0]}")

    def _cmd_printf(self, args: List[str]):
        """Format and print data / 格式化并打印数据"""
        if not args:
            print("Usage: printf <format> [arguments...]")
            return

        fmt = args[0]
        values = args[1:] if len(args) > 1 else []

        try:
            if values:
                print(fmt % tuple(values))
            else:
                print(fmt)
        except Exception as e:
            print(f"printf: {e}")

    def _cmd_test(self, args: List[str]):
        """Evaluate expression / 求值表达式"""
        if not args:
            print("Usage: test <expression>")
            return

        # Simple test implementation / 简单测试实现
        if args[0] == '-f' and len(args) > 1:
            # Check if file exists / 检查文件是否存在
            if os.path.exists(args[1]) and os.path.isfile(args[1]):
                return
            sys.exit(1)

        if args[0] == '-d' and len(args) > 1:
            # Check if directory exists / 检查目录是否存在
            if os.path.exists(args[1]) and os.path.isdir(args[1]):
                return
            sys.exit(1)

        if args[0] == '-e' and len(args) > 1:
            # Check if path exists / 检查路径是否存在
            if os.path.exists(args[1]):
                return
            sys.exit(1)

        if len(args) == 3 and args[1] == '=':
            # String equality / 字符串相等
            if args[0] == args[2]:
                return
            sys.exit(1)

        if len(args) == 3 and args[1] == '!=':
            # String inequality / 字符串不相等
            if args[0] != args[2]:
                return
            sys.exit(1)

        # Default: return true / 默认返回真
        return