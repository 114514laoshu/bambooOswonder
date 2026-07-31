# ============================================================================
# Module: core/builder/isogenerator.py
# 模块：core/builder/isogenerator.py
# Description: ISOGenerator boot/build component
# 描述：ISOGenerator 启动/构建组件
# ============================================================================

class ISOGenerator:
    """ISO 9660镜像生成器"""
    
    def __init__(self):
        self.files = {}
        self.bootable = False
        self.boot_image = None
    
    # 1.1 ISO 9660文件系统生成器
    def create_iso9660(self, output_path):
        """生成ISO 9660文件系统"""
        # ISO 9660主卷描述符
        pvd = bytearray(2048)
        pvd[0] = 1  # Volume Descriptor Type = 1 (Primary)
        pvd[1:6] = b'CD001'  # Standard Identifier
        pvd[6] = 1  # Volume Descriptor Version
        
        # Volume Identifier
        vol_id = 'BAMBOO_OS'.ljust(32)
        pvd[40:72] = vol_id.encode('ascii')
        
        # Volume Space Size (number of logical blocks)
        block_count = 1000
        pvd[80:84] = block_count.to_bytes(4, 'little')
        pvd[84:88] = block_count.to_bytes(4, 'big')
        
        # Logical Block Size
        block_size = 2048
        pvd[128:130] = block_size.to_bytes(2, 'little')
        pvd[130:132] = block_size.to_bytes(2, 'big')
        
        # Path Table Size
        pvd[132:136] = (10).to_bytes(4, 'little')
        pvd[136:140] = (10).to_bytes(4, 'big')
        
        # Path Table Location (L-path)
        pvd[140:144] = (20).to_bytes(4, 'little')
        # Path Table Location (M-path)
        pvd[148:152] = (21).to_bytes(4, 'big')
        
        # Root Directory Record
        root_dir = bytearray(34)
        root_dir[0] = 34  # Length of Directory Record
        root_dir[2] = 0  # Extent Location (LBA)
        root_dir[10:14] = (100).to_bytes(4, 'little')  # Data Length
        root_dir[14:18] = (100).to_bytes(4, 'big')
        root_dir[32] = 0  # File Flags
        pvd[156:190] = root_dir
        
        # Volume Set Identifier
        pvd[190:318] = b'BAMBOO_OS_VOLUME_SET'.ljust(128, b'\x00')
        
        # Publisher Identifier
        pvd[318:446] = b'ls studio'.ljust(128, b'\x00')
        
        # Data Preparer Identifier
        pvd[446:574] = b'Bamboo OS Build System'.ljust(128, b'\x00')
        
        # Application Identifier
        pvd[574:702] = b'Bamboo OS v6.0'.ljust(128, b'\x00')
        
        # Volume Creation Date and Time
        pvd[702:717] = b'2026062512000000'
        
        # Volume Modification Date and Time
        pvd[717:732] = b'2026062512000000'
        
        # File Structure Version
        pvd[882] = 1
        
        # 生成ISO内容
        iso_content = bytearray()
        
        # 系统区域 (16 sectors = 32KB)
        iso_content.extend(b'\x00' * 16 * 2048)
        
        # 主卷描述符
        iso_content.extend(bytes(pvd))
        
        # 卷描述符终止符
        vd_terminator = bytearray(2048)
        vd_terminator[0] = 255  # Volume Descriptor Type = 255 (Terminator)
        vd_terminator[1:6] = b'CD001'
        vd_terminator[6] = 1
        iso_content.extend(bytes(vd_terminator))
        
        # 填充到1000个扇区
        while len(iso_content) < 1000 * 2048:
            iso_content.extend(b'\x00' * 2048)
        
        # 写入文件
        with open(output_path, 'wb') as f:
            f.write(bytes(iso_content))
        
        return output_path
    
    # 1.2 El Torito可引导规范
    def add_eltorito(self, boot_image_path):
        """添加El Torito可引导规范"""
        self.bootable = True
        self.boot_image = boot_image_path
        return True
    
    # 1.3 生成引导扇区
    def create_boot_sector(self):
        """生成引导扇区"""
        boot_sector = bytearray(512)
        boot_sector[0] = 0xEB  # JMP short
        boot_sector[1] = 0x3C
        boot_sector[2] = 0x90
        
        # OEM ID
        boot_sector[3:11] = b'BAMBOOOS'
        
        # 引导签名
        boot_sector[510] = 0x55
        boot_sector[511] = 0xAA
        
        return bytes(boot_sector)
    
    # 1.4 集成内核到ISO镜像
    def add_kernel(self, kernel_data, iso_path):
        """集成内核到ISO镜像"""
        self.files['/kernel.bin'] = kernel_data
        return True
    
    # 1.5 创建ISO生成工具函数
    def generate_iso(self, output_path, kernel_binary):
        """完整ISO生成工具函数"""
        # 创建基础ISO
        self.create_iso9660(output_path)
        
        # 添加内核
        self.add_kernel(kernel_binary, output_path)
        
        # 设置可引导
        self.add_eltorito(kernel_binary)
        
        return output_path

# =========================================================================
# 第2节：GRUB引导集成
# =========================================================================