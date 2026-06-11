# 星夜航记 — Yip's Blog

> 个人博客，基于 Hexo 构建，部署于 GitHub Pages。
>
> 在线地址：https://leoyip.github.io

---

## 目录结构

```
博客/
├── source/                     # 博客源文件
│   ├── _posts/                 # 📝 文章（Markdown）
│   ├── about/index.md          # 关于页面
│   ├── categories/index.md     # 分类页面
│   ├── tags/index.md           # 标签页面
│   ├── images/                 # 图片资源
│   │   ├── avatar.png          # 头像
│   │   ├── banner.jpg          # 首页横幅
│   │   └── imported/           # 从外部下载的图片
│   └── 404.html                # 404 页面
├── _config.yml                 # Hexo 主配置
├── _config.butterfly.yml       # Butterfly 主题配置
├── scaffolds/                  # 文章模板
├── tools/                      # 导入脚本
├── package.json                # Node.js 依赖
└── README.md                   # 本文件
```

---

## 快速命令

```bash
# 写新文章
hexo new post "文章标题"

# 本地预览
hexo server                    # http://localhost:4000

# 生成静态文件
hexo generate

# 部署到 GitHub Pages
hexo deploy

# 清理缓存（修改配置后建议执行）
hexo clean && hexo generate

# 完整流程
hexo clean && hexo generate && hexo deploy
```

---

## 分支管理

本仓库采用双分支策略：

| 分支 | 内容 | 说明 |
|------|------|------|
| `source` | Hexo 源文件 | 文章、配置、主题设置 |
| `master` | 生成的静态页面 | GitHub Pages 直接发布 |

### 日常操作

```bash
# 1. 写文章（在 source 分支）
git checkout source
hexo new post "新文章标题"
# 编辑 source/_posts/新文章标题.md

# 2. 本地预览
hexo server

# 3. 备份源文件
git add .
git commit -m "feat: 添加新文章"
git push origin source

# 4. 部署上线
hexo clean && hexo generate && hexo deploy
```

---

## 技术栈

| 组件 | 版本/名称 |
|------|-----------|
| 框架 | Hexo 8.x |
| 主题 | Butterfly 5.5.5 |
| 部署 | hexo-deployer-git → GitHub Pages |
| Node.js | >= 22.x |
| 图片处理 | Turndown (HTML→Markdown) |

---

## 文章分类

本博客文章按以下分类组织：

- **技术** — 编程、服务器、运维笔记
- **随笔** — 生活感悟、影评、杂谈
- **HowWiKi** — 教程类（如 Hexo 安装）
- **1000个生活片段** — 生活经历系列
- **书信** — 写信系列
- **草稿** — 未完成的文章
- **读书笔记** — 读书心得

---

## 文章 Frontmatter 格式

每篇 Markdown 文章以 YAML frontmatter 开头：

```yaml
---
title: 文章标题          # 必填
date: 2024-01-01 12:00:00  # 必填，发表日期
categories: 技术           # 可选，分类
tags:                      # 可选，标签
  - Hexo
  - 教程
---
```

文章正文使用 Markdown 格式，支持代码块、图片、表格等。

---

## 主题配置

主题配置在 `_config.butterfly.yml` 中，主要配置项：

```yaml
# 导航菜单
menu:
  首页: / || fa fa-home
  归档: /archives/ || fa fa-archive

# 社交链接
social:
  fab fa-github: https://github.com/leoyip || GitHub

# 首页横幅 subtitle
subtitle:
  enable: true
  effect: true            # 打字机效果
  sub: '副标题文字'

# 主页顶部图
index_img: /images/banner.jpg
```

完整配置说明见：https://butterfly.js.org/posts/4aa8abbe/

---

## 导入工具

`tools/` 目录下包含内容迁移脚本：

| 脚本 | 用途 |
|------|------|
| `import-posts.js` | 从 Hexo 生成的 HTML 导入旧文章 |
| `import-jianshu.js` | 从简书导出文件批量导入 |
| `import-csdn.js` | 从 CSDN 抓取文章（需登录） |
| `download-images.js` | 下载文章中的外部图片到本地 |
| `fix-dates.js` | 从简书 API 修复文章日期 |

---

## 常见问题

### Q: 修改配置后页面没变化？
A: 执行 `hexo clean && hexo generate` 清理缓存再生成。

### Q: 文章显示 "未命名"？
A: 标题若以 `#` 开头，需要在 frontmatter 中用引号包裹：`title: "#标题"`

### Q: 写文章时需要插入图片？
A: 把图片放到 `source/images/` 目录，引用方式：`![描述](/images/图片名.jpg)`

### Q: 如何回滚到 NexT 主题？
A: 取消注释 `_config.yml` 中的 `theme_config` 部分，并设置 `theme: next`

---

## 维护者

- **Leo Yip** — 博客作者

---

## License

博客内容版权归作者所有。
