; ============================================================================
; Module: kernel/boot/boot_stub_32.asm
; 模块：kernel/boot/boot_stub_32.asm
; Description: 32-bit boot stub for Bamboo OS
; 描述：Bamboo OS 的 32 位启动桩
; ============================================================================

; ============================================================================
; Multiboot2 Header
; ============================================================================
section .multiboot2
align 8
mb2_header:
    dd 0xE85250D6              ; Magic / 魔数
    dd 0                       ; Architecture / 架构 (i386)
    dd mb2_header_end - mb2_header ; Header length / 头长度
    dd 0x100000000 - (0xE85250D6 + 0 + (mb2_header_end - mb2_header)) ; Checksum

    ; End tag / 结束标签
    dw 0                       ; Type / 类型
    dw 0                       ; Flags / 标志
    dd 8                       ; Size / 大小
mb2_header_end:

; ============================================================================
; Multiboot1 Header (for legacy GRUB compatibility)
; ============================================================================
section .multiboot1
align 4
mb1_header:
    dd 0x1BADB002              ; Magic / 魔数
    dd 0x00010003              ; Flags / 标志
    dd -(0x1BADB002 + 0x00010003) ; Checksum / 校验和

; ============================================================================
; 32-bit Entry Point / 32 位入口点
; ============================================================================
section .text
global _start
_start:
    ; Disable interrupts / 禁用中断
    cli

    ; Set up stack (grows downward) / 设置栈（向下增长）
    mov esp, 0x90000
    mov ebp, esp

    ; Save Multiboot info / 保存 Multiboot 信息
    ; eax = magic (0x2BADB002 for M1, 0x36D76289 for M2)
    ; ebx = multiboot info pointer
    mov [multiboot_magic], eax
    mov [multiboot_info], ebx

    ; Enable PAE (Page Address Extension) / 启用 PAE
    mov eax, cr4
    or eax, 0x20                ; Set PAE bit / 设置 PAE 位
    mov cr4, eax

    ; Set up page tables at 0x70000 / 在 0x70000 设置页表
    mov edi, 0x70000
    mov ecx, 0x1000 * 5 / 4     ; 5 pages / 5 页
    xor eax, eax
    rep stosd

    ; PML4[0] -> PDPT at 0x71000 / PML4[0] -> PDPT 在 0x71000
    mov dword [0x70000], 0x71000 + 0x03

    ; PML4[256] -> PDPT (higher half) / PML4[256] -> PDPT（高半）
    mov dword [0x70000 + 256*8], 0x71000 + 0x03

    ; PDPT[0] -> PD at 0x72000 / PDPT[0] -> PD 在 0x72000
    mov dword [0x71000], 0x72000 + 0x03

    ; Fill PD with 2MB pages (first 512 entries = 1GB) / 用 2MB 页填充 PD
    mov ebx, 0x72000
    mov eax, 0x83               ; Present + Writable + Large / 存在+可写+大页
    mov ecx, 512
.fill_pd:
    mov [ebx], eax
    add eax, 0x200000           ; Next 2MB / 下一个 2MB
    add ebx, 8
    dec ecx
    jnz .fill_pd

    ; Load PML4 into CR3 / 加载 PML4 到 CR3
    mov eax, 0x70000
    mov cr3, eax

    ; Enable Long Mode (EFER.LME) / 启用长模式
    mov ecx, 0xC0000080         ; EFER MSR / EFER MSR
    rdmsr
    or eax, 0x100               ; Set LME bit / 设置 LME 位
    wrmsr

    ; Enable Paging / 启用分页
    mov eax, cr0
    or eax, 0x80000001          ; Set PG + PE bits / 设置 PG + PE 位
    mov cr0, eax

    ; Load 64-bit GDT / 加载 64 位 GDT
    lgdt [gdt64_pointer]

    ; Far jump to 64-bit mode / 远跳转到 64 位模式
    jmp 0x08:long_mode_entry_64

; ============================================================================
; GDT64 (temporary) / GDT64（临时）
; ============================================================================
section .data
align 8
gdt64:
    dq 0                        ; Null / 空
    dq 0x00AF9A000000FFFF      ; Kernel code / 内核代码段 (0x08)
    dq 0x00CF92000000FFFF      ; Kernel data / 内核数据段 (0x10)

gdt64_pointer:
    dw $ - gdt64 - 1            ; Limit / 限制
    dq gdt64                    ; Base / 基址

; ============================================================================
; Data Section / 数据段
; ============================================================================
section .bss
align 4
multiboot_magic:
    resd 1
multiboot_info:
    resd 1

; ============================================================================
; 64-bit Entry (actual target of far jump) / 64 位入口（远跳转目标）
; ============================================================================
section .text
long_mode_entry_64:
    ; Set up 64-bit segment registers / 设置 64 位段寄存器
    mov ax, 0x10                ; Kernel data selector / 内核数据选择子
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; Set up kernel stack / 设置内核栈
    mov rsp, 0x90000
    mov rbp, 0

    ; Jump to kmain / 跳转到 kmain
    extern kmain
    call kmain

    ; Should never return / 不应返回
    cli
    hlt
    jmp $