---
title: Hexo博客安装与更新-1
date: 2016-03-19 23:07:40
categories: HowWiKi
tags: Hexo
---

个人安装Hexo的记录  
<!-- more -->

### [](#安装步骤 "安装步骤")安装步骤

网络上关于 Hexo博客的安装教程已经多如牛毛，我觉得自己没有必要重复造轮子。安装教程大多数基于windows环境，其实linux环境下也大同小异的。  
大体步骤如下：

1.  了解Hexo ：[hexo.io](http://hexo.io/)
2.  安装git ：[GitHub Windows](https://windows.github.com/)
3.  安装Node.js : [Node.js](http://nodejs.org/)
4.  Hexo初始化配置 : [Hexo Setup](https://hexo.io/zh-cn/docs/setup.html)
5.  部署静态网页到GitHub

详细步骤参考：[使用GitHub和Hexo搭建免费静态Blog](http://wsgzao.github.io/post/hexo-guide/)

### [](#问题及解决 "问题及解决")问题及解决

下面主要我在建站过程中遇到的问题和解决方法，仅供参考。

#### [](#yml文件忘加空格错误 "yml文件忘加空格错误")yml文件忘加空格错误

安装Hexo时，在配置\_config.yml文件的过程中，如果参数冒号后面忘记加空格就会报错：

> FATAL can not read a block mapping entry; a multiline key may not be an implicit key at line 8, column 12

解决办法：yml文件格式问题，你自己检查一下是不是冒号后面没有写空格。

#### [](#npm-警告 "npm 警告")npm 警告

提示如下：

> npm WARN optional dep failed, continuing [fsevents@1.0.8](mailto:fsevents@1.0.8)

目前没有去解决，似乎不会影响建站。

[github 讨论](https://github.com/foreverjs/forever/issues/788)

#### [](#缺少-git文件报错 "缺少.git文件报错")缺少.git文件报错

发生环节:windows下，将本地Hexo部署到github时。  
将会有以下几种错误提示：  

```plain
spawn git ENOENT

ERROR Deployer not found: github

fatal: Not a git repository (or any of the parent directories): .git
```

截图如下：

解决方案：**在Hexo的安装目录下生成.git文件**，然后deploy一下。  
随后有可能会遇到版本不一致的问题，需要同步一下。

具体操作：

1.  检查blog blog 目录下的 \_config.yml 文件

```plain
deploy:</br>
type: git</br>
repo: git@github.com:xxx/xxx.github.io.git #不是github@</br>
branch: master
```

2.  安装插件  
    npm install hexo-deployer-git –save
    
3.  发布页面  
    hexo g #创建静态页面  
    hexo d #发布：清空.deploy\_git/里文件，从public/复制新生成的文件
    
4.  解决`fatal: Not a git repository (or any of the parent directories)`错误  
    使用everything搜索隐藏目录下的.git文件复制到Hexo文件的`.deploy_git`目录下。再次运行`hexo d`。
    
5.  如果上一步骤出现`Permission denied`或者提示版本不一致问题，首先cd 到`.deploy_git`下，然后处理版本问题。  
    6.git版本冲突问题解决
    

```plain
git init #解决fatal: Not a git repository (or any of the parent directories): .git

git pull #拉到本地

git merge #测试版本一致性

git push #再次发布
```

我的Hexo下，**.git**安装路径为  
`E:\hexo\blog\\.deploy_git\\.git`  
是由于远程仓库中代码版本与本地不一致冲突导致的。

解决：  
`git pull`  
再自动merge或手动merge冲突,  
再次git push,  
成功解决问题。

参考：[Git push 报错](http://blog.sina.com.cn/s/blog_5f2ca1ed010167hs.html)

#### [](#无法访问github-com错误 "无法访问github.com错误")无法访问github.com错误

`Fatal Error : Can't resolve host github.com`

我遇到的只是暂时性无法访问，多试几次就可以了。

### [](#扩展阅读 "扩展阅读")扩展阅读

1.  [Yip’s Blog](http://leoyip.github.io)
2.  [我的github主页](https://github.com/leoyip)
3.  [Pro Git book](https://git-scm.com/book/zh/v2)
4.  [Hexo文档](https://hexo.io/zh-cn/docs/)
5.  [七牛图床](https://portal.qiniu.com/)
6.  [Markdown 语法说明 (简体中文版)](http://wowubuntu.com/markdown/)
7.  [w3school](http://www.w3school.com.cn/)
8.  [Hexo常见问题解决方案](https://xuanwo.org/2014/08/14/hexo-usual-problem/)  
      
    

### [](#参考博客 "参考博客")参考博客

-   [hexo你的博客](http://ibruce.info/2013/11/22/hexo-your-blog/)
-   [Hexo(一)：在GitHub上搭建静态博客](http://blog.hjtxxx.com/2015/08/13/Hexo-%E4%B8%80-%EF%BC%9A%E5%9C%A8GitHub%E4%B8%8A%E6%90%AD%E5%BB%BA%E9%9D%99%E6%80%81%E5%8D%9A%E5%AE%A2/)
-   [Hexo GitHub Pages 搭建个人博客的心酸历程](http://huyaohui.com/2015/03/22/Hexo-GitHub-Pages-%E6%90%AD%E5%BB%BA%E4%B8%AA%E4%BA%BA%E5%8D%9A%E5%AE%A2%E7%9A%84%E5%BF%83%E9%85%B8%E5%8E%86%E7%A8%8B/)
-   [jackraken’s blog](http://jackraken.github.io/2014/07/16/new_post2/)
-   [解决使用hexo -d提交不了blog的问题](http://blog.52fhy.com/2015/07/05/hexo/solve_hexo_-d_problem/)