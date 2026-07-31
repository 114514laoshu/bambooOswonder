# Bamboo OS User Manual

# Bamboo OS 用户手册

Welcome to Bamboo OS Wonder Series! This manual will help you get started with using Bamboo OS.

欢迎使用 Bamboo OS Wonder 系列！本手册将帮助您开始使用 Bamboo OS。

## Table of Contents / 目录

- [Getting Started / 快速开始](#getting-started--快速开始)
- [Booting Up / 启动](#booting-up--启动)
- [Shell Commands / Shell 命令](#shell-commands--shell-命令)
- [File System / 文件系统](#file-system--文件系统)
- [GUI Desktop / GUI 桌面](#gui-desktop--gui-桌面)
- [Applications / 应用程序](#applications--应用程序)
- [Games / 游戏](#games--游戏)
- [Networking / 网络](#networking--网络)
- [Settings / 设置](#settings--设置)
- [Troubleshooting / 故障排除](#troubleshooting--故障排除)

## Getting Started / 快速开始

### What is Bamboo OS? / 什么是 Bamboo OS？

Bamboo OS is a complete operating system for x86-64 computers, featuring:

Bamboo OS 是一个完整的 x86-64 计算机操作系统，具有以下特性：

- **Full GUI Desktop** - Graphical desktop environment / 图形桌面环境
- **25+ Built-in Apps** - Text editor, file manager, calculator, and more / 25+ 内置应用
- **12+ Games** - Classic games like Snake, Tetris, Minesweeper / 12+ 游戏
- **Office Suite** - Word processor, spreadsheet, presentation / 办公套件
- **Web Browser** - Basic web browsing / 网络浏览器
- **Media Player** - Audio and video playback / 媒体播放器
- **Complete Toolchain** - C compiler, assembler, linker / 完整工具链

### System Requirements / 系统要求

**Minimum / 最低配置:**
- x86-64 processor (or QEMU) / x86-64 处理器（或 QEMU）
- 256MB RAM / 256MB 内存
- 100MB storage / 100MB 存储空间

**Recommended / 推荐配置:**
- x86-64 processor / x86-64 处理器
- 512MB RAM / 512MB 内存
- 500MB storage / 500MB 存储空间
- VGA graphics / VGA 显卡

## Booting Up / 启动

### Booting in QEMU / 在 QEMU 中启动

```bash
# Run Wonder 2.0
python scripts/run_qemu.py --target=wonder2

# Run with GUI window
python scripts/run_qemu.py --target=wonder2 --gui

# Run with more memory
python scripts/run_qemu.py --target=wonder2 --memory=1024M
```

### Boot Sequence / 启动序列

1. **GRUB Boot Loader** - GRUB 引导加载程序
2. **Kernel Loading** - 内核加载
3. **Memory Initialization** - 内存初始化
4. **Driver Loading** - 驱动加载
5. **File System Mount** - 文件系统挂载
6. **Shell/Desktop Start** - Shell/桌面启动

### Boot Options / 启动选项

When the GRUB menu appears, you can select:

当 GRUB 菜单出现时，您可以选择：

- **Bamboo OS Wonder** - Normal boot / 正常启动
- **Safe Mode** - Minimal drivers / 安全模式
- **Memory Test** - Test RAM / 内存测试

## Shell Commands / Shell 命令

Bamboo OS includes a powerful command-line shell with 300+ commands.

Bamboo OS 包含一个功能强大的命令行 Shell，拥有 300+ 命令。

### Basic Commands / 基本命令

| Command | Description / 描述 | Example / 示例 |
|---------|-------------------|----------------|
| `ls` | List directory contents / 列出目录内容 | `ls /home` |
| `cd` | Change directory / 切换目录 | `cd /apps` |
| `pwd` | Print working directory / 打印当前目录 | `pwd` |
| `cat` | Display file contents / 显示文件内容 | `cat readme.txt` |
| `echo` | Print text / 打印文本 | `echo "Hello"` |
| `clear` | Clear screen / 清屏 | `clear` |
| `help` | Show help / 显示帮助 | `help` |
| `exit` | Exit shell / 退出 Shell | `exit` |

### File Operations / 文件操作

| Command | Description / 描述 | Example / 示例 |
|---------|-------------------|----------------|
| `mkdir` | Create directory / 创建目录 | `mkdir mydir` |
| `rmdir` | Remove directory / 删除目录 | `rmdir mydir` |
| `cp` | Copy file / 复制文件 | `cp a.txt b.txt` |
| `mv` | Move/rename file / 移动/重命名文件 | `mv a.txt b.txt` |
| `rm` | Remove file / 删除文件 | `rm file.txt` |
| `touch` | Create empty file / 创建空文件 | `touch new.txt` |
| `find` | Find files / 查找文件 | `find / -name *.txt` |

### System Commands / 系统命令

| Command | Description / 描述 | Example / 示例 |
|---------|-------------------|----------------|
| `ps` | List processes / 列出进程 | `ps` |
| `kill` | Kill process / 终止进程 | `kill 123` |
| `top` | System monitor / 系统监控 | `top` |
| `free` | Memory info / 内存信息 | `free` |
| `df` | Disk usage / 磁盘使用 | `df` |
| `uname` | System info / 系统信息 | `uname -a` |
| `date` | Show date/time / 显示日期时间 | `date` |
| `reboot` | Reboot system / 重启系统 | `reboot` |
| `shutdown` | Shutdown system / 关机 | `shutdown` |

### Network Commands / 网络命令

| Command | Description / 描述 | Example / 示例 |
|---------|-------------------|----------------|
| `ifconfig` | Network interfaces / 网络接口 | `ifconfig` |
| `ping` | Ping host / Ping 主机 | `ping 8.8.8.8` |
| `netstat` | Network status / 网络状态 | `netstat` |
| `wget` | Download file / 下载文件 | `wget http://...` |
| `curl` | HTTP request / HTTP 请求 | `curl http://...` |
| `dns` | DNS lookup / DNS 查询 | `dns example.com` |

### Text Editing / 文本编辑

| Command | Description / 描述 | Example / 示例 |
|---------|-------------------|----------------|
| `edit` | Text editor / 文本编辑器 | `edit file.txt` |
| `nano` | Nano-style editor / Nano 风格编辑器 | `nano file.txt` |
| `vi` | Vi-style editor / Vi 风格编辑器 | `vi file.txt` |

### Getting Help / 获取帮助

```bash
# List all commands / 列出所有命令
help

# Get help for a specific command / 获取特定命令的帮助
help ls

# Command info / 命令信息
info ps
```

## File System / 文件系统

### Directory Structure / 目录结构

```
/
├── bin/          # User binaries / 用户二进制文件
├── sbin/         # System binaries / 系统二进制文件
├── etc/          # Configuration files / 配置文件
├── dev/          # Device files / 设备文件
├── proc/         # Process info / 进程信息
├── sys/          # System info / 系统信息
├── tmp/          # Temporary files / 临时文件
├── home/         # User directories / 用户目录
├── root/         # Root home / Root 用户目录
├── var/          # Variable data / 可变数据
├── usr/          # User programs / 用户程序
│   ├── bin/      # User binaries / 用户二进制
│   ├── lib/      # Libraries / 库
│   └── include/  # Headers / 头文件
├── lib/          # System libraries / 系统库
├── apps/         # BPP applications / BPP 应用
│   ├── System/   # System apps / 系统应用
│   ├── Office/   # Office suite / 办公套件
│   ├── Games/    # Games / 游戏
│   └── Tools/    # Tools / 工具
└── boot/         # Boot files / 启动文件
```

### File Permissions / 文件权限

Bamboo OS uses Unix-style file permissions.

Bamboo OS 使用 Unix 风格的文件权限。

```
rwxr-xr--  user  group  size  date  filename
│││││││││
││││││││└── Others: read only / 其他人：只读
││││││└──── Others: no execute / 其他人：无执行
│││││└───── Others: no write / 其他人：无写
││││└────── Group: read + execute / 组：读+执行
│││└─────── Group: no write / 组：无写
││└──────── Group: read / 组：读
│└───────── Owner: execute / 所有者：执行
└────────── Owner: write / 所有者：写
            Owner: read / 所有者：读
```

## GUI Desktop / GUI 桌面

Wonder 1.0 and Wonder 2.0 include a full graphical desktop environment.

Wonder 1.0 和 Wonder 2.0 包含完整的图形桌面环境。

### Desktop Components / 桌面组件

**Desktop / 桌面:**
- Wallpaper background / 壁纸背景
- Desktop icons / 桌面图标
- Right-click menu / 右键菜单

**Taskbar / 任务栏:**
- Start menu button / 开始菜单按钮
- Open windows / 打开的窗口
- System tray / 系统托盘
- Clock / 时钟

**Start Menu / 开始菜单:**
- Applications / 应用程序
- Games / 游戏
- Settings / 设置
- Shut down / 关机

### Window Management / 窗口管理

**Window Controls / 窗口控制:**
- Minimize button / 最小化按钮
- Maximize button / 最大化按钮
- Close button / 关闭按钮

**Window Operations / 窗口操作:**
- **Move** - Drag title bar / 拖拽标题栏移动
- **Resize** - Drag edges / 拖拽边缘缩放
- **Minimize** - Click minimize button / 点击最小化按钮
- **Maximize** - Click maximize button / 点击最大化按钮
- **Close** - Click close button / 点击关闭按钮
- **Switch** - Click taskbar / 点击任务栏切换

### Keyboard Shortcuts / 键盘快捷键

| Shortcut | Action / 操作 |
|----------|--------------|
| `Alt+Tab` | Switch windows / 切换窗口 |
| `Alt+F4` | Close window / 关闭窗口 |
| `Win+D` | Show desktop / 显示桌面 |
| `Win+E` | File manager / 文件管理器 |
| `Win+R` | Run dialog / 运行对话框 |
| `Ctrl+Alt+Del` | Task manager / 任务管理器 |
| `PrintScreen` | Screenshot / 截图 |

## Applications / 应用程序

### System Applications / 系统应用

| App | Description / 描述 |
|-----|-------------------|
| **File Manager** | Browse and manage files / 浏览和管理文件 |
| **Terminal** | Command-line terminal / 命令行终端 |
| **Text Editor** | Edit text files / 编辑文本文件 |
| **Calculator** | Scientific calculator / 科学计算器 |
| **Settings** | System settings / 系统设置 |
| **System Monitor** | Monitor CPU/memory / 监控 CPU/内存 |
| **Package Manager** | Install/remove apps / 安装/卸载应用 |

### Office Suite / 办公套件

| App | Description / 描述 |
|-----|-------------------|
| **Word Processor** | Document editing / 文档编辑 |
| **Spreadsheet** | Spreadsheet calculations / 电子表格计算 |
| **Presentation** | Slide presentations / 幻灯片演示 |
| **PDF Viewer** | View PDF files / 查看 PDF 文件 |

### Internet / 网络

| App | Description / 描述 |
|-----|-------------------|
| **Web Browser** | Browse the web / 网页浏览 |
| **Email Client** | Email management / 邮件管理 |
| **Downloader** | File downloads / 文件下载 |

### Media / 媒体

| App | Description / 描述 |
|-----|-------------------|
| **Audio Player** | Play music files / 播放音乐文件 |
| **Video Player** | Play video files / 播放视频文件 |
| **Image Viewer** | View images / 查看图片 |
| **Paint** | Bitmap editor / 位图编辑器 |

### Utilities / 工具

| App | Description / 描述 |
|-----|-------------------|
| **Calculator** | Scientific calculator / 科学计算器 |
| **Calendar** | Calendar and events / 日历和事件 |
| **Clock** | Digital/analog clock / 数字/模拟时钟 |
| **Notes** | Note taking / 记笔记 |

## Games / 游戏

### 2D Games / 2D 游戏

| Game | Description / 描述 |
|------|-------------------|
| **Snake** | Classic snake game / 经典贪吃蛇 |
| **Tetris** | Block puzzle game / 方块益智游戏 |
| **Minesweeper** | Mine detection game / 扫雷游戏 |
| **Chess** | Chess with AI / 国际象棋（带 AI） |
| **Platformer** | Jump and run / 跳跃奔跑 |
| **Maze** | Maze generation / 迷宫生成 |
| **Poker** | Card game / 纸牌游戏 |

### 3D Games / 3D 游戏

| Game | Description / 描述 |
|------|-------------------|
| **Doom-like** | First-person shooter / 第一人称射击 |
| **Racer** | 3D racing game / 3D 赛车游戏 |
| **Blocks** | Minecraft-style / 我的世界风格 |

### Game Controls / 游戏控制

**Snake / 贪吃蛇:**
- Arrow keys - Move / 方向键移动
- Space - Pause / 空格暂停

**Tetris / 俄罗斯方块:**
- Left/Right - Move / 左右移动
- Down - Soft drop / 软降
- Up - Rotate / 旋转
- Space - Hard drop / 硬降

**Minesweeper / 扫雷:**
- Click - Reveal / 点击揭开
- Right-click - Flag / 右键标记

## Networking / 网络

### Network Configuration / 网络配置

Bamboo OS supports DHCP and static IP configuration.

Bamboo OS 支持 DHCP 和静态 IP 配置。

**Checking network status / 检查网络状态:**
```bash
ifconfig
```

**Testing connectivity / 测试连接:**
```bash
ping 8.8.8.8
```

**DNS lookup / DNS 查询:**
```bash
dns example.com
```

### Supported Services / 支持的服务

- **HTTP/HTTPS** - Web browsing / 网页浏览
- **DNS** - Domain name resolution / 域名解析
- **DHCP** - Automatic IP / 自动 IP 配置
- **TCP/UDP** - Transport protocols / 传输协议
- **ICMP** - Ping / Ping 命令

## Settings / 设置

### System Settings / 系统设置

**Display / 显示:**
- Screen resolution / 屏幕分辨率
- Color depth / 颜色深度
- Wallpaper / 壁纸
- Theme / 主题

**Input / 输入:**
- Keyboard layout / 键盘布局
- Mouse speed / 鼠标速度
- Double-click speed / 双击速度

**Network / 网络:**
- IP configuration / IP 配置
- DNS servers / DNS 服务器
- Proxy settings / 代理设置

**Sound / 声音:**
- Volume / 音量
- Input device / 输入设备
- Output device / 输出设备

### Themes / 主题

Bamboo OS includes multiple themes:

Bamboo OS 包含多个主题：

- **Bamboo** - Default green theme / 默认绿色主题
- **Dark** - Dark mode / 深色模式
- **Light** - Light mode / 浅色模式

To change theme / 更改主题：
```
Settings → Appearance → Theme
```

## Troubleshooting / 故障排除

### Common Issues / 常见问题

#### System won't boot / 系统无法启动

**Symptoms / 症状:**
- Black screen / 黑屏
- GRUB error / GRUB 错误

**Solutions / 解决方案:**
1. Try Safe Mode / 尝试安全模式
2. Check ISO integrity / 检查 ISO 完整性
3. Verify hardware compatibility / 验证硬件兼容性

#### No network / 没有网络

**Symptoms / 症状:**
- `ping` fails / ping 失败
- No IP address / 没有 IP 地址

**Solutions / 解决方案:**
1. Check network cable / 检查网线
2. Run `ifconfig` to see interfaces / 运行 ifconfig 查看接口
3. Try `dhclient` to get IP / 尝试 dhclient 获取 IP

#### GUI not starting / GUI 不启动

**Symptoms / 症状:**
- Boots to command line only / 只启动到命令行

**Solutions / 解决方案:**
1. Check if GUI is enabled / 检查 GUI 是否启用
2. Try `startx` command / 尝试 startx 命令
3. Check video driver / 检查显卡驱动

#### Slow performance / 性能缓慢

**Symptoms / 症状:**
- System is sluggish / 系统反应迟钝

**Solutions / 解决方案:**
1. Increase RAM in QEMU / 在 QEMU 中增加内存
2. Close unused apps / 关闭不用的应用
3. Use Education version / 使用教学版

### Getting Help / 获取帮助

If you encounter issues:

如果遇到问题：

1. Check this manual / 查看本手册
2. Check the [FAQ](#)
3. Search [GitHub Issues](https://github.com/bamboo-os/wonder/issues)
4. Open a new issue with:
   - Your OS version / 您的操作系统版本
   - Bamboo OS version / Bamboo OS 版本
   - Exact error message / 确切的错误信息
   - Steps to reproduce / 复现步骤

## Tips and Tricks / 技巧

### Keyboard Shortcuts / 键盘快捷键

Learn these shortcuts to work faster:

学习这些快捷键可以提高工作效率：

- `Ctrl+C` - Cancel current command / 取消当前命令
- `Ctrl+L` - Clear screen / 清屏
- `Tab` - Auto-complete / 自动补全
- `Up/Down` - Command history / 命令历史
- `Ctrl+Shift+C` - Copy / 复制
- `Ctrl+Shift+V` - Paste / 粘贴

### Useful Commands / 有用的命令

```bash
# Find large files / 查找大文件
find / -size +10M

# Count files / 统计文件数
ls | wc -l

# Disk usage / 磁盘使用
du -sh /apps

# Process tree / 进程树
ps aux

# System info / 系统信息
uname -a
```

### Customization / 自定义

- Change wallpaper / 更改壁纸
- Install new themes / 安装新主题
- Add custom commands / 添加自定义命令
- Create shell scripts / 创建 Shell 脚本

## See Also / 另请参阅

- [Build Guide](BUILD_GUIDE.md) - How to build / 如何构建
- [Developer Guide](DEVELOPER_GUIDE.md) - Development docs / 开发文档
- [API Reference](API_REFERENCE.md) - API documentation / API 文档

---

**Enjoy using Bamboo OS!**
**享受使用 Bamboo OS！**
