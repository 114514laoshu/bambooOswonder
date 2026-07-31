# ============================================================================
# Module: kernel/resources/shellhelpdatabase.py
# 模块：kernel/resources/shellhelpdatabase.py
# Description: ShellHelpDatabase resource management
# 描述：ShellHelpDatabase 资源管理
# ============================================================================

class ShellHelpDatabase:
    """集中存储所有Shell命令的帮助文本"""
    
    def __init__(self, compiler):
        self.c = compiler
        self.commands = {}
    
    def add_command(self, name, short_help, long_help=""):
        """添加命令帮助信息"""
        self.commands[name] = {
            'short': short_help,
            'long': long_help
        }
        # 注册到RODATA段
        self.c.rodata_string(f"help_{name}_short", short_help)
        if long_help:
            self.c.rodata_string(f"help_{name}_long", long_help)
    
    def register_all_commands(self):
        """注册所有300+Shell命令"""
        
        # ========== 文件系统命令 ==========
        self.add_command("ls", "List directory contents", 
                        "Usage: ls [path]\nList files and directories in the current or specified directory")
        self.add_command("cd", "Change working directory")
        self.add_command("pwd", "Print working directory")
        self.add_command("mkdir", "Create directory")
        self.add_command("rmdir", "Remove directory")
        self.add_command("rm", "Remove file")
        self.add_command("cp", "Copy file")
        self.add_command("mv", "Move/rename file")
        self.add_command("cat", "Display file contents")
        self.add_command("touch", "Create empty file")
        self.add_command("chmod", "Change file permissions")
        self.add_command("chown", "Change file owner")
        self.add_command("find", "Search for files")
        self.add_command("grep", "Search text in files")
        
        # ========== 进程管理命令 ==========
        self.add_command("ps", "List running processes")
        self.add_command("top", "Display process statistics")
        self.add_command("kill", "Terminate process")
        self.add_command("nice", "Set process priority")
        self.add_command("renice", "Change process priority")
        self.add_command("fork", "Create new process")
        self.add_command("exec", "Execute program")
        self.add_command("wait", "Wait for process")
        self.add_command("exit", "Exit current process")
        self.add_command("bg", "Run process in background")
        self.add_command("fg", "Bring process to foreground")
        self.add_command("jobs", "List background jobs")
        
        # ========== 内存管理命令 ==========
        self.add_command("free", "Display memory usage")
        self.add_command("meminfo", "Detailed memory information")
        self.add_command("slabinfo", "Slab allocator statistics")
        self.add_command("vmstat", "Virtual memory statistics")
        self.add_command("mmap", "Map memory region")
        self.add_command("munmap", "Unmap memory region")
        self.add_command("mprotect", "Set memory protection")
        
        # ========== 系统信息命令 ==========
        self.add_command("uname", "Print system information")
        self.add_command("hostname", "Print/set hostname")
        self.add_command("uptime", "System uptime")
        self.add_command("date", "Print/set date and time")
        self.add_command("time", "Time command execution")
        self.add_command("whoami", "Print current user")
        self.add_command("id", "Print user and group IDs")
        self.add_command("dmesg", "Print kernel messages")
        self.add_command("lspci", "List PCI devices")
        self.add_command("lsusb", "List USB devices")
        self.add_command("cpuinfo", "CPU information")
        
        # ========== 网络命令 ==========
        self.add_command("ifconfig", "Network interface configuration")
        self.add_command("ip", "IP routing and devices")
        self.add_command("ping", "Test network connectivity")
        self.add_command("netstat", "Network statistics")
        self.add_command("ss", "Socket statistics")
        self.add_command("route", "Routing table")
        self.add_command("arp", "ARP table")
        self.add_command("nc", "Network cat")
        self.add_command("wget", "Download file from web")
        self.add_command("curl", "Transfer data with URL")
        self.add_command("ssh", "Secure shell client")
        self.add_command("tcpdump", "Packet capture")
        self.add_command("bn", "Bamboo Tunnel - 内网穿透服务",
                        "Usage: bn [start|stop|mode|port|nas|status|log|enable|disable|passwd|Save|Load|key|iv|allow|deny]\n"
                        "  start   - 启动穿透服务（需root密码）\n"
                        "  stop    - 停止穿透服务（需root密码）\n"
                        "  mode    - 设置工作模式(nat/lan)\n"
                        "  port    - 设置端口映射(local:remote)\n"
                        "  nas     - 设置NAS模式存储路径\n"
                        "  status  - 查看服务状态\n"
                        "  log     - 查看日志\n"
                        "  enable  - 启用服务（需root密码）\n"
                        "  disable - 禁用服务（需root密码）\n"
                        "  passwd  - 设置root密码\n"
                        "  Save    - 保存配置到文件（需root密码）\n"
                        "  Load    - 从文件加载配置（需root密码）\n"
                        "  key     - 设置加密密钥（需root密码）\n"
                        "  iv      - 设置加密初始化向量（需root密码）\n"
                        "  allow   - 添加IP到白名单（需root密码）\n"
                        "  deny    - 清空IP白名单（需root密码）")
        
        # ========== Shell内置命令 ==========
        self.add_command("help", "Display help information")
        self.add_command("history", "Command history")
        self.add_command("clear", "Clear screen")
        self.add_command("echo", "Print text")
        self.add_command("alias", "Create command alias")
        self.add_command("unalias", "Remove alias")
        self.add_command("set", "Set shell options")
        self.add_command("export", "Set environment variable")
        self.add_command("env", "List environment variables")
        self.add_command("source", "Execute script file")
        self.add_command(".", "Execute script file (alias for source)")
        self.add_command("read", "Read input from user")
        
        # ========== 文本处理命令 ==========
        self.add_command("cat", "Concatenate and print files")
        self.add_command("head", "Output first part of files")
        self.add_command("tail", "Output last part of files")
        self.add_command("sort", "Sort lines of text")
        self.add_command("uniq", "Remove duplicate lines")
        self.add_command("wc", "Word count")
        self.add_command("cut", "Remove sections from lines")
        self.add_command("paste", "Merge lines of files")
        self.add_command("join", "Join lines on common field")
        self.add_command("tr", "Translate characters")
        self.add_command("sed", "Stream editor")
        self.add_command("awk", "Pattern scanning language")
        
        # ========== 归档压缩命令 ==========
        self.add_command("tar", "Tape archive")
        self.add_command("gzip", "GNU zip compression")
        self.add_command("gunzip", "Decompress gzip files")
        self.add_command("zip", "Package and compress files")
        self.add_command("unzip", "Extract zip archives")
        self.add_command("xz", "LZMA compression")
        
        # ========== 权限和用户命令 ==========
        self.add_command("su", "Switch user")
        self.add_command("sudo", "Execute as superuser")
        self.add_command("passwd", "Change user password")
        self.add_command("useradd", "Create new user")
        self.add_command("userdel", "Delete user")
        self.add_command("groupadd", "Create new group")
        self.add_command("groupdel", "Delete group")
        
        # ========== 磁盘命令 ==========
        self.add_command("df", "Disk free space")
        self.add_command("du", "Disk usage")
        self.add_command("mount", "Mount filesystem")
        self.add_command("umount", "Unmount filesystem")
        self.add_command("fsck", "Filesystem check")
        self.add_command("mkfs", "Make filesystem")
        self.add_command("fdisk", "Partition table manipulator")
        self.add_command("parted", "Partition editor")
        
        # ========== 内核调试命令 ==========
        self.add_command("sysctl", "Configure kernel parameters")
        self.add_command("klog", "Kernel log")
        self.add_command("panic", "Trigger kernel panic (for testing)")
        self.add_command("reboot", "Reboot system")
        self.add_command("shutdown", "Shutdown system")
        self.add_command("halt", "Halt system")
        
        # ========== 其他实用命令 ==========
        self.add_command("man", "Manual pages")
        self.add_command("info", "Info documentation")
        self.add_command("which", "Locate command")
        self.add_command("whereis", "Locate binary/source/manual")
        self.add_command("file", "Determine file type")
        self.add_command("diff", "Compare files")
        self.add_command("patch", "Apply diff file")
        self.add_command("tee", "Read from stdin, write to stdout and files")
        self.add_command("yes", "Output string repeatedly")
        self.add_command("true", "Return true value")
        self.add_command("false", "Return false value")
        self.add_command("sleep", "Delay for specified time")
        self.add_command("printenv", "Print environment variables")
        self.add_command("printf", "Format and print data")
        self.add_command("test", "Evaluate expression")
        self.add_command("[", "Test expression (alias for test)")
        self.add_command("basename", "Strip directory path")
        self.add_command("dirname", "Strip last component")
        self.add_command("realpath", "Resolve canonical path")
        self.add_command("link", "Create hard link")
        self.add_command("symlink", "Create symbolic link")
        self.add_command("readlink", "Read symbolic link")
        
        return len(self.commands)


# =============================================================================
# Binary Resource Embedder - 二进制数据嵌入机制
# =============================================================================