# ============================================================================
# Module: kernel/resources/kernelstringmanager.py
# 模块：kernel/resources/kernelstringmanager.py
# Description: KernelStringManager resource management
# 描述：KernelStringManager 资源管理
# ============================================================================

class KernelStringManager:
    """集中管理所有内核字符串常量，自动注册到RODATA段"""
    
    def __init__(self, compiler):
        self.c = compiler
        self.strings = {}
        self.messages = {}
        self.errors = {}
        self.prompts = {}
    
    def add_string(self, name, value):
        """添加字符串常量并自动注册到RODATA"""
        self.strings[name] = value
        self.c.rodata_string(name, value)
        return name
    
    def add_message(self, msg_id, text):
        """添加内核消息"""
        self.messages[msg_id] = text
        name = f"msg_{msg_id}"
        self.c.rodata_string(name, text)
        return name
    
    def add_error(self, err_id, text):
        """添加错误信息"""
        self.errors[err_id] = text
        name = f"err_{err_id}"
        self.c.rodata_string(name, text)
        return name
    
    def add_prompt(self, prompt_id, text):
        """添加提示文本"""
        self.prompts[prompt_id] = text
        name = f"prompt_{prompt_id}"
        self.c.rodata_string(name, text)
        return name
    
    def batch_register(self):
        """批量注册标准内核字符串"""
        # 内核启动消息
        self.add_message("boot_start", "Bamboo OS v6.0 booting...\n")
        self.add_message("boot_ok", "Kernel initialized successfully\n")
        self.add_message("hello_world", "Hello World from Bamboo OS!\n")
        
        # 错误信息
        self.add_error("panic", "KERNEL PANIC: ")
        self.add_error("oops", "Oops: ")
        self.add_error("page_fault", "Page fault at address: ")
        self.add_error("gp_fault", "General protection fault\n")
        
        # Shell提示
        self.add_prompt("shell", "bamboo> ")
        self.add_prompt("welcome", "Welcome to Bamboo OS v6.0\n")
        self.add_prompt("help_hint", "Type 'help' for available commands\n")
        
        return len(self.strings) + len(self.messages) + len(self.errors) + len(self.prompts)


# =============================================================================
# Shell Help Database - 300+命令帮助文本
# =============================================================================