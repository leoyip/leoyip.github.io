const fs = require('fs');
const path = require('path');

const srcDir = '/tmp/jianshu-posts/user-447752-1781162459';
const destDir = path.join(__dirname, '..', 'source', '_posts');

// Category mapping
const CATEGORY_MAP = {
  '文章': '随笔',
  '随笔': '随笔',
  '技术笔记': '技术',
  '给你写的信': '书信',
  '草稿箱': '草稿',
};

// Check for duplicates with existing posts
function buildSlug(title) {
  return title.replace(/[/\\?%*:|"<>#]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '').toLowerCase();
}

const existingPosts = fs.readdirSync(destDir).filter(f => f.endsWith('.md'));
const existingSlugs = new Set(existingPosts.map(f => f.replace(/\.md$/, '')));

console.log(`Found ${existingPosts.length} existing posts\n`);

let imported = 0;
let skipped = 0;

// Walk through all directories
const dirs = fs.readdirSync(srcDir, {withFileTypes: true});
for (const dir of dirs) {
  if (!dir.isDirectory() || dir.name === '云计算') continue; // Skip empty entries and non-dirs

  const category = CATEGORY_MAP[dir.name] || '随笔';
  const dirPath = path.join(srcDir, dir.name);
  const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.md') || f.endsWith('.html'));

  for (const file of files) {
    const filePath = path.join(dirPath, file);
    let content = fs.readFileSync(filePath, 'utf-8').trim();

    if (!content || content.length < 10) {
      console.log(`  ⏭ Skipped empty: ${dir.name}/${file}`);
      continue;
    }

    // Check if it's the unnamed empty file
    if (file === '.md') continue;

    // Get title from filename
    let title = file.replace(/\.(md|html)$/, '');

    // Check for duplicate by slug
    const slug = buildSlug(title);
    if (existingSlugs.has(slug)) {
      console.log(`  ⏭ Skipped (duplicate): ${title}`);
      skipped++;
      continue;
    }

    // Get file mtime as date
    const stats = fs.statSync(filePath);
    const mtime = stats.mtime;
    const pad = n => String(n).padStart(2, '0');
    const dateStr = `${mtime.getFullYear()}-${pad(mtime.getMonth()+1)}-${pad(mtime.getDate())} ${pad(mtime.getHours())}:${pad(mtime.getMinutes())}:${pad(mtime.getSeconds())}`;

    // Build frontmatter
    let frontmatter = '---\n';
    frontmatter += `title: ${title}\n`;
    frontmatter += `date: ${dateStr}\n`;
    frontmatter += `categories: ${category}\n`;
    frontmatter += '---\n\n';

    // Write to Hexo posts
    const destFile = path.join(destDir, `${slug}.md`);
    fs.writeFileSync(destFile, frontmatter + content + '\n', 'utf-8');

    console.log(`  ✅ [${category}] ${title} (${dateStr})`);
    imported++;
  }
}

console.log(`\nDone! Imported: ${imported}, Skipped (duplicates): ${skipped}`);
