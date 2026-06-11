---
title: 如何检测局网内哪些ip被占用
date: 2015-01-02 12:00:00
categories: 技术
tags:
  - 网络
  - Windows
---

情景：

网络中心新增设备，需要了解还有那些IP可用，因此要批量测试ip的连通性。

思路：

首先，使用Windows批处理命令进行ping测试，通过ping的IP说明已被使用而且ping的通；
但是也有可能部分设备禁ping，所以还要获取ARP缓存查看局域网上哪些IP被占用；
最后，ARP缓存中没有出现的IP设置到计算机上，看看能否访问Internet。

步骤：

1、由于要批量ping测试，最好使用自动化处理的命令：

```
FOR /L %%i IN (130,1,240) Do ping 222.200.98.%%i -n 1 >> pingtest.txt
```

这条命令表示自动ping 222.200.98.130-222.200.98.240 间每个IP，每个IP检测时只发送一个数据包"-n 1"，">> pingtest.txt"表示ping的结果添加到文本文件pingtest中去，以备查看。

2、使用"arp -a"命令获取arp缓存，保存到arp-mac文本文件中。

```
arp -a>>d:\arp-mac.txt
```

3、根据 pingtest.txt 和 arp-mac.txt 可以知道ping不通又不在arp缓存上的那部分IP，由此我们可以得到一张表iplist。我们可以据iplist进行设置。

为了简化工作量，我们使用命令来设置IP：

```
netsh interface ip set address "连接名称" static 静态IP 掩码 网关
```

连接名称一般是"本地连接"，分别替换"静态IP"、"掩码"和"网关"，接着我们还需设置DNS：

```
netsh interface ip set dns "以太网" static 114.114.114.114
```

运行即可完成设置。

也可以通过命令来设置DHCP：

```
netsh interface ip set address name="本地连接" source=dhcp
```

显示设置结果：

```
netsh interface ip show address
```

参考博客：

在windows下使用命令行修改IP地址的方法

windows命令行修改ip地址和dns服务器地址的方法

如何检测网内IP地址是否被占用(组图)
