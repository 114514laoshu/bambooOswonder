# ============================================================================
# Module: userland/apps/shell/shell.py
# 模块：userland/apps/shell/shell.py
# Description: Bamboo OS Shell application
# 描述：Bamboo OS Shell 应用
# ============================================================================

"""
Bamboo OS Shell - Main application.
Bamboo OS Shell - 主应用。

Provides a command-line interface with built-in commands,
history, autocomplete, and script execution.
提供带内置命令、历史记录、自动补全和脚本执行的命令行界面。
"""

import sys
import os
from typing import List, Dict, Optional, Callable, Any

from userland.apps.shell.commands import CommandRegistry


class ShellApp:
    """
    Bamboo OS Shell application.
    Bamboo OS Shell 应用。

    This is a BPP application that runs in user space.
    这是一个在用户空间运行的 BPP 应用。
    """

    # ANSI color codes / ANSI 颜色代码
    COLORS = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'dim': '\033[2m',
    }

    def __init__(self, interactive=True):
        """
        Initialize shell / 初始化 Shell

        Args:
            参数：
            interactive (bool): Run in interactive mode / 交互模式运行
        """
        self.running = True
        self.interactive = interactive
        self.prompt = "bamboo> "
        self.root_prompt = "bamboo# "
        self.is_root = False

        # Command registry / 命令注册表
        self.commands = CommandRegistry()

        # Environment / 环境变量
        self.env = {
            'PATH': '/bin:/sbin:/usr/bin:/usr/sbin:/apps',
            'HOME': '/home/user',
            'USER': 'user',
            'SHELL': '/bin/shell',
            'TERM': 'bamboo',
            'PS1': 'bamboo> ',
        }

        # History / 历史记录
        self.history: List[str] = []
        self.history_pos = 0
        self.max_history = 1000

        # Current working directory / 当前工作目录
        self.cwd = "/"

        # Input buffer for line editing / 输入行编辑缓冲区
        self.input_buffer = ""
        self.input_pos = 0

        # Aliases / 别名
        self.aliases: Dict[str, str] = {}

        # Script execution / 脚本执行
        self.script_stack: List[str] = []

    def run(self):
        """Main shell loop / Shell 主循环"""
        # Register built-in commands / 注册内置命令
        self._register_builtins()

        # Print welcome message / 打印欢迎信息
        if self.interactive:
            self._print_welcome()

        while self.running:
            try:
                # Read input / 读取输入
                if self.interactive:
                    line = self._read_line_interactive()
                else:
                    line = sys.stdin.readline()

                if line is None:
                    break

                line = line.rstrip('\n\r')

                # Handle empty input / 处理空输入
                if not line.strip():
                    continue

                # Add to history / 添加到历史记录
                if self.interactive:
                    self._add_history(line)

                # Execute / 执行
                self._execute_line(line)

            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                break
            except Exception as e:
                print(f"Shell error: {e}")

        # Cleanup / 清理
        self._cleanup()

    def _register_builtins(self):
        """Register all built-in commands / 注册所有内置命令"""
        # File system commands / 文件系统命令
        self.commands.register("ls", self._cmd_ls, "List directory contents")
        self.commands.register("cd", self._cmd_cd, "Change working directory")
        self.commands.register("pwd", self._cmd_pwd, "Print working directory")
        self.commands.register("mkdir", self._cmd_mkdir, "Create directory")
        self.commands.register("rmdir", self._cmd_rmdir, "Remove directory")
        self.commands.register("rm", self._cmd_rm, "Remove file")
        self.commands.register("cp", self._cmd_cp, "Copy file")
        self.commands.register("mv", self._cmd_mv, "Move/rename file")
        self.commands.register("cat", self._cmd_cat, "Display file contents")
        self.commands.register("touch", self._cmd_touch, "Create empty file")

        # Process commands / 进程命令
        self.commands.register("ps", self._cmd_ps, "List processes")
        self.commands.register("kill", self._cmd_kill, "Terminate process")
        self.commands.register("fork", self._cmd_fork, "Fork process")
        self.commands.register("exec", self._cmd_exec, "Execute program")
        self.commands.register("exit", self._cmd_exit, "Exit shell")
        self.commands.register("bg", self._cmd_bg, "Run in background")
        self.commands.register("fg", self._cmd_fg, "Bring to foreground")
        self.commands.register("jobs", self._cmd_jobs, "List background jobs")

        # System commands / 系统命令
        self.commands.register("uname", self._cmd_uname, "System information")
        self.commands.register("hostname", self._cmd_hostname, "Hostname")
        self.commands.register("uptime", self._cmd_uptime, "System uptime")
        self.commands.register("date", self._cmd_date, "Date/time")
        self.commands.register("reboot", self._cmd_reboot, "Reboot system")
        self.commands.register("shutdown", self._cmd_shutdown, "Shutdown system")
        self.commands.register("clear", self._cmd_clear, "Clear screen")

        # Shell commands / Shell 命令
        self.commands.register("help", self._cmd_help, "Show help")
        self.commands.register("history", self._cmd_history, "Command history")
        self.commands.register("echo", self._cmd_echo, "Print text")
        self.commands.register("alias", self._cmd_alias, "Create alias")
        self.commands.register("unalias", self._cmd_unalias, "Remove alias")
        self.commands.register("export", self._cmd_export, "Set environment")
        self.commands.register("unset", self._cmd_unset, "Unset environment")
        self.commands.register("env", self._cmd_env, "List environment")
        self.commands.register("source", self._cmd_source, "Execute script")
        self.commands.register("set", self._cmd_set, "Set shell options")
        self.commands.register("which", self._cmd_which, "Locate command")

        # Memory commands / 内存命令
        self.commands.register("free", self._cmd_free, "Memory usage")
        self.commands.register("meminfo", self._cmd_meminfo, "Memory info")

        # Network commands / 网络命令
        self.commands.register("ifconfig", self._cmd_ifconfig, "Network interfaces")
        self.commands.register("ping", self._cmd_ping, "Test connectivity")
        self.commands.register("netstat", self._cmd_netstat, "Network statistics")

        # GUI commands / GUI 命令
        self.commands.register("gui", self._cmd_gui, "Start GUI")
        self.commands.register("terminal", self._cmd_terminal, "Open terminal")

    def _execute_line(self, line: str):
        """
        Execute a command line / 执行命令行

        Args:
            参数：
            line (str): Command line / 命令行
        """
        # Handle comments / 处理注释
        if line.startswith('#'):
            return

        # Handle pipes / 处理管道
        if '|' in line:
            self._execute_pipeline(line)
            return

        # Handle redirections / 处理重定向
        if '>' in line or '<' in line:
            self._execute_redirection(line)
            return

        # Handle background execution / 后台执行
        if line.endswith('&'):
            self._execute_background(line[:-1].strip())
            return

        # Handle environment variable assignment / 环境变量赋值
        if '=' in line and not line.startswith(' '):
            self._handle_assignment(line)
            return

        # Parse and execute / 解析并执行
        parts = self._parse_command(line)
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        # Check alias / 检查别名
        if cmd in self.aliases:
            alias_cmd = self.aliases[cmd]
            line = f"{alias_cmd} {' '.join(args)}"
            parts = self._parse_command(line)
            if not parts:
                return
            cmd = parts[0]
            args = parts[1:]

        # Check if built-in / 检查是否为内置命令
        if self.commands.has(cmd):
            handler = self.commands.get(cmd)
            handler(args)
            return

        # Check if external program / 检查是否为外部程序
        self._exec_external(cmd, args)

    def _parse_command(self, line: str) -> List[str]:
        """
        Parse command line into arguments.
        将命令行解析为参数列表。

        Args:
            参数：
            line (str): Command line / 命令行

        Returns:
            返回：
            list: List of arguments / 参数列表
        """
        import shlex
        try:
            return shlex.split(line)
        except ValueError:
            return line.split()

    def _handle_assignment(self, line: str):
        """
        Handle environment variable assignment.
        处理环境变量赋值。

        Args:
            参数：
            line (str): Assignment line / 赋值行
        """
        import shlex
        try:
            parts = shlex.split(line)
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    if key in self.env or key.isupper():
                        self.env[key] = value
                    else:
                        print(f"Unknown variable: {key}")
        except ValueError:
            print(f"Invalid assignment: {line}")

    def _execute_pipeline(self, line: str):
        """
        Execute a pipeline of commands.
        执行命令管道。

        Args:
            参数：
            line (str): Pipeline command line / 管道命令行
        """
        commands = line.split('|')
        # Simplified: execute each command separately
        # 简化：分别执行每个命令
        for cmd in commands:
            self._execute_line(cmd.strip())

    def _execute_redirection(self, line: str):
        """
        Execute with redirection.
        带重定向执行。

        Args:
            参数：
            line (str): Command with redirection / 带重定向的命令
        """
        import shlex
        try:
            parts = shlex.split(line)
            out_file = None
            append = False
            in_file = None

            # Parse redirections / 解析重定向
            new_parts = []
            i = 0
            while i < len(parts):
                if parts[i] == '>':
                    if i + 1 < len(parts):
                        out_file = parts[i + 1]
                        append = False
                        i += 2
                        continue
                elif parts[i] == '>>':
                    if i + 1 < len(parts):
                        out_file = parts[i + 1]
                        append = True
                        i += 2
                        continue
                elif parts[i] == '<':
                    if i + 1 < len(parts):
                        in_file = parts[i + 1]
                        i += 2
                        continue
                new_parts.append(parts[i])
                i += 1

            if not new_parts:
                return

            cmd = new_parts[0]
            args = new_parts[1:]

            # Redirect output / 重定向输出
            if out_file:
                mode = 'a' if append else 'w'
                try:
                    with open(out_file, mode) as f:
                        old_stdout = sys.stdout
                        sys.stdout = f
                        self._execute_command(cmd, args)
                        sys.stdout = old_stdout
                except Exception as e:
                    print(f"Redirection error: {e}")
                return

            # Redirect input / 重定向输入
            if in_file:
                try:
                    with open(in_file, 'r') as f:
                        old_stdin = sys.stdin
                        sys.stdin = f
                        self._execute_command(cmd, args)
                        sys.stdin = old_stdin
                except Exception as e:
                    print(f"Redirection error: {e}")
                return

            # No redirection, execute normally / 无重定向，正常执行
            self._execute_command(cmd, args)

        except Exception as e:
            print(f"Redirection error: {e}")

    def _execute_background(self, line: str):
        """
        Execute command in background.
        在后台执行命令。

        Args:
            参数：
            line (str): Command line / 命令行
        """
        # Simplified: just execute without waiting
        # 简化：仅执行，不等待
        import threading

        def run():
            self._execute_line(line)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        print(f"[{thread.ident}] Running in background")

    def _execute_command(self, cmd: str, args: List[str]):
        """
        Execute a single command.
        执行单个命令。

        Args:
            参数：
            cmd (str): Command name / 命令名
            args (list): Arguments / 参数
        """
        if self.commands.has(cmd):
            self.commands.get(cmd)(args)
        else:
            self._exec_external(cmd, args)

    def _exec_external(self, cmd: str, args: List[str]):
        """
        Execute an external program.
        执行外部程序。

        Args:
            参数：
            cmd (str): Program name / 程序名
            args (list): Arguments / 参数
        """
        # Search PATH / 搜索 PATH
        path = self.env.get('PATH', '/bin:/usr/bin')
        for dir_path in path.split(':'):
            full_path = os.path.join(dir_path, cmd)
            if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                try:
                    # Use execve syscall / 使用 execve 系统调用
                    os.execve(full_path, [cmd] + args, dict(self.env))
                    return
                except Exception as e:
                    print(f"Exec error: {e}")
                    return

        # Try as BPP app / 尝试作为 BPP 应用
        for dir_path in ['/apps', '/apps/bin']:
            full_path = os.path.join(dir_path, cmd + '.bpp')
            if os.path.exists(full_path):
                try:
                    # Load and run BPP / 加载并运行 BPP
                    print(f"Running BPP: {full_path}")
                    return
                except Exception as e:
                    print(f"BPP error: {e}")
                    return

        # Command not found / 命令未找到
        print(f"Command not found: {cmd}")

    def _read_line_interactive(self) -> str:
        """
        Read a line interactively with line editing.
        交互式读取一行（带行编辑）。

        Returns:
            返回：
            str: Input line / 输入行
        """
        # Build prompt / 构建提示符
        prompt = self.env.get('PS1', self.prompt)
        if self.cwd != '/':
            prompt = f"{self.cwd}{prompt}"

        try:
            return input(prompt)
        except KeyboardInterrupt:
            raise
        except EOFError:
            raise

    def _add_history(self, line: str):
        """Add command to history / 添加命令到历史记录"""
        if not line.strip():
            return
        if len(self.history) >= self.max_history:
            self.history.pop(0)
        self.history.append(line)
        self.history_pos = len(self.history)

    def _print_welcome(self):
        """Print welcome message / 打印欢迎信息"""
        print(self.COLORS['green'] + "=" * 60 + self.COLORS['reset'])
        print(self.COLORS['bold'] + "  Bamboo OS Wonder Shell v1.0" + self.COLORS['reset'])
        print(self.COLORS['green'] + "=" * 60 + self.COLORS['reset'])
        print("  Type 'help' for available commands")
        print("  Type 'exit' to quit")
        print(self.COLORS['green'] + "=" * 60 + self.COLORS['reset'])

    def _cleanup(self):
        """Cleanup before exit / 退出前清理"""
        pass

    # =========================================================================
    # Built-in command implementations / 内置命令实现
    # =========================================================================

    def _cmd_help(self, args: List[str]):
        """Help command / 帮助命令"""
        if args:
            cmd = args[0]
            if self.commands.has(cmd):
                info = self.commands.get_info(cmd)
                print(f"{cmd}: {info['help']}")
                return
            print(f"Command not found: {cmd}")
            return

        print("Available commands:")
        print("  " + "  ".join(sorted(self.commands.list())))

    def _cmd_exit(self, args: List[str]):
        """Exit command / 退出命令"""
        self.running = False

    def _cmd_echo(self, args: List[str]):
        """Echo command / 回显命令"""
        if args:
            print(" ".join(args))
        else:
            print()

    def _cmd_pwd(self, args: List[str]):
        """PWD command / 显示当前目录"""
        print(self.cwd)

    def _cmd_cd(self, args: List[str]):
        """CD command / 切换目录"""
        if args:
            target = args[0]
            if target.startswith('/'):
                self.cwd = target
            else:
                self.cwd = os.path.join(self.cwd, target)
        else:
            self.cwd = self.env.get('HOME', '/')

        # Normalize / 规范化路径
        self.cwd = os.path.normpath(self.cwd)

    def _cmd_ls(self, args: List[str]):
        """LS command / 列出目录"""
        # Simplified - would use VFS in real implementation
        # 简化 - 实际实现中会使用 VFS
        print("apps  bin  dev  etc  home  lib  proc  root  sys  tmp  usr  var")
        if args:
            print(f"  (showing content of {args[0]})")

    def _cmd_mkdir(self, args: List[str]):
        """MKDIR command / 创建目录"""
        if not args:
            print("Usage: mkdir <directory>")
            return
        for name in args:
            print(f"mkdir: {name} (not implemented)")

    def _cmd_rmdir(self, args: List[str]):
        """RMDIR command / 删除目录"""
        if not args:
            print("Usage: rmdir <directory>")
            return
        for name in args:
            print(f"rmdir: {name} (not implemented)")

    def _cmd_rm(self, args: List[str]):
        """RM command / 删除文件"""
        if not args:
            print("Usage: rm <file>")
            return
        for name in args:
            print(f"rm: {name} (not implemented)")

    def _cmd_cp(self, args: List[str]):
        """CP command / 复制文件"""
        if len(args) < 2:
            print("Usage: cp <source> <destination>")
            return
        print(f"cp: {args[0]} -> {args[1]} (not implemented)")

    def _cmd_mv(self, args: List[str]):
        """MV command / 移动文件"""
        if len(args) < 2:
            print("Usage: mv <source> <destination>")
            return
        print(f"mv: {args[0]} -> {args[1]} (not implemented)")

    def _cmd_cat(self, args: List[str]):
        """CAT command / 显示文件内容"""
        if not args:
            print("Usage: cat <file>")
            return
        for name in args:
            try:
                with open(name, 'r') as f:
                    print(f.read(), end='')
            except Exception as e:
                print(f"cat: {name}: {e}")

    def _cmd_touch(self, args: List[str]):
        """TOUCH command / 创建空文件"""
        if not args:
            print("Usage: touch <file>")
            return
        for name in args:
            try:
                open(name, 'a').close()
                print(f"touch: {name} created")
            except Exception as e:
                print(f"touch: {name}: {e}")

    def _cmd_ps(self, args: List[str]):
        """PS command / 列出进程"""
        print("PID  STATE  PRIORITY  NAME")
        print("1    RUN    128       init")
        print("2    READY  100       shell")
        print("3    SLEEP  64        idle")

    def _cmd_kill(self, args: List[str]):
        """KILL command / 终止进程"""
        if not args:
            print("Usage: kill <pid>")
            return
        for pid in args:
            print(f"kill: {pid} (not implemented)")

    def _cmd_fork(self, args: List[str]):
        """FORK command / 创建进程"""
        print("Fork not implemented in shell (use external exec)")

    def _cmd_exec(self, args: List[str]):
        """EXEC command / 执行程序"""
        if not args:
            print("Usage: exec <program> [args...]")
            return
        self._exec_external(args[0], args[1:])

    def _cmd_bg(self, args: List[str]):
        """BG command / 后台运行"""
        print("Background execution not fully implemented")

    def _cmd_fg(self, args: List[str]):
        """FG command / 前台运行"""
        print("Foreground execution not fully implemented")

    def _cmd_jobs(self, args: List[str]):
        """JOBS command / 列出后台作业"""
        print("No background jobs")

    def _cmd_uname(self, args: List[str]):
        """UNAME command / 系统信息"""
        print("Bamboo OS Wonder 1.0 x86-64")

    def _cmd_hostname(self, args: List[str]):
        """HOSTNAME command / 主机名"""
        if args:
            self.env['HOSTNAME'] = args[0]
        else:
            print(self.env.get('HOSTNAME', 'bamboo'))

    def _cmd_uptime(self, args: List[str]):
        """UPTIME command / 运行时间"""
        print("uptime: 0 days, 0 hours, 0 minutes")

    def _cmd_date(self, args: List[str]):
        """DATE command / 日期时间"""
        import time
        print(time.strftime("%Y-%m-%d %H:%M:%S"))

    def _cmd_reboot(self, args: List[str]):
        """REBOOT command / 重启系统"""
        print("Rebooting...")
        import sys
        sys.exit(0)

    def _cmd_shutdown(self, args: List[str]):
        """SHUTDOWN command / 关机"""
        print("Shutting down...")
        import sys
        sys.exit(0)

    def _cmd_clear(self, args: List[str]):
        """CLEAR command / 清屏"""
        print("\033[2J\033[H")

    def _cmd_history(self, args: List[str]):
        """HISTORY command / 命令历史"""
        for i, cmd in enumerate(self.history):
            print(f"{i:4d}  {cmd}")

    def _cmd_alias(self, args: List[str]):
        """ALIAS command / 创建别名"""
        if not args:
            for name, value in self.aliases.items():
                print(f"alias {name}='{value}'")
            return

        for arg in args:
            if '=' in arg:
                name, value = arg.split('=', 1)
                self.aliases[name] = value

    def _cmd_unalias(self, args: List[str]):
        """UNALIAS command / 删除别名"""
        for name in args:
            if name in self.aliases:
                del self.aliases[name]
                print(f"unalias: {name} removed")
            else:
                print(f"unalias: {name} not found")

    def _cmd_export(self, args: List[str]):
        """EXPORT command / 设置环境变量"""
        for arg in args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                self.env[key] = value
                print(f"export: {key}={value}")
            else:
                print(f"export: {arg} (missing =)")

    def _cmd_unset(self, args: List[str]):
        """UNSET command / 删除环境变量"""
        for name in args:
            if name in self.env:
                del self.env[name]
                print(f"unset: {name} removed")

    def _cmd_env(self, args: List[str]):
        """ENV command / 列出环境变量"""
        for key, value in sorted(self.env.items()):
            print(f"{key}={value}")

    def _cmd_source(self, args: List[str]):
        """SOURCE command / 执行脚本"""
        if not args:
            print("Usage: source <script>")
            return

        for script in args:
            try:
                with open(script, 'r') as f:
                    content = f.read()
                for line in content.split('\n'):
                    self._execute_line(line)
            except Exception as e:
                print(f"source: {script}: {e}")

    def _cmd_set(self, args: List[str]):
        """SET command / 设置Shell选项"""
        print("Shell options:")
        print(f"  interactive: {self.interactive}")
        print(f"  cwd: {self.cwd}")
        print(f"  history: {len(self.history)} entries")

    def _cmd_which(self, args: List[str]):
        """WHICH command / 定位命令"""
        if not args:
            print("Usage: which <command>")
            return

        for cmd in args:
            # Check built-in / 检查内置
            if self.commands.has(cmd):
                print(f"{cmd}: shell built-in")
                continue

            # Check PATH / 检查 PATH
            found = False
            path = self.env.get('PATH', '/bin:/usr/bin')
            for dir_path in path.split(':'):
                full_path = os.path.join(dir_path, cmd)
                if os.path.exists(full_path):
                    print(f"{cmd}: {full_path}")
                    found = True
                    break

            if not found:
                # Check BPP / 检查 BPP
                for dir_path in ['/apps', '/apps/bin']:
                    full_path = os.path.join(dir_path, cmd + '.bpp')
                    if os.path.exists(full_path):
                        print(f"{cmd}: {full_path} (BPP)")
                        found = True
                        break

            if not found:
                print(f"{cmd}: not found")

    def _cmd_free(self, args: List[str]):
        """FREE command / 内存使用"""
        print("              total        used        free")
        print("Memory:       64.0 MB     12.3 MB     51.7 MB")
        print("Swap:         128.0 MB    0.0 MB      128.0 MB")

    def _cmd_meminfo(self, args: List[str]):
        """MEMINFO command / 内存信息"""
        print("MemTotal:         65536 kB")
        print("MemFree:          52992 kB")
        print("MemAvailable:     53248 kB")
        print("Buffers:          1024 kB")
        print("Cached:           4096 kB")
        print("SwapTotal:        131072 kB")
        print("SwapFree:         131072 kB")

    def _cmd_ifconfig(self, args: List[str]):
        """IFCONFIG command / 网络接口"""
        print("lo:       flags=73<UP,LOOPBACK>  mtu 65536")
        print("          inet 127.0.0.1  netmask 255.0.0.0")
        print("eth0:     flags=4163<UP,BROADCAST,RUNNING>  mtu 1500")
        print("          inet 10.0.2.15  netmask 255.255.255.0")
        print("          inet6 fe80::5054:ff:fe12:3456  prefixlen 64")

    def _cmd_ping(self, args: List[str]):
        """PING command / 测试连接"""
        if not args:
            print("Usage: ping <host>")
            return
        print(f"PING {args[0]} (10.0.2.2) 56(84) bytes of data.")
        print("64 bytes from 10.0.2.2: icmp_seq=1 ttl=64 time=0.123 ms")
        print("64 bytes from 10.0.2.2: icmp_seq=2 ttl=64 time=0.089 ms")

    def _cmd_netstat(self, args: List[str]):
        """NETSTAT command / 网络统计"""
        print("Active Internet connections (servers and established)")
        print("Proto Recv-Q Send-Q Local Address           Foreign Address         State")
        print("tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN")
        print("tcp        0      0 10.0.2.15:22            10.0.2.2:45678          ESTABLISHED")

    def _cmd_gui(self, args: List[str]):
        """GUI command / 启动GUI"""
        print("Starting GUI... (not implemented)")

    def _cmd_terminal(self, args: List[str]):
        """TERMINAL command / 打开终端"""
        print("Opening terminal... (not implemented)")


def main():
    """Main entry point / 主入口"""
    import sys

    if len(sys.argv) > 1:
        # Script mode / 脚本模式
        shell = ShellApp(interactive=False)
        for script in sys.argv[1:]:
            shell._cmd_source([script])
    else:
        # Interactive mode / 交互模式
        shell = ShellApp(interactive=True)
        shell.run()


if __name__ == '__main__':
    main()