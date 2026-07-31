# ============================================================================
# Module: userland/libs/libgame2d/particle.py
# Description: Particle system framework
# 描述：粒子系统框架
# ============================================================================

"""
Particle system for visual effects.
视觉效果粒子系统。

Provides particle emission, animation, and rendering.
提供粒子发射、动画和渲染。
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass, field
import random
import math


@dataclass
class Particle:
    """Single particle / 单个粒子"""
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    life: float = 1.0
    max_life: float = 1.0
    size: float = 4.0
    color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    gravity: float = 0.0
    drag: float = 0.01

    def update(self, dt: float):
        """Update particle / 更新粒子"""
        self.vy += self.gravity * dt
        self.vx *= (1.0 - self.drag)
        self.vy *= (1.0 - self.drag)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    @property
    def is_alive(self) -> bool:
        return self.life > 0

    @property
    def alpha(self) -> float:
        return max(0.0, self.life / self.max_life)


class ParticleEmitter:
    """
    Particle emitter / 粒子发射器
    """

    def __init__(self, x: float = 0.0, y: float = 0.0,
                 emit_rate: float = 10.0, max_particles: int = 100):
        self.x = x
        self.y = y
        self.emit_rate = emit_rate
        self.max_particles = max_particles
        self.particles: List[Particle] = []
        self._emit_accumulator = 0.0

        # Emission parameters
        self.speed_min = 20.0
        self.speed_max = 80.0
        self.angle_min = 0.0
        self.angle_max = 2 * math.pi
        self.life_min = 0.5
        self.life_max = 2.0
        self.size_min = 2.0
        self.size_max = 6.0
        self.gravity = 50.0
        self.color_start = (255, 200, 50, 255)
        self.color_end = (255, 50, 0, 0)

    def emit_particle(self) -> Particle:
        """Emit a single particle / 发射单个粒子"""
        angle = random.uniform(self.angle_min, self.angle_max)
        speed = random.uniform(self.speed_min, self.speed_max)
        life = random.uniform(self.life_min, self.life_max)
        size = random.uniform(self.size_min, self.size_max)

        p = Particle(
            x=self.x, y=self.y,
            vx=math.cos(angle) * speed,
            vy=math.sin(angle) * speed,
            life=life, max_life=life,
            size=size,
            color=self.color_start,
            gravity=self.gravity,
        )
        return p

    def update(self, dt: float):
        """Update emitter and particles / 更新发射器和粒子"""
        # Emit new particles
        self._emit_accumulator += self.emit_rate * dt
        while self._emit_accumulator >= 1.0 and len(self.particles) < self.max_particles:
            self.particles.append(self.emit_particle())
            self._emit_accumulator -= 1.0

        # Update existing particles
        for p in self.particles:
            p.update(dt)

        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive]


class ParticleSystem:
    """
    Particle system manager / 粒子系统管理器
    """

    def __init__(self):
        self.emitters: List[ParticleEmitter] = []

    def add_emitter(self, emitter: ParticleEmitter) -> ParticleEmitter:
        """Add emitter / 添加发射器"""
        self.emitters.append(emitter)
        return emitter

    def remove_emitter(self, emitter: ParticleEmitter):
        """Remove emitter / 移除发射器"""
        if emitter in self.emitters:
            self.emitters.remove(emitter)

    def update(self, dt: float):
        """Update all emitters / 更新所有发射器"""
        for emitter in self.emitters:
            emitter.update(dt)

    @property
    def particle_count(self) -> int:
        return sum(len(e.particles) for e in self.emitters)
