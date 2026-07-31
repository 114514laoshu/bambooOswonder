# ============================================================================
# Module: toolchain/bamboo_pack.py
# 模块：toolchain/bamboo_pack.py
# Description: BPP (Bamboo Package) packager for Bamboo OS
# 描述：Bamboo OS 的 BPP 包打包工具
# ============================================================================

import struct
import os
import json
import hashlib
from pathlib import Path


# BPP Magic number / BPP 魔数
BPP_MAGIC = 0x7F505042  # "BPP\x7F" little-endian

# BPP Version / BPP 版本
BPP_VERSION = 0x00010000  # 1.0.0

# BPP Header size / BPP 头部大小
BPP_HEADER_SIZE = 128  # bytes

# Flag bits / 标志位
BPP_FLAG_EXECUTABLE = 0x00000001  # Executable / 可执行
BPP_FLAG_DYNAMIC = 0x00000002     # Dynamic linking / 动态链接
BPP_FLAG_GUI = 0x00000004         # Requires GUI / 需要 GUI
BPP_FLAG_NETWORK = 0x00000008     # Requires network / 需要网络
BPP_FLAG_PRIVILEGED = 0x00000010  # Privileged app / 特权应用


class BPPHeader:
    """
    BPP file header structure.
    BPP 文件头部结构。

    Layout:
    - Magic (4B)
    - Version (4B)
    - HeaderSize (4B)
    - Flags (4B)
    - EntryPoint (8B)
    - LoadBase (8B)
    - ImageSize (8B)
    - BSSSize (8B)
    - StackSize (8B)
    - HeapSize (8B)
    - LibCount (8B)
    - LibNamesOff (8B)
    - SymTabOff (8B)
    - SymCount (8B)
    - RelocOff (8B)
    - RelocCount (8B)
    - Reserved (16B)
    """

    FORMAT = '<IIIIQQQQQQQQQQQQ16s'
    SIZE = struct.calcsize(FORMAT)

    def __init__(self):
        """Initialize BPP header / 初始化 BPP 头部"""
        self.magic = BPP_MAGIC
        self.version = BPP_VERSION
        self.header_size = BPP_HEADER_SIZE
        self.flags = 0
        self.entry_point = 0
        self.load_base = 0
        self.image_size = 0
        self.bss_size = 0
        self.stack_size = 0x10000  # 64KB default stack
        self.heap_size = 0x400000   # 4MB default heap
        self.lib_count = 0
        self.lib_names_off = 0
        self.sym_tab_off = 0
        self.sym_count = 0
        self.reloc_off = 0
        self.reloc_count = 0
        self.reserved = b'\x00' * 16

    def pack(self):
        """
        Pack header to bytes / 将头部打包为字节

        Returns:
            返回：
            bytes: Packed header / 打包后的头部
        """
        return struct.pack(
            self.FORMAT,
            self.magic,
            self.version,
            self.header_size,
            self.flags,
            self.entry_point,
            self.load_base,
            self.image_size,
            self.bss_size,
            self.stack_size,
            self.heap_size,
            self.lib_count,
            self.lib_names_off,
            self.sym_tab_off,
            self.sym_count,
            self.reloc_off,
            self.reloc_count,
            self.reserved
        )

    @classmethod
    def unpack(cls, data):
        """
        Unpack header from bytes / 从字节解包头部

        Args:
            参数：
            data (bytes): Header data / 头部数据

        Returns:
            返回：
            BPPHeader: Unpacked header / 解包后的头部
        """
        header = cls()
        (
            header.magic,
            header.version,
            header.header_size,
            header.flags,
            header.entry_point,
            header.load_base,
            header.image_size,
            header.bss_size,
            header.stack_size,
            header.heap_size,
            header.lib_count,
            header.lib_names_off,
            header.sym_tab_off,
            header.sym_count,
            header.reloc_off,
            header.reloc_count,
            header.reserved
        ) = struct.unpack(cls.FORMAT, data[:cls.SIZE])
        return header

    def is_valid(self):
        """
        Check if header is valid / 检查头部是否有效

        Returns:
            返回：
            bool: True if valid / 有效返回 True
        """
        return self.magic == BPP_MAGIC


