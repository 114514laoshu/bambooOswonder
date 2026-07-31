# Bamboo OS Wonder Series

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/bamboo-os/wonder)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/bamboo-os/wonder)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org/)

Bamboo OS Wonder Series is a complete x86-64 operating system generator with GUI, applications, games, and office suite.

Bamboo OS Wonder 系列是一个完整的 x86-64 操作系统生成器，包含图形界面、应用、游戏和办公套件。

## Features / 特性

- **Full GUI Desktop** / 完整图形桌面
- **25+ Built-in Apps** / 25+ 内置应用
- **12+ Games** / 12+ 游戏
- **Office Suite** / 办公套件
- **Web Browser** / 网络浏览器
- **Media Player** / 媒体播放器
- **Complete Toolchain** / 完整工具链
- **Education Version** / 教学版本
- **Cross-Platform Build** / 跨平台构建
- **BPP App Format** / BPP 应用格式
- **Multiboot2 Compatible** / Multiboot2 兼容

## Versions / 版本

| Version | Boot Method | GUI | Apps | Games | Direct Boot | Description |
|---------|-------------|-----|------|-------|-------------|-------------|
| **Wonder 1.0** | GRUB2 | ✅ | ✅ | ✅ | ❌ | Full version with GRUB2 boot |
| **Wonder 2.0** | GRUB2 + Direct | ✅ | ✅ | ✅ | ✅ | Enhanced version with direct boot |
| **Education** | GRUB2 | ❌ | ❌ | ❌ | ❌ | Minimal version for learning |

## Quick Start / 快速开始

### Build / 构建

```bash
# Build Wonder 2.0 (recommended)
python buildmain.py --target=wonder2

# Build all versions
python buildmain.py --target=all

# Build with ISO output
python buildmain.py --target=wonder2 --output-iso

# Build Education version
python buildmain.py --target=edu
```

### Run / 运行

```bash
# Run in QEMU
python scripts/run_qemu.py --target=wonder2

# Run with GUI
python scripts/run_qemu.py --target=wonder2 --gui

# Run with debug mode
python scripts/run_qemu.py --target=wonder2 --debug
```

## Project Structure / 项目结构

```
bamboo-os-wonder/
├── buildmain.py              # Main build script / 主构建脚本
├── configs/                  # Configuration files / 配置文件
│   ├── wonder1_config.py     # Wonder 1.0 config
│   ├── wonder2_config.py     # Wonder 2.0 config
│   └── education_config.py   # Education config
├── core/                     # Core engine / 核心引擎
│   ├── assembler/            # x86-64 assembler / 汇编器
│   ├── builder/              # ELF/ISO/BIN builders / 构建器
│   └── linker/               # GDT/IDT/page tables / 链接器
├── kernel/                   # Kernel modules / 内核模块
│   ├── boot/                 # Boot code / 启动代码
│   ├── mm/                   # Memory management / 内存管理
│   ├── sched/                # Scheduler / 调度器
│   ├── fs/                   # File systems / 文件系统
│   ├── net/                  # Network stack / 网络栈
│   ├── drivers/              # Device drivers / 设备驱动
│   ├── gui/                  # GUI subsystem / 图形子系统
│   ├── syscall/              # System calls / 系统调用
│   ├── ipc/                  # IPC / 进程间通信
│   ├── init/                 # Kernel init / 内核初始化
│   └── security/             # Security / 安全
├── userland/                 # User space / 用户空间
│   ├── apps/                 # Applications / 应用
│   └── libs/                 # Libraries / 库
├── toolchain/                # Toolchain / 工具链
│   ├── bamboo_cc.py          # C compiler / C 编译器
│   ├── bamboo_as.py          # Assembler / 汇编器
│   ├── bamboo_ld.py          # Linker / 链接器
│   ├── bamboo_db.py          # Debugger / 调试器
│   └── bamboo_pack.py        # BPP packager / BPP 打包工具
├── resources/                # Resources / 资源
│   ├── fonts/                # Fonts / 字体
│   ├── icons/                # Icons / 图标
│   ├── themes/               # Themes / 主题
│   └── grub/                 # GRUB config / GRUB 配置
├── scripts/                  # Helper scripts / 辅助脚本
│   ├── run_qemu.py           # QEMU runner / QEMU 启动器
│   ├── create_iso.py         # ISO creator / ISO 创建器
│   └── validate.py           # Build validator / 构建验证器
├── docs/                     # Documentation / 文档
│   ├── BUILD_GUIDE.md        # Build guide / 构建指南
│   ├── API_REFERENCE.md      # API reference / API 参考
│   ├── DEVELOPER_GUIDE.md    # Developer guide / 开发者指南
│   ├── USER_MANUAL.md        # User manual / 用户手册
│   └── EDUCATION/            # Education labs / 教学实验
├── tests/                    # Tests / 测试
├── LICENSE                   # GPL v3
├── README.md                 # This file / 本文件
└── CONTRIBUTING.md           # Contributing guide / 贡献指南
```

