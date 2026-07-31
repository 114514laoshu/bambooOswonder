# ============================================================================
# Module: userland/graphics/3d_accelerator.py
# 模块：userland/graphics/3d_accelerator.py
# Description: 3D graphics accelerator
# 描述：3D 图形加速器
# ============================================================================

"""
3D graphics accelerator for Bamboo OS.
Bamboo OS 3D 图形加速器。

Provides software-based 3D rendering with OpenGL-compatible API.
提供基于软件的 3D 渲染，带 OpenGL 兼容 API。
"""

import math
from typing import List, Tuple, Optional, Dict, Any


class Vector3:
    """3D vector / 3D 向量"""

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other: 'Vector3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3') -> 'Vector3':
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self) -> 'Vector3':
        l = self.length()
        if l == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / l, self.y / l, self.z / l)


class Matrix4x4:
    """4x4 transformation matrix / 4x4 变换矩阵"""

    def __init__(self):
        self.m = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    def multiply(self, other: 'Matrix4x4') -> 'Matrix4x4':
        result = Matrix4x4()
        for i in range(4):
            for j in range(4):
                result.m[i][j] = sum(self.m[i][k] * other.m[k][j] for k in range(4))
        return result

    def transform(self, v: Vector3) -> Vector3:
        return Vector3(
            v.x * self.m[0][0] + v.y * self.m[0][1] + v.z * self.m[0][2] + self.m[0][3],
            v.x * self.m[1][0] + v.y * self.m[1][1] + v.z * self.m[1][2] + self.m[1][3],
            v.x * self.m[2][0] + v.y * self.m[2][1] + v.z * self.m[2][2] + self.m[2][3]
        )

    @staticmethod
    def translation(x: float, y: float, z: float) -> 'Matrix4x4':
        m = Matrix4x4()
        m.m[0][3] = x
        m.m[1][3] = y
        m.m[2][3] = z
        return m

    @staticmethod
    def rotation_x(angle: float) -> 'Matrix4x4':
        c = math.cos(angle)
        s = math.sin(angle)
        m = Matrix4x4()
        m.m[1][1] = c
        m.m[1][2] = -s
        m.m[2][1] = s
        m.m[2][2] = c
        return m

    @staticmethod
    def rotation_y(angle: float) -> 'Matrix4x4':
        c = math.cos(angle)
        s = math.sin(angle)
        m = Matrix4x4()
        m.m[0][0] = c
        m.m[0][2] = s
        m.m[2][0] = -s
        m.m[2][2] = c
        return m

    @staticmethod
    def rotation_z(angle: float) -> 'Matrix4x4':
        c = math.cos(angle)
        s = math.sin(angle)
        m = Matrix4x4()
        m.m[0][0] = c
        m.m[0][1] = -s
        m.m[1][0] = s
        m.m[1][1] = c
        return m

    @staticmethod
    def scale(x: float, y: float, z: float) -> 'Matrix4x4':
        m = Matrix4x4()
        m.m[0][0] = x
        m.m[1][1] = y
        m.m[2][2] = z
        return m


class Triangle3D:
    """3D triangle / 3D 三角形"""

    def __init__(self, v1: Vector3, v2: Vector3, v3: Vector3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.color = (255, 255, 255)
        self.normal: Optional[Vector3] = None

    def get_normal(self) -> Vector3:
        if self.normal is None:
            edge1 = self.v2 - self.v1
            edge2 = self.v3 - self.v1
            self.normal = edge1.cross(edge2).normalize()
        return self.normal


class Mesh3D:
    """3D mesh / 3D 网格"""

    def __init__(self):
        self.vertices: List[Vector3] = []
        self.triangles: List[Triangle3D] = []
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)
        self.scale = Vector3(1, 1, 1)

    def add_triangle(self, v1: Vector3, v2: Vector3, v3: Vector3, color: Tuple[int, int, int] = (255, 255, 255)):
        tri = Triangle3D(v1, v2, v3)
        tri.color = color
        self.triangles.append(tri)

    def get_transform(self) -> Matrix4x4:
        m = Matrix4x4()
        m = Matrix4x4.translation(self.position.x, self.position.y, self.position.z).multiply(m)
        m = Matrix4x4.rotation_x(self.rotation.x).multiply(m)
        m = Matrix4x4.rotation_y(self.rotation.y).multiply(m)
        m = Matrix4x4.rotation_z(self.rotation.z).multiply(m)
        m = Matrix4x4.scale(self.scale.x, self.scale.y, self.scale.z).multiply(m)
        return m