class BPPPackager:
    """
    BPP package creator.
    BPP 包创建器。
    """

    def __init__(self):
        """Initialize packager / 初始化打包器"""
        self.header = BPPHeader()
        self.code = bytearray()
        self.data = bytearray()
        self.rodata = bytearray()
        self.bss_size = 0
        self.libraries = []
        self.symbols = {}
        self.relocations = []
        self.metadata = {}

    def add_code(self, code_bytes):
        """
        Add code segment / 添加代码段

        Args:
            参数：
            code_bytes (bytes): Code data / 代码数据
        """
        self.code.extend(code_bytes)

    def add_data(self, data_bytes):
        """
        Add data segment / 添加数据段

        Args:
            参数：
            data_bytes (bytes): Data data / 数据数据
        """
        self.data.extend(data_bytes)

    def add_rodata(self, rodata_bytes):
        """
        Add read-only data segment / 添加只读数据段

        Args:
            参数：
            rodata_bytes (bytes): Read-only data / 只读数据
        """
        self.rodata.extend(rodata_bytes)

    def add_library(self, lib_name):
        """
        Add library dependency / 添加库依赖

        Args:
            参数：
            lib_name (str): Library name / 库名
        """
        if lib_name not in self.libraries:
            self.libraries.append(lib_name)

    def add_symbol(self, name, address, sym_type=0):
        """
        Add symbol / 添加符号

        Args:
            参数：
            name (str): Symbol name / 符号名
            address (int): Symbol address / 符号地址
            sym_type (int): Symbol type / 符号类型
        """
        self.symbols[name] = (address, sym_type)

    def add_relocation(self, offset, sym_name, reloc_type=0):
        """
        Add relocation entry / 添加重定位条目

        Args:
            参数：
            offset (int): Offset in image / 镜像中的偏移
            sym_name (str): Symbol name / 符号名
            reloc_type (int): Relocation type / 重定位类型
        """
        self.relocations.append((offset, sym_name, reloc_type))

    def set_metadata(self, key, value):
        """
        Set metadata / 设置元数据

        Args:
            参数：
            key (str): Metadata key / 元数据键
            value: Metadata value / 元数据值
        """
        self.metadata[key] = value

    def set_flags(self, executable=False, dynamic=False, gui=False, network=False, privileged=False):
        """
        Set header flags / 设置头部标志

        Args:
            参数：
            executable (bool): Executable flag / 可执行标志
            dynamic (bool): Dynamic linking flag / 动态链接标志
            gui (bool): GUI required flag / 需要 GUI 标志
            network (bool): Network required flag / 需要网络标志
            privileged (bool): Privileged flag / 特权标志
        """
        flags = 0
        if executable:
            flags |= BPP_FLAG_EXECUTABLE
        if dynamic:
            flags |= BPP_FLAG_DYNAMIC
        if gui:
            flags |= BPP_FLAG_GUI
        if network:
            flags |= BPP_FLAG_NETWORK
        if privileged:
            flags |= BPP_FLAG_PRIVILEGED
        self.header.flags = flags

    def build(self, entry_point=0, load_base=0):
        """
        Build BPP package / 构建 BPP 包

        Args:
            参数：
            entry_point (int): Entry point address / 入口点地址
            load_base (int): Load base address / 加载基址

        Returns:
            返回：
            bytes: Complete BPP package / 完整的 BPP 包
        """
        # Calculate image layout / 计算镜像布局
        code_offset = self.header.header_size
        rodata_offset = code_offset + len(self.code)
        data_offset = rodata_offset + len(self.rodata)
        image_size = data_offset + len(self.data)

        # Update header / 更新头部
        self.header.entry_point = entry_point
        self.header.load_base = load_base
        self.header.image_size = image_size
        self.header.bss_size = self.bss_size
        self.header.lib_count = len(self.libraries)

        # Build library names section / 构建库名表
        lib_names_data = b''
        for lib in self.libraries:
            lib_names_data += lib.encode('utf-8') + b'\x00'
        self.header.lib_names_off = image_size
        image_size += len(lib_names_data)

        # Build symbol table / 构建符号表
        sym_data = b''
        sym_count = 0
        for name, (addr, stype) in self.symbols.items():
            name_bytes = name.encode('utf-8') + b'\x00'
            sym_data += struct.pack('<QB', addr, stype)
            sym_data += name_bytes
            sym_count += 1
        self.header.sym_tab_off = image_size
        self.header.sym_count = sym_count
        image_size += len(sym_data)

        # Build relocation table / 构建重定位表
        reloc_data = b''
        reloc_count = 0
        for offset, sym_name, rtype in self.relocations:
            name_bytes = sym_name.encode('utf-8') + b'\x00'
            reloc_data += struct.pack('<QB', offset, rtype)
            reloc_data += name_bytes
            reloc_count += 1
        self.header.reloc_off = image_size
        self.header.reloc_count = reloc_count
        image_size += len(reloc_data)

        # Assemble package / 组装包
        result = bytearray()
        result.extend(self.header.pack())
        result.extend(self.code)
        result.extend(self.rodata)
        result.extend(self.data)
        result.extend(lib_names_data)
        result.extend(sym_data)
        result.extend(reloc_data)

        return bytes(result)

    def save(self, filepath):
        """
        Save BPP package to file / 保存 BPP 包到文件

        Args:
            参数：
            filepath (str): Output file path / 输出文件路径

        Returns:
            返回：
            int: File size in bytes / 文件大小（字节）
        """
        data = self.build()
        with open(filepath, 'wb') as f:
            f.write(data)
        return len(data)


