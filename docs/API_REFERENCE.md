# Bamboo OS API Reference

# Bamboo OS API 参考

This document describes the API for Bamboo OS Wonder Series.

本文档描述了 Bamboo OS Wonder 系列的 API。

## Table of Contents / 目录

- [System Calls / 系统调用](#system-calls--系统调用)
- [Kernel API / 内核 API](#kernel-api--内核-api)
- [User Library API / 用户库 API](#user-library-api--用户库-api)
- [BPP Format / BPP 格式](#bpp-format--bpp-格式)
- [Build System API / 构建系统 API](#build-system-api--构建系统-api)

## System Calls / 系统调用

### Bamboo Native System Calls / Bamboo 原生系统调用

Bamboo OS provides 256 native system calls for kernel operations.

Bamboo OS 提供 256 个原生系统调用用于内核操作。

#### Process Management / 进程管理

| Number | Name | Description / 描述 |
|--------|------|-------------------|
| 0 | sys_exit | Exit process / 退出进程 |
| 1 | sys_fork | Create new process / 创建新进程 |
| 2 | sys_execve | Execute program / 执行程序 |
| 3 | sys_waitpid | Wait for process / 等待进程 |
| 4 | sys_getpid | Get process ID / 获取进程 ID |
| 5 | sys_getppid | Get parent process ID / 获取父进程 ID |
| 6 | sys_sched_yield | Yield CPU / 让出 CPU |
| 7 | sys_nanosleep | Sleep for nanoseconds / 纳秒级睡眠 |

#### Memory Management / 内存管理

| Number | Name | Description / 描述 |
|--------|------|-------------------|
| 10 | sys_mmap | Map memory / 映射内存 |
| 11 | sys_munmap | Unmap memory / 取消映射 |
| 12 | sys_mprotect | Change memory protection / 修改内存保护 |
| 13 | sys_brk | Change program break / 修改程序间断点 |
| 14 | sys_shmget | Get shared memory / 获取共享内存 |
| 15 | sys_shmat | Attach shared memory / 附加共享内存 |
| 16 | sys_shmdt | Detach shared memory / 分离共享内存 |

#### File System / 文件系统

| Number | Name | Description / 描述 |
|--------|------|-------------------|
| 20 | sys_open | Open file / 打开文件 |
| 21 | sys_close | Close file / 关闭文件 |
| 22 | sys_read | Read from file / 读取文件 |
| 23 | sys_write | Write to file / 写入文件 |
| 24 | sys_lseek | Seek in file / 文件定位 |
| 25 | sys_stat | Get file status / 获取文件状态 |
| 26 | sys_fstat | Get file status (fd) / 获取文件状态（fd） |
| 27 | sys_mkdir | Create directory / 创建目录 |
| 28 | sys_rmdir | Remove directory / 删除目录 |
| 29 | sys_unlink | Delete file / 删除文件 |
| 30 | sys_rename | Rename file / 重命名文件 |

#### I/O / 输入输出

| Number | Name | Description / 描述 |
|--------|------|-------------------|
| 40 | sys_readv | Scatter read / 分散读取 |
| 41 | sys_writev | Gather write / 聚集写入 |
| 42 | sys_pread | Positioned read / 定位读取 |
| 43 | sys_pwrite | Positioned write / 定位写入 |
| 44 | sys_ioctl | I/O control / I/O 控制 |
| 45 | sys_fcntl | File control / 文件控制 |

#### Network / 网络

| Number | Name | Description / 描述 |
|--------|------|-------------------|
| 50 | sys_socket | Create socket / 创建套接字 |
| 51 | sys_bind | Bind socket / 绑定套接字 |
| 52 | sys_listen | Listen for connections / 监听连接 |
| 53 | sys_accept | Accept connection / 接受连接 |
| 54 | sys_connect | Connect to server / 连接服务器 |
| 55 | sys_send | Send data / 发送数据 |
| 56 | sys_recv | Receive data / 接收数据 |
| 57 | sys_sendto | Send to address / 发送到地址 |
| 58 | sys_recvfrom | Receive from address / 从地址接收 |

#### Time / 时间

| Number | Name | Description / 描述 |
|--------|------|-------------------|
| 70 | sys_time | Get current time / 获取当前时间 |
| 71 | sys_gettimeofday | Get time of day / 获取时间 |
| 72 | sys_clock_gettime | Get clock time / 获取时钟时间 |
| 73 | sys_setitimer | Set interval timer / 设置间隔定时器 |
| 74 | sys_alarm | Set alarm / 设置闹钟 |

### Linux Compatible System Calls / Linux 兼容系统调用

Bamboo OS provides 512 Linux-compatible system calls for POSIX compatibility.

Bamboo OS 提供 512 个 Linux 兼容系统调用以实现 POSIX 兼容性。

## Kernel API / 内核 API

### X64Assembler / x86-64 汇编器

The core assembler class for generating x86-64 machine code.

生成 x86-64 机器码的核心汇编器类。

```python
from core.assembler import X64Assembler

asm = X64Assembler()

# Emit instructions / 发射指令
asm.mov_r64_imm(asm.REG64["rax"], 42)
asm.add_rr(asm.REG64["rax"], asm.REG64["rbx"])
asm.ret()

# Get generated code / 获取生成的代码
code = asm.code
```

#### Methods / 方法

**Instruction Generation / 指令生成**

- `emit(*args)` - Emit raw bytes / 发射原始字节
- `mov_r64_imm(reg, imm)` - Move immediate to 64-bit register / 立即数传送到64位寄存器
- `mov_rr(dst, src)` - Move register to register / 寄存器间传送
- `add_rr(dst, src)` - Add registers / 寄存器加法
- `sub_rr(dst, src)` - Subtract registers / 寄存器减法
- `and_rr(dst, src)` - AND registers / 寄存器与
- `or_rr(dst, src)` - OR registers / 寄存器或
- `xor_rr(dst, src)` - XOR registers / 寄存器异或
- `cmp_rr(dst, src)` - Compare registers / 寄存器比较
- `jmp_near(label)` - Near jump / 近跳转
- `jz(label)` - Jump if zero / 零标志跳转
- `jnz(label)` - Jump if not zero / 非零跳转
- `call(label)` - Call function / 调用函数
- `ret()` - Return from function / 函数返回
- `push_r64(reg)` - Push 64-bit register / 压入64位寄存器
- `pop_r64(reg)` - Pop 64-bit register / 弹出64位寄存器

**Label Management / 标签管理**

- `label(name)` - Define label / 定义标签
- `label_addr(name)` - Get label address / 获取标签地址
- `resolve()` - Resolve all labels / 解析所有标签

**Memory / 内存**

- `mov_m_r(addr, src)` - Move register to memory / 寄存器传送到内存
- `mov_r_m(reg, addr)` - Move memory to register / 内存传送到寄存器
- `mov_r_m_offset(reg, base, offset)` - Move from memory offset / 从内存偏移传送

**System / 系统**

- `cli()` - Disable interrupts / 禁用中断
- `sti()` - Enable interrupts / 启用中断
- `hlt()` - Halt CPU / 暂停 CPU
- `nop()` - No operation / 空操作
- `int_n(n)` - Software interrupt / 软件中断
- `iretq()` - Interrupt return / 中断返回

**Segmentation / 分段**

- `setup_gdt_register(addr, limit)` - Setup GDTR / 设置 GDT 寄存器
- `setup_idt_register(addr, limit)` - Setup IDTR / 设置 IDT 寄存器
- `create_gdt_entry(base, limit, access, flags)` - Create GDT entry / 创建 GDT 条目
- `create_idt_entry(offset, selector, ist, type_attr)` - Create IDT entry / 创建 IDT 条目

**Paging / 分页**

- `enable_paging()` - Enable paging / 启用分页
- `enable_pae()` - Enable PAE / 启用 PAE
- `enable_long_mode()` - Enable long mode / 启用长模式
- `setup_cr3(pml4_addr)` - Setup CR3 / 设置 CR3
- `setup_identity_mapping(pml4_addr, max_phys)` - Setup identity mapping / 设置恒等映射

### Kernel Generator / 内核生成器

```python
from kernel.kernel_generator import generate_kernel

# Generate full kernel / 生成完整内核
size = generate_kernel(config, output_path)

# Generate minimal kernel / 生成最小内核
size = generate_minimal_kernel(config, output_path)
```

## User Library API / 用户库 API

### libbamboo / 核心库

Core system library providing basic OS functionality.

提供基本操作系统功能的核心系统库。

#### Functions / 函数

- `bamboo_init()` - Initialize library / 初始化库
- `bamboo_get_version()` - Get OS version / 获取操作系统版本
- `bamboo_syscall(num, ...)` - Raw system call / 原始系统调用

### libc / C 标准库

Standard C library implementation.

标准 C 库实现。

#### Functions / 函数

- `printf(format, ...)` - Print formatted output / 格式化输出
- `malloc(size)` - Allocate memory / 分配内存
- `free(ptr)` - Free memory / 释放内存
- `strlen(s)` - String length / 字符串长度
- `strcpy(dst, src)` - Copy string / 复制字符串
- `memcpy(dst, src, n)` - Copy memory / 复制内存
- `memset(dst, c, n)` - Set memory / 设置内存

### libgui / GUI 库

Graphical user interface library.

图形用户界面库。

#### Classes / 类

**Window / 窗口**

```python
window = Window(x, y, width, height, title)
window.show()
window.hide()
window.move(x, y)
window.resize(width, height)
window.close()
```

**Widget / 控件**

- `Button(x, y, width, height, text)` - Button / 按钮
- `TextBox(x, y, width, height)` - Text input / 文本输入
- `ListBox(x, y, width, height)` - List box / 列表框
- `ScrollBar(x, y, width, height)` - Scroll bar / 滚动条
- `Menu(x, y, items)` - Menu / 菜单
- `Dialog(title, message)` - Dialog box / 对话框

### libnet / 网络库

Networking library.

网络库。

#### Functions / 函数

- `net_init()` - Initialize network / 初始化网络
- `net_get_ip()` - Get IP address / 获取 IP 地址
- `dns_resolve(hostname)` - DNS resolution / DNS 解析
- `http_get(url)` - HTTP GET request / HTTP GET 请求

### libgame2d / 2D 游戏引擎

2D game engine library.

2D 游戏引擎库。

#### Classes / 类

- `Sprite(x, y, image)` - Game sprite / 游戏精灵
- `Animation(frames, speed)` - Animation / 动画
- `Scene()` - Game scene / 游戏场景
- `ParticleEmitter(x, y)` - Particle system / 粒子系统

## BPP Format / BPP 格式

### BPP Header / BPP 头部

| Offset | Size | Field | Description / 描述 |
|--------|------|-------|-------------------|
| 0 | 4 | Magic | "BPP\x7F" (0x7F505042) |
| 4 | 4 | Version | Format version / 格式版本 |
| 8 | 4 | HeaderSize | Header size / 头部大小 |
| 12 | 4 | Flags | Flags / 标志 |
| 16 | 8 | EntryPoint | Entry point address / 入口点地址 |
| 24 | 8 | LoadBase | Load base address / 加载基址 |
| 32 | 8 | ImageSize | Total image size / 总镜像大小 |
| 40 | 8 | BSSSize | BSS segment size / BSS 段大小 |
| 48 | 8 | StackSize | Stack size / 栈大小 |
| 56 | 8 | HeapSize | Heap size / 堆大小 |
| 64 | 8 | LibCount | Number of libraries / 库数量 |
| 72 | 8 | LibNamesOff | Library names offset / 库名偏移 |
| 80 | 8 | SymTabOff | Symbol table offset / 符号表偏移 |
| 88 | 8 | SymCount | Symbol count / 符号数量 |
| 96 | 8 | RelocOff | Relocation table offset / 重定位表偏移 |
| 104 | 8 | RelocCount | Relocation count / 重定位数量 |
| 112 | 16 | Reserved | Reserved / 保留 |

### Flags / 标志

| Bit | Name | Description / 描述 |
|-----|------|-------------------|
| 0 | EXECUTABLE | Executable file / 可执行文件 |
| 1 | DYNAMIC | Dynamic linking / 动态链接 |
| 2 | GUI | Requires GUI / 需要 GUI |
| 3 | NETWORK | Requires network / 需要网络 |
| 4 | PRIVILEGED | Privileged application / 特权应用 |

### Python API / Python API

```python
from toolchain.bamboo_pack import BPPPackager, BPPLoader, create_simple_bpp

# Create a BPP package / 创建 BPP 包
packager = BPPPackager()
packager.add_code(code_bytes)
packager.set_flags(executable=True, gui=True)
packager.add_library('libgui.so')
packager.save('myapp.bpp')

# Load a BPP package / 加载 BPP 包
loader = BPPLoader('myapp.bpp')
info = loader.get_info()
code = loader.get_code()
libs = loader.get_libraries()
```

## Build System API / 构建系统 API

### BuildMain / 构建主类

```python
from buildmain import BuildMain

builder = BuildMain()
builder.build()
```

### Configuration / 配置

```python
from configs import load_config

config = load_config('wonder2')
print(config.VERSION)
print(config.KERNEL_CONFIG)
print(config.GUI_CONFIG)
```

### Platform Detection / 平台检测

```python
from buildmain import PlatformDetector

platform = PlatformDetector.get_platform()
qemu_cmd = PlatformDetector.get_qemu_command()
```

### Build Logger / 构建日志

```python
from buildmain import BuildLogger

logger = BuildLogger(verbose=True)
logger.info("Information message")
logger.success("Success message")
logger.warning("Warning message")
logger.error("Error message")
```

## See Also / 另请参阅

- [Developer Guide](DEVELOPER_GUIDE.md) - Development documentation / 开发文档
- [User Manual](USER_MANUAL.md) - User documentation / 用户文档
- [Build Guide](BUILD_GUIDE.md) - Build instructions / 构建指南
