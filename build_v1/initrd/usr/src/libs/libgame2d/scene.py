# ============================================================================
# Module: userland/libs/libgame2d/scene.py
# Description: Scene management framework
# 描述：场景管理框架
# ============================================================================

"""
Scene management for games.
游戏场景管理。

Provides scene loading, switching, and lifecycle management.
提供场景加载、切换和生命周期管理。
"""

from typing import Dict, List, Optional, Any


class Scene:
    """
    Base scene class / 基础场景类
    """

    def __init__(self, name: str = "scene"):
        self.name = name
        self.entities: List[Any] = []
        self._is_loaded = False
        self._is_active = False

    def load(self):
        """Load scene resources / 加载场景资源"""
        self._is_loaded = True

    def unload(self):
        """Unload scene resources / 卸载场景资源"""
        self._is_loaded = False
        self.entities.clear()

    def on_enter(self):
        """Called when scene becomes active / 场景激活时调用"""
        self._is_active = True

    def on_exit(self):
        """Called when scene becomes inactive / 场景失活时调用"""
        self._is_active = False

    def update(self, dt: float):
        """Update scene logic / 更新场景逻辑"""
        pass

    def render(self, renderer: Any):
        """Render scene / 渲染场景"""
        pass

    def add_entity(self, entity: Any):
        """Add entity to scene / 添加实体"""
        self.entities.append(entity)

    def remove_entity(self, entity: Any):
        """Remove entity from scene / 移除实体"""
        if entity in self.entities:
            self.entities.remove(entity)

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def is_active(self) -> bool:
        return self._is_active


class SceneManager:
    """
    Scene manager / 场景管理器
    """

    def __init__(self):
        self._scenes: Dict[str, Scene] = {}
        self._current_scene: Optional[Scene] = None
        self._pending_scene: Optional[str] = None

    def register_scene(self, scene: Scene):
        """Register a scene / 注册场景"""
        self._scenes[scene.name] = scene

    def unregister_scene(self, name: str):
        """Unregister a scene / 注销场景"""
        if name in self._scenes:
            scene = self._scenes[name]
            if scene.is_loaded:
                scene.unload()
            del self._scenes[name]

    def switch_scene(self, name: str):
        """Switch to a scene / 切换场景"""
        if name not in self._scenes:
            raise ValueError(f"Scene '{name}' not registered")
        self._pending_scene = name

    def update(self, dt: float):
        """Update current scene / 更新当前场景"""
        # Handle pending scene switch
        if self._pending_scene:
            if self._current_scene:
                self._current_scene.on_exit()
            self._current_scene = self._scenes[self._pending_scene]
            if not self._current_scene.is_loaded:
                self._current_scene.load()
            self._current_scene.on_enter()
            self._pending_scene = None

        if self._current_scene and self._current_scene.is_active:
            self._current_scene.update(dt)

    def render(self, renderer: Any):
        """Render current scene / 渲染当前场景"""
        if self._current_scene and self._current_scene.is_active:
            self._current_scene.render(renderer)

    @property
    def current_scene(self) -> Optional[Scene]:
        return self._current_scene

    @property
    def scene_names(self) -> List[str]:
        return list(self._scenes.keys())
