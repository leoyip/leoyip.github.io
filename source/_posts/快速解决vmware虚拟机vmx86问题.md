---
title: 快速解决Vmware虚拟机 vmx86问题
date: 2015-01-01 12:00:00
categories: 技术
tags:
  - VMware
  - 虚拟机
---

你的vmware虚拟机如果提示这个错误：

> Unable to open kernel device "\\.\Global\vmx86": 系统找不到指定的文件. Did you reboot after installing VMware Workstation?
> Failed to initialize monitor device.

试一下这个方法：

1、关闭虚拟机，下载绿色破解版Vmware，得到vmware安装包

2、解压得到一个文件夹，在此文件夹中搜索"vmx86.sys"，复制

3、进入这个路径：C:\Windows\System32\drivers ，搜索"vmx86.sys"，若存在这个文件则替换（注意备份被替换文件），不存在就直接粘贴

4、在开始菜单"运行"输入：net start vmx86，按确定；

5、启动虚拟机，一切又恢复正常。

注：该方法亲测可行，部分步骤参考网络，请读者结合爱机实际进行操作。
