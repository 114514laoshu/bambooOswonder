# ============================================================================
# Module: userland/apps/editor/editor.py
# 模块：userland/apps/editor/editor.py
# Description: Text editor application
# 描述：文本编辑器应用
# ============================================================================

"""
Text editor for Bamboo OS.
Bamboo OS 文本编辑器。

A simple text editor with syntax highlighting and file operations.
一个带有语法高亮和文件操作的简单文本编辑器。
"""

import os
import sys
from typing import List, Optional, Tuple, Dict, Any


class EditorApp:
    """
    Text editor application.
    文本编辑器应用。

    This is a BPP application that provides text editing capabilities.
    这是一个提供文本编辑功能的 BPP 应用。
    """

    # Syntax highlighting / 语法高亮
    SYNTAX_KEYWORDS = {
        'python': [
            'import', 'from', 'def', 'class', 'if', 'elif', 'else',
            'for', 'while', 'return', 'yield', 'try', 'except',
            'finally', 'with', 'as', 'pass', 'break', 'continue',
            'lambda', 'nonlocal', 'global', 'async', 'await',
        ],
        'c': [
            'int', 'char', 'void', 'return', 'if', 'else', 'while',
            'for', 'struct', 'union', 'enum', 'typedef', 'extern',
            'static', 'const', 'volatile', 'unsigned', 'signed',
            'sizeof', 'break', 'continue', 'goto', 'switch',
        ],
        'shell': [
            'if', 'then', 'else', 'elif', 'fi', 'for', 'while',
            'do', 'done', 'case', 'esac', 'function', 'return',
            'break', 'continue', 'export', 'local', 'readonly',
        ],
    }

    def __init__(self, filepath: Optional[str] = None):
        """
        Initialize editor.
        初始化编辑器。

        Args:
            参数：
            filepath (str): File to edit / 要编辑的文件
        """
        self.filepath = filepath

        # Buffer / 缓冲区
        self.lines: List[str] = []
        self.line_states: List[Dict[str, Any]] = []

        # Cursor / 光标
        self.cursor_x = 0
        self.cursor_y = 0

        # Scroll / 滚动
        self.scroll_x = 0
        self.scroll_y = 0
        self.width = 80
        self.height = 24

        # Mode / 模式
        self.mode = 'normal'  # normal / insert / visual / command
        self.mode_message = "NORMAL"

        # Clipboard / 剪贴板
        self.clipboard: List[str] = []

        # File info / 文件信息
        self.filename = filepath or "untitled"
        self.modified = False
        self.language = self._detect_language(self.filename)

        # History / 历史
        self.undo_stack: List[Tuple[str, int, str, str]] = []
        self.redo_stack: List[Tuple[str, int, str, str]] = []
        self.max_undo = 100

        # Running state / 运行状态
        self.running = True

        # Load file if exists / 如果文件存在则加载
        if filepath and os.path.exists(filepath):
            self._load_file(filepath)

    def run(self):
        """Main editor loop / 编辑器主循环"""
        self._init_screen()

        while self.running:
            self._render()
            key = self._get_key()
            if key:
                self._handle_key(key)

        self._cleanup()

    def _init_screen(self):
        """Initialize screen / 初始化屏幕"""
        # In real implementation, setup curses / 实际实现中设置 curses
        print("\033[2J\033[H")
        print(f"Editing: {self.filename}")

    def _get_key(self) -> Optional[str]:
        """Get user input / 获取用户输入"""
        import sys
        import select
        import tty
        import termios

        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                if select.select([sys.stdin], [], [], 0.05)[0]:
                    ch = sys.stdin.read(1)
                    if ch == '\x1b':
                        # Escape sequence / 转义序列
                        if select.select([sys.stdin], [], [], 0.05)[0]:
                            ch2 = sys.stdin.read(1)
                            if ch2 == '[':
                                ch3 = sys.stdin.read(1)
                                if ch3:
                                    return f'\x1b[{ch3}'
                            return ch + ch2
                    return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            pass
        return None

    def _handle_key(self, key: str):
        """
        Handle key press.
        处理按键。

        Args:
            参数：
            key (str): Key character / 按键字符
        """
        # Mode switching / 模式切换
        if key == 'i' and self.mode == 'normal':
            self.mode = 'insert'
            self.mode_message = "INSERT"
            return

        if key == 'v' and self.mode == 'normal':
            self.mode = 'visual'
            self.mode_message = "VISUAL"
            self._visual_start = (self.cursor_x, self.cursor_y)
            return

        if key == ':' and self.mode == 'normal':
            self.mode = 'command'
            self.mode_message = "COMMAND"
            self.command_buffer = ""
            return

        if key == '\x1b' or key == '\x1b[':
            self.mode = 'normal'
            self.mode_message = "NORMAL"
            return

        # Mode-specific handling / 模式特定处理
        if self.mode == 'normal':
            self._handle_normal(key)
        elif self.mode == 'insert':
            self._handle_insert(key)
        elif self.mode == 'visual':
            self._handle_visual(key)
        elif self.mode == 'command':
            self._handle_command(key)

    def _handle_normal(self, key: str):
        """Handle normal mode keys / 处理正常模式按键"""
        if key == 'h':
            self.cursor_x = max(0, self.cursor_x - 1)
        elif key == 'l':
            self.cursor_x = min(len(self.lines[self.cursor_y]) if self.lines else 0,
                              self.cursor_x + 1)
        elif key == 'j':
            self.cursor_y = min(len(self.lines) - 1, self.cursor_y + 1)
            self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]) if self.lines else 0)
        elif key == 'k':
            self.cursor_y = max(0, self.cursor_y - 1)
            self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]) if self.lines else 0)
        elif key == '0':
            self.cursor_x = 0
        elif key == '$':
            self.cursor_x = len(self.lines[self.cursor_y]) if self.lines else 0
        elif key == 'x':
            self._delete_char()
        elif key == 'd' and self._next_key_is('d'):
            self._delete_line()
        elif key == 'o':
            self._insert_line_below()
            self.mode = 'insert'
            self.mode_message = "INSERT"
        elif key == 'O':
            self._insert_line_above()
            self.mode = 'insert'
            self.mode_message = "INSERT"
        elif key == 'w':
            self._save_file()
        elif key == 'q':
            self._quit()
        elif key == 'u':
            self._undo()
        elif key == 'r':
            self._redo()
        elif key == '/':
            self.mode = 'command'
            self.mode_message = "SEARCH"
            self.command_buffer = "/"

    def _handle_insert(self, key: str):
        """Handle insert mode keys / 处理插入模式按键"""
        if key == '\x7f':  # Backspace / 退格
            if self.cursor_x > 0:
                self._add_undo('delete', self.cursor_y, str(self.cursor_x - 1), '')
                self.lines[self.cursor_y] = (self.lines[self.cursor_y][:self.cursor_x - 1] +
                                            self.lines[self.cursor_y][self.cursor_x:])
                self.cursor_x -= 1
            elif self.cursor_y > 0:
                # Merge with previous line / 合并到上一行
                prev_len = len(self.lines[self.cursor_y - 1])
                self.lines[self.cursor_y - 1] += self.lines[self.cursor_y]
                self.lines.pop(self.cursor_y)
                self.cursor_y -= 1
                self.cursor_x = prev_len
        elif key == '\r':  # Enter / 回车
            self._add_undo('insert', self.cursor_y, '', '\n')
            self.lines.insert(self.cursor_y + 1,
                             self.lines[self.cursor_y][self.cursor_x:])
            self.lines[self.cursor_y] = self.lines[self.cursor_y][:self.cursor_x]
            self.cursor_y += 1
            self.cursor_x = 0
        elif key.isprintable():
            self._add_undo('insert', self.cursor_y, '', key)
            self.lines[self.cursor_y] = (self.lines[self.cursor_y][:self.cursor_x] +
                                         key +
                                         self.lines[self.cursor_y][self.cursor_x:])
            self.cursor_x += 1

    def _handle_visual(self, key: str):
        """Handle visual mode keys / 处理可视模式按键"""
        # Similar to normal mode but with selection / 与正常模式类似但带选择
        self._handle_normal(key)

        # Update selection / 更新选择
        if key in 'hjlky':
            start = self._visual_start
            end = (self.cursor_x, self.cursor_y)

            if start == end:
                self.mode = 'normal'
                self.mode_message = "NORMAL"
                return

        if key == 'y':  # Yank / 复制
            self._yank_selection()
            self.mode = 'normal'
            self.mode_message = "NORMAL"
        elif key == 'd':  # Delete / 删除
            self._delete_selection()
            self.mode = 'normal'
            self.mode_message = "NORMAL"

    def _handle_command(self, key: str):
        """Handle command mode keys / 处理命令模式按键"""
        if key == '\r':  # Enter / 回车
            self._execute_command(self.command_buffer)
            self.mode = 'normal'
            self.mode_message = "NORMAL"
            self.command_buffer = ""
        elif key == '\x7f':  # Backspace / 退格
            self.command_buffer = self.command_buffer[:-1]
        elif key.isprintable():
            self.command_buffer += key
        elif key == '\x1b':  # Escape / 退出
            self.mode = 'normal'
            self.mode_message = "NORMAL"
            self.command_buffer = ""

    def _execute_command(self, cmd: str):
        """
        Execute a command.
        执行命令。

        Args:
            参数：
            cmd (str): Command string / 命令字符串
        """
        if not cmd:
            return

        if cmd.startswith('/'):
            self._search(cmd[1:])
            return

        if cmd == 'w':
            self._save_file()
        elif cmd == 'wq':
            self._save_file()
            self._quit()
        elif cmd == 'q':
            self._quit()
        elif cmd == 'q!':
            self.modified = False
            self._quit()
        elif cmd.startswith('set '):
            self._set_option(cmd[4:])
        elif cmd == 'help':
            self._show_help()
        else:
            print(f"Unknown command: {cmd}")

    def _delete_char(self):
        """Delete character at cursor / 删除光标处的字符"""
        if not self.lines:
            return

        if self.cursor_x < len(self.lines[self.cursor_y]):
            self._add_undo('delete', self.cursor_y,
                          str(self.cursor_x),
                          self.lines[self.cursor_y][self.cursor_x])
            self.lines[self.cursor_y] = (self.lines[self.cursor_y][:self.cursor_x] +
                                        self.lines[self.cursor_y][self.cursor_x + 1:])

    def _delete_line(self):
        """Delete current line / 删除当前行"""
        if not self.lines:
            return

        self._add_undo('delete', self.cursor_y, 'line', self.lines[self.cursor_y])
        self.lines.pop(self.cursor_y)
        if self.cursor_y >= len(self.lines):
            self.cursor_y = len(self.lines) - 1

    def _insert_line_below(self):
        """Insert line below / 在下方插入行"""
        if not self.lines:
            self.lines = ['']
        else:
            self.lines.insert(self.cursor_y + 1, '')
            self.cursor_y += 1
        self.cursor_x = 0

    def _insert_line_above(self):
        """Insert line above / 在上方插入行"""
        if not self.lines:
            self.lines = ['']
        else:
            self.lines.insert(self.cursor_y, '')
        self.cursor_x = 0

    def _yank_selection(self):
        """Yank selected text / 复制选中的文本"""
        start = self._visual_start
        end = (self.cursor_x, self.cursor_y)

        y1, y2 = min(start[1], end[1]), max(start[1], end[1])
        self.clipboard = []

        for y in range(y1, y2 + 1):
            if y == y1 and y == y2:
                x1, x2 = min(start[0], end[0]), max(start[0], end[0])
                line = self.lines[y][x1:x2]
                self.clipboard.append(line)
            elif y == y1:
                line = self.lines[y][start[0]:]
                self.clipboard.append(line)
            elif y == y2:
                line = self.lines[y][:end[0]]
                self.clipboard.append(line)
            else:
                self.clipboard.append(self.lines[y])

    def _delete_selection(self):
        """Delete selected text / 删除选中的文本"""
        start = self._visual_start
        end = (self.cursor_x, self.cursor_y)

        y1, y2 = min(start[1], end[1]), max(start[1], end[1])

        for y in range(y2, y1 - 1, -1):
            if y == y1 and y == y2:
                x1, x2 = min(start[0], end[0]), max(start[0], end[0])
                self.lines[y] = self.lines[y][:x1] + self.lines[y][x2:]
            elif y == y2:
                self.lines[y] = self.lines[y][:end[0]]
            elif y == y1:
                self.lines[y] = self.lines[y][start[0]:]
            else:
                self.lines.pop(y)

        self.cursor_x = min(start[0], end[0])
        self.cursor_y = y1

    def _search(self, pattern: str):
        """
        Search for pattern.
        搜索模式。

        Args:
            参数：
            pattern (str): Search pattern / 搜索模式
        """
        if not pattern:
            return

        for y in range(self.cursor_y + 1, len(self.lines)):
            if pattern in self.lines[y]:
                self.cursor_y = y
                self.cursor_x = self.lines[y].index(pattern)
                return

        # Wrap around / 环绕
        for y in range(0, self.cursor_y + 1):
            if pattern in self.lines[y]:
                self.cursor_y = y
                self.cursor_x = self.lines[y].index(pattern)
                return

    def _add_undo(self, operation: str, line: int, pos: str, data: str):
        """Add undo record / 添加撤消记录"""
        self.undo_stack.append((operation, line, pos, data))
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def _undo(self):
        """Undo last operation / 撤消上次操作"""
        if not self.undo_stack:
            return

        op, line, pos, data = self.undo_stack.pop()
        self.redo_stack.append((op, line, pos, data))

        if op == 'insert':
            # Remove inserted text / 移除插入的文本
            if pos == '':
                # Line insertion / 行插入
                if line < len(self.lines):
                    self.lines.pop(line)
            else:
                # Character insertion / 字符插入
                self.lines[line] = (self.lines[line][:int(pos)] +
                                   self.lines[line][int(pos) + 1:])
        elif op == 'delete':
            # Restore deleted text / 恢复删除的文本
            if pos == 'line':
                self.lines.insert(line, data)
            else:
                self.lines[line] = (self.lines[line][:int(pos)] +
                                   data +
                                   self.lines[line][int(pos):])

    def _redo(self):
        """Redo last undone operation / 重做上次撤消的操作"""
        if not self.redo_stack:
            return

        op, line, pos, data = self.redo_stack.pop()
        self.undo_stack.append((op, line, pos, data))

        if op == 'insert':
            if pos == '':
                self.lines.insert(line, '')
            else:
                self.lines[line] = (self.lines[line][:int(pos)] +
                                   data +
                                   self.lines[line][int(pos):])
        elif op == 'delete':
            if pos == 'line':
                self.lines.pop(line)
            else:
                self.lines[line] = (self.lines[line][:int(pos)] +
                                   self.lines[line][int(pos) + 1:])

    def _load_file(self, filepath: str):
        """Load file into buffer / 加载文件到缓冲区"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.lines = f.read().splitlines()
                if not self.lines:
                    self.lines = ['']
            self.modified = False
        except Exception as e:
            print(f"Error loading file: {e}")
            self.lines = ['']

    def _save_file(self):
        """Save buffer to file / 保存缓冲区到文件"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.lines))
            self.modified = False
            self.mode_message = f"Saved: {self.filename}"
        except Exception as e:
            self.mode_message = f"Error saving: {e}"

    def _quit(self):
        """Quit editor / 退出编辑器"""
        if self.modified:
            self.mode_message = "File modified, use :wq or :q!"
            return
        self.running = False

    def _set_option(self, opt: str):
        """Set editor option / 设置编辑器选项"""
        if opt == 'number':
            self._show_line_numbers = True
        elif opt == 'nonumber':
            self._show_line_numbers = False
        else:
            self.mode_message = f"Unknown option: {opt}"

    def _show_help(self):
        """Show help / 显示帮助"""
        help_text = """
        === Bamboo Editor Help ===

        Normal mode:
          h/j/k/l  - Move cursor
          i        - Enter insert mode
          v        - Enter visual mode
          :        - Enter command mode
          x        - Delete character
          dd       - Delete line
          o/O      - Insert line below/above
          w        - Save file
          q        - Quit
          u        - Undo
          r        - Redo
          /        - Search

        Insert mode:
          Type text to insert
          ESC      - Return to normal mode

        Command mode:
          w        - Save
          wq       - Save and quit
          q!       - Quit without saving
          set number   - Show line numbers
          set nonumber - Hide line numbers
          help     - Show this help
        """
        self.mode_message = help_text

    def _detect_language(self, filename: str) -> str:
        """Detect language from filename / 从文件名检测语言"""
        ext = os.path.splitext(filename)[1].lower()
        language_map = {
            '.py': 'python',
            '.c': 'c',
            '.h': 'c',
            '.cpp': 'c',
            '.cc': 'c',
            '.sh': 'shell',
            '.bash': 'shell',
            '.txt': 'text',
            '.md': 'markdown',
        }
        return language_map.get(ext, 'text')

    def _render(self):
        """Render editor / 渲染编辑器"""
        # Clear screen / 清屏
        sys.stdout.write('\033[2J\033[H')

        # Status line / 状态行
        status = f"{self.filename} - {self.mode_message}"
        print(f"\033[7m{status:<80}\033[0m")

        # Line numbers / 行号
        show_numbers = getattr(self, '_show_line_numbers', True)

        # Content / 内容
        start_y = self.scroll_y
        end_y = min(start_y + self.height - 2, len(self.lines))

        for y in range(start_y, end_y):
            if show_numbers:
                num = f"{y + 1:4d} "
                sys.stdout.write(num)

            line = self.lines[y]
            if y == self.cursor_y and self.mode in ('insert', 'normal'):
                # Highlight cursor / 高亮光标
                cursor_pos = self.cursor_x
                before = line[:cursor_pos]
                after = line[cursor_pos:]
                sys.stdout.write(before + '\033[7m' + (after[0] if after else ' ') + '\033[0m' + after[1:])
            else:
                sys.stdout.write(line)
            sys.stdout.write('\n')

        # Command line / 命令行
        if self.mode == 'command':
            print(f":{self.command_buffer}")

        sys.stdout.flush()

    def _cleanup(self):
        """Clean up / 清理"""
        # Restore terminal / 恢复终端
        sys.stdout.write('\033[?25h')


def main():
    """Main entry point / 主入口"""
    import sys
    filepath = sys.argv[1] if len(sys.argv) > 1 else None

    editor = EditorApp(filepath)
    editor.run()


if __name__ == '__main__':
    main()