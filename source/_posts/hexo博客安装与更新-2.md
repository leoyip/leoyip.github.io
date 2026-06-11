---
title: Hexo博客安装与更新-2
date: 2016-03-23 20:25:32
categories: HowWiKi
tags: Hexo
---

修复博客主页显示异常和发布后无法更新的两大问题。  
<!-- more -->

### [](#主页显示异常 "主页显示异常")主页显示异常

在前几天博客发布成功后，发现主页排版混乱，拖了几天，今晚终于上去修复主页。

因为同时还存在发布后无法更新的问题，没办法在本地更新页面，于是我直接上github更改。（我也不知道自己为什么不先去修复更新问题、或者在github  
Desktop更改也是可以的）

通过查看主页的index.html文件，发现有两个`<html/>`标签，文件头部和尾部有一些乱码，推断可能是我没有clean掉上一版本，所以导致新旧代码混乱。

我把多余的旧的代码删除后，主页显示正常。

### [](#发布后无法更新问题 "发布后无法更新问题")发布后无法更新问题

在执行`hexo d`命令时报错：  

```plain
FATAL Warning: Permanently added 'github.com,192.30.252.131' (RSA) to the list of known hosts.
ERROR: Repository not found.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.

Error: Warning: Permanently added 'github.com,192.30.252.131' (RSA) to the list of known hosts.
ERROR: Repository not found.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

通过排查，发现是配置文件的参数问题，在\_config.yml文件中，原来配置是这样：  

```plain
deploy:
  type: git	#部署工具的类型
  repository: git@github.com:leoyip/leoyip.github.io.github #SSH链接
  branch: master 	#分支
```

然后主要将`repository`后面的链接域名错误，域名应该是`.git`，改回来即可。

### [](#更新博客 "更新博客")更新博客

完成了以上的修改，应该马上更新博客，测试一下。执行以下命令：  

```plain
cd /.deploy_git		# master权限
hexo clean		# 清除旧文件
hexo g		# 生成新文件
hexo d		# 发布到 github page
```

### [](#存疑 "存疑")存疑

在搜索`ERROR: Repository not found.`的解决方法时，发现github上面讨论的这个问题：

[Error occurs when deploy to Github Pages #648](https://github.com/hexojs/hexo/issues/648)

问题的大概意思是要检查Repository的URL是否正确，要输入命令  

```plain
cd .deploy
git remote -v
`
```

查看，正常结果是：  

```plain
github  git@github.com:paprikachan/paprikachan.github.io.git (fetch)
github  git@github.com:paprikachan/paprikachan.github.io.git (push)
```

异常结果是：  

```plain
origin   https://github.com/metasean/metasean.github.io.git (fetch)
origin   https://github.com/metasean/metasean.github.io.git (push)
```

然后在相关问题下，jr0cket 对出现这种异常的解释是：

> I suspect this because your \_config.yml file has the URL in the form of [git@github.com](mailto:git@github.com):metasean/metasean.github.io.git where as the above result of git remote -v is using the https form of the URL.

> Please confirm  
> 1) You have a .deploy directory which contains a .git directory  
> 2) The output of the git remote -v command from within the metasean.github.io/.deploy directory  
> 3) That you are running the command in order hexo init metasean.github.io, cd metasean.github.io, edit the \_config.yml to add the github configuration, hexo generate, hexo deploy.

然后我才去检查\_config.yml文件，结果真的是github的域名写错了。

改正过来之后，再次检查Repository的URL是否正确，结果还是异常，但是博客已经可以正常更新了。奇了个怪。