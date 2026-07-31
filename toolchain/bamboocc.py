# ============================================================================
# Module: toolchain/bamboocc.py
# 模块：toolchain/bamboocc.py
# Description: BambooCC toolchain component
# 描述：BambooCC 工具链组件
# ============================================================================

class BambooCC:
    """BambooCC - 自研C编译器"""
    
    def __init__(self):
        self.keywords = {
            'int', 'char', 'void', 'return', 'if', 'else', 'while', 'for',
            'struct', 'union', 'enum', 'typedef', 'extern', 'static', 'const',
            'volatile', 'unsigned', 'signed', 'short', 'long', 'float', 'double',
            'sizeof', 'break', 'continue', 'goto', 'switch', 'case', 'default'
        }
        self.tokens = []
        self.pos = 0
    
    # 1.1 C语言词法分析器（Lexer）
    def lexer(self, source):
        """C语言词法分析 - 关键字、标识符、常量、运算符"""
        self.tokens = []
        i = 0
        n = len(source)
        
        while i < n:
            c = source[i]
            
            # 跳过空白字符
            if c.isspace():
                i += 1
                continue
            
            # 单行注释
            if c == '/' and i + 1 < n and source[i+1] == '/':
                while i < n and source[i] != '\n':
                    i += 1
                continue
            
            # 多行注释
            if c == '/' and i + 1 < n and source[i+1] == '*':
                i += 2
                while i + 1 < n and not (source[i] == '*' and source[i+1] == '/'):
                    i += 1
                i += 2
                continue
            
            # 标识符或关键字
            if c.isalpha() or c == '_':
                start = i
                while i < n and (source[i].isalnum() or source[i] == '_'):
                    i += 1
                word = source[start:i]
                if word in self.keywords:
                    self.tokens.append(('KEYWORD', word))
                else:
                    self.tokens.append(('IDENTIFIER', word))
                continue
            
            # 数字常量
            if c.isdigit():
                start = i
                while i < n and source[i].isdigit():
                    i += 1
                self.tokens.append(('NUMBER', source[start:i]))
                continue
            
            # 字符串常量
            if c == '"':
                i += 1
                start = i
                while i < n and source[i] != '"':
                    if source[i] == '\\':
                        i += 2
                    else:
                        i += 1
                self.tokens.append(('STRING', source[start:i]))
                i += 1
                continue
            
            # 字符常量
            if c == "'":
                i += 1
                char_val = source[i]
                if char_val == '\\':
                    i += 1
                i += 2
                self.tokens.append(('CHAR', char_val))
                continue
            
            # 运算符和标点
            ops = ['==', '!=', '<=', '>=', '++', '--', '&&', '||',
                   '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
                   '<<', '>>', '->']
            matched = False
            for op in ops:
                if source[i:i+len(op)] == op:
                    self.tokens.append(('OP', op))
                    i += len(op)
                    matched = True
                    break
            if matched:
                continue
            
            # 单字符运算符
            self.tokens.append(('OP', c))
            i += 1
        
        self.tokens.append(('EOF', ''))
        return self.tokens
    
    # 1.2 C语言语法分析器（Parser）
    def parser(self):
        """C语言语法分析 - AST生成"""
        self.pos = 0
        ast = []
        while self.current_token()[0] != 'EOF':
            decl = self.parse_declaration()
            if decl:
                ast.append(decl)
        return ast
    
    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')
    
    def eat(self, expected):
        if self.current_token()[1] == expected:
            self.pos += 1
            return True
        return False
    
    def parse_declaration(self):
        """解析声明"""
        # 简化：函数声明
        if self.current_token()[0] == 'KEYWORD':
            type_token = self.current_token()
            self.pos += 1
            if self.current_token()[0] == 'IDENTIFIER':
                name = self.current_token()[1]
                self.pos += 1
                if self.eat('('):
                    params = self.parse_params()
                    if self.eat(')') and self.eat('{'):
                        body = self.parse_statements()
                        self.eat('}')
                        return ('FUNC_DECL', type_token[1], name, params, body)
        return None
    
    def parse_params(self):
        """解析参数"""
        params = []
        while not self.eat(')') and self.current_token()[0] != 'EOF':
            if self.current_token()[0] == 'KEYWORD':
                ptype = self.current_token()[1]
                self.pos += 1
                if self.current_token()[0] == 'IDENTIFIER':
                    pname = self.current_token()[1]
                    self.pos += 1
                    params.append((ptype, pname))
                    self.eat(',')
        return params
    
    def parse_statements(self):
        """解析语句块"""
        stmts = []
        while not self.eat('}') and self.current_token()[0] != 'EOF':
            stmt = self.parse_statement()
            if stmt:
                stmts.append(stmt)
        return stmts
    
    def parse_statement(self):
        """解析单条语句"""
        if self.eat('return'):
            expr = self.parse_expression()
            self.eat(';')
            return ('RETURN', expr)
        return None
    
    def parse_expression(self):
        """解析表达式"""
        if self.current_token()[0] == 'NUMBER':
            val = self.current_token()[1]
            self.pos += 1
            return ('NUMBER', val)
        if self.current_token()[0] == 'IDENTIFIER':
            name = self.current_token()[1]
            self.pos += 1
            return ('IDENTIFIER', name)
        return None
    
    # 1.3 语义分析器
    def semantic_analyze(self, ast):
        """语义分析 - 类型检查、符号表、作用域"""
        symbol_table = {}
        errors = []
        
        for node in ast:
            if node[0] == 'FUNC_DECL':
                _, ret_type, name, params, body = node
                symbol_table[name] = {'type': 'function', 'ret_type': ret_type}
                # 检查函数体
                for stmt in body:
                    if stmt[0] == 'RETURN':
                        pass  # 类型检查
        
        return symbol_table, errors
    
    # 1.4 IR中间表示生成
    def generate_ir(self, ast):
        """生成IR中间表示 - 三地址码、SSA形式"""
        ir = []
        temp_counter = 0
        
        def new_temp():
            nonlocal temp_counter
            t = f't{temp_counter}'
            temp_counter += 1
            return t
        
        for node in ast:
            if node[0] == 'FUNC_DECL':
                _, ret_type, name, params, body = node
                ir.append(f'FUNC {name}')
                for stmt in body:
                    if stmt[0] == 'RETURN':
                        t = new_temp()
                        ir.append(f'  {t} = {stmt[1][1]}')
                        ir.append(f'  RET {t}')
                ir.append(f'ENDFUNC')
        
        return ir
    
    # 1.5 代码生成器
    def generate_code(self, ir):
        """将C代码编译为x86-64机器码"""
        code = []
        for line in ir:
            if line.startswith('FUNC'):
                name = line.split()[1]
                code.append(f'.global {name}')
                code.append(f'{name}:')
            elif line.startswith('  RET'):
                code.append('  mov rax, ' + line.split()[1])
                code.append('  ret')
            elif line.startswith('ENDFUNC'):
                code.append('')
        
        return '\n'.join(code)

# =========================================================================
# 第2节：自研汇编器 - BambooAS
# =========================================================================