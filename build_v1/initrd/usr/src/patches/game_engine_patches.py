# ============================================================================
# Module: userland/patches/game_engine_patches.py
# 模块：userland/patches/game_engine_patches.py
# Description: Game engine patches for P3+
# 描述：P3+ 游戏引擎补丁
# ============================================================================

"""
Game engine patches for P3+.
P3+ 游戏引擎补丁。

Extends 2D game engine with advanced features:
- Camera system / 摄像机系统
- Tilemap support / 瓦片地图支持
- Advanced physics / 高级物理
- Particle effects / 粒子特效
- Positional audio / 位置音频
"""

import math
import random
import time
from typing import List, Optional, Tuple, Dict, Any


class Camera2D:
    """
    2D Camera system.
    2D 摄像机系统。

    Provides viewport control, panning, zooming, and shaking.
    提供视口控制、平移、缩放和震动。
    """

    def __init__(self, viewport_width: int = 800, viewport_height: int = 600):
        """
        Initialize camera.
        初始化摄像机。

        Args:
            参数：
            viewport_width (int): Viewport width / 视口宽度
            viewport_height (int): Viewport height / 视口高度
        """
        self.x = 0.0
        self.y = 0.0
        self.zoom = 1.0
        self.rotation = 0.0
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        # Shake / 震动
        self.shake_intensity = 0.0
        self.shake_duration = 0.0
        self.shake_elapsed = 0.0

        # Target / 目标
        self.target_x: Optional[float] = None
        self.target_y: Optional[float] = None
        self.lerp_speed = 4.0

    def follow(self, x: float, y: float, smooth: bool = True):
        """
        Follow a target.
        跟随目标。

        Args:
            参数：
            x (float): Target X / 目标 X
            y (float): Target Y / 目标 Y
            smooth (bool): Smooth follow / 平滑跟随
        """
        if smooth:
            self.target_x = x
            self.target_y = y
        else:
            self.x = x
            self.y = y
            self.target_x = None
            self.target_y = None

    def update(self, dt: float):
        """
        Update camera.
        更新摄像机。

        Args:
            参数：
            dt (float): Delta time / 增量时间
        """
        # Smooth follow / 平滑跟随
        if self.target_x is not None and self.target_y is not None:
            self.x += (self.target_x - self.x) * min(1.0, self.lerp_speed * dt)
            self.y += (self.target_y - self.y) * min(1.0, self.lerp_speed * dt)

        # Shake / 震动
        if self.shake_duration > 0:
            self.shake_elapsed += dt
            if self.shake_elapsed >= self.shake_duration:
                self.shake_intensity = 0.0
                self.shake_duration = 0.0
            else:
                progress = 1.0 - (self.shake_elapsed / self.shake_duration)
                intensity = self.shake_intensity * progress

                # Random offset / 随机偏移
                self._shake_offset_x = (random.random() - 0.5) * 2 * intensity
                self._shake_offset_y = (random.random() - 0.5) * 2 * intensity
        else:
            self._shake_offset_x = 0.0
            self._shake_offset_y = 0.0

    def shake(self, intensity: float, duration: float):
        """
        Trigger camera shake.
        触发摄像机震动。

        Args:
            参数：
            intensity (float): Shake intensity / 震动强度
            duration (float): Shake duration / 震动持续时间
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_elapsed = 0.0

    def world_to_screen(self, wx: float, wy: float) -> Tuple[float, float]:
        """
        Convert world coordinates to screen coordinates.
        将世界坐标转换为屏幕坐标。

        Args:
            参数：
            wx (float): World X / 世界 X
            wy (float): World Y / 世界 Y

        Returns:
            返回：
            tuple: Screen coordinates / 屏幕坐标
        """
        # Apply shake / 应用震动
        offset_x = getattr(self, '_shake_offset_x', 0.0)
        offset_y = getattr(self, '_shake_offset_y', 0.0)

        sx = (wx - self.x) * self.zoom + self.viewport_width / 2 + offset_x
        sy = (wy - self.y) * self.zoom + self.viewport_height / 2 + offset_y

        return sx, sy

    def screen_to_world(self, sx: float, sy: float) -> Tuple[float, float]:
        """
        Convert screen coordinates to world coordinates.
        将屏幕坐标转换为世界坐标。

        Args:
            参数：
            sx (float): Screen X / 屏幕 X
            sy (float): Screen Y / 屏幕 Y

        Returns:
            返回：
            tuple: World coordinates / 世界坐标
        """
        wx = (sx - self.viewport_width / 2) / self.zoom + self.x
        wy = (sy - self.viewport_height / 2) / self.zoom + self.y
        return wx, wy


class TileMap:
    """
    2D TileMap system.
    2D 瓦片地图系统。

    Provides layered tile maps with collision detection.
    提供带碰撞检测的分层瓦片地图。
    """

    def __init__(self, tile_width: int = 32, tile_height: int = 32,
                 map_width: int = 20, map_height: int = 15):
        """
        Initialize tile map.
        初始化瓦片地图。

        Args:
            参数：
            tile_width (int): Tile width / 瓦片宽度
            tile_height (int): Tile height / 瓦片高度
            map_width (int): Map width in tiles / 地图宽度（瓦片数）
            map_height (int): Map height in tiles / 地图高度（瓦片数）
        """
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.map_width = map_width
        self.map_height = map_height

        # Layers / 层
        self.layers: List[List[List[int]]] = []

        # Tile set / 瓦片集
        self.tileset: Dict[int, Any] = {}

        # Collision layer / 碰撞层
        self.collision_map: List[List[bool]] = []

    def add_layer(self, data: Optional[List[List[int]]] = None):
        """
        Add a layer to the map.
        向地图添加一层。

        Args:
            参数：
            data (list): Layer data / 层数据
        """
        if data is None:
            data = [[0] * self.map_width for _ in range(self.map_height)]
        self.layers.append(data)

    def set_tile(self, layer: int, x: int, y: int, tile_id: int):
        """
        Set a tile.
        设置一个瓦片。

        Args:
            参数：
            layer (int): Layer index / 层索引
            x (int): Tile X / 瓦片 X
            y (int): Tile Y / 瓦片 Y
            tile_id (int): Tile ID / 瓦片 ID
        """
        if 0 <= layer < len(self.layers):
            if 0 <= x < self.map_width and 0 <= y < self.map_height:
                self.layers[layer][y][x] = tile_id

    def get_tile(self, layer: int, x: int, y: int) -> int:
        """
        Get a tile.
        获取一个瓦片。

        Args:
            参数：
            layer (int): Layer index / 层索引
            x (int): Tile X / 瓦片 X
            y (int): Tile Y / 瓦片 Y

        Returns:
            返回：
            int: Tile ID / 瓦片 ID
        """
        if 0 <= layer < len(self.layers):
            if 0 <= x < self.map_width and 0 <= y < self.map_height:
                return self.layers[layer][y][x]
        return 0

    def set_collision(self, x: int, y: int, solid: bool = True):
        """
        Set collision at a tile position.
        在瓦片位置设置碰撞。

        Args:
            参数：
            x (int): Tile X / 瓦片 X
            y (int): Tile Y / 瓦片 Y
            solid (bool): Solid flag / 实心标志
        """
        if not self.collision_map:
            self.collision_map = [[False] * self.map_width for _ in range(self.map_height)]

        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            self.collision_map[y][x] = solid

    def is_solid(self, x: float, y: float) -> bool:
        """
        Check if a world position is solid.
        检查世界位置是否实心。

        Args:
            参数：
            x (float): World X / 世界 X
            y (float): World Y / 世界 Y

        Returns:
            返回：
            bool: True if solid / 实心返回 True
        """
        if not self.collision_map:
            return False

        tile_x = int(x // self.tile_width)
        tile_y = int(y // self.tile_height)

        if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
            return self.collision_map[tile_y][tile_x]

        return False

    def render(self, renderer, camera: Optional[Camera2D] = None):
        """
        Render tile map.
        渲染瓦片地图。

        Args:
            参数：
            renderer: Renderer instance / 渲染器实例
            camera (Camera2D): Camera instance / 摄像机实例
        """
        # In real implementation, render visible tiles / 实际实现中渲染可见瓦片
        pass


class AdvancedPhysics:
    """
    Advanced physics system.
    高级物理系统。

    Provides gravity, friction, damping, and impulses.
    提供重力、摩擦力、阻尼和冲量。
    """

    def __init__(self, gravity_x: float = 0.0, gravity_y: float = 980.0,
                 damping: float = 0.99, friction: float = 0.9):
        """
        Initialize physics system.
        初始化物理系统。

        Args:
            参数：
            gravity_x (float): Gravity X / 重力 X
            gravity_y (float): Gravity Y / 重力 Y
            damping (float): Damping factor / 阻尼因子
            friction (float): Friction factor / 摩擦力因子
        """
        self.gravity_x = gravity_x
        self.gravity_y = gravity_y
        self.damping = damping
        self.friction = friction
        self.bodies: List[PhysicsBody] = []

    def add_body(self, body: 'PhysicsBody'):
        """Add physics body / 添加物理体"""
        self.bodies.append(body)

    def update(self, dt: float):
        """
        Update physics.
        更新物理。

        Args:
            参数：
            dt (float): Delta time / 增量时间
        """
        for body in self.bodies:
            # Apply gravity / 应用重力
            body.velocity_x += self.gravity_x * dt
            body.velocity_y += self.gravity_y * dt

            # Apply damping / 应用阻尼
            body.velocity_x *= self.damping
            body.velocity_y *= self.damping

            # Apply friction / 应用摩擦力
            if abs(body.velocity_x) < 0.1:
                body.velocity_x *= self.friction
            if abs(body.velocity_y) < 0.1:
                body.velocity_y *= self.friction

            # Update position / 更新位置
            body.x += body.velocity_x * dt
            body.y += body.velocity_y * dt

        # Collision detection / 碰撞检测
        self._resolve_collisions()

    def _resolve_collisions(self):
        """Resolve collisions between bodies / 解决物体间碰撞"""
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                a = self.bodies[i]
                b = self.bodies[j]

                if a.collides_with(b):
                    # Simple elastic collision / 简单弹性碰撞
                    dx = b.x - a.x
                    dy = b.y - a.y
                    dist = math.sqrt(dx * dx + dy * dy)

                    if dist == 0:
                        continue

                    overlap = (a.radius + b.radius) - dist
                    if overlap > 0:
                        # Separate bodies / 分离物体
                        nx = dx / dist
                        ny = dy / dist
                        a.x -= nx * overlap / 2
                        a.y -= ny * overlap / 2
                        b.x += nx * overlap / 2
                        b.y += ny * overlap / 2

                        # Exchange velocities / 交换速度
                        vx = a.velocity_x
                        vy = a.velocity_y
                        a.velocity_x = b.velocity_x
                        a.velocity_y = b.velocity_y
                        b.velocity_x = vx
                        b.velocity_y = vy


class PhysicsBody:
    """
    Physics body with collision.
    带碰撞的物理体。
    """

    def __init__(self, x: float = 0, y: float = 0, radius: float = 16):
        """
        Initialize physics body.
        初始化物理体。

        Args:
            参数：
            x (float): X position / X 位置
            y (float): Y position / Y 位置
            radius (float): Radius / 半径
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.mass = 1.0
        self.restitution = 0.5
        self.static = False

    def apply_impulse(self, imp_x: float, imp_y: float):
        """Apply impulse / 应用冲量"""
        if self.static:
            return
        self.velocity_x += imp_x / self.mass
        self.velocity_y += imp_y / self.mass

    def collides_with(self, other: 'PhysicsBody') -> bool:
        """Check collision with another body / 检查与另一个物体的碰撞"""
        dx = self.x - other.x
        dy = self.y - other.y
        dist = math.sqrt(dx * dx + dy * dy)
        return dist < self.radius + other.radius


