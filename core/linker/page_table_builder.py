# ============================================================================
# Module: core/linker/page_table_builder.py
# 模块：core/linker/page_table_builder.py
# Description: Page table builder for x86-64 paging
# 描述：x86-64 分页页表构建器
# ============================================================================

"""
Page Table Builder for x86-64 4-level paging.
x86-64 4 级分页页表构建器。

Supports:
- 4KB pages
- 2MB huge pages
- 1GB huge pages (if supported)
- Kernel higher-half mapping
"""


class PageTableBuilder:
    """
    Page Table Builder for x86-64.
    x86-64 页表构建器。
    """

    # Page size constants / 页大小常量
    PAGE_SIZE_4KB = 4096
    PAGE_SIZE_2MB = 0x200000
    PAGE_SIZE_1GB = 0x40000000

    # Page table entry flags / 页表条目标志
    PTE_PRESENT = 0x001
    PTE_WRITABLE = 0x002
    PTE_USER = 0x004
    PTE_WRITE_THROUGH = 0x008
    PTE_CACHE_DISABLE = 0x010
    PTE_ACCESSED = 0x020
    PTE_DIRTY = 0x040
    PTE_LARGE = 0x080
    PTE_GLOBAL = 0x100
    PTE_PAT = 0x080  # Same bit as LARGE, context dependent
    PTE_NX = 0x8000000000000000  # No Execute (if supported)

    # Page table levels / 页表级别
    LEVEL_PML4 = 0
    LEVEL_PDPT = 1
    LEVEL_PD = 2
    LEVEL_PT = 3

    # Number of entries per level / 每级条目数
    ENTRIES_PER_LEVEL = 512

    # Entry size in bytes / 条目大小（字节）
    ENTRY_SIZE = 8

    @staticmethod
    def create_pte(phys_addr, flags=PTE_PRESENT | PTE_WRITABLE):
        """
        Create a page table entry.
        创建一个页表条目。

        Args:
            参数：
            phys_addr (int): Physical address (aligned to page size) / 物理地址
            flags (int): Page flags / 页标志

        Returns:
            返回：
            int: Page table entry / 页表条目
        """
        return (phys_addr & ~0xFFF) | (flags & 0xFFF)

    @staticmethod
    def create_huge_pte(phys_addr, flags=PTE_PRESENT | PTE_WRITABLE | PTE_LARGE):
        """
        Create a huge page (2MB) entry.
        创建一个大页（2MB）条目。

        Args:
            参数：
            phys_addr (int): Physical address (aligned to 2MB) / 物理地址
            flags (int): Page flags / 页标志

        Returns:
            返回：
            int: Huge page entry / 大页条目
        """
        return (phys_addr & ~(PageTableBuilder.PAGE_SIZE_2MB - 1)) | (flags & 0xFFF)

    @staticmethod
    def get_pml4_index(addr):
        """
        Get PML4 index from virtual address.
        从虚拟地址获取 PML4 索引。

        Args:
            参数：
            addr (int): Virtual address / 虚拟地址

        Returns:
            返回：
            int: PML4 index (0-511) / PML4 索引
        """
        return (addr >> 39) & 0x1FF

    @staticmethod
    def get_pdpt_index(addr):
        """
        Get PDPT index from virtual address.
        从虚拟地址获取 PDPT 索引。

        Args:
            参数：
            addr (int): Virtual address / 虚拟地址

        Returns:
            返回：
            int: PDPT index (0-511) / PDPT 索引
        """
        return (addr >> 30) & 0x1FF

    @staticmethod
    def get_pd_index(addr):
        """
        Get PD index from virtual address.
        从虚拟地址获取 PD 索引。

        Args:
            参数：
            addr (int): Virtual address / 虚拟地址

        Returns:
            返回：
            int: PD index (0-511) / PD 索引
        """
        return (addr >> 21) & 0x1FF

    @staticmethod
    def get_pt_index(addr):
        """
        Get PT index from virtual address.
        从虚拟地址获取 PT 索引。

        Args:
            参数：
            addr (int): Virtual address / 虚拟地址

        Returns:
            返回：
            int: PT index (0-511) / PT 索引
        """
        return (addr >> 12) & 0x1FF

    @staticmethod
    def identity_map_range(pml4_addr, start_phys, end_phys, flags=PTE_PRESENT | PTE_WRITABLE):
        """
        Generate identity mapping for a physical address range.
        生成物理地址范围的恒等映射。

        Args:
            参数：
            pml4_addr (int): PML4 physical address / PML4 物理地址
            start_phys (int): Start physical address / 起始物理地址
            end_phys (int): End physical address / 结束物理地址
            flags (int): Page flags / 页标志

        Returns:
            返回：
            list: List of (level, index, pte) tuples / (级别, 索引, PTE) 元组列表
        """
        entries = []
        # Align to page boundaries / 对齐到页边界
        start = start_phys & ~(PageTableBuilder.PAGE_SIZE_4KB - 1)
        end = (end_phys + PageTableBuilder.PAGE_SIZE_4KB - 1) & ~(PageTableBuilder.PAGE_SIZE_4KB - 1)

        for addr in range(start, end, PageTableBuilder.PAGE_SIZE_4KB):
            pml4_idx = PageTableBuilder.get_pml4_index(addr)
            pdpt_idx = PageTableBuilder.get_pdpt_index(addr)
            pd_idx = PageTableBuilder.get_pd_index(addr)
            pt_idx = PageTableBuilder.get_pt_index(addr)

            # PML4 entry / PML4 条目
            entries.append((PageTableBuilder.LEVEL_PML4, pml4_idx,
                            PageTableBuilder.create_pte(pml4_addr + 0x1000 + pdpt_idx * 8, flags)))
            # PDPT entry / PDPT 条目
            entries.append((PageTableBuilder.LEVEL_PDPT, pdpt_idx,
                            PageTableBuilder.create_pte(pml4_addr + 0x2000 + pd_idx * 8, flags)))
            # PD entry / PD 条目
            entries.append((PageTableBuilder.LEVEL_PD, pd_idx,
                            PageTableBuilder.create_pte(pml4_addr + 0x3000 + pt_idx * 8, flags)))
            # PT entry / PT 条目
            entries.append((PageTableBuilder.LEVEL_PT, pt_idx,
                            PageTableBuilder.create_pte(addr, flags)))

        return entries

    @staticmethod
    def higher_half_map(pml4_addr, phys_start, virt_start, size, flags=PTE_PRESENT | PTE_WRITABLE):
        """
        Map physical memory to higher-half virtual address.
        将物理内存映射到高半虚拟地址。

        Args:
            参数：
            pml4_addr (int): PML4 physical address / PML4 物理地址
            phys_start (int): Start physical address / 起始物理地址
            virt_start (int): Start virtual address (kernel base) / 起始虚拟地址
            size (int): Size to map / 映射大小
            flags (int): Page flags / 页标志

        Returns:
            返回：
            list: List of (level, index, pte) tuples / (级别, 索引, PTE) 元组列表
        """
        entries = []
        # PML4[256-511] is used for higher half / PML4[256-511] 用于高半
        # The kernel base is typically 0xFFFFFFFF80000000
        # PML4 index for kernel base: (0xFFFFFFFF80000000 >> 39) & 0x1FF = 256

        # For simplicity, map using 2MB huge pages / 简化：使用 2MB 大页映射
        pml4_idx = PageTableBuilder.get_pml4_index(virt_start)
        pdpt_idx = PageTableBuilder.get_pdpt_index(virt_start)

        # PML4 entry / PML4 条目
        pdpt_addr = pml4_addr + 0x1000  # PDPT follows PML4
        entries.append((PageTableBuilder.LEVEL_PML4, pml4_idx,
                        PageTableBuilder.create_pte(pdpt_addr, flags)))

        # PDPT entry / PDPT 条目
        pd_addr = pml4_addr + 0x2000  # PD follows PDPT
        entries.append((PageTableBuilder.LEVEL_PDPT, pdpt_idx,
                        PageTableBuilder.create_pte(pd_addr, flags)))

        # Map using 2MB pages / 使用 2MB 大页映射
        num_pages = (size + PageTableBuilder.PAGE_SIZE_2MB - 1) // PageTableBuilder.PAGE_SIZE_2MB
        for i in range(num_pages):
            pd_idx = PageTableBuilder.get_pd_index(virt_start + i * PageTableBuilder.PAGE_SIZE_2MB)
            phys = phys_start + i * PageTableBuilder.PAGE_SIZE_2MB
            entries.append((PageTableBuilder.LEVEL_PD, pd_idx,
                            PageTableBuilder.create_huge_pte(phys, flags | PageTableBuilder.PTE_LARGE)))

        return entries

    @staticmethod
    def get_default_pml4_layout():
        """
        Get default PML4 layout addresses.
        获取默认 PML4 布局地址。

        Returns:
            返回：
            dict: Layout addresses / 布局地址
        """
        return {
            'pml4': 0x70000,
            'pdpt': 0x71000,
            'pd': 0x72000,
            'pt': 0x73000,
            'kernel_pdpt': 0x74000,
            'kernel_pd': 0x75000,
        }

    @staticmethod
    def clear_page_table(addr, num_entries=ENTRIES_PER_LEVEL):
        """
        Clear a page table (fill with zeros).
        清空一个页表（填充零）。

        Args:
            参数：
            addr (int): Page table address / 页表地址
            num_entries (int): Number of entries to clear / 清空的条目数

        Returns:
            返回：
            bytes: Zero-filled page table bytes / 零填充的页表字节
        """
        return b'\x00' * (num_entries * PageTableBuilder.ENTRY_SIZE)


# Page table layout constants / 页表布局常量
PML4_ADDR = 0x70000
PDPT_ADDR = 0x71000
PD_ADDR = 0x72000
PT_ADDR = 0x73000
KERNEL_PDPT_ADDR = 0x74000
KERNEL_PD_ADDR = 0x75000
KERNEL_PT_ADDR = 0x76000

# Kernel higher-half base (canonical address) / 内核高半基址（规范地址）
KERNEL_BASE = 0xFFFFFFFF80000000
KERNEL_PML4_INDEX = (KERNEL_BASE >> 39) & 0x1FF  # 256