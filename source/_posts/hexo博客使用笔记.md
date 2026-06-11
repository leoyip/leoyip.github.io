---
title: Hexo博客使用笔记
date: 2016-03-23 21:16:56
categories: HowWiKi
tags: Hexo
---

持续更新Hexo博客的使用方法和技巧  
<!-- more -->

### [](#如何发布新文章 "如何发布新文章")如何发布新文章

以下为gitbash命令。其他命令行工具，命令有所不同。

```plain
$ hexo new [layout] <title>		# 生成文章 ，不同layout保存路径不同，见下表。

$ cd .deploy_git		# 转到master目录下

$ hexo clean		# 清除旧文档

$ hexo g		# 生成新文档

$ hexo d		# 发布新文档
```

布局

路径

post

source/\_posts

page

source

draft

source/\_drafts

更多内容：[写作](https://hexo.io/zh-cn/docs/writing.html)