class AdvancedParticleSystem:
    """
    Advanced particle system.
    高级粒子系统。

    Provides particles with color and size over lifetime,
    gravity wells, and turbulence.
    提供生命周期内颜色和大小变化、引力井和湍流。
    """

    def __init__(self, max_particles: int = 1000):
        """
        Initialize particle system.
        初始化粒子系统。

        Args:
            参数：
            max_particles (int): Maximum particles / 最大粒子数
        """
        self.particles: List[Particle] = []
        self.max_particles = max_particles
        self.emitters: List[ParticleEmitter] = []

        # Gravity wells / 引力井
        self.gravity_wells: List[Tuple[float, float, float]] = []

        # Turbulence / 湍流
        self.turbulence_strength = 0.0

    def add_gravity_well(self, x: float, y: float, strength: float):
        """
        Add a gravity well.
        添加引力井。

        Args:
            参数：
            x (float): X position / X 位置
            y (float): Y position / Y 位置
            strength (float): Well strength / 井强度
        """
        self.gravity_wells.append((x, y, strength))

    def update(self, dt: float):
        """
        Update all particles.
        更新所有粒子。

        Args:
            参数：
            dt (float): Delta time / 增量时间
        """
        # Update emitters / 更新发射器
        for emitter in self.emitters:
            if emitter.active:
                emitter.update(dt, self)

        # Update particles / 更新粒子
        for particle in self.particles[:]:
            particle.update(dt)

            # Apply gravity wells / 应用引力井
            for gx, gy, strength in self.gravity_wells:
                dx = gx - particle.x
                dy = gy - particle.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > 0:
                    force = strength / (dist * dist + 1)
                    particle.vx += dx / dist * force * dt
                    particle.vy += dy / dist * force * dt

            # Apply turbulence / 应用湍流
            if self.turbulence_strength > 0:
                particle.vx += (random.random() - 0.5) * self.turbulence_strength * dt
                particle.vy += (random.random() - 0.5) * self.turbulence_strength * dt

            # Remove dead particles / 移除死亡粒子
            if particle.life <= 0:
                self.particles.remove(particle)

        # Limit particles / 限制粒子数
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[:self.max_particles]


