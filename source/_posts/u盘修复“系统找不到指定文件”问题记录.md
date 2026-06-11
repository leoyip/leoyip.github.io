---
title: U盘修复“系统找不到指定文件”问题记录
date: 2017-06-25 16:38:06
categories: 技术
---

很久以前手贱，在Mac上格式化U盘，然后发现U盘插回PC已经用不了。U盘闲置了一段时间后，最近尝试修复，最终还是失败了。明显用不了的的表现是：
> U盘无法识别，磁盘管理中格式化时提示“系统找不到指定文件”

## 先说解决方法
评论区周某某先生提供了这个方法，已经有两位网友依法炮制，修复了U盘：
> 遇到一样的情况，但是找到一种方法可以修复
1、在cmd中运行 diskpart 回车，然后输入list disk回车，查看目前电脑上所有的磁盘，如果U盘为1，那么输入以下命令将焦点指定到该磁盘select disk 1回车，然后再输入clean,这时候系统提示出错系统找不到指定文件，但是（很重要的一点），U盘此时已经有盘符了，只是无法格式化，也没有信息
2、在1的基础上（U盘有盘符），下载一个U盘格式化工具（[http://www.upantool.com/hfxf/xiufu/2015/FormatTool.html#softdown](http://www.upantool.com/hfxf/xiufu/2015/FormatTool.html#softdown)），然后选择U盘盘符进行格式化，格式化成功。

<后面的可以不看了>

---

## 尝试使用DiskGenius格式化U盘，没有成功
操作步骤参考：[U盘无法识别，磁盘管理中格式化时提示“系统找不到指定文件”的解决方法](https://blog.csdn.net/github_29503619/article/details/46748111)

## 尝试diskpart修复u盘，失败
参考资料：[U盘无法设定盘符。系统找不到指定的文件？ - 有一个人的回答 - 知乎](
https://www.zhihu.com/question/38024355/answer/218344753)
**操作步骤**：
1. win+r 打开运行，输入：`C:\Windows\System32\diskpart.exe` 运行**diskpart.exe**。
2. 依次输入以下命令：
```
DISKPART> sel
DISKPART> list disk
DISKPART> sel disk 1
DISKPART> clean
```
我遇到的问题是，输入`clean`命令后，提示：
````
DiskPart 遇到错误: 拒绝访问。
有关详细信息，请参阅系统事件日志。 
````

<del> 后来度娘显示，有可能是U盘坏了，建议新购··· 

## 写在最后
如果朋友你也遇到这种情况，找到了解决方法，请联系我 /摊手</del>
