# ============================================================================
# Module: userland/apps/shell/extensions/job_control.py
# 模块：userland/apps/shell/extensions/job_control.py
# Description: Job control extension for Shell
# 描述：Shell 作业控制扩展
# ============================================================================

"""
Job control extension for Shell application.
Shell 应用的作业控制扩展。

Adds job control features (bg, fg, jobs) to the shell.
为 Shell 添加作业控制功能（bg、fg、jobs）。
"""

import os
import sys
import signal
import subprocess
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto


class JobState(Enum):
    """Job state / 作业状态"""
    RUNNING = auto()
    SUSPENDED = auto()
    DONE = auto()


@dataclass
class Job:
    """Job information / 作业信息"""
    job_id: int
    pid: int
    command: str
    state: JobState = JobState.RUNNING
    process: Optional[subprocess.Popen] = None
    returncode: Optional[int] = None


class JobControl:
    """
    Job control for Shell.
    Shell 作业控制。

    Manages background and foreground jobs.
    管理后台和前台作业。
    """

    def __init__(self, shell_instance):
        """
        Initialize job control.
        初始化作业控制。

        Args:
            参数：
            shell_instance: ShellApp instance / ShellApp 实例
        """
        self.shell = shell_instance
        self.jobs: Dict[int, Job] = {}
        self.next_job_id = 1
        self.current_job: Optional[Job] = None

        # Register signal handlers / 注册信号处理函数
        self._register_signal_handlers()

    def _register_signal_handlers(self):
        """Register signal handlers for job control / 注册作业控制信号处理函数"""
        try:
            # SIGCHLD for child process termination / SIGCHLD 用于子进程终止
            signal.signal(signal.SIGCHLD, self._handle_sigchld)
            # SIGTSTP for job suspension / SIGTSTP 用于作业暂停
            signal.signal(signal.SIGTSTP, self._handle_sigtstp)
            # SIGCONT for job continuation / SIGCONT 用于作业继续
            signal.signal(signal.SIGCONT, self._handle_sigcont)
        except AttributeError:
            pass  # Windows doesn't support these signals / Windows 不支持这些信号

    def _handle_sigchld(self, signum, frame):
        """Handle SIGCHLD - child process termination / 处理 SIGCHLD - 子进程终止"""
        # In real implementation, would reap child processes / 实际实现中会收割子进程
        pass

    def _handle_sigtstp(self, signum, frame):
        """Handle SIGTSTP - suspend current job / 处理 SIGTSTP - 暂停当前作业"""
        if self.current_job and self.current_job.process:
            try:
                self.current_job.process.send_signal(signal.SIGTSTP)
                self.current_job.state = JobState.SUSPENDED
                print(f"Job {self.current_job.job_id} suspended")
            except Exception as e:
                print(f"Failed to suspend job: {e}")

    def _handle_sigcont(self, signum, frame):
        """Handle SIGCONT - continue suspended job / 处理 SIGCONT - 继续暂停的作业"""
        for job in self.jobs.values():
            if job.state == JobState.SUSPENDED and job.process:
                try:
                    job.process.send_signal(signal.SIGCONT)
                    job.state = JobState.RUNNING
                    print(f"Job {job.job_id} continued")
                except Exception as e:
                    print(f"Failed to continue job: {e}")

    def add_job(self, pid: int, command: str, process: subprocess.Popen) -> int:
        """
        Add a background job.
        添加后台作业。

        Args:
            参数：
            pid (int): Process ID / 进程 ID
            command (str): Command string / 命令字符串
            process (subprocess.Popen): Process object / 进程对象

        Returns:
            返回：
            int: Job ID / 作业 ID
        """
        job_id = self.next_job_id
        self.next_job_id += 1

        job = Job(
            job_id=job_id,
            pid=pid,
            command=command,
            process=process,
            state=JobState.RUNNING
        )

        self.jobs[job_id] = job
        self.current_job = job

        print(f"[{job_id}] {pid} {command}")
        return job_id

    def get_job(self, job_id: int) -> Optional[Job]:
        """Get job by ID / 按 ID 获取作业"""
        return self.jobs.get(job_id)

    def get_job_by_pid(self, pid: int) -> Optional[Job]:
        """Get job by PID / 按 PID 获取作业"""
        for job in self.jobs.values():
            if job.pid == pid:
                return job
        return None

    def remove_job(self, job_id: int) -> bool:
        """Remove job / 移除作业"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            if self.current_job and self.current_job.job_id == job_id:
                self.current_job = None
            return True
        return False

    def fg(self, job_id: Optional[int] = None):
        """
        Bring job to foreground.
        将作业带到前台。

        Args:
            参数：
            job_id (int): Job ID or None for current / 作业 ID 或 None
        """
        if job_id is None:
            job_id = self.next_job_id - 1

        job = self.get_job(job_id)
        if not job:
            print(f"fg: job {job_id} not found")
            return

        if not job.process:
            print(f"fg: job {job_id} no process")
            return

        try:
            # Send SIGCONT if suspended / 如果暂停则发送 SIGCONT
            if job.state == JobState.SUSPENDED:
                job.process.send_signal(signal.SIGCONT)

            # Wait for process / 等待进程
            self.current_job = job
            job.process.wait()
            job.state = JobState.DONE
            job.returncode = job.process.returncode

            print(f"Job {job_id} completed with code {job.returncode}")
            self.remove_job(job_id)

        except Exception as e:
            print(f"fg: {e}")

    def bg(self, job_id: Optional[int] = None):
        """
        Resume job in background.
        在后台恢复作业。

        Args:
            参数：
            job_id (int): Job ID or None for current / 作业 ID 或 None
        """
        if job_id is None:
            job_id = self.next_job_id - 1

        job = self.get_job(job_id)
        if not job:
            print(f"bg: job {job_id} not found")
            return

        if job.state == JobState.DONE:
            print(f"bg: job {job_id} already done")
            return

        if not job.process:
            print(f"bg: job {job_id} no process")
            return

        try:
            job.process.send_signal(signal.SIGCONT)
            job.state = JobState.RUNNING
            print(f"[{job_id}] {job.command} continued")
        except Exception as e:
            print(f"bg: {e}")

    def jobs(self):
        """List jobs / 列出作业"""
        if not self.jobs:
            print("No jobs")
            return

        for job in self.jobs.values():
            state = job.state.name.lower()
            status = f"[{job.job_id}]  {state:10s}  {job.pid:6d}  {job.command}"
            if job.returncode is not None:
                status += f" (exit {job.returncode})"
            print(status)

    def jobs_command(self, args: List[str]):
        """Jobs command handler / Jobs 命令处理函数"""
        if args and args[0] == '-l':
            # Long format / 长格式
            for job in self.jobs.values():
                print(f"{job.job_id}: {job.pid} {job.command}")
        else:
            self.jobs()


# Command handlers for job control / 作业控制命令处理函数
def cmd_bg(args: List[str], job_control: JobControl):
    """Background command / 后台命令"""
    if not job_control:
        print("bg: job control not available")
        return

    job_id = None
    if args:
        try:
            job_id = int(args[0])
        except ValueError:
            print(f"bg: invalid job ID: {args[0]}")
            return

    job_control.bg(job_id)


def cmd_fg(args: List[str], job_control: JobControl):
    """Foreground command / 前台命令"""
    if not job_control:
        print("fg: job control not available")
        return

    job_id = None
    if args:
        try:
            job_id = int(args[0])
        except ValueError:
            print(f"fg: invalid job ID: {args[0]}")
            return

    job_control.fg(job_id)


def cmd_jobs(args: List[str], job_control: JobControl):
    """Jobs command / 作业列表命令"""
    if not job_control:
        print("jobs: job control not available")
        return

    job_control.jobs()