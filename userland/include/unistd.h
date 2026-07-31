/*
 * ============================================================================
 * Module: userland/include/unistd.h
 * 模块：userland/include/unistd.h
 * Description: POSIX system calls header
 * 描述：POSIX 系统调用头文件
 * ============================================================================
 */

#ifndef _UNISTD_H
#define _UNISTD_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==========================================================================
 * Standard file descriptors / 标准文件描述符
 * ========================================================================== */

#define STDIN_FILENO  0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2

/* ==========================================================================
 * File seek flags / 文件定位标志
 * ========================================================================== */

#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

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
 * Function declarations / 函数声明
 * ========================================================================== */

/* File operations / 文件操作 */
int open(const char *path, int flags, ...);
int close(int fd);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
off_t lseek(int fd, off_t offset, int whence);
int unlink(const char *path);
int rename(const char *old, const char *new);
int mkdir(const char *path, mode_t mode);
int rmdir(const char *path);
int chdir(const char *path);
char *getcwd(char *buf, size_t size);

/* Process management / 进程管理 */
pid_t getpid(void);
pid_t getppid(void);
pid_t fork(void);
int execve(const char *path, char *const argv[], char *const envp[]);
int execvp(const char *file, char *const argv[]);
void exit(int status);
pid_t wait(int *status);
pid_t waitpid(pid_t pid, int *status, int options);
int kill(pid_t pid, int sig);

/* Time / 时间 */
unsigned int sleep(unsigned int seconds);
int usleep(useconds_t usec);
time_t time(time_t *t);

/* System information / 系统信息 */
int uname(struct utsname *buf);
int gethostname(char *name, size_t len);
int sethostname(const char *name, size_t len);

/* User/Group / 用户/组 */
uid_t getuid(void);
gid_t getgid(void);
uid_t geteuid(void);
gid_t getegid(void);

/* Pipes / 管道 */
int pipe(int pipefd[2]);
int dup(int fd);
int dup2(int oldfd, int newfd);

#ifdef __cplusplus
}
#endif

#endif /* _UNISTD_H */