class BPPLoader:
    """
    BPP package loader/reader.
    BPP 包加载器/读取器。
    """

    def __init__(self, filepath=None, data=None):
        """
        Initialize loader / 初始化加载器

        Args:
            参数：
            filepath (str): Path to BPP file / BPP 文件路径
            data (bytes): BPP file data / BPP 文件数据
        """
        self.data = None
        self.header = None

        if filepath:
            with open(filepath, 'rb') as f:
                self.data = f.read()
        elif data:
            self.data = data

        if self.data:
            self._parse()

    def _parse(self):
        """Parse BPP file / 解析 BPP 文件"""
        if len(self.data) < BPPHeader.SIZE:
            raise ValueError("File too small to be BPP")

        self.header = BPPHeader.unpack(self.data)

        if not self.header.is_valid():
            raise ValueError("Invalid BPP magic number")

    def is_valid(self):
        """
        Check if BPP file is valid / 检查 BPP 文件是否有效

        Returns:
            返回：
            bool: True if valid / 有效返回 True
        """
        return self.header is not None and self.header.is_valid()

    def get_code(self):
        """
        Get code segment / 获取代码段

        Returns:
            返回：
            bytes: Code segment / 代码段
        """
        offset = self.header.header_size
        # Code is first segment after header / 代码是头部后的第一个段
        return self.data[offset:offset + self._get_code_size()]

    def _get_code_size(self):
        """Calculate code size / 计算代码大小"""
        # For simplicity, assume code + rodata + data = image_size - header_size
        # In a real implementation, we'd have program headers
        return len(self.data) - self.header.header_size  # Simplified

    def get_libraries(self):
        """
        Get list of library dependencies / 获取库依赖列表

        Returns:
            返回：
            list: List of library names / 库名列表
        """
        if self.header.lib_count == 0:
            return []

        offset = self.header.lib_names_off
        libs = []
        current = b''

        for i in range(offset, len(self.data)):
            byte = self.data[i:i+1]
            if byte == b'\x00':
                if current:
                    libs.append(current.decode('utf-8'))
                    current = b''
                    if len(libs) >= self.header.lib_count:
                        break
            else:
                current += byte

        return libs

    def get_info(self):
        """
        Get package information / 获取包信息

        Returns:
            返回：
            dict: Package information / 包信息
        """
        if not self.header:
            return {}

        return {
            'version': f"{(self.header.version >> 16) & 0xFF}.{(self.header.version >> 8) & 0xFF}.{self.header.version & 0xFF}",
            'flags': {
                'executable': bool(self.header.flags & BPP_FLAG_EXECUTABLE),
                'dynamic': bool(self.header.flags & BPP_FLAG_DYNAMIC),
                'gui': bool(self.header.flags & BPP_FLAG_GUI),
                'network': bool(self.header.flags & BPP_FLAG_NETWORK),
                'privileged': bool(self.header.flags & BPP_FLAG_PRIVILEGED),
            },
            'entry_point': hex(self.header.entry_point),
            'load_base': hex(self.header.load_base),
            'image_size': self.header.image_size,
            'bss_size': self.header.bss_size,
            'stack_size': self.header.stack_size,
            'heap_size': self.header.heap_size,
            'library_count': self.header.lib_count,
            'symbol_count': self.header.sym_count,
            'relocation_count': self.header.reloc_count,
            'libraries': self.get_libraries(),
        }


