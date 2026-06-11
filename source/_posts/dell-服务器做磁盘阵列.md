---
title: Dell-服务器做磁盘阵列
date: 2017-01-19 20:06:51
categories: 技术
---

# 前言
这是Dell服务器装机教程的第1篇，全系列包括：

1. [Dell服务器做磁盘阵列](http://www.jianshu.com/p/59826ffecbaf)
2. [Dell 服务器安装 Windows 2008 R2 操作系统](http://www.jianshu.com/p/0f567a0126bf)
3. [Dell服务器简单配置](http://www.jianshu.com/p/ea9ec683d319)

在安装系统前，需要做一些准备工作。做磁盘阵列以保护服务器的数据安全，设置适当的条带宽度以提高服务器的I/O性能。限于篇幅，本文不介绍磁盘阵列以及条带大小的背景知识，只讲解设置的步骤。

步骤预览：
1.  进入设备管理平台
2.  清除旧的设置
3.  创建新的虚拟磁盘
4.  采用剩余的空间创建虚拟磁盘
5.  检查虚拟盘配置是否正确
6.  设置BOOT sequence，从光盘或U盘启动

# 1. 进入设备管理平台

- 启动服务器，过了黑屏背景的页面后，出现蓝屏页面，按提示按F2进入System Setup界面。
 ![](/images/imported/upload-images-jianshu-io-upload-images-447752-b75bbd2f2a6e3380-jpg.jpg)

- 在System Setting Main Menu下面选择Device Setting
![figure_03](/images/imported/upload-images-jianshu-io-upload-images-447752-1d85f2b4edbfaf09-jpg.jpg)

- 选择第一个RAID Controller
![figure_04](/images/imported/upload-images-jianshu-io-upload-images-447752-d1604dc3c1828d66-jpg.jpg)

# 2. 清除旧的设置

- 点击进入配置管理（Configuration Management）
![](/images/imported/upload-images-jianshu-io-upload-images-447752-d5dc0cc10d983b73-jpg.jpg)
- 清理旧的设置
![](/images/imported/upload-images-jianshu-io-upload-images-447752-d832f048a1baa4ec-jpg.jpg)
- 确认
- 退回到Main Menu。

# 3. 创建新的虚拟磁盘
-  重新进入Configuration management,点击创建虚拟盘。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-ceedb67462f6a52b-jpg.jpg)
- 选择磁盘阵列类型。一般两个磁盘做阵列选择Raid 1，五个以上选择Raid 5。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-2d7a89b98098eb80-jpg.jpg)
- 选择磁盘。点击**Select Physical Disks**，进入磁盘选择页面。选择SSD和HDD切换固态硬盘列表和机械盘列表。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-cebfe48edf2e278b-jpg.jpg)
- 设置虚拟盘名字、大小、条带大小，其他参数采用默认。个人选择系统盘大小为80GB，所有磁盘的条带大小都为128KB。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-33421af85b63e835-jpg.jpg)
- 点击左下角**Creat Virtual Disk**,确认创建虚拟盘。

# 4. 采用剩余的空间创建虚拟磁盘
部分磁盘做完阵列，创建一个虚拟盘之后还有剩余空间，可以用来创建其他的虚拟盘，这里讲解如何用剩余阵列空间创建虚拟磁盘。

- 选择RAID类型。个人Raid 1的磁盘还没有用完，故使用Raid 1。勾选**Free Capacity**，然后再点击**Select Physical Disks**，进入磁盘选择页面。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-a4870b83317f088c-jpg.jpg)

- 选择剩空间。勾选一个你要使用的**Disk Group**,如果有多个未用完的磁盘阵列则会有多个group。这座这里只有一个。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-dda322ff19bb6ef8-jpg.jpg)
- 够选好**Disk Group**后点击**Apply Change**保存设置，返回上一级菜单设置虚拟盘名字、大小、以及条带大小，与步骤3类似。

# 5. 检查虚拟盘配置是否正确
做完磁盘阵列的设置后，有必要及时进行检查，避免出错。

- 返回Main Menu，点击**Virtual Disk Management**进入虚拟盘管理页面
![](/images/imported/upload-images-jianshu-io-upload-images-447752-d5dc0cc10d983b73-jpg.jpg)
- 虚拟盘管理页面会显示已经设置好的虚拟盘列表，依次点击查看详细信息。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-56ceb496c73122b6-jpg.jpg)
- 点击高级选项可以查看条带大小信息
![](/images/imported/upload-images-jianshu-io-upload-images-447752-f517764a29cdc918-jpg.jpg)

![](/images/imported/upload-images-jianshu-io-upload-images-447752-d095946ae99f4abd-jpg.jpg)
- 如果确认无误则无需更改直接退出。

# 6. 设置BOOT sequence，从光盘或U盘启动
做好磁盘阵列之后，为了确保接下来正常安装系统，需要设置服务器的启动顺序。这个设置可以在系统设置主菜单下，点击系统引导系统进入设置

- 返回System Setup Main Menu，点击进入System BIOS。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-88a91c2b2ca1f352-jpg.jpg)
- 点击进入BIOS Setting
![](/images/imported/upload-images-jianshu-io-upload-images-447752-05c655e26d982327-jpg.jpg)
- 点击进入 Boot Sequence。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-4ce5249e42952c3b-jpg.jpg)
- 更改启动顺序。选中设备，点击加号上移，减号下移。服务器启动时会从上到下一次查询设备，从最先查询到的设备启动。
![](/images/imported/upload-images-jianshu-io-upload-images-447752-2629279e2793d5ff-jpg.jpg)
