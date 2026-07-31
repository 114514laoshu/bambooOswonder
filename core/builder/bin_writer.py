# ============================================================================
# Module: core/builder/bin_writer.py
# Description: Binary writer for building kernel binary
# 描述：内核二进制文件写入器
# ============================================================================

import struct


class BinWriter:
    """Writes assembled code into binary format."""

    def __init__(self):
        self.data = bytearray()

    def write_byte(self, value):
        self.data.append(value & 0xFF)

    def write_word(self, value):
        self.data.extend(struct.pack('<H', value & 0xFFFF))

    def write_dword(self, value):
        self.data.extend(struct.pack('<I', value & 0xFFFFFFFF))

    def write_qword(self, value):
        self.data.extend(struct.pack('<Q', value & 0xFFFFFFFFFFFFFFFF))

    def write_bytes(self, data):
        self.data.extend(data)

    def write_to_file(self, path):
        with open(path, 'wb') as f:
            f.write(self.data)
        return len(self.data)

    def reset(self):
        self.data = bytearray()
