# ============================================================================
# Module: userland/init/launcher.py
# 模块：userland/init/launcher.py
# Description: Userland launcher
# 描述：用户态启动器
# ============================================================================

"""
Userland launcher for Bamboo OS.
Bamboo OS 用户态启动器。

Starts userland processes and applications.
启动用户态进程和应用。
"""

import os
import sys
import time
import subprocess
from typing import List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class Service:
    """Service definition / 服务定义"""
    name: str
    command: List[str]
    enabled: bool = True
    daemon: bool = False
    startup_order: int = 0
    required: bool = False


class UserlandLauncher:
    """
    Userland launcher.
    用户态启动器。

    Starts all userland services and applications.
    启动所有用户态服务和应用程序。
    """

    def __init__(self):
        """Initialize launcher / 初始化启动器"""
        self.services: Dict[str, Service] = {}
        self.running_processes: List[subprocess.Popen] = []
        self.env = os.environ.copy()

        self._register_services()

    def _register_services(self):
        """Register built-in services / 注册内置服务"""
        services = [
            Service(
                name="syslog",
                command=["/sbin/syslogd"],
                daemon=True,
                startup_order=10,
                required=True,
            ),
            Service(
                name="udev",
                command=["/sbin/udevd"],
                daemon=True,
                startup_order=20,
                required=True,
            ),
            Service(
                name="dbus",
                command=["/bin/dbus-daemon", "--system"],
                daemon=True,
                startup_order=30,
                required=False,
            ),
            Service(
                name="network",
                command=["/sbin/ifconfig", "eth0", "up"],
                daemon=False,
                startup_order=40,
                required=False,
            ),
            Service(
                name="shell",
                command=["/bin/shell"],
                daemon=False,
                startup_order=100,
                required=True,
            ),
            Service(
                name="desktop",
                command=["/apps/desktop"],
                daemon=True,
                startup_order=110,
                required=False,
            ),
            Service(
                name="app_store",
                command=["/apps/app_store/app_store"],
                daemon=True,
                startup_order=120,
                required=False,
            ),
        ]

        for service in services:
            self.services[service.name] = service

    def start_service(self, name: str) -> bool:
        """
        Start a service.
        启动一个服务。

        Args:
            参数：
            name (str): Service name / 服务名称

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        if name not in self.services:
            print(f"Service not found: {name}")
            return False

        service = self.services[name]
        if not service.enabled:
            print(f"Service disabled: {name}")
            return True

        print(f"Starting: {name}")

        try:
            if service.daemon:
                # Start daemon / 启动守护进程
                proc = subprocess.Popen(
                    service.command,
                    env=self.env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
            else:
                # Start foreground process / 启动前台进程
                proc = subprocess.Popen(
                    service.command,
                    env=self.env,
                )

            self.running_processes.append(proc)
            return True

        except Exception as e:
            print(f"Failed to start {name}: {e}")
            return False

    def start_all(self) -> bool:
        """
        Start all enabled services.
        启动所有已启用的服务。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        print("Starting userland services...")

        # Sort by startup order / 按启动顺序排序
        ordered = sorted(
            self.services.values(),
            key=lambda s: s.startup_order
        )

        for service in ordered:
            if service.enabled:
                if not self.start_service(service.name):
                    if service.required:
                        print(f"Required service failed: {service.name}")
                        return False

        print("All services started")
        return True

    def stop_service(self, name: str) -> bool:
        """
        Stop a service.
        停止一个服务。

        Args:
            参数：
            name (str): Service name / 服务名称

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        # In real implementation, send SIGTERM / 实际实现中发送 SIGTERM
        print(f"Stopping: {name}")
        return True

    def stop_all(self) -> bool:
        """
        Stop all services.
        停止所有服务。

        Returns:
            返回：
            bool: True on success / 成功返回 True
        """
        print("Stopping userland services...")

        # Stop in reverse order / 按逆序停止
        for name in reversed(list(self.services.keys())):
            self.stop_service(name)

        return True

    def wait(self):
        """Wait for processes / 等待进程"""
        for proc in self.running_processes:
            try:
                proc.wait()
            except Exception:
                pass


def main():
    """Main entry point / 主入口"""
    launcher = UserlandLauncher()

    try:
        launcher.start_all()
        print("Userland ready")
        launcher.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        launcher.stop_all()


if __name__ == '__main__':
    main()