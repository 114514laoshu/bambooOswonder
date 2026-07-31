# ============================================================================
# Module: userland/office/spreadsheet.py
# 模块：userland/office/spreadsheet.py
# Description: Spreadsheet application
# 描述：电子表格应用
# ============================================================================

"""
Spreadsheet application for Bamboo OS.
Bamboo OS 电子表格应用。

Provides spreadsheet with formulas, charts, and cell formatting.
提供带公式、图表和单元格格式的电子表格。
"""

from typing import Dict, List, Any, Optional, Tuple
import math
import re


class Cell:
    """
    Spreadsheet cell.
    电子表格单元格。
    """

    def __init__(self, value: Any = None):
        """
        Initialize cell.
        初始化单元格。

        Args:
            参数：
            value: Cell value / 单元格值
        """
        self.value = value
        self.formula = None
        self.format = 'general'
        self.bg_color = 0xFFFFFF
        self.fg_color = 0x000000
        self.bold = False
        self.italic = False
        self.alignment = 'left'
        self.width = 80
        self.height = 20

    def is_number(self) -> bool:
        """Check if cell contains a number / 检查单元格是否包含数字"""
        return isinstance(self.value, (int, float))

    def is_text(self) -> bool:
        """Check if cell contains text / 检查单元格是否包含文本"""
        return isinstance(self.value, str)

    def get_display_value(self) -> str:
        """Get display value / 获取显示值"""
        if self.value is None:
            return ""
        if self.is_number():
            if self.format == 'percent':
                return f"{self.value * 100:.1f}%"
            elif self.format == 'currency':
                return f"${self.value:.2f}"
            elif self.format == 'scientific':
                return f"{self.value:.2e}"
            return str(self.value)
        return str(self.value)


