# ============================================================================
# Module: userland/libs/libgame2d/__init__.py
# 模块：userland/libs/libgame2d/__init__.py
# Description: 2D game engine package
# 描述：2D 游戏引擎包
# ============================================================================

from userland.libs.libgame2d.sprite import Sprite, SpriteSheet
from userland.libs.libgame2d.animation import Animation, AnimationPlayer
from userland.libs.libgame2d.physics import PhysicsBody, PhysicsWorld, Collision
from userland.libs.libgame2d.particle import ParticleSystem, ParticleEmitter
from userland.libs.libgame2d.scene import Scene, SceneManager

__all__ = [
    'Sprite',
    'SpriteSheet',
    'Animation',
    'AnimationPlayer',
    'PhysicsBody',
    'PhysicsWorld',
    'Collision',
    'ParticleSystem',
    'ParticleEmitter',
    'Scene',
    'SceneManager',
]

__version__ = "1.0.0"