/*
 * ============================================================================
 * Module: userland/include/string.h
 * 模块：userland/include/string.h
 * Description: String operations header
 * 描述：字符串操作头文件
 * ============================================================================
 */

#ifndef _STRING_H
#define _STRING_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==========================================================================
 * Functions / 函数
 * ========================================================================== */

/* String length / 字符串长度 */
size_t strlen(const char *s);
size_t strnlen(const char *s, size_t maxlen);

/* String copy / 字符串复制 */
char *strcpy(char *dest, const char *src);
char *strncpy(char *dest, const char *src, size_t n);
char *strdup(const char *s);
char *strndup(const char *s, size_t n);

/* String concatenation / 字符串连接 */
char *strcat(char *dest, const char *src);
char *strncat(char *dest, const char *src, size_t n);

/* String comparison / 字符串比较 */
int strcmp(const char *a, const char *b);
int strncmp(const char *a, const char *b, size_t n);
int strcasecmp(const char *a, const char *b);
int strncasecmp(const char *a, const char *b, size_t n);

/* String search / 字符串搜索 */
char *strchr(const char *s, int c);
char *strrchr(const char *s, int c);
char *strstr(const char *s, const char *substr);
char *strcasestr(const char *s, const char *substr);

/* String tokenization / 字符串分词 */
char *strtok(char *s, const char *delim);
char *strtok_r(char *s, const char *delim, char **saveptr);

/* Memory functions / 内存函数 */
void *memcpy(void *dest, const void *src, size_t n);
void *memmove(void *dest, const void *src, size_t n);
void *memset(void *s, int c, size_t n);
int memcmp(const void *a, const void *b, size_t n);
void *memchr(const void *s, int c, size_t n);

/* Error messages / 错误消息 */
char *strerror(int errnum);

/* String conversion / 字符串转换 */
char *strlwr(char *s);
char *strupr(char *s);

#ifdef __cplusplus
}
#endif

#endif /* _STRING_H */