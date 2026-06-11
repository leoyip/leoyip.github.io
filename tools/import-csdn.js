const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const TurndownService = require('turndown');

// CSDN cookie from user
const COOKIE = 'uuid_tt_dd=10_19017996660-1776351706626-982426; UserName=u010282836; UserNick=aHowl; UN=u010282836; AU=C85';

// Parse cookie string into array
const cookies = COOKIE.split('; ').map(c => {
  const [name, value] = c.split('=');
  return { name, value, domain: '.blog.csdn.net', path: '/' };
});

// Articles to import (new ones not already in blog)
const articles = [
  { id: '16832303', title: '快速解决Vmware虚拟机 vmx86问题' },
  { id: '50608325', title: 'vi-vim基本使用方法' },
  { id: '42008117', title: '如何检测局网内哪些ip被占用' },
  { id: '41382359', title: '在vSphere Web Client中恢复孤立的虚拟机' },
  { id: '39562965', title: 'HP的iLO技术' },
  { id: '39483655', title: '用软件查看内存大小和插槽数' },
  { id: '38796427', title: 'ios编程笔记之' },
  { id: '37504035', title: 'swift语言之fallthrough' },
  { id: '37311681', title: 'swift学习笔记' },
  { id: '37345779', title: 'swift学习关于断言' },
  { id: '34417957', title: '玩机笔记' },
  { id: '26243895', title: '控件使用部分链接' },
  { id: '25989005', title: '大小写转换的一种方法' },
  { id: '25971723', title: '稀疏矩阵的转置' },
  { id: '25957647', title: 'C语言枚举类型enum' },
  { id: '25957361', title: 'C语言共用体' },
  { id: '25954997', title: 'xcode编译c语言报错重复符号' },
];

const postsDir = path.join(__dirname, '..', 'source', '_posts');
const turndown = new TurndownService({ headingStyle: 'atx', codeBlockStyle: 'fenced' });

async function fetchArticle(browser, id, title) {
  const page = await browser.newPage();

  try {
    // Set cookies
    await page.context().addCookies(cookies.map(c => ({
      ...c,
      domain: c.domain,
      path: c.path
    })));

    // Navigate to article
    const url = `https://blog.csdn.net/u010282836/article/details/${id}`;
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    // Wait for article content
    await page.waitForSelector('#articleContentId, .article_content', { timeout: 15000 }).catch(() => {});

    // Extract data
    const result = await page.evaluate(() => {
      const title = document.querySelector('#articleContentId')?.textContent?.trim()
        || document.querySelector('h1')?.textContent?.trim()
        || document.title?.replace(' - CSDN博客', '');

      const content = document.querySelector('.article_content')?.innerHTML
        || document.querySelector('#article_content')?.innerHTML
        || '';

      const date = document.querySelector('.article-header-info .date')?.textContent?.trim()
        || document.querySelector('.article-info .date')?.textContent?.trim()
        || '';

      const tags = [...document.querySelectorAll('.tags-box a, .article-tags a')].map(a => a.textContent.trim());

      return { title, content, date, tags };
    });

    return result;
  } catch (e) {
    console.error(`  ❌ ${title}: ${e.message}`);
    return null;
  } finally {
    await page.close();
  }
}

async function main() {
  console.log(`Launching browser...`);
  const browser = await chromium.launch({ headless: true });

  let success = 0;
  let fail = 0;

  for (const article of articles) {
    console.log(`\n📡 Fetching: ${article.title}...`);
    const result = await fetchArticle(browser, article.id, article.title);

    if (!result || !result.content || result.content.length < 50) {
      console.log(`  ⏭ No content (behind paywall or JS issue)`);
      fail++;
      continue;
    }

    const title = result.title || article.title;
    const slug = title.replace(/[/\\?%*:|"<>#]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '').toLowerCase();
    const markdown = turndown.turndown(result.content);

    // Build frontmatter
    let frontmatter = '---\n';
    frontmatter += `title: ${title}\n`;
    frontmatter += `date: 2015-01-01 12:00:00\n`;
    frontmatter += `categories: 技术\n`;
    if (result.tags && result.tags.length > 0) {
      frontmatter += 'tags:\n';
      result.tags.forEach(t => frontmatter += `  - ${t}\n`);
    }
    frontmatter += '---\n\n';

    const destFile = path.join(postsDir, `${slug}.md`);
    fs.writeFileSync(destFile, frontmatter + markdown + '\n', 'utf-8');
    console.log(`  ✅ Created: ${slug}.md (${markdown.length} chars)`);
    success++;
  }

  await browser.close();
  console.log(`\nDone! ${success} imported, ${fail} failed`);
}

main().catch(console.error);