## Documentation / 文档

- [User Manual](docs/USER_MANUAL.md) - How to use Bamboo OS / 如何使用 Bamboo OS
- [Build Guide](docs/BUILD_GUIDE.md) - Building from source / 从源码构建
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Development documentation / 开发文档
- [API Reference](docs/API_REFERENCE.md) - API documentation / API 文档
- [Education Tutorial](docs/EDUCATION/) - Learning materials / 学习材料

## System Requirements / 系统要求

### Build Requirements / 构建要求
- Python 3.8+
- 500MB free disk space
- Windows / Linux / macOS

### Run Requirements / 运行要求
- QEMU (qemu-system-x86_64)
- 512MB RAM (minimum)
- 1GB RAM (recommended for GUI)

## Building from Source / 从源码构建

### Prerequisites / 前置条件

```bash
# Python 3.8+ is required
python3 --version
```

### Build Steps / 构建步骤

1. Clone the repository / 克隆仓库
```bash
git clone https://github.com/bamboo-os/wonder.git
cd wonder
```

2. Build Wonder 2.0 / 构建 Wonder 2.0
```bash
python buildmain.py --target=wonder2
```

3. Run in QEMU / 在 QEMU 中运行
```bash
python scripts/run_qemu.py --target=wonder2
```

### Build Options / 构建选项

```bash
# Show help / 显示帮助
python buildmain.py --help

# Build with debug symbols / 带调试符号构建
python buildmain.py --target=wonder2 --debug

# Build and test / 构建并测试
python buildmain.py --target=wonder2 --test

# Verbose output / 详细输出
python buildmain.py --target=wonder2 --verbose

# Clean build / 清理构建
python buildmain.py --target=wonder2 --clean
```

## BPP Application Format / BPP 应用格式

Bamboo OS uses the BPP (Bamboo Package) format for applications.

Bamboo OS 使用 BPP（Bamboo 包）格式作为应用格式。

```python
from toolchain.bamboo_pack import BPPPackager, create_simple_bpp

# Create a simple BPP / 创建简单的 BPP
packager = BPPPackager()
packager.add_code(code_bytes)
packager.set_flags(executable=True, gui=True)
packager.add_library('libgui.so')
packager.save('myapp.bpp')
```

## Contributing / 贡献

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解行为准则和提交拉取请求的流程。

## License / 许可证

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

本项目采用 GNU 通用公共许可证 v3.0 授权 - 详见 [LICENSE](LICENSE) 文件。

## Authors / 作者

- LSS (BAMBOOOSTEAM2026)

## Acknowledgments / 致谢

- Thanks to all contributors and open-source projects that made this possible.
- 感谢所有贡献者和开源项目。
- Inspired by Linux, Minix, and other educational OS projects.
- 灵感来自 Linux、Minix 和其他教学操作系统项目。

## Support / 支持

- GitHub Issues: [github.com/bamboo-os/wonder/issues](https://github.com/bamboo-os/wonder/issues)
- Documentation: [docs/](docs/)

---
Correction: The official GitHub repository of this project is https://github.com/114514laoshu/bambooOswonder. Thank you for your understanding!
注意：本项目github地址为https://github.com/114514laoshu/bambooOswonder，感谢理解！
**Bamboo OS Wonder Series** - Build your own operating system!
**Bamboo OS Wonder 系列** - 构建你自己的操作系统！