class Particle:
    """
    Individual particle.
    单个粒子。
    """

    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0,
                 life: float = 1.0, max_life: float = 1.0,
                 size: float = 4, max_size: float = 4,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 end_color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Initialize particle.
        初始化粒子。

        Args:
            参数：
            x (float): X position / X 位置
            y (float): Y position / Y 位置
            vx (float): X velocity / X 速度
            vy (float): Y velocity / Y 速度
            life (float): Current life / 当前生命
            max_life (float): Maximum life / 最大生命
            size (float): Current size / 当前大小
            max_size (float): Maximum size / 最大大小
            color (tuple): Start color / 起始颜色
            end_color (tuple): End color / 结束颜色
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = max_life
        self.size = size
        self.max_size = max_size
        self.color = color
        self.end_color = end_color
        self.rotation = 0.0
        self.angular_velocity = 0.0

    def update(self, dt: float):
        """Update particle / 更新粒子"""
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rotation += self.angular_velocity * dt

        # Size over life / 生命周期大小变化
        progress = 1.0 - (self.life / self.max_life)
        self.size = self.max_size * (1.0 - progress)

    def get_color(self) -> Tuple[int, int, int]:
        """Get interpolated color / 获取插值颜色"""
        progress = 1.0 - (self.life / self.max_life)
        r = int(self.color[0] + (self.end_color[0] - self.color[0]) * progress)
        g = int(self.color[1] + (self.end_color[1] - self.color[1]) * progress)
        b = int(self.color[2] + (self.end_color[2] - self.color[2]) * progress)
        return (r, g, b)


