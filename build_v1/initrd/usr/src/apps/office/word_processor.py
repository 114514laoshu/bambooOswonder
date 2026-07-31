# ============================================================================
# Module: userland/office/word_processor.py
# 模块：userland/office/word_processor.py
# Description: Word processor application
# 描述：文字处理器应用
# ============================================================================

"""
Word processor for Bamboo OS.
Bamboo OS 文字处理器。

Provides document editing with formatting, tables, and images.
提供带格式、表格和图像的文档编辑。
"""

from typing import List, Dict, Optional, Any, Tuple
import json


class WordDocument:
    """
    Word document model.
    文字文档模型。
    """

    def __init__(self):
        """Initialize document / 初始化文档"""
        self.title = "Untitled"
        self.author = "User"
        self.created = 0
        self.modified = 0
        self.pages: List[WordPage] = []
        self.metadata: Dict[str, Any] = {}

    def add_page(self, page: 'WordPage'):
        """Add a page / 添加一页"""
        self.pages.append(page)

    def get_text(self) -> str:
        """Get document text / 获取文档文本"""
        return '\n'.join(p.get_text() for p in self.pages)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary / 转换为字典"""
        return {
            'title': self.title,
            'author': self.author,
            'created': self.created,
            'modified': self.modified,
            'pages': [p.to_dict() for p in self.pages],
            'metadata': self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WordDocument':
        """Create from dictionary / 从字典创建"""
        doc = cls()
        doc.title = data.get('title', 'Untitled')
        doc.author = data.get('author', 'User')
        doc.created = data.get('created', 0)
        doc.modified = data.get('modified', 0)
        doc.pages = [WordPage.from_dict(p) for p in data.get('pages', [])]
        doc.metadata = data.get('metadata', {})
        return doc


class WordPage:
    """
    Document page.
    文档页。
    """

    def __init__(self, number: int = 1):
        """
        Initialize page.
        初始化页。

        Args:
            参数：
            number (int): Page number / 页码
        """
        self.number = number
        self.paragraphs: List[WordParagraph] = []

    def add_paragraph(self, paragraph: 'WordParagraph'):
        """Add a paragraph / 添加一个段落"""
        self.paragraphs.append(paragraph)

    def get_text(self) -> str:
        """Get page text / 获取页文本"""
        return '\n'.join(p.get_text() for p in self.paragraphs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary / 转换为字典"""
        return {
            'number': self.number,
            'paragraphs': [p.to_dict() for p in self.paragraphs],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WordPage':
        """Create from dictionary / 从字典创建"""
        page = cls(data.get('number', 1))
        page.paragraphs = [WordParagraph.from_dict(p) for p in data.get('paragraphs', [])]
        return page


class WordParagraph:
    """
    Document paragraph.
    文档段落。
    """

    def __init__(self, text: str = "", style: str = "normal"):
        """
        Initialize paragraph.
        初始化段落。

        Args:
            参数：
            text (str): Paragraph text / 段落文本
            style (str): Paragraph style / 段落样式
        """
        self.text = text
        self.style = style
        self.runs: List[WordRun] = []
        self.alignment = 'left'
        self.indent = 0.0
        self.spacing = 0.0

    def add_run(self, run: 'WordRun'):
        """Add a run / 添加一个运行"""
        self.runs.append(run)

    def get_text(self) -> str:
        """Get paragraph text / 获取段落文本"""
        return ''.join(r.text for r in self.runs) or self.text

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary / 转换为字典"""
        return {
            'text': self.text,
            'style': self.style,
            'runs': [r.to_dict() for r in self.runs],
            'alignment': self.alignment,
            'indent': self.indent,
            'spacing': self.spacing,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WordParagraph':
        """Create from dictionary / 从字典创建"""
        para = cls(data.get('text', ''), data.get('style', 'normal'))
        para.runs = [WordRun.from_dict(r) for r in data.get('runs', [])]
        para.alignment = data.get('alignment', 'left')
        para.indent = data.get('indent', 0.0)
        para.spacing = data.get('spacing', 0.0)
        return para


class WordRun:
    """
    Text run with formatting.
    带格式的文本运行。
    """

    def __init__(self, text: str = ""):
        """
        Initialize text run.
        初始化文本运行。

        Args:
            参数：
            text (str): Run text / 运行文本
        """
        self.text = text
        self.bold = False
        self.italic = False
        self.underline = False
        self.strikethrough = False
        self.font_size = 12
        self.font_name = "Arial"
        self.color = 0x000000

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary / 转换为字典"""
        return {
            'text': self.text,
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline,
            'strikethrough': self.strikethrough,
            'font_size': self.font_size,
            'font_name': self.font_name,
            'color': self.color,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WordRun':
        """Create from dictionary / 从字典创建"""
        run = cls(data.get('text', ''))
        run.bold = data.get('bold', False)
        run.italic = data.get('italic', False)
        run.underline = data.get('underline', False)
        run.strikethrough = data.get('strikethrough', False)
        run.font_size = data.get('font_size', 12)
        run.font_name = data.get('font_name', 'Arial')
        run.color = data.get('color', 0x000000)
        return run


class WordProcessor:
    """
    Word processor application.
    文字处理器应用。
    """

    def __init__(self):
        """Initialize word processor / 初始化文字处理器"""
        self.document = WordDocument()
        self.current_page = 0
        self.current_paragraph = 0
        self.current_run = 0
        self.cursor_position = 0
        self.selection_start = None
        self.selection_end = None
        self.zoom = 1.0

    def new_document(self):
        """Create a new document / 创建新文档"""
        self.document = WordDocument()
        page = WordPage(1)
        para = WordParagraph("", "normal")
        page.add_paragraph(para)
        self.document.add_page(page)
        self.current_page = 0
        self.current_paragraph = 0
        self.current_run = 0
        self.cursor_position = 0

    def open_document(self, filepath: str) -> bool:
        """
        Open a document from file.
        从文件打开文档。

        Args:
            参数：
            filepath (str): File path / 文件路径

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.document = WordDocument.from_dict(data)
            return True
        except Exception as e:
            print(f"Error opening document: {e}")
            return False

    def save_document(self, filepath: str) -> bool:
        """
        Save document to file.
        保存文档到文件。

        Args:
            参数：
            filepath (str): File path / 文件路径

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        try:
            self.document.modified = int(time.time())
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.document.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving document: {e}")
            return False

    def insert_text(self, text: str):
        """Insert text at cursor / 在光标处插入文本"""
        page = self.document.pages[self.current_page]
        para = page.paragraphs[self.current_paragraph]

        if self.current_run < len(para.runs):
            run = para.runs[self.current_run]
            run.text = run.text[:self.cursor_position] + text + run.text[self.cursor_position:]
            self.cursor_position += len(text)
        else:
            run = WordRun(text)
            para.add_run(run)
            self.current_run = len(para.runs) - 1
            self.cursor_position = len(text)

    def get_current_text(self) -> str:
        """Get text at cursor / 获取光标处的文本"""
        page = self.document.pages[self.current_page]
        para = page.paragraphs[self.current_paragraph]
        return para.get_text()

    def render(self, renderer, x: int, y: int, width: int, height: int):
        """Render document / 渲染文档"""
        # In real implementation, render with formatting / 实际实现中带格式渲染
        page = self.document.pages[self.current_page] if self.document.pages else None
        if not page:
            return

        line_y = y + 20
        for para in page.paragraphs:
            text = para.get_text()
            if text:
                renderer.draw_text(x + 20, line_y, text, 0x000000)
            line_y += 30


def main():
    """Main entry point / 主入口"""
    wp = WordProcessor()
    wp.new_document()
    wp.insert_text("Hello from Bamboo OS Word Processor!")
    print(wp.get_current_text())
    print("Word Processor started!")


if __name__ == '__main__':
    main()