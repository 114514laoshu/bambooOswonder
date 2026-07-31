# ============================================================================
# Module: userland/libs/libnet/http.py
# 模块：userland/libs/libnet/http.py
# Description: HTTP client for Bamboo OS
# 描述：Bamboo OS HTTP 客户端
# ============================================================================

"""
HTTP client for Bamboo OS networking.
Bamboo OS 网络 HTTP 客户端。

Provides HTTP/1.1 client implementation.
提供 HTTP/1.1 客户端实现。
"""

from typing import Dict, Optional, Any, Tuple
import urllib.parse


class HTTPRequest:
    """
    HTTP request.
    HTTP 请求。
    """

    def __init__(self, method: str = "GET", url: str = "",
                 headers: Dict[str, str] = None, body: bytes = b""):
        """
        Initialize HTTP request.
        初始化 HTTP 请求。

        Args:
            参数：
            method (str): HTTP method / HTTP 方法
            url (str): URL / URL
            headers (dict): Headers / 头部
            body (bytes): Body data / 主体数据
        """
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.body = body
        self.parsed_url = urllib.parse.urlparse(url)

    @property
    def host(self) -> str:
        """Get host from URL / 从 URL 获取主机"""
        return self.parsed_url.hostname or ""

    @property
    def port(self) -> int:
        """Get port from URL / 从 URL 获取端口"""
        return self.parsed_url.port or 80

    @property
    def path(self) -> str:
        """Get path from URL / 从 URL 获取路径"""
        path = self.parsed_url.path or "/"
        if self.parsed_url.query:
            path += "?" + self.parsed_url.query
        return path

    def to_bytes(self) -> bytes:
        """Convert request to bytes / 将请求转换为字节"""
        lines = [
            f"{self.method} {self.path} HTTP/1.1",
            f"Host: {self.host}",
        ]

        for key, value in self.headers.items():
            lines.append(f"{key}: {value}")

        if self.body:
            lines.append(f"Content-Length: {len(self.body)}")

        lines.append("")
        lines.append("")

        return "\r\n".join(lines).encode('utf-8') + self.body


class HTTPResponse:
    """
    HTTP response.
    HTTP 响应。
    """

    def __init__(self, status_code: int = 200, status_text: str = "OK",
                 headers: Dict[str, str] = None, body: bytes = b""):
        """
        Initialize HTTP response.
        初始化 HTTP 响应。

        Args:
            参数：
            status_code (int): Status code / 状态码
            status_text (str): Status text / 状态文本
            headers (dict): Headers / 头部
            body (bytes): Body data / 主体数据
        """
        self.status_code = status_code
        self.status_text = status_text
        self.headers = headers or {}
        self.body = body

    def is_success(self) -> bool:
        """Check if response is successful / 检查响应是否成功"""
        return 200 <= self.status_code < 300

    @classmethod
    def from_bytes(cls, data: bytes) -> 'HTTPResponse':
        """Parse HTTP response from bytes / 从字节解析 HTTP 响应"""
        lines = data.split(b'\r\n')
        if not lines:
            return cls(500, "Invalid Response")

        # Status line / 状态行
        status_line = lines[0].decode('utf-8')
        parts = status_line.split(' ', 2)
        if len(parts) < 3:
            return cls(500, "Invalid Status Line")

        status_code = int(parts[1])
        status_text = parts[2]

        # Headers / 头部
        headers = {}
        body_start = 0
        for i in range(1, len(lines)):
            if lines[i] == b'':
                body_start = i + 1
                break
            if b':' in lines[i]:
                key, value = lines[i].decode('utf-8').split(':', 1)
                headers[key.strip()] = value.strip()

        # Body / 主体
        body = b'\r\n'.join(lines[body_start:]) if body_start < len(lines) else b''

        return cls(status_code, status_text, headers, body)


class HTTPClient:
    """
    HTTP client.
    HTTP 客户端。
    """

    def __init__(self, timeout: int = 30):
        """
        Initialize HTTP client.
        初始化 HTTP 客户端。

        Args:
            参数：
            timeout (int): Timeout in seconds / 超时秒数
        """
        self.timeout = timeout
        self.user_agent = "BambooOS/1.0"
        self.default_headers = {
            "User-Agent": self.user_agent,
            "Accept": "*/*",
            "Connection": "close",
        }

    def request(self, req: HTTPRequest) -> HTTPResponse:
        """
        Send HTTP request.
        发送 HTTP 请求。

        Args:
            参数：
            req (HTTPRequest): HTTP request / HTTP 请求

        Returns:
            返回：
            HTTPResponse: HTTP response / HTTP 响应
        """
        # Merge headers / 合并头部
        headers = self.default_headers.copy()
        headers.update(req.headers)
        req.headers = headers

        # In real implementation, use socket / 实际实现中使用套接字
        # For now, return dummy response / 现在，返回虚拟响应
        body = f"Hello from Bamboo OS!\nRequest: {req.method} {req.url}\n"
        return HTTPResponse(200, "OK", {
            "Content-Type": "text/plain",
            "Content-Length": str(len(body)),
            "Server": "BambooOS/1.0",
        }, body.encode('utf-8'))

    def get(self, url: str, headers: Dict[str, str] = None) -> HTTPResponse:
        """
        Send GET request.
        发送 GET 请求。

        Args:
            参数：
            url (str): URL / URL
            headers (dict): Additional headers / 额外头部

        Returns:
            返回：
            HTTPResponse: HTTP response / HTTP 响应
        """
        req = HTTPRequest("GET", url, headers)
        return self.request(req)

    def post(self, url: str, data: bytes = b"",
             headers: Dict[str, str] = None) -> HTTPResponse:
        """
        Send POST request.
        发送 POST 请求。

        Args:
            参数：
            url (str): URL / URL
            data (bytes): Post data / POST 数据
            headers (dict): Additional headers / 额外头部

        Returns:
            返回：
            HTTPResponse: HTTP response / HTTP 响应
        """
        req = HTTPRequest("POST", url, headers, data)
        return self.request(req)

    def head(self, url: str, headers: Dict[str, str] = None) -> HTTPResponse:
        """
        Send HEAD request.
        发送 HEAD 请求。

        Args:
            参数：
            url (str): URL / URL
            headers (dict): Additional headers / 额外头部

        Returns:
            返回：
            HTTPResponse: HTTP response / HTTP 响应
        """
        req = HTTPRequest("HEAD", url, headers)
        return self.request(req)