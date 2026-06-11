---
title: Markdown语法备忘
date: 2016-02-06 18:28:02
categories: 随笔
---

#### 简介
摘自[Markdown wiki](https://zh.wikipedia.org/wiki/Markdown)
> **Markdown** 是一种[轻量级标记语言](https://zh.wikipedia.org/wiki/%E8%BD%BB%E9%87%8F%E7%BA%A7%E6%A0%87%E8%AE%B0%E8%AF%AD%E8%A8%80)，创始人为[约翰·格鲁伯](https://zh.wikipedia.org/w/index.php?title=%E7%B4%84%E7%BF%B0%C2%B7%E6%A0%BC%E9%AD%AF%E4%BC%AF&action=edit&redlink=1)（John Gruber）。它允许人们“使用易读易写的纯文本格式编写文档，然后转换成有效的[XHTML](https://zh.wikipedia.org/wiki/XHTML)(或者[HTML](https://zh.wikipedia.org/wiki/HTML))文档”。[[3]](https://zh.wikipedia.org/wiki/Markdown#cite_note-md-3)
这种语言吸收了很多在[电子邮件](https://zh.wikipedia.org/wiki/%E7%94%B5%E5%AD%90%E9%82%AE%E4%BB%B6)中已有的纯文本标记的特性。

#### 本文结构
1. 标题
- 列表
- 链接和图片
- 引用
- 粗体和斜体
- 表格
- 代码
- 分割线
- 更多

#### 1. 标题
代码：
`# 一级标题`
`## 二级标题`
`### 三级标题`
`#### 四级标题`
`##### 五级标题`
`###### 六级标题`

效果：
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
---
#### 2. 列表

（1）无序列表
代码：
`* 列表一`
`+ 列表二`
`- 列表三`
效果：
* 列表一
+ 列表二
- 列表三

注意：`*  +  -`都可以用来标记无序列表。

---
#### 3. 链接和图片
(1)链接
代码：`[简书](www.jianshu.com)`
效果：[简书](www.jianshu.com)
(2)插入图片
代码：
`![](/images/imported/upload-images-jianshu-io-upload-images-447752-b1cafcf98cc3708b-gif.gif)`
效果：![](/images/imported/upload-images-jianshu-io-upload-images-447752-b1cafcf98cc3708b-gif.gif)

---
#### 4. 引用
代码：`> When you are going through the hell, keep going. —Winston Churchill`
效果：
> When you are going through the hell, keep going. —Winston Churchill

---
#### 5. 粗体和斜体
代码：
`**This is Blod style**
 *This Italic style*`
效果：
**This is Blod style**
 *This Italic style*

---
#### 6. 表格
代码：
`| Table | is | cool |
|-----|:--------:|-----:|
| 第一列 | 靠左显示  |￥1200|
| 第二列 | 居中显示 | ￥200 |
| 第三列 | 靠右显示 | ￥10|`   
效果：

| Table | is | cool |
|-----|:--------:|-----:|
| 第一列 | 靠左显示  |￥1200|
| 第二列 | 居中显示 | ￥200 |
| 第三列 | 靠右显示 | ￥10|
注意：如果不能正常显示，试试在表格前后添加换行。

---
#### 7. 代码
代码：`  \`Hello World\` `
效果：`Hello World`
ps：
>如何插入代码区块
作为程序猿经常要使用代码贴在文章中，而这些代码，我们都要保持它的格式不被修改。在Markdown中，markdown会将代码块使用`<pre>`和`<code>`标签将之包起来。 那么我们如何使用代码块呢?4个空格或者一个TAB。嗯，就是这样简单。

[引用来源：学习Markdown语法笔记](http://snails.github.io/2012/05/08/Learn-to-Markdown/)
---
#### 8. 分割线
代码：`---`
效果：

---
#### 9. 更多
[Markdown 语法说明 (简体中文版) ](http://wowubuntu.com/markdown/)
[献给写作者的 Markdown 新手指南](http://www.jianshu.com/p/q81RER)
