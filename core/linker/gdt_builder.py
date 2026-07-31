# ============================================================================
# Module: core/linker/gdt_builder.py
# 模块：core/linker/gdt_builder.py
# Description: GDT (Global Descriptor Table) builder for x86-64 long mode
# 描述：x86-64 长模式 GDT（全局描述符表）构建器
# ============================================================================

"""
GDT Builder for x86-64 Long Mode.
x86-64 长模式 GDT 构建器。

Creates 64-bit GDT entries for kernel and user mode.
创建内核和用户模式的 64 位 GDT 条目。
"""


class GDTBuilder:
    """
    GDT Builder for x86-64 long mode.
    x86-64 长模式 GDT 构建器。
    """

    # GDT entry size in bytes / GDT 条目大小（字节）
    GDT_ENTRY_SIZE = 8

    # Segment selectors / 段选择子
    SEL_NULL = 0x00
    SEL_KERNEL_CODE = 0x08
    SEL_KERNEL_DATA = 0x10
    SEL_USER_CODE = 0x1B
    SEL_USER_DATA = 0x23
    SEL_TSS = 0x28

    @staticmethod
    def create_null():
        """
        Create null descriptor (all zeros).
        创建空描述符（全零）。

        Returns:
            返回：
            int: 64-bit null descriptor / 64位空描述符        """
        return 0

    @staticmethod
    def create_kernel_code():
        """
        Create 64-bit kernel code segment descriptor.
        创建 64 位内核代码段描述符。

        Entry fields:
        - Base: 0
        - Limit: 0xFFFFF (4GB)
        - G (Granularity): 1 (4KB units)
        - D/B: 0 (64-bit mode)
        - L: 1 (64-bit code)
        - AVL: 0
        - P: 1 (Present)
        - DPL: 0 (Kernel)
        - S: 1 (Code/Data)
        - Type: 0xA (Execute/Read)

        Returns:
            返回：
            int: 64-bit descriptor / 64位描述符
        """
        # Format: Limit[15:0] (16 bits) | Base[23:0] (24 bits) | Access (8 bits)
        #         | Limit[19:16] (4 bits) | Flags (4 bits) | Base[31:24] (8 bits)
        # For 64-bit: Base=0, Limit=0xFFFFF, G=1, L=1
        return 0x00AF9A000000FFFF

    @staticmethod
    def create_kernel_data():
        """
        Create 64-bit kernel data segment descriptor.
        创建 64 位内核数据段描述符。

        Returns:
            返回：
            int: 64-bit descriptor / 64位描述符
        """
        # Type: 0x2 (Read/Write), D/B: 1 (32-bit stack), G: 1
        return 0x00CF92000000FFFF

    @staticmethod
    def create_user_code():
        """
        Create 64-bit user code segment descriptor (Ring 3).
        创建 64 位用户代码段描述符（Ring 3）。

        Returns:
            返回：
            int: 64-bit descriptor / 64位描述符
        """
        # DPL: 3 (User), Type: 0xA (Execute/Read)
        return 0x00AFFA000000FFFF

    @staticmethod
    def create_user_data():
        """
        Create 64-bit user data segment descriptor (Ring 3).
        创建 64 位用户数据段描述符（Ring 3）。

        Returns:
            返回：
            int: 64-bit descriptor / 64位描述符
        """
        # DPL: 3 (User), Type: 0x2 (Read/Write)
        return 0x00CFF2000000FFFF

    @staticmethod
    def create_tss(base, limit=0x67):
        """
        Create TSS (Task State Segment) descriptor.
        创建 TSS（任务状态段）描述符。

        TSS descriptor is 16 bytes (two 8-byte entries):
        - Entry 0: limit[15:0], base[23:0], type, limit[19:16], base[31:24]
        - Entry 1: base[63:32]

        Args:
            参数：
            base (int): TSS base address / TSS 基址
            limit (int): TSS limit (default 0x67 = 103 bytes) / TSS 限制

        Returns:
            返回：
            tuple: (low_64, high_64) / (低64位, 高64位)
        """
        low = 0
        high = 0

        # Low 64 bits
        low |= (limit & 0xFFFF) << 0
        low |= ((base >> 0) & 0xFFFFFF) << 16
        low |= (0x89 << 40)  # Type: 0x89 (64-bit TSS, available)
        low |= ((limit >> 16) & 0x0F) << 48
        low |= ((base >> 24) & 0xFF) << 56

        # High 64 bits
        high |= (base >> 32) << 0

        return low, high

    @staticmethod
    def build_gdt():
        """
        Build a complete GDT with all standard entries.
        构建包含所有标准条目的完整 GDT。

        Returns:
            返回：
            list: List of 64-bit GDT entries / 64位 GDT 条目列表
        """
        gdt = []

        # Entry 0: Null descriptor / 空描述符
        gdt.append(GDTBuilder.create_null())

        # Entry 1: Kernel code (0x08) / 内核代码段
        gdt.append(GDTBuilder.create_kernel_code())

        # Entry 2: Kernel data (0x10) / 内核数据段
        gdt.append(GDTBuilder.create_kernel_data())

        # Entry 3: User code (0x1B) / 用户代码段
        gdt.append(GDTBuilder.create_user_code())

        # Entry 4: User data (0x23) / 用户数据段
        gdt.append(GDTBuilder.create_user_data())

        # Entry 5-6: TSS (0x28) / TSS 段（两个 64 位条目）
        tss_base = 0  # Will be filled by linker
        tss_low, tss_high = GDTBuilder.create_tss(tss_base)
        gdt.append(tss_low)
        gdt.append(tss_high)

        return gdt

    @staticmethod
    def get_gdt_limit(gdt_entries):
        """
        Get GDT limit (size - 1).
        获取 GDT 限制（大小减 1）。

        Args:
            参数：
            gdt_entries (list): GDT entries / GDT 条目

        Returns:
            返回：
            int: GDT limit / GDT 限制
        """
        return len(gdt_entries) * GDTBuilder.GDT_ENTRY_SIZE - 1

    @staticmethod
    def pack_gdt(gdt_entries):
        """
        Pack GDT entries into bytes.
        将 GDT 条目打包为字节。

        Args:
            参数：
            gdt_entries (list): GDT entries / GDT 条目

        Returns:
            返回：
            bytes: Packed GDT bytes / 打包的 GDT 字节
        """
        import struct
        result = bytearray()
        for entry in gdt_entries:
            result.extend(struct.pack('<Q', entry))
        return bytes(result)