class Renderer3D:
    """
    3D software renderer.
    3D 软件渲染器。
    """

    def __init__(self, width: int = 800, height: int = 600):
        """
        Initialize 3D renderer.
        初始化 3D 渲染器。

        Args:
            参数：
            width (int): Render width / 渲染宽度
            height (int): Render height / 渲染高度
        """
        self.width = width
        self.height = height
        self.z_buffer: List[List[float]] = []
        self.framebuffer: List[List[Tuple[int, int, int]]] = []
        self.light_position = Vector3(0, 0, -5)

        self._init_buffers()

    def _init_buffers(self):
        """Initialize render buffers / 初始化渲染缓冲区"""
        self.z_buffer = [[float('inf')] * self.width for _ in range(self.height)]
        self.framebuffer = [[(0, 0, 0)] * self.width for _ in range(self.height)]

    def clear(self, color: Tuple[int, int, int] = (0, 0, 0)):
        """Clear buffers / 清空缓冲区"""
        for y in range(self.height):
            for x in range(self.width):
                self.z_buffer[y][x] = float('inf')
                self.framebuffer[y][x] = color

    def project(self, v: Vector3, model_view: Matrix4x4, projection: Matrix4x4) -> Optional[Tuple[float, float, float]]:
        """
        Project a 3D point to 2D.
        将 3D 点投影到 2D。

        Args:
            参数：
            v (Vector3): 3D point / 3D 点
            model_view (Matrix4x4): Model-view matrix / 模型-视图矩阵
            projection (Matrix4x4): Projection matrix / 投影矩阵

        Returns:
            返回：
            tuple: (x, y, z) or None if behind camera / (x, y, z) 或 None
        """
        # Transform to camera space / 变换到摄像机空间
        v_camera = model_view.transform(v)

        # Behind camera / 在摄像机后面
        if v_camera.z <= 0:
            return None

        # Project to screen / 投影到屏幕
        v_proj = projection.transform(v_camera)

        # Convert to screen coordinates / 转换为屏幕坐标
        x = (v_proj.x / v_proj.w) * self.width / 2 + self.width / 2
        y = -(v_proj.y / v_proj.w) * self.height / 2 + self.height / 2
        z = v_proj.z / v_proj.w

        return (x, y, z)

    def draw_triangle(self, tri: Triangle3D, model_view: Matrix4x4, projection: Matrix4x4):
        """
        Draw a triangle to the framebuffer.
        将三角形绘制到帧缓冲。

        Args:
            参数：
            tri (Triangle3D): Triangle to draw / 要绘制的三角形
            model_view (Matrix4x4): Model-view matrix / 模型-视图矩阵
            projection (Matrix4x4): Projection matrix / 投影矩阵
        """
        # Project vertices / 投影顶点
        p1 = self.project(tri.v1, model_view, projection)
        p2 = self.project(tri.v2, model_view, projection)
        p3 = self.project(tri.v3, model_view, projection)

        if not p1 or not p2 or not p3:
            return

        x1, y1, z1 = p1
        x2, y2, z2 = p2
        x3, y3, z3 = p3

        # Calculate lighting / 计算光照
        normal = tri.get_normal()
        light_dir = (self.light_position - tri.v1).normalize()
        intensity = max(0.0, normal.dot(light_dir))

        # Color with lighting / 带光照的颜色
        r = int(tri.color[0] * (0.3 + 0.7 * intensity))
        g = int(tri.color[1] * (0.3 + 0.7 * intensity))
        b = int(tri.color[2] * (0.3 + 0.7 * intensity))
        color = (min(255, r), min(255, g), min(255, b))

        # Draw filled triangle / 绘制填充三角形
        self._draw_filled_triangle(int(x1), int(y1), z1,
                                   int(x2), int(y2), z2,
                                   int(x3), int(y3), z3,
                                   color)

    def _draw_filled_triangle(self, x1: int, y1: int, z1: float,
                              x2: int, y2: int, z2: float,
                              x3: int, y3: int, z3: float,
                              color: Tuple[int, int, int]):
        """
        Draw a filled triangle with z-buffer.
        绘制带 Z 缓冲的填充三角形。
        """
        # Sort vertices by y / 按 y 排序顶点
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            z1, z2 = z2, z1
        if y1 > y3:
            x1, x3 = x3, x1
            y1, y3 = y3, y1
            z1, z3 = z3, z1
        if y2 > y3:
            x2, x3 = x3, x2
            y2, y3 = y3, y2
            z2, z3 = z3, z2

        # Clamp to screen / 限制到屏幕
        y1 = max(0, min(self.height - 1, y1))
        y2 = max(0, min(self.height - 1, y2))
        y3 = max(0, min(self.height - 1, y3))

        if y1 == y2 == y3:
            return

        # Scanline rasterization / 扫描线光栅化
        for y in range(y1, y3 + 1):
            if y < 0 or y >= self.height:
                continue

            # Calculate x bounds / 计算 x 边界
            if y <= y2:
                x_left = x1 + (x2 - x1) * (y - y1) / (y2 - y1) if y2 != y1 else x1
                z_left = z1 + (z2 - z1) * (y - y1) / (y2 - y1) if y2 != y1 else z1
            else:
                x_left = x2 + (x3 - x2) * (y - y2) / (y3 - y2) if y3 != y2 else x2
                z_left = z2 + (z3 - z2) * (y - y2) / (y3 - y2) if y3 != y2 else z2

            x_right = x1 + (x3 - x1) * (y - y1) / (y3 - y1) if y3 != y1 else x1
            z_right = z1 + (z3 - z1) * (y - y1) / (y3 - y1) if y3 != y1 else z1

            if x_left > x_right:
                x_left, x_right = x_right, x_left
                z_left, z_right = z_right, z_left

            x_left = max(0, min(self.width - 1, int(x_left)))
            x_right = max(0, min(self.width - 1, int(x_right)))

            for x in range(x_left, x_right + 1):
                # Interpolate z / 插值 Z
                t = (x - x_left) / (x_right - x_left + 1) if x_right != x_left else 0
                z = z_left + (z_right - z_left) * t

                if z < self.z_buffer[y][x]:
                    self.z_buffer[y][x] = z
                    self.framebuffer[y][x] = color

    def get_framebuffer(self) -> List[List[Tuple[int, int, int]]]:
        """Get framebuffer / 获取帧缓冲"""
        return self.framebuffer


