# ============================================================================
# Module: toolchain/bambootoolchain.py
# 模块：toolchain/bambootoolchain.py
# Description: BambooToolchain toolchain component
# 描述：BambooToolchain 工具链组件
# ============================================================================

# Fix: Add imports for all toolchain components / 修复：添加所有工具链组件的导入
from toolchain.bamboocc import BambooCC
from toolchain.bambooas import BambooAS
from toolchain.bamboold import BambooLD
from toolchain.bamboodb import BambooDB
from toolchain.bamboolibc import BambooLibc


class BambooToolchain:
    """
    Bamboo Toolchain integration.
    Bamboo 工具链集成。

    This class integrates all Bamboo toolchain components:
    - BambooCC: C compiler / C 编译器
    - BambooAS: Assembler / 汇编器
    - BambooLD: Linker / 链接器
    - BambooDB: Debugger / 调试器
    - BambooLibc: C standard library / C 标准库
    """

    def __init__(self):
        """Initialize toolchain components / 初始化工具链组件"""
        self.cc = BambooCC()
        self.as_ = BambooAS()
        self.ld = BambooLD()
        self.db = BambooDB()
        self.libc = BambooLibc()
        self.verbose = False
        self.optimization_level = 0
        self.include_paths = []
        self.library_paths = []

    def set_verbose(self, verbose=True):
        """Set verbose mode / 设置详细模式"""
        self.verbose = verbose
        return self

    def set_optimization(self, level=0):
        """Set optimization level (0-3) / 设置优化级别"""
        self.optimization_level = min(max(level, 0), 3)
        return self

    def add_include_path(self, path):
        """Add include path / 添加包含路径"""
        self.include_paths.append(path)
        return self

    def add_library_path(self, path):
        """Add library path / 添加库路径"""
        self.library_paths.append(path)
        return self

    # 6.1 统一驱动程序
    def compile(self, c_source, output_file=None, compile_only=False):
        """
        Unified compile driver.
        统一编译驱动。

        Args:
            参数：
            c_source (str): C source code / C 源代码
            output_file (str): Output file path / 输出文件路径
            compile_only (bool): Compile only (no link) / 仅编译（不链接）

        Returns:
            返回：
            bytes: Compiled output / 编译输出
        """
        if self.verbose:
            print(f"[BambooToolchain] Compiling {len(c_source)} bytes of C code")

        # Lexical analysis / 词法分析
        tokens = self.cc.lexer(c_source)
        if self.verbose:
            print(f"[BambooToolchain] Lexer: {len(tokens)} tokens")

        # Parse / 解析
        ast = self.cc.parser()
        if self.verbose:
            print(f"[BambooToolchain] Parser: {len(ast)} AST nodes")

        # Semantic analysis / 语义分析
        symbols, errors = self.cc.semantic_analyze(ast)
        if errors:
            if self.verbose:
                print(f"[BambooToolchain] Semantic errors: {len(errors)}")
            return None

        # Generate IR / 生成 IR
        ir = self.cc.generate_ir(ast)
        if self.verbose:
            print(f"[BambooToolchain] IR: {len(ir)} instructions")

        # Generate assembly / 生成汇编
        asm = self.cc.generate_code(ir)
        if self.verbose:
            print(f"[BambooToolchain] Assembly: {len(asm)} lines")

        # Assemble / 汇编
        self.as_.parse_assembly(asm)
        obj = self.as_.generate_elf_object()

        if self.verbose:
            print(f"[BambooToolchain] Object size: {len(obj)} bytes")

        if compile_only:
            return obj

        # Link / 链接
        if output_file:
            self.ld.object_files.append(self.as_)
            self.ld.resolve_symbols()
            self.ld.merge_sections()
            executable = self.ld.generate_executable()
            with open(output_file, 'wb') as f:
                f.write(executable)
            if self.verbose:
                print(f"[BambooToolchain] Linked: {output_file} ({len(executable)} bytes)")
            return executable

        return obj

    # 6.2 Makefile构建规则
    def makefile_rules(self):
        """Generate Makefile build rules / 生成 Makefile 构建规则"""
        return """
# Bamboo Toolchain Makefile Rules
# Bamboo 工具链 Makefile 规则

%.o: %.c
\tbamboo-cc -c $< -o $@

%.elf: %.o
\tbamboo-ld $< -o $@

%.bpp: %.elf
\tbamboo-pack create $@ $<

clean:
\trm -f *.o *.elf *.bpp
"""

    # 6.3 内核编译集成
    def compile_kernel(self, kernel_source):
        """Kernel compilation integration / 内核编译集成"""
        return self.compile(kernel_source)

    # 6.4 用户程序编译支持
    def compile_user_program(self, source):
        """User program compilation support / 用户程序编译支持"""
        return self.compile(source)

    # 6.5 自举测试
    def bootstrap_test(self):
        """Toolchain bootstrap test / 工具链自举测试"""
        test_code = "int main() { return 42; }"
        result = self.compile(test_code)
        return result is not None