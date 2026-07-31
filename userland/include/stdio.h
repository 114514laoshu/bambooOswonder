/*
 * ============================================================================
 * Module: userland/include/stdio.h
 * 模块：userland/include/stdio.h
 * Description: Standard I/O header
 * 描述：标准 I/O 头文件
 * ============================================================================
 */

#ifndef _STDIO_H
#define _STDIO_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==========================================================================
 * Standard streams / 标准流
 * ========================================================================== */

#define stdin  ((FILE *)0)
#define stdout ((FILE *)1)
#define stderr ((FILE *)2)

/* ==========================================================================
 * Types / 类型
 * ========================================================================== */

typedef struct _FILE FILE;

/* ==========================================================================
 * Functions / 函数
 * ========================================================================== */

/* Formatted output / 格式化输出 */
int printf(const char *fmt, ...);
int fprintf(FILE *stream, const char *fmt, ...);
int sprintf(char *str, const char *fmt, ...);
int snprintf(char *str, size_t size, const char *fmt, ...);

/* Formatted input / 格式化输入 */
int scanf(const char *fmt, ...);
int fscanf(FILE *stream, const char *fmt, ...);
int sscanf(const char *str, const char *fmt, ...);

/* Character I/O / 字符 I/O */
int getchar(void);
int putchar(int c);
int fgetc(FILE *stream);
int fputc(int c, FILE *stream);

/* String I/O / 字符串 I/O */
char *fgets(char *s, int size, FILE *stream);
int fputs(const char *s, FILE *stream);

/* File operations / 文件操作 */
FILE *fopen(const char *path, const char *mode);
int fclose(FILE *stream);
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream);
int fseek(FILE *stream, long offset, int whence);
long ftell(FILE *stream);
void rewind(FILE *stream);

/* Error handling / 错误处理 */
void perror(const char *s);
int feof(FILE *stream);
int ferror(FILE *stream);

#ifdef __cplusplus
}
#endif

#endif /* _STDIO_H */