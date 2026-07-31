# ============================================================================
# Module: core/linker/idt_builder.py
# 模块：core/linker/idt_builder.py
# Description: IDT (Interrupt Descriptor Table) builder for x86-64
# 描述：x86-64 IDT（中断描述符表）构建器
# ============================================================================

"""
IDT Builder for x86-64 interrupt handling.
x86-64 中断处理 IDT 构建器。

Creates 16-byte interrupt gate entries for up to 256 vectors.
创建最多 256 个向量的 16 字节中断门条目。
"""


class IDTBuilder:
    """
    IDT Builder for x86-64.
    x86-64 IDT 构建器。
    """

    # IDT entry size in bytes / IDT 条目大小（字节）
    IDT_ENTRY_SIZE = 16

    # Maximum number of IDT entries / IDT 最大条目数
    MAX_ENTRIES = 256

    # Gate types / 门类型
    GATE_INTERRUPT = 0xE
    GATE_TRAP = 0xF
    GATE_TASK = 0x5

    # Present bit / 存在位
    PRESENT = 1 << 7

    # DPL bits / DPL 位
    DPL_KERNEL = 0 << 5
    DPL_USER = 3 << 5

    # Interrupt stack table (IST) indexes / 中断栈表索引
    IST_NONE = 0
    IST_DOUBLE_FAULT = 1
    IST_NMI = 2
    IST_MACHINE_CHECK = 3

    @staticmethod
    def create_interrupt_gate(offset, selector=0x08, dpl=DPL_KERNEL, ist=IST_NONE):
        """
        Create an interrupt gate entry.
        创建一个中断门条目。

        Args:
            参数：
            offset (int): Handler address / 处理函数地址
            selector (int): Code segment selector / 代码段选择子
            dpl (int): Descriptor privilege level / 描述符特权级
            ist (int): IST index / IST 索引

        Returns:
            返回：
            tuple: (low_64, high_64) / (低64位, 高64位)
        """
        low = 0
        high = 0

        # Low 64 bits:
        # Offset[15:0] (bits 0-15)
        low |= (offset & 0xFFFF) << 0
        # Selector[15:0] (bits 16-31)
        low |= (selector & 0xFFFF) << 16
        # IST[2:0] (bits 32-34)
        low |= (ist & 0x7) << 32
        # Type/Attr (bits 40-47)
        attr = IDTBuilder.PRESENT | dpl | IDTBuilder.GATE_INTERRUPT
        low |= (attr & 0xFF) << 40
        # Offset[31:16] (bits 48-63)
        low |= ((offset >> 16) & 0xFFFF) << 48

        # High 64 bits:
        # Offset[63:32] (bits 0-31)
        high |= (offset >> 32) << 0
        # Reserved (bits 32-63) = 0

        return low, high

    @staticmethod
    def create_trap_gate(offset, selector=0x08, dpl=DPL_KERNEL, ist=IST_NONE):
        """
        Create a trap gate entry.
        创建一个陷阱门条目。

        Args:
            参数：
            offset (int): Handler address / 处理函数地址
            selector (int): Code segment selector / 代码段选择子
            dpl (int): Descriptor privilege level / 描述符特权级
            ist (int): IST index / IST 索引

        Returns:
            返回：
            tuple: (low_64, high_64) / (低64位, 高64位)
        """
        low = 0
        high = 0

        low |= (offset & 0xFFFF) << 0
        low |= (selector & 0xFFFF) << 16
        low |= (ist & 0x7) << 32
        attr = IDTBuilder.PRESENT | dpl | IDTBuilder.GATE_TRAP
        low |= (attr & 0xFF) << 40
        low |= ((offset >> 16) & 0xFFFF) << 48
        high |= (offset >> 32) << 0

        return low, high

    @staticmethod
    def create_syscall_gate(offset, selector=0x08, ist=IST_NONE):
        """
        Create a syscall (int 0x80) gate with DPL=3.
        创建系统调用（int 0x80）门，DPL=3。

        Args:
            参数：
            offset (int): Handler address / 处理函数地址
            selector (int): Code segment selector / 代码段选择子
            ist (int): IST index / IST 索引

        Returns:
            返回：
            tuple: (low_64, high_64) / (低64位, 高64位)
        """
        return IDTBuilder.create_interrupt_gate(
            offset=offset,
            selector=selector,
            dpl=IDTBuilder.DPL_USER,
            ist=ist
        )

    @staticmethod
    def create_default_idt(handler_addr=0):
        """
        Create a default IDT with all entries pointing to a default handler.
        创建默认 IDT，所有条目指向默认处理函数。

        Args:
            参数：
            handler_addr (int): Default handler address / 默认处理函数地址

        Returns:
            返回：
            list: List of (low_64, high_64) tuples / (低64位, 高64位) 元组列表
        """
        entries = []
        for _ in range(IDTBuilder.MAX_ENTRIES):
            low, high = IDTBuilder.create_interrupt_gate(handler_addr)
            entries.append((low, high))
        return entries

    @staticmethod
    def pack_idt(entries):
        """
        Pack IDT entries into bytes.
        将 IDT 条目打包为字节。

        Args:
            参数：
            entries (list): List of (low_64, high_64) tuples / (低64位, 高64位) 元组列表

        Returns:
            返回：
            bytes: Packed IDT bytes / 打包的 IDT 字节
        """
        import struct
        result = bytearray()
        for low, high in entries:
            result.extend(struct.pack('<QQ', low, high))
        return bytes(result)