class Spreadsheet:
    """
    Spreadsheet application.
    电子表格应用。
    """

    def __init__(self, rows: int = 100, cols: int = 26):
        """
        Initialize spreadsheet.
        初始化电子表格。

        Args:
            参数：
            rows (int): Number of rows / 行数
            cols (int): Number of columns / 列数
        """
        self.rows = rows
        self.cols = cols
        self.cells: Dict[str, Cell] = {}
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.selection_range: Optional[Tuple[int, int, int, int]] = None
        self.name = "Untitled"

    def get_cell_key(self, row: int, col: int) -> str:
        """Get cell key / 获取单元格键"""
        return f"{chr(65 + col)}{row + 1}"

    def get_cell(self, row: int, col: int) -> Cell:
        """Get cell / 获取单元格"""
        key = self.get_cell_key(row, col)
        if key not in self.cells:
            self.cells[key] = Cell()
        return self.cells[key]

    def set_cell(self, row: int, col: int, value: Any):
        """Set cell value / 设置单元格值"""
        cell = self.get_cell(row, col)
        cell.value = value

        # Check if it's a formula / 检查是否为公式
        if isinstance(value, str) and value.startswith('='):
            self._evaluate_formula(row, col, value)

    def _evaluate_formula(self, row: int, col: int, formula: str):
        """
        Evaluate a formula.
        求值一个公式。

        Args:
            参数：
            row (int): Row index / 行索引
            col (int): Column index / 列索引
            formula (str): Formula string / 公式字符串
        """
        # Remove '=' prefix / 移除 '=' 前缀
        expr = formula[1:].upper()

        # Simple functions / 简单函数
        if expr.startswith('SUM('):
            # Parse range / 解析范围
            range_str = expr[4:-1]
            total = 0.0
            for r, c in self._parse_range(range_str):
                val = self.get_cell(r, c).value
                if isinstance(val, (int, float)):
                    total += val
            self.get_cell(row, col).value = total
            self.get_cell(row, col).formula = formula
            return

        if expr.startswith('AVG('):
            range_str = expr[4:-1]
            total = 0.0
            count = 0
            for r, c in self._parse_range(range_str):
                val = self.get_cell(r, c).value
                if isinstance(val, (int, float)):
                    total += val
                    count += 1
            self.get_cell(row, col).value = total / count if count > 0 else 0
            self.get_cell(row, col).formula = formula
            return

        if expr.startswith('MAX('):
            range_str = expr[4:-1]
            max_val = None
            for r, c in self._parse_range(range_str):
                val = self.get_cell(r, c).value
                if isinstance(val, (int, float)):
                    if max_val is None or val > max_val:
                        max_val = val
            self.get_cell(row, col).value = max_val if max_val is not None else 0
            self.get_cell(row, col).formula = formula
            return

        if expr.startswith('MIN('):
            range_str = expr[4:-1]
            min_val = None
            for r, c in self._parse_range(range_str):
                val = self.get_cell(r, c).value
                if isinstance(val, (int, float)):
                    if min_val is None or val < min_val:
                        min_val = val
            self.get_cell(row, col).value = min_val if min_val is not None else 0
            self.get_cell(row, col).formula = formula
            return

        # Simple arithmetic / 简单算术
        try:
            # Replace cell references / 替换单元格引用
            def replace_cell(match):
                col_str = match.group(1)
                row_str = match.group(2)
                c = ord(col_str) - 65
                r = int(row_str) - 1
                val = self.get_cell(r, c).value
                return str(val) if val is not None else "0"

            pattern = r'([A-Z])(\d+)'
            expr = re.sub(pattern, replace_cell, expr)

            # Evaluate expression safely / 安全求值表达式
            allowed_names = {
                'abs': abs, 'max': max, 'min': min, 'sum': sum,
                'round': round, 'floor': math.floor, 'ceil': math.ceil,
                'sqrt': math.sqrt, 'pow': pow, 'pi': math.pi
            }
            result = eval(expr, {"__builtins__": {}}, allowed_names)
            self.get_cell(row, col).value = result
            self.get_cell(row, col).formula = formula
        except Exception:
            self.get_cell(row, col).value = "#ERROR"
            self.get_cell(row, col).formula = formula

    def _parse_range(self, range_str: str) -> List[Tuple[int, int]]:
        """
        Parse a cell range string.
        解析单元格范围字符串。

        Args:
            参数：
            range_str (str): Range string / 范围字符串

        Returns:
            返回：
            list: List of (row, col) tuples / (行, 列) 元组列表
        """
        if ':' in range_str:
            start, end = range_str.split(':')
            c1 = ord(start[0]) - 65
            r1 = int(start[1:]) - 1
            c2 = ord(end[0]) - 65
            r2 = int(end[1:]) - 1

            cells = []
            for r in range(min(r1, r2), max(r1, r2) + 1):
                for c in range(min(c1, c2), max(c1, c2) + 1):
                    cells.append((r, c))
            return cells
        else:
            # Single cell / 单个单元格
            c = ord(range_str[0]) - 65
            r = int(range_str[1:]) - 1
            return [(r, c)]

    def get_value(self, row: int, col: int) -> Any:
        """Get cell value / 获取单元格值"""
        return self.get_cell(row, col).value

    def render(self, renderer, x: int, y: int, width: int, height: int):
        """Render spreadsheet / 渲染电子表格"""
        # In real implementation, render grid and cells / 实际实现中渲染网格和单元格
        row_height = 20
        col_width = 80

        # Draw grid / 绘制网格
        for c in range(min(10, self.cols)):
            cx = x + c * col_width
            renderer.draw_line(cx, y, cx, y + 10 * row_height, 0x888888)

        for r in range(min(10, self.rows)):
            cy = y + r * row_height
            renderer.draw_line(x, cy, x + 10 * col_width, cy, 0x888888)

        # Draw cells / 绘制单元格
        for r in range(min(10, self.rows)):
            for c in range(min(10, self.cols)):
                cell = self.get_cell(r, c)
                cx = x + c * col_width + 4
                cy = y + r * row_height + 2
                renderer.draw_text(cx, cy, str(cell.get_display_value())[:15], 0x000000)


def main():
    """Main entry point / 主入口"""
    ss = Spreadsheet()
    ss.set_cell(0, 0, 10)
    ss.set_cell(0, 1, 20)
    ss.set_cell(0, 2, "=SUM(A1:B1)")
    print(f"A1: {ss.get_value(0, 0)}")
    print(f"B1: {ss.get_value(0, 1)}")
    print(f"C1: {ss.get_value(0, 2)}")
    print("Spreadsheet started!")


if __name__ == '__main__':
    main()