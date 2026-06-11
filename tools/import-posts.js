const fs = require('fs');
const path = require('path');
const TurndownService = require('turndown');

const turndown = new TurndownService({
  headingStyle: 'atx',
  codeBlockStyle: 'fenced',
  emDelimiter: '*',
  bulletListMarker: '-',
});

// Keep <a id="more"></a> as-it-is for excerpt
turndown.addRule('moreTag', {
  filter: (node) => {
    return node.tagName === 'A' && node.id === 'more';
  },
  replacement: () => '<!-- more -->\n\n',
});

// Convert highlight figure blocks to code blocks
turndown.addRule('hexoCodeBlock', {
  filter: (node) => {
    return node.tagName === 'FIGURE' && node.classList.contains('highlight');
  },
  replacement: (content, node) => {
    const code = node.querySelector('code');
    const table = node.querySelector('table');
    let codeContent = '';

    if (table) {
      // Has line numbers - extract code lines
      const lines = table.querySelectorAll('.code .line');
      codeContent = Array.from(lines).map(l => l.textContent).join('\n');
    } else if (code) {
      codeContent = code.textContent;
    } else {
      codeContent = node.textContent;
    }

    const lang = node.className.match(/highlight\s+(\w+)/)?.[1] || '';
    return '\n```' + lang + '\n' + codeContent + '\n```\n\n';
  },
});

// Convert img tags
turndown.addRule('images', {
  filter: 'img',
  replacement: (content, node) => {
    const alt = node.alt || '';
    const src = node.src || '';
    const width = node.getAttribute('width');
    const style = node.getAttribute('style');

    let markdown = `![${alt}](${src})`;
    if (width) markdown = `<img src="${src}" alt="${alt}" width="${width}">`;

    return markdown;
  },
});

function parseArticle(filePath) {
  const html = fs.readFileSync(filePath, 'utf-8');

  // Extract title
  const titleMatch = html.match(/<h1 class="post-title"[^>]*>([\s\S]*?)<\/h1>/);
  const title = titleMatch ? titleMatch[1].trim() : 'Untitled';

  // Extract date from time tag
  const dateRegex = new RegExp('<time[^>]+datetime="([^"]+)"');
  const dateMatch = html.match(dateRegex);
  const date = dateMatch ? dateMatch[1] : '';

  // Extract categories
  const categories = [];
  const catRegex = /<span itemprop="name">([^<]+)<\/span>/g;
  let catMatch;
  // Only get categories from the sidebar/post-meta area (before post-body)
  const metaSection = html.split('post-body')[0];
  while ((catMatch = catRegex.exec(metaSection)) !== null) {
    categories.push(catMatch[1]);
  }

  // Extract tags
  const tags = [];
  const tagRegex = /<a href="\/tags\/([^"/]+)\/" rel="tag">#([^<]+)<\/a>/g;
  let tagMatch;
  while ((tagMatch = tagRegex.exec(html)) !== null) {
    tags.push(tagMatch[2] || tagMatch[1]);
  }

  // Extract body content
  const bodyMatch = html.match(/<div class="post-body" itemprop="articleBody">([\s\S]*?)<\/div>\s*<div>/);
  let bodyHtml = '';
  if (bodyMatch) {
    bodyHtml = bodyMatch[1].trim();
    // Remove the "阅读更多" anchor and extra content after more tag
    // Keep the <!-- more --> tag for excerpt
  } else {
    console.warn(`  ⚠ No body found in ${filePath}`);
  }

  // Clean up HTML: remove unnecessary br/empty tags
  bodyHtml = bodyHtml.replace(/<br>\s*<br>/g, '\n');
  bodyHtml = bodyHtml.replace(/<p><br><\/p>/g, '');
  bodyHtml = bodyHtml.replace(/<a><\/a>/g, '');

  // Convert HTML to Markdown
  let markdown = turndown.turndown(bodyHtml);

  // Clean up excessive newlines
  markdown = markdown.replace(/\n{4,}/g, '\n\n\n');

  return { title, date, categories, tags, markdown };
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  const pad = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function createFrontMatter(article) {
  let front = '---\n';
  // Quote title if it starts with special YAML characters
  const safeTitle = article.title.startsWith('#') ? `"${article.title}"` : article.title;
  front += `title: ${safeTitle}\n`;
  front += `date: ${formatDate(article.date)}\n`;

  if (article.categories.length > 0) {
    if (article.categories.length === 1) {
      front += `categories: ${article.categories[0]}\n`;
    } else {
      front += 'categories:\n';
      article.categories.forEach(c => front += `  - ${c}\n`);
    }
  }

  if (article.tags.length > 0) {
    if (article.tags.length === 1) {
      front += `tags: ${article.tags[0]}\n`;
    } else {
      front += 'tags:\n';
      article.tags.forEach(t => front += `  - ${t}\n`);
    }
  }

  front += '---\n\n';
  return front;
}

function buildSlug(title) {
  // Generate a filesystem-safe slug
  return title
    .replace(/[/\\?%*:|"<>]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .toLowerCase();
}

// Main
const postsDir = path.join(__dirname, '..');
const outputDir = path.join(postsDir, 'source', '_posts');

// Find all old article HTML files
const articlePaths = [];
function findArticles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && !entry.name.startsWith('.') && !['node_modules', 'public', 'vendors', 'css', 'js', 'images', 'fonts', 'scaffolds', 'source', 'themes', 'scripts', '.git'].includes(entry.name)) {
      findArticles(fullPath);
    } else if (entry.name === 'index.html' && dir.match(/\/\d{4}\/\d{2}\/\d{2}\//)) {
      articlePaths.push(fullPath);
    }
  }
}
findArticles(postsDir);

console.log(`Found ${articlePaths.length} articles:\n`);

let successCount = 0;
for (const filePath of articlePaths) {
  console.log(`Processing: ${path.relative(postsDir, filePath)}`);

  try {
    const article = parseArticle(filePath);

    if (!article.markdown || article.markdown.trim().length < 10) {
      console.warn(`  ⚠ Skipping (content too short or empty)`);
      continue;
    }

    const frontMatter = createFrontMatter(article);
    const slug = buildSlug(article.title);
    const outputFile = path.join(outputDir, `${slug}.md`);

    fs.writeFileSync(outputFile, frontMatter + article.markdown, 'utf-8');
    console.log(`  ✅ Created: ${slug}.md`);
    console.log(`     Title: ${article.title}`);
    console.log(`     Date:  ${formatDate(article.date)}`);
    console.log(`     Tags:  [${article.tags.join(', ')}]`);
    successCount++;
  } catch (err) {
    console.error(`  ❌ Error: ${err.message}`);
  }
  console.log('');
}

console.log(`\nDone! ${successCount}/${articlePaths.length} articles imported.`);
