---
title: xcode上编译c语言程序报错：重复符号
date: 2015-01-09 12:00:00
categories: 技术
tags:
  - Xcode
  - C语言
  - 编译错误
---

最近使用Xcode编译C语言程序，发现在多文件运行时总会有error提示：

```
ld: 1 duplicate symbol for architecture x86_64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

在网上查了一下：

`duplicate symbol` 的大概意思是，编译器认为你重复定义了一些东西。

`linker command failed with exit code 1`，则可能是项目引入了多个相同的文件。

## 解决方法

先看看main.c文件是不是包含了自己写的.c文件，例如：

```c
#include "addressPrint.c"
```

如果是，删除该语句，使用到自定义文件的函数前声明一下，Ok。

```c
void print1(int *ptr, int rows);

int main(int argc, const char * argv[])
{
    // insert code here...
    printf("Hello, World!\n");
    int one[] = {0,1,2,3,4};
    print1(one, 5);
    return 0;
}
```

编译器会自动找到在 `addressPrint.c` 文件里的方法：

```c
void print1(int *ptr, int rows) {
    /*
     print out a one-dimensional array using a pointer
     */
    int i;
    printf("Address Contents\n");
    for (i = 0; i < rows; i++) {
        printf("%8u%5d\n", ptr + i, *(ptr + i));
    }
    printf("\n");
}
```