def create_simple_bpp(name, code_bytes, output_path, entry_point=0,
                      executable=True, gui=False, libraries=None):
    """
    Create a simple BPP package.
    创建一个简单的 BPP 包。

    Args:
        参数：
        name (str): Package name / 包名
        code_bytes (bytes): Code data / 代码数据
        output_path (str): Output file path / 输出文件路径
        entry_point (int): Entry point offset / 入口点偏移
        executable (bool): Is executable / 是否可执行
        gui (bool): Requires GUI / 是否需要 GUI
        libraries (list): Library dependencies / 库依赖

    Returns:
        返回：
        int: File size in bytes / 文件大小（字节）
    """
    packager = BPPPackager()
    packager.add_code(code_bytes)
    packager.set_flags(executable=executable, gui=gui, dynamic=bool(libraries))

    if libraries:
        for lib in libraries:
            packager.add_library(lib)

    packager.set_metadata('name', name)

    return packager.save(output_path)


def verify_bpp(filepath):
    """
    Verify a BPP file.
    验证 BPP 文件。

    Args:
        参数：
        filepath (str): Path to BPP file / BPP 文件路径

    Returns:
        返回：
        tuple: (is_valid, info) / (是否有效, 信息)
    """
    try:
        loader = BPPLoader(filepath)
        if loader.is_valid():
            return True, loader.get_info()
        return False, {'error': 'Invalid header'}
    except Exception as e:
        return False, {'error': str(e)}


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: bamboo_pack.py <command> [args...]")
        print("Commands:")
        print("  create <output.bpp> <input.bin>  - Create BPP from binary")
        print("  verify <file.bpp>                - Verify BPP file")
        print("  info <file.bpp>                  - Show BPP info")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'create' and len(sys.argv) >= 4:
        output = sys.argv[2]
        input_file = sys.argv[3]
        with open(input_file, 'rb') as f:
            code = f.read()
        size = create_simple_bpp('app', code, output)
        print(f"Created {output} ({size} bytes)")

    elif command == 'verify' and len(sys.argv) >= 3:
        valid, info = verify_bpp(sys.argv[2])
        if valid:
            print("BPP file is valid")
        else:
            print(f"BPP file is invalid: {info.get('error')}")
        sys.exit(0 if valid else 1)

    elif command == 'info' and len(sys.argv) >= 3:
        valid, info = verify_bpp(sys.argv[2])
        if valid:
            import json
            print(json.dumps(info, indent=2))
        else:
            print(f"Error: {info.get('error')}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
