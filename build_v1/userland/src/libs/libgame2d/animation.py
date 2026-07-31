# ============================================================================
# Module: userland/libs/libgame2d/animation.py
# 模块：userland/libs/libgame2d/animation.py
# Description: Animation system for 2D games
# 描述：2D 游戏动画系统
# ============================================================================

"""
Animation system for 2D games.
2D 游戏动画系统。

Provides frame and skeletal animations.
提供帧动画和骨骼动画。
"""

from typing import List, Optional, Dict, Any
import time


class Frame:
    """
    Animation frame.
    动画帧。
    """

    def __init__(self, sprite_index: int, duration: float = 0.1,
                 x_offset: float = 0, y_offset: float = 0):
        """
        Initialize frame.
        初始化帧。

        Args:
            参数：
            sprite_index (int): Sprite sheet index / 精灵表索引
            duration (float): Frame duration (seconds) / 帧持续时间（秒）
            x_offset (float): X offset / X 偏移
            y_offset (float): Y offset / Y 偏移
        """
        self.sprite_index = sprite_index
        self.duration = duration
        self.x_offset = x_offset
        self.y_offset = y_offset


class Animation:
    """
    Animation definition.
    动画定义。
    """

    def __init__(self, name: str = "default", frames: Optional[List[Frame]] = None,
                 loop: bool = True):
        """
        Initialize animation.
        初始化动画。

        Args:
            参数：
            name (str): Animation name / 动画名称
            frames (list): List of frames / 帧列表
            loop (bool): Loop animation / 循环动画
        """
        self.name = name
        self.frames = frames or []
        self.loop = loop
        self.total_duration = sum(f.duration for f in self.frames)

    def add_frame(self, sprite_index: int, duration: float = 0.1,
                  x_offset: float = 0, y_offset: float = 0):
        """Add frame to animation / 向动画添加帧"""
        self.frames.append(Frame(sprite_index, duration, x_offset, y_offset))
        self.total_duration += duration

    def get_frame_at(self, time_pos: float) -> Optional[Frame]:
        """
        Get frame at time position.
        获取时间位置处的帧。

        Args:
            参数：
            time_pos (float): Time position / 时间位置

        Returns:
            返回：
            Frame: Frame at position / 位置处的帧
        """
        if not self.frames:
            return None

        if self.loop:
            time_pos = time_pos % self.total_duration
        elif time_pos >= self.total_duration:
            return self.frames[-1]

        elapsed = 0.0
        for frame in self.frames:
            elapsed += frame.duration
            if time_pos < elapsed:
                return frame

        return self.frames[-1]


class AnimationPlayer:
    """
    Animation player.
    动画播放器。
    """

    def __init__(self):
        """
        Initialize animation player.
        初始化动画播放器。
        """
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[Animation] = None
        self.current_frame_index: int = 0
        self.elapsed_time: float = 0.0
        self.is_playing: bool = False
        self.speed: float = 1.0
        self.on_frame_change = None
        self.on_animation_end = None

    def add_animation(self, animation: Animation):
        """Add animation to player / 向播放器添加动画"""
        self.animations[animation.name] = animation

    def play(self, name: str):
        """
        Play animation.
        播放动画。

        Args:
            参数：
            name (str): Animation name / 动画名称
        """
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_frame_index = 0
            self.elapsed_time = 0.0
            self.is_playing = True

    def stop(self):
        """Stop animation / 停止动画"""
        self.is_playing = False

    def update(self, dt: float):
        """
        Update animation.
        更新动画。

        Args:
            参数：
            dt (float): Delta time / 增量时间
        """
        if not self.is_playing or not self.current_animation:
            return

        self.elapsed_time += dt * self.speed

        frame = self.current_animation.get_frame_at(self.elapsed_time)
        if frame:
            new_index = self.current_animation.frames.index(frame)
            if new_index != self.current_frame_index:
                self.current_frame_index = new_index
                if self.on_frame_change:
                    self.on_frame_change(new_index, frame)

        # Check if animation ended / 检查动画是否结束
        if (self.elapsed_time >= self.current_animation.total_duration and
                not self.current_animation.loop):
            self.is_playing = False
            if self.on_animation_end:
                self.on_animation_end()

    def get_current_frame(self) -> Optional[Frame]:
        """
        Get current frame.
        获取当前帧。

        Returns:
            返回：
            Frame: Current frame / 当前帧
        """
        if not self.current_animation:
            return None
        return self.current_animation.get_frame_at(self.elapsed_time)

    def get_current_sprite_index(self) -> int:
        """Get current sprite index / 获取当前精灵索引"""
        frame = self.get_current_frame()
        return frame.sprite_index if frame else 0