def main():
    """Main entry point / 主入口"""
    renderer = Renderer3D(640, 480)

    # Create a simple cube / 创建一个简单立方体
    mesh = Mesh3D()
    vertices = [
        Vector3(-1, -1, -1), Vector3(1, -1, -1),
        Vector3(1, 1, -1), Vector3(-1, 1, -1),
        Vector3(-1, -1, 1), Vector3(1, -1, 1),
        Vector3(1, 1, 1), Vector3(-1, 1, 1)
    ]

    # Define cube faces / 定义立方体面
    faces = [
        (0, 1, 2, 3),  # Front / 前面
        (4, 7, 6, 5),  # Back / 后面
        (3, 2, 6, 7),  # Top / 顶面
        (0, 4, 5, 1),  # Bottom / 底面
        (0, 3, 7, 4),  # Left / 左面
        (1, 5, 6, 2),  # Right / 右面
    ]

    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (255, 0, 255), (0, 255, 255)
    ]

    for i, face in enumerate(faces):
        v1, v2, v3, v4 = face
        mesh.add_triangle(vertices[v1], vertices[v2], vertices[v3], colors[i % len(colors)])
        mesh.add_triangle(vertices[v3], vertices[v4], vertices[v1], colors[i % len(colors)])

    mesh.position = Vector3(0, 0, 0)
    mesh.rotation = Vector3(0.3, 0.5, 0)

    # Render loop / 渲染循环
    import time
    start = time.time()

    for frame in range(60):
        mesh.rotation.x += 0.02
        mesh.rotation.y += 0.03
        mesh.rotation.z += 0.01

        renderer.clear((32, 32, 64))

        model_view = mesh.get_transform()
        projection = Matrix4x4()
        # Simple perspective projection / 简单透视投影
        fov = 1.0
        far = 10.0
        near = 0.1
        projection.m[0][0] = fov
        projection.m[1][1] = fov
        projection.m[2][2] = -(far + near) / (far - near)
        projection.m[2][3] = -(2 * far * near) / (far - near)
        projection.m[3][2] = -1

        for tri in mesh.triangles:
            renderer.draw_triangle(tri, model_view, projection)

    print(f"3D Renderer: 60 frames in {time.time() - start:.2f}s")


if __name__ == '__main__':
    main()