# Bamboo OS Build Guide

# Bamboo OS 构建指南

This guide will walk you through building Bamboo OS from source on Windows, Linux, and macOS.

本指南将指导您在 Windows、Linux 和 macOS 上从源码构建 Bamboo OS。

## Table of Contents / 目录

- [Prerequisites / 前置条件](#prerequisites--前置条件)
- [Quick Start / 快速开始](#quick-start--快速开始)
- [Building on Windows / 在 Windows 上构建](#building-on-windows--在-windows-上构建)
- [Building on Linux / 在 Linux 上构建](#building-on-linux--在-linux-上构建)
- [Building on macOS / 在 macOS 上构建](#building-on-macos--在-macos-上构建)
- [Build Options / 构建选项](#build-options--构建选项)
- [Output Files / 输出文件](#output-files--输出文件)
- [Troubleshooting / 故障排除](#troubleshooting--故障排除)

## Prerequisites / 前置条件

### Required / 必需

- **Python 3.8+** - The build system is written in Python / 构建系统用 Python 编写
- **500MB free disk space** - For build output / 用于构建输出

### Optional / 可选

- **QEMU** - For testing the OS / 用于测试操作系统
- **Git** - For version control / 用于版本控制

### Checking Python / 检查 Python

```bash
python3 --version
# or on Windows
python --version
```

## Quick Start / 快速开始

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/bamboo-os/wonder.git
cd wonder

# Build Wonder 2.0 / 构建 Wonder 2.0
python buildmain.py --target=wonder2

# Run in QEMU / 在 QEMU 中运行
python scripts/run_qemu.py --target=wonder2
```

## Building on Windows / 在 Windows 上构建

### Install Python / 安装 Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```

### Install QEMU (Optional) / 安装 QEMU（可选）

1. Download QEMU from [qemu.org](https://www.qemu.org/download/#windows)
2. Run the installer
3. Add QEMU to PATH or use full path

### Build Steps / 构建步骤

```cmd
cd bamboo-os-wonder
python buildmain.py --target=wonder2
```

### Running / 运行

```cmd
python scripts\run_qemu.py --target=wonder2
```

## Building on Linux / 在 Linux 上构建

### Install Python / 安装 Python

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### Fedora/RHEL:
```bash
sudo dnf install python3
```

#### Arch:
```bash
sudo pacman -S python
```

### Install QEMU (Optional) / 安装 QEMU（可选）

#### Ubuntu/Debian:
```bash
sudo apt install qemu-system-x86
```

#### Fedora/RHEL:
```bash
sudo dnf install qemu-system-x86-core
```

#### Arch:
```bash
sudo pacman -S qemu-desktop
```

### Build Steps / 构建步骤

```bash
cd bamboo-os-wonder
python3 buildmain.py --target=wonder2
```

### Running / 运行

```bash
python3 scripts/run_qemu.py --target=wonder2
```

## Building on macOS / 在 macOS 上构建

### Install Python / 安装 Python

Using Homebrew:
```bash
brew install python
```

Or download from [python.org](https://www.python.org/downloads/macos/).

### Install QEMU (Optional) / 安装 QEMU（可选）

```bash
brew install qemu
```

### Build Steps / 构建步骤

```bash
cd bamboo-os-wonder
python3 buildmain.py --target=wonder2
```

### Running / 运行

```bash
python3 scripts/run_qemu.py --target=wonder2
```

## Build Options / 构建选项

### Target Selection / 目标选择

```bash
# Build Wonder 1.0 (GRUB2 only)
python buildmain.py --target=wonder1

# Build Wonder 2.0 (GRUB2 + direct boot)
python buildmain.py --target=wonder2

# Build Education version
python buildmain.py --target=edu

# Build all versions
python buildmain.py --target=all
```

### Output Options / 输出选项

```bash
# Output ELF only (default)
python buildmain.py --target=wonder2 --output-elf

# Output ISO image
python buildmain.py --target=wonder2 --output-iso

# Output direct boot binary (Wonder 2.0 only)
python buildmain.py --target=wonder2 --output-bin

# Output all formats
python buildmain.py --target=wonder2 --output-elf --output-iso --output-bin
```

### Build Options / 构建选项

```bash
# Verbose output
python buildmain.py --target=wonder2 --verbose

# Debug symbols
python buildmain.py --target=wonder2 --debug

# Clean build
python buildmain.py --target=wonder2 --clean

# Test after build
python buildmain.py --target=wonder2 --test

# Specify memory size
python buildmain.py --target=wonder2 --memory=1024M

# Include specific apps
python buildmain.py --target=wonder2 --apps=Shell,FileManager
```

## Output Files / 输出文件

### Wonder 1.0 / Wonder 2.0

```
build/wonder2/
├── wonder2.elf          # Kernel ELF (Multiboot2)
├── wonder2.bin          # Direct boot binary (Wonder 2.0 only)
├── bamboo-wonder2.iso   # Bootable ISO image
├── initrd.tar           # Initial ramdisk
├── disk.img             # Disk image
└── build_info.json      # Build information
```

### Education / 教学版

```
build/education/
├── education.elf        # Kernel ELF
├── initrd.tar           # Initial ramdisk
├── disk.img             # Disk image
└── build_info.json      # Build information
```

## Troubleshooting / 故障排除

### Common Issues / 常见问题

#### Python not found / 找不到 Python

**Problem:** `python: command not found`

**Solution:**
- Ensure Python is installed
- Use `python3` instead of `python` on Linux/macOS
- Add Python to PATH on Windows

#### QEMU not found / 找不到 QEMU

**Problem:** `qemu-system-x86_64: command not found`

**Solution:**
- Install QEMU (see prerequisites)
- Add QEMU to PATH
- Use full path to QEMU executable

#### Build fails with import error / 构建因导入错误失败

**Problem:** `ModuleNotFoundError`

**Solution:**
- Ensure you're running from the project root directory
- Check that all files are present
- Try a clean build: `python buildmain.py --target=wonder2 --clean`

#### Kernel too large / 内核过大

**Problem:** Kernel size exceeds available memory

**Solution:**
- Use Education version for smaller footprint
- Reduce included apps
- Build with minimal configuration

### Getting More Help / 获取更多帮助

If you encounter issues not listed here:

如果遇到此处未列出的问题：

1. Check the [GitHub Issues](https://github.com/bamboo-os/wonder/issues)
2. Search the documentation
3. Open a new issue with:
   - Your operating system
   - Python version
   - Exact error message
   - Steps to reproduce

## Advanced Build / 高级构建

### Custom Configuration / 自定义配置

Copy an existing config and modify it:

复制现有配置并修改：

```bash
cp configs/wonder2_config.py configs/my_config.py
# Edit my_config.py
python buildmain.py --target=my_config
```

### Cross-Compilation / 交叉编译

The build system runs entirely in Python and generates x86-64 machine code. No cross-compiler is needed.

构建系统完全在 Python 中运行并生成 x86-64 机器码。不需要交叉编译器。

### Build Speed / 构建速度

- Typical build time: 5-30 seconds
- Wonder 2.0 full build: ~15 seconds
- Education build: ~5 seconds

## Next Steps / 下一步

After building successfully:

成功构建后：

1. [Run in QEMU](#running--运行)
2. Read the [User Manual](USER_MANUAL.md)
3. Explore the [Developer Guide](DEVELOPER_GUIDE.md)
4. Try the [Education Labs](EDUCATION/)
