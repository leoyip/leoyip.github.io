const fs = require('fs');
const path = require('path');

const postsDir = path.join(__dirname, '..', 'source', '_posts');
const slugMap = {};

// Build slug map from jianshu slugs to post files
// Jianshu export files don't have slugs embedded, but we can match by title
// Let's first list all the slugs we know from the jianshu export

const jianshuArticles = [
  { title: '西虹市首富影评', slug: '72f47e3bdfa1' },
  { title: '如何应对消极情绪', slug: '5c75ef5c49b7' },
  { title: '销售是一种怎样的存在？', slug: 'b30a7f464f0a' },
  { title: '如何快速整理手机上的照片-#iOS+Android', slug: '5cbc4ae063cf' },
  { title: '冬日少述', slug: '33911e510ce3' },
  { title: '人工智能和第三种未来', slug: '228e2fd9824a' },
  { title: '企业IT架构与共享经济', slug: 'b1279f6b3a24' },
  { title: '解决华硕笔记本不认U盘问题', slug: 'e32935041d40' },
  { title: 'U盘修复"系统找不到指定文件"问题记录', slug: '3623cecb41bb' },
  { title: '在你醒来的梦里', slug: '5c20c73d1e39' },
  { title: '《三体》的爱与孤独', slug: '2ff68c64618d' },
  { title: 'Dell服务器简单配置', slug: 'ea9ec683d319' },
  { title: 'Dell-服务器做磁盘阵列', slug: '59826ffecbaf' },
  { title: 'Dell-服务器安装-Windows-2008-R2-操作系统', slug: '0f567a0126bf' },
  { title: '两步搭建私有云盘', slug: '9e3b05aa1b28' },
  { title: 'windows操作系统如何设置全局视图为详细列表', slug: 'b277a72ef807' },
  { title: 'Markdown文档中插入公式', slug: 'dbab7d1089f7' },
  { title: '那个···我想让文字颠倒一下', slug: 'e552e4b5b061' },
  { title: '一千件美妙小事', slug: '348f0b6dd952' },
  { title: '混沌（CHAOS）', slug: 'efad34d7104a' },
  { title: '随便聊聊自由', slug: '3fa322b6326d' },
  { title: '一位数学家和一部电影的故事', slug: '5907500263a5' },
  { title: 'vmware-vsphere中如何限制某一台虚拟机的流量', slug: 'aaa2076ad373' },
  { title: 'Moo-do快捷键', slug: '32dc8b2ef971' },
  { title: 'Todoist应用介绍', slug: '64c612c5d269' },
  { title: 'iNode客户端"IP刷新超时"修复', slug: '21388ac4a703' },
  { title: '【MOOC-LHTL】访谈写作教练-记忆和写作技巧', slug: '9bebcd08c437' },
  { title: 'Markdown语法备忘', slug: 'dd6ffcc60c9e' },
];

// Update normalizeTitle to handle Chinese quotes
function normalizeTitle(title) {
  return title.replace(/[""""]/g, '').replace(/[/\\?%*:|<>#]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '').toLowerCase();
}

async function fetchDate(slug) {
  try {
    const resp = await fetch(`https://www.jianshu.com/asimov/p/${slug}`, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json'
      }
    });
    if (!resp.ok) return null;
    const data = await resp.json();
    return data.first_shared_at || null;
  } catch (e) {
    return null;
  }
}

function formatDate(isoStr) {
  if (!isoStr) return '';
  const d = new Date(isoStr);
  if (isNaN(d.getTime())) return '';
  const pad = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function normalizeTitle(title) {
  return title.replace(/[/\\?%*:|"<>#]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '').toLowerCase();
}

async function main() {
  // Read all current posts
  const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'));
  console.log(`Checking ${files.length} posts...\n`);

  let fixed = 0;
  let notFound = 0;

  for (const article of jianshuArticles) {
    // Find matching file
    const normalizedTitle = normalizeTitle(article.title);
    const matchFile = files.find(f => normalizeTitle(f.replace('.md','')) === normalizedTitle);

    if (!matchFile) {
      console.log(`  ⏭ No file for: ${article.title}`);
      notFound++;
      continue;
    }

    console.log(`  📡 Fetching date for: ${article.title}...`);
    const dateStr = await fetchDate(article.slug);

    if (!dateStr) {
      console.log(`     ❌ No date from API`);
      continue;
    }

    const formattedDate = formatDate(dateStr);
    const filePath = path.join(postsDir, matchFile);
    let content = fs.readFileSync(filePath, 'utf-8');

    // Replace date in frontmatter
    content = content.replace(/^date: .+/m, `date: ${formattedDate}`);
    fs.writeFileSync(filePath, content, 'utf-8');

    console.log(`     ✅ ${formattedDate}`);
    fixed++;
  }

  console.log(`\nDone! Updated: ${fixed}, Not found: ${notFound}`);
}

main().catch(console.error);