class IDTPointer:
    """
    IDTR (IDT Pointer) structure for LIDT instruction.
    用于 LIDT 指令的 IDTR（IDT 指针）结构。

    Structure:
    - Limit (2 bytes)
    - Base (8 bytes)
    """

    @staticmethod
    def create_pointer(limit, base):
        """
        Create IDTR pointer bytes.
        创建 IDTR 指针字节。

        Args:
            参数：
            limit (int): IDT limit / IDT 限制
            base (int): IDT base address / IDT 基址

        Returns:
            返回：
            bytes: IDTR bytes / IDTR 字节
        """
        import struct
        return struct.pack('<HQ', limit, base)

    @staticmethod
    def create_pointer_from_entries(num_entries, base_addr):
        """
        Create IDTR pointer from number of entries.
        从条目数创建 IDTR 指针。

        Args:
            参数：
            num_entries (int): Number of IDT entries / IDT 条目数
            base_addr (int): IDT base address / IDT 基址

        Returns:
            返回：
            bytes: IDTR bytes / IDTR 字节
        """
        limit = num_entries * IDTBuilder.IDT_ENTRY_SIZE - 1
        return IDTPointer.create_pointer(limit, base_addr)


# Exception vectors / 异常向量
EXCEPTION_VECTORS = {
    0: "Division Error",
    1: "Debug",
    2: "NMI",
    3: "Breakpoint",
    4: "Overflow",
    5: "Bound Range Exceeded",
    6: "Invalid Opcode",
    7: "Device Not Available",
    8: "Double Fault",
    9: "Coprocessor Segment Overrun",
    10: "Invalid TSS",
    11: "Segment Not Present",
    12: "Stack-Segment Fault",
    13: "General Protection",
    14: "Page Fault",
    15: "Reserved",
    16: "x87 FPU Error",
    17: "Alignment Check",
    18: "Machine Check",
    19: "SIMD Exception",
    20: "Virtualization",
    21: "Control Protection",
    22: "Reserved",
    23: "Reserved",
    24: "Reserved",
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Hypervisor",
    29: "VMM Communication",
    30: "Security",
    31: "Reserved",
}

# IRQ vectors (PIC remapped to 32-47) / IRQ 向量（PIC 重映射到 32-47）
IRQ_BASE = 32
IRQ_VECTORS = {
    0: "Timer",        # IRQ0 -> Vector 32
    1: "Keyboard",     # IRQ1 -> Vector 33
    2: "Cascade",      # IRQ2 -> Vector 34
    3: "COM2",         # IRQ3 -> Vector 35
    4: "COM1",         # IRQ4 -> Vector 36
    5: "LPT2",         # IRQ5 -> Vector 37
    6: "Floppy",       # IRQ6 -> Vector 38
    7: "LPT1",         # IRQ7 -> Vector 39
    8: "RTC",          # IRQ8 -> Vector 40
    9: "ACPI",         # IRQ9 -> Vector 41
    10: "IRQ10",       # IRQ10 -> Vector 42
    11: "IRQ11",       # IRQ11 -> Vector 43
    12: "Mouse",       # IRQ12 -> Vector 44
    13: "FPU",         # IRQ13 -> Vector 45
    14: "Primary ATA", # IRQ14 -> Vector 46
    15: "Secondary ATA", # IRQ15 -> Vector 47
}