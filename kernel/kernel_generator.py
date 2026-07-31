# ============================================================================
# Module: kernel/kernel_generator.py
# 模块：kernel/kernel_generator.py
# Description: Kernel code generator for Bamboo OS Wonder Series
# 描述：Bamboo OS Wonder 系列内核代码生成器
# ============================================================================

import os
import sys
from pathlib import Path


def generate_kernel(config, output_path):
    """
    Generate kernel binary using X64Compiler.
    使用 X64Compiler 生成内核二进制。

    Args:
        参数：
        config: Configuration module / 配置模块
        output_path (Path): Output file path / 输出文件路径

    Returns:
        返回：
        int: Size of generated kernel in bytes / 生成的内核大小（字节）
    """
    # Import the core compiler / 导入核心编译器
    from kernel.bamboo_os_core import X64Compiler

    # Create compiler instance / 创建编译器实例
    c = X64Compiler()

    # Apply configuration / 应用配置
    kernel_config = config.KERNEL_CONFIG
    memory_config = config.MEMORY_CONFIG
    fs_config = config.FS_CONFIG

    # ========================================================================
    # Phase 0: Boot & Core Infrastructure / 启动与核心基础设施
    # ========================================================================

    # Generate Multiboot2 header / 生成 Multiboot2 头
    if kernel_config.get('multiboot', 2) == 2:
        c.create_multiboot2_header()

    # Generate 32-bit startup stub / 生成 32 位启动桩
    c.create_32bit_startup_stub()

    # Generate long mode switch / 生成长模式切换
    c.create_long_mode_switch()

    # Generate page tables / 生成页表
    c.build_initial_page_tables()

    # Generate GDT / 生成 GDT
    c.build_gdt_table()

    # Generate kmain / 生成内核主函数
    c.create_kmain()

    # ========================================================================
    # Phase 1: Memory Management / 内存管理
    # ========================================================================

    # Physical memory manager / 物理内存管理器
    c.create_pmm_init()
    c.create_pmm_init_bitmap()
    c.create_pmm_init_buddy()
    c.create_pmm_alloc_buddy()
    c.create_pmm_free_buddy()
    c.create_pmm_alloc_page()
    c.create_pmm_free_page()
    c.create_pmm_stats()
    c.create_pmm_debug()

    # Virtual memory manager / 虚拟内存管理器
    c.create_vmm_walk_page_table()
    c.create_vmm_map_page()
    c.create_vmm_unmap_page()
    c.create_vmm_protect_page()
    c.create_vmm_kernel_space_map()
    c.create_vmm_user_space_map()
    c.create_vmm_check_user_addr()
    c.create_address_space_struct()

    # Slab allocator / Slab 分配器
    c.create_kmem_cache_struct()
    c.create_kmem_cache_create()
    c.create_kmem_cache_destroy()
    c.create_kmem_cache_alloc()
    c.create_kmem_cache_free()
    c.create_kmalloc()
    c.create_kfree()
    c.create_slab_caches_init()
    c.create_emergency_pool()

    # User memory management / 用户内存管理
    c.create_sys_mmap()
    c.create_sys_munmap()
    c.create_sys_mprotect()
    c.create_cow_mechanism()
    c.create_sys_brk()
    c.create_shared_memory()

    # Advanced memory features / 高级内存特性
    c.create_swap_support()
    c.create_memory_compaction()
    c.create_hugepage_support()
    c.create_numa_allocator()
    c.create_memory_hotplug()

    # Memory debugging / 内存调试
    c.create_kasan()
    c.create_rbtree_memory_tracking()
    c.create_slab_poisoning()
    c.create_kmemleak()
    c.create_proc_meminfo()

    # ========================================================================
    # Phase 2: Process & Scheduling / 进程与调度
    # ========================================================================

    c.create_pcb_struct()
    c.create_scheduler()
    c.create_context_switch()
    c.create_sync_primitives()
    c.create_ipc()

    # ========================================================================
    # Phase 3: Interrupts & System Calls / 中断与系统调用
    # ========================================================================

    c.create_interrupt_handling()
    c.create_exception_handling()
    c.create_syscall_framework()

    # ========================================================================
    # Phase 4: File System / 文件系统
    # ========================================================================

    c.create_vfs_core()
    c.create_fat32()
    c.create_ext_filesystems()
    c.create_proc_sysfs()
    c.create_vfs_advanced()

    # ========================================================================
    # Phase 5: Device Drivers / 设备驱动
    # ========================================================================

    c.create_device_model()
    c.create_block_device()
    c.create_network_stack()
    c.create_graphics_input()
    c.create_advanced_drivers()

    # ========================================================================
    # Phase 6: SMP & Security / SMP 与安全
    # ========================================================================

    c.create_smp_support()
    c.create_security_features()

    # ========================================================================
    # Phase 7: Advanced Features / 高级特性
    # ========================================================================

    c.create_virtualization()
    c.create_container_support()
    c.create_dynamic_linker()
    c.create_posix_compat()

    # ========================================================================
    # Phase 8: Network Services & GUI / 网络服务与图形界面
    # ========================================================================

    c.create_network_services()
    c.create_gui()
    c.create_av_subsystem()

    # ========================================================================
    # Phase 9: Toolchain & System Services / 工具链与系统服务
    # ========================================================================

    c.create_toolchain()
    c.create_package_manager()
    c.create_system_services()

    # ========================================================================
    # Phase 10: Test & Release / 测试与发布
    # ========================================================================

    c.create_test_certification()
    c.create_release_maintenance()

    # ========================================================================
    # Resolve and Save / 解析并保存
    # ========================================================================

    # Resolve labels / 解析标签
    c.resolve()

    # Save kernel binary / 保存内核二进制
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    size = c.save(str(output_path))

    return size


def generate_minimal_kernel(config, output_path):
    """
    Generate minimal kernel for Education version.
    为教学版生成最小内核。

    Args:
        参数：
        config: Configuration module / 配置模块
        output_path (Path): Output file path / 输出文件路径

    Returns:
        返回：
        int: Size of generated kernel in bytes / 生成的内核大小（字节）
    """
    from kernel.bamboo_os_core import X64Compiler

    c = X64Compiler()

    # Minimal kernel: boot + basic memory + shell / 最小内核：启动 + 基本内存 + shell
    c.create_multiboot2_header()
    c.create_32bit_startup_stub()
    c.create_long_mode_switch()
    c.build_initial_page_tables()
    c.build_gdt_table()
    c.create_kmain()
    c.create_pmm_init_bitmap()
    c.create_pmm_alloc_page()
    c.create_pmm_free_page()
    c.create_vmm_walk_page_table()
    c.create_vmm_map_page()
    c.create_kmalloc()
    c.create_kfree()
    c.create_scheduler()
    c.create_interrupt_handling()
    c.create_exception_handling()
    c.create_syscall_framework()
    c.create_vfs_core()
    c.create_fat32()
    c.create_graphics_input()

    c.resolve()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    size = c.save(str(output_path))

    return size