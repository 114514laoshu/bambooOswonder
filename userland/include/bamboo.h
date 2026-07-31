/*
 * ============================================================================
 * Module: userland/include/bamboo.h
 * 模块：userland/include/bamboo.h
 * Description: Bamboo OS core API header
 * 描述：Bamboo OS 核心 API 头文件
 * ============================================================================
 */

#ifndef _BAMBOO_H
#define _BAMBOO_H

#ifdef __cplusplus
extern "C" {
#endif

/* ==========================================================================
 * System calls / 系统调用
 * ========================================================================== */

#define SYS_READ    0
#define SYS_WRITE   1
#define SYS_OPEN    2
#define SYS_CLOSE   3
#define SYS_STAT    4
#define SYS_FSTAT   5
#define SYS_LSEEK   6
#define SYS_POLL    7
#define SYS_MMAP    8
#define SYS_MPROTECT 9
#define SYS_MUNMAP  10
#define SYS_BRK     11
#define SYS_SIGACTION 12
#define SYS_SIGPROCMASK 13
#define SYS_IOCTL   14
#define SYS_PREAD64 15
#define SYS_PWRITE64 16
#define SYS_READV   17
#define SYS_WRITEV  18
#define SYS_ACCESS  19
#define SYS_PIPE    20
#define SYS_SELECT  21
#define SYS_SCHED_YIELD 22
#define SYS_MREMAP  23
#define SYS_MSYNC   24
#define SYS_MINCORE 25
#define SYS_MADVISE 26
#define SYS_SHMGET  27
#define SYS_SHMAT   28
#define SYS_SHMCTL  29
#define SYS_DUP     30
#define SYS_DUP2    31
#define SYS_PAUSE   32
#define SYS_NANOSLEEP 33
#define SYS_GETITIMER 34
#define SYS_ALARM   35
#define SYS_SETITIMER 36
#define SYS_GETPID  37
#define SYS_SENDFILE 38
#define SYS_SOCKET  39
#define SYS_CONNECT 40
#define SYS_ACCEPT  41
#define SYS_SENDTO  42
#define SYS_RECVFROM 43
#define SYS_SENDMSG 44
#define SYS_RECVMSG 45
#define SYS_SHUTDOWN 46
#define SYS_BIND    47
#define SYS_LISTEN  48
#define SYS_GETSOCKNAME 49
#define SYS_GETPEERNAME 50
#define SYS_SOCKETPAIR 51
#define SYS_SETSOCKOPT 52
#define SYS_GETSOCKOPT 53
#define SYS_CLONE   54
#define SYS_FORK    55
#define SYS_EXECVE  56
#define SYS_EXIT    57
#define SYS_WAIT4   58
#define SYS_KILL    59
#define SYS_UNAME   60
#define SYS_SEMGET  61
#define SYS_SEMOP   62
#define SYS_SEMCTL  63
#define SYS_SHMDT   64
#define SYS_MSGGET  65
#define SYS_MSGSND  66
#define SYS_MSGRCV  67
#define SYS_MSGCTL  68

/* ==========================================================================
 * File open flags / 文件打开标志
 * ========================================================================== */

#define O_RDONLY    0
#define O_WRONLY    1
#define O_RDWR      2
#define O_CREAT     0x40
#define O_TRUNC     0x200
#define O_APPEND    0x400
#define O_EXCL      0x80

/* ==========================================================================
 * Standard file descriptors / 标准文件描述符
 * ========================================================================== */

#define STDIN_FILENO  0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2

/* ==========================================================================
 * Memory protection flags / 内存保护标志
 * ========================================================================== */

#define PROT_READ   0x1
#define PROT_WRITE  0x2
#define PROT_EXEC   0x4
#define PROT_NONE   0x0

/* ==========================================================================
 * Memory mapping flags / 内存映射标志
 * ========================================================================== */

#define MAP_SHARED  0x01
#define MAP_PRIVATE 0x02
#define MAP_ANONYMOUS 0x20
#define MAP_FIXED   0x10

/* ==========================================================================
 * Error codes / 错误码
 * ========================================================================== */

#define EOK         0
#define EPERM       1
#define ENOENT      2
#define ESRCH       3
#define EINTR       4
#define EIO         5
#define ENXIO       6
#define E2BIG       7
#define ENOEXEC     8
#define EBADF       9
#define ECHILD      10
#define EAGAIN      11
#define ENOMEM      12
#define EACCES      13
#define EFAULT      14
#define EBUSY       16
#define EEXIST      17
#define EINVAL      22
#define ENFILE      23
#define EMFILE      24
#define ENOSPC      28
#define ENOSYS      38
#define ENOTEMPTY   39
#define ECONNREFUSED 61
#define ETIMEDOUT   60
#define ENETUNREACH 51

/* ==========================================================================
 * Function declarations / 函数声明
 * ========================================================================== */

/* File operations / 文件操作 */
int bamboo_open(const char *path, int flags, int mode);
int bamboo_close(int fd);
int bamboo_read(int fd, void *buf, int count);
int bamboo_write(int fd, const void *buf, int count);
int bamboo_lseek(int fd, int offset, int whence);

/* Process management / 进程管理 */
int bamboo_getpid(void);
int bamboo_fork(void);
int bamboo_execve(const char *path, char *const argv[], char *const envp[]);
void bamboo_exit(int code);
int bamboo_kill(int pid, int signal);

/* Memory management / 内存管理 */
void *bamboo_mmap(void *addr, int length, int prot, int flags, int fd, int offset);
int bamboo_munmap(void *addr, int length);
int bamboo_mprotect(void *addr, int length, int prot);
int bamboo_brk(void *addr);

/* Time / 时间 */
int bamboo_sleep(int seconds);

/* System information / 系统信息 */
int bamboo_uname(struct utsname *buf);
int bamboo_gethostname(char *name, int len);

#ifdef __cplusplus
}
#endif

#endif /* _BAMBOO_H */