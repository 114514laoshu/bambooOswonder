# ============================================================================
# Module: userland/libs/libgame2d/physics.py
# Description: 2D Physics engine framework
# 描述：2D 物理引擎框架
# ============================================================================

"""
2D Physics engine for games.
2D 游戏物理引擎。

Provides basic physics simulation with rigid bodies and collision detection.
提供刚体和碰撞检测的基本物理模拟。
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass, field
import math


@dataclass
class Collision:
    """Collision information / 碰撞信息"""
    body_a: 'PhysicsBody' = None
    body_b: 'PhysicsBody' = None
    normal: Tuple[float, float] = (0.0, 0.0)
    depth: float = 0.0
    point: Tuple[float, float] = (0.0, 0.0)


class PhysicsBody:
    """
    2D rigid body / 2D 刚体
    """

    def __init__(self, x: float = 0.0, y: float = 0.0,
                 width: float = 32.0, height: float = 32.0,
                 mass: float = 1.0, is_static: bool = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.inv_mass = 0.0 if is_static or mass == 0 else 1.0 / mass
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.restitution = 0.5
        self.friction = 0.3
        self.is_static = is_static

    def apply_force(self, fx: float, fy: float):
        """Apply force / 施加力"""
        if self.is_static:
            return
        self.ax += fx * self.inv_mass
        self.ay += fy * self.inv_mass

    def apply_impulse(self, ix: float, iy: float):
        """Apply impulse / 施加冲量"""
        if self.is_static:
            return
        self.vx += ix * self.inv_mass
        self.vy += iy * self.inv_mass

    def update(self, dt: float):
        """Update body state / 更新物体状态"""
        if self.is_static:
            return
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.ax = 0.0
        self.ay = 0.0

    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get AABB bounds / 获取 AABB 边界"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)


class PhysicsWorld:
    """
    2D physics world / 2D 物理世界
    """

    def __init__(self, gravity_y: float = 9.8):
        self.bodies: List[PhysicsBody] = []
        self.gravity_x = 0.0
        self.gravity_y = gravity_y

    def add_body(self, body: PhysicsBody) -> PhysicsBody:
        """Add body to world / 添加物体"""
        self.bodies.append(body)
        return body

    def remove_body(self, body: PhysicsBody):
        """Remove body from world / 移除物体"""
        if body in self.bodies:
            self.bodies.remove(body)

    def step(self, dt: float):
        """Step simulation / 步进模拟"""
        # Apply gravity
        for body in self.bodies:
            if not body.is_static:
                body.apply_force(self.gravity_x * body.mass, self.gravity_y * body.mass)

        # Update positions
        for body in self.bodies:
            body.update(dt)

        # Detect and resolve collisions
        collisions = self.detect_collisions()
        self.resolve_collisions(collisions)

    def detect_collisions(self) -> List[Collision]:
        """Detect collisions between bodies / 检测碰撞"""
        collisions = []
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                a = self.bodies[i]
                b = self.bodies[j]
                if a.is_static and b.is_static:
                    continue
                col = self._check_aabb(a, b)
                if col:
                    collisions.append(col)
        return collisions

    def _check_aabb(self, a: PhysicsBody, b: PhysicsBody) -> Optional[Collision]:
        """AABB collision check / AABB 碰撞检测"""
        ax1, ay1, ax2, ay2 = a.get_bounds()
        bx1, by1, bx2, by2 = b.get_bounds()

        if ax1 >= bx2 or ax2 <= bx1 or ay1 >= by2 or ay2 <= by1:
            return None

        overlap_x = min(ax2, bx2) - max(ax1, bx1)
        overlap_y = min(ay2, by2) - max(ay1, by1)

        col = Collision()
        col.body_a = a
        col.body_b = b
        col.depth = min(overlap_x, overlap_y)

        if overlap_x < overlap_y:
            col.normal = (1.0 if a.x < b.x else -1.0, 0.0)
        else:
            col.normal = (0.0, 1.0 if a.y < b.y else -1.0)

        return col

    def resolve_collisions(self, collisions: List[Collision]):
        """Resolve collisions / 解决碰撞"""
        for col in collisions:
            a = col.body_a
            b = col.body_b
            total_inv_mass = a.inv_mass + b.inv_mass
            if total_inv_mass == 0:
                continue

            # Separation
            sep = col.depth / total_inv_mass
            a.x -= col.normal[0] * sep * a.inv_mass
            a.y -= col.normal[1] * sep * a.inv_mass
            b.x += col.normal[0] * sep * b.inv_mass
            b.y += col.normal[1] * sep * b.inv_mass

            # Impulse
            rel_vx = b.vx - a.vx
            rel_vy = b.vy - a.vy
            vel_along_normal = rel_vx * col.normal[0] + rel_vy * col.normal[1]
            if vel_along_normal > 0:
                continue

            e = min(a.restitution, b.restitution)
            j = -(1 + e) * vel_along_normal / total_inv_mass

            a.vx -= j * a.inv_mass * col.normal[0]
            a.vy -= j * a.inv_mass * col.normal[1]
            b.vx += j * b.inv_mass * col.normal[0]
            b.vy += j * b.inv_mass * col.normal[1]