class ParticleEmitter:
    """
    Particle emitter.
    粒子发射器。
    """

    def __init__(self, x: float = 0, y: float = 0, rate: float = 10,
                 active: bool = True):
        """
        Initialize particle emitter.
        初始化粒子发射器。

        Args:
            参数：
            x (float): Emitter X / 发射器 X
            y (float): Emitter Y / 发射器 Y
            rate (float): Emission rate (particles/sec) / 发射率
            active (bool): Active flag / 活动标志
        """
        self.x = x
        self.y = y
        self.rate = rate
        self.active = active
        self.accumulator = 0.0

        # Particle parameters / 粒子参数
        self.speed_min = 50.0
        self.speed_max = 200.0
        self.life_min = 0.5
        self.life_max = 2.0
        self.size_min = 2.0
        self.size_max = 8.0
        self.color = (255, 255, 255)
        self.end_color = (255, 0, 0)
        self.spread = 360.0  # Degrees / 角度

    def emit(self, system: AdvancedParticleSystem, count: int = 1):
        """
        Emit particles.
        发射粒子。

        Args:
            参数：
            system (AdvancedParticleSystem): Particle system / 粒子系统
            count (int): Number of particles / 粒子数
        """
        for _ in range(count):
            angle = random.uniform(0, self.spread) * math.pi / 180
            speed = random.uniform(self.speed_min, self.speed_max)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            life = random.uniform(self.life_min, self.life_max)
            size = random.uniform(self.size_min, self.size_max)

            particle = Particle(
                x=self.x, y=self.y,
                vx=vx, vy=vy,
                life=life, max_life=life,
                size=size, max_size=size,
                color=self.color, end_color=self.end_color
            )
            system.particles.append(particle)

    def update(self, dt: float, system: AdvancedParticleSystem):
        """
        Update emitter.
        更新发射器。

        Args:
            参数：
            dt (float): Delta time / 增量时间
            system (AdvancedParticleSystem): Particle system / 粒子系统
        """
        if not self.active:
            return

        self.accumulator += dt * self.rate
        while self.accumulator >= 1.0:
            self.emit(system, 1)
            self.accumulator -= 1.0