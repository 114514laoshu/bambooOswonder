; ============================================================================
; Module: kernel/boot/boot_stub_64.asm
; 模块：kernel/boot/boot_stub_64.asm
; Description: 64-bit boot stub entry for Bamboo OS
; 描述：Bamboo OS 的 64 位启动桩入口
; ============================================================================

section .text
global long_mode_entry

long_mode_entry:
    ; Disable interrupts / 禁用中断
    cli

    ; Set up segment registers / 设置段寄存器
    mov ax, 0x10                ; Kernel data selector / 内核数据选择子
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; Set up kernel stack / 设置内核栈
    ; Stack grows downward from 0x90000 / 栈从 0x90000 向下增长
    mov rsp, 0x90000
    mov rbp, 0

    ; Clear BSS section / 清空 BSS 段
    extern bss_start
    extern bss_end
    mov rdi, bss_start
    mov rcx, bss_end
    sub rcx, rdi
    xor rax, rax
    rep stosb

    ; Load GDT / 加载 GDT
    extern gdt64_pointer
    lgdt [gdt64_pointer]

    ; Load IDT / 加载 IDT
    extern idt_pointer
    lidt [idt_pointer]

    ; Jump to kernel main / 跳转到内核主函数
    extern kmain
    call kmain

    ; Should never return / 不应返回
    cli
    hlt
    jmp $

; ============================================================================
; GDT64 (64-bit) / GDT64（64位）
; ============================================================================
section .data
align 8
global gdt64
gdt64:
    dq 0                        ; 0x00: Null / 空
    dq 0x00AF9A000000FFFF      ; 0x08: Kernel code / 内核代码段
    dq 0x00CF92000000FFFF      ; 0x10: Kernel data / 内核数据段
    dq 0x00AFFA000000FFFF      ; 0x1B: User code / 用户代码段
    dq 0x00CFF2000000FFFF      ; 0x23: User data / 用户数据段
    dq 0x0000890000000068      ; 0x28: TSS low / TSS 低 64 位 (placeholder)
    dq 0x0000000000000000      ; 0x30: TSS high / TSS 高 64 位 (placeholder)

global gdt64_pointer
gdt64_pointer:
    dw ($ - gdt64) - 1          ; Limit / 限制
    dq gdt64                    ; Base / 基址

; ============================================================================
; IDT (temporary) / IDT（临时）
; ============================================================================
section .data
global idt_entries
idt_entries:
    ; Fill with 256 default entries / 填充 256 个默认条目
    %rep 256
    dw 0                        ; Offset[15:0]
    dw 0x08                     ; Selector / 选择子 (0x08)
    db 0                        ; IST
    db 0x8E                     ; Type/Attr (Present, Interrupt Gate) / 类型/属性
    dw 0                        ; Offset[31:16]
    dd 0                        ; Offset[63:32]
    dd 0                        ; Reserved / 保留
    %endrep

global idt_pointer
idt_pointer:
    dw (256 * 16) - 1           ; Limit / 限制
    dq idt_entries              ; Base / 基址