class GDTPointer:
    """
    GDTR (GDT Pointer) structure for LGDT instruction.
    用于 LGDT 指令的 GDTR（GDT 指针）结构。

    Structure:
    - Limit (2 bytes)
    - Base (8 bytes)
    """

    @staticmethod
    def create_pointer(limit, base):
        """
        Create GDTR pointer bytes.
        创建 GDTR 指针字节。

        Args:
            参数：
            limit (int): GDT limit / GDT 限制
            base (int): GDT base address / GDT 基址

        Returns:
            返回：
            bytes: GDTR bytes / GDTR 字节
        """
        import struct
        return struct.pack('<HQ', limit, base)

    @staticmethod
    def create_pointer_from_gdt(gdt_entries, base_addr):
        """
        Create GDTR pointer from GDT entries.
        从 GDT 条目创建 GDTR 指针。

        Args:
            参数：
            gdt_entries (list): GDT entries / GDT 条目
            base_addr (int): GDT base address / GDT 基址

        Returns:
            返回：
            bytes: GDTR bytes / GDTR 字节
        """
        limit = GDTBuilder.get_gdt_limit(gdt_entries)
        return GDTPointer.create_pointer(limit, base_addr)


# Export constants / 导出常量
GDTR_LIMIT_OFFSET = 0
GDTR_BASE_OFFSET = 2
GDTR_SIZE = 10  # 2 bytes limit + 8 bytes base