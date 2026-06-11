const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const postsDir = path.join(__dirname, '..', 'source', '_posts');
const imageDir = path.join(__dirname, '..', 'source', 'images', 'imported');

fs.mkdirSync(imageDir, { recursive: true });

// Find all external image URLs in markdown files
const urlMap = new Map(); // oldUrl -> localPath

function findImageUrls() {
  const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'));
  const urls = [];

  for (const file of files) {
    const content = fs.readFileSync(path.join(postsDir, file), 'utf-8');
    const regex = /(!\[.*?\]\()([^)]+)\)/g;
    let match;
    while ((match = regex.exec(content)) !== null) {
      const fullUrl = match[2].split('?')[0]; // remove query params
      if (fullUrl.startsWith('http') && !fullUrl.includes('localhost') && !fullUrl.includes('leoyip.github.io')) {
        urls.push({ url: fullUrl, full: match[2], file });
      }
    }
  }
  return urls;
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(dest)) {
      console.log(`  ⏭ Already exists: ${path.basename(dest)}`);
      resolve(dest);
      return;
    }
    const client = url.startsWith('https') ? https : http;
    client.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0' },
      timeout: 30000
    }, (resp) => {
      if (resp.statusCode === 200) {
        const file = fs.createWriteStream(dest);
        resp.pipe(file);
        file.on('finish', () => {
          file.close();
          const size = fs.statSync(dest).size;
          console.log(`  ✅ Downloaded: ${path.basename(dest)} (${size} bytes)`);
          resolve(dest);
        });
      } else if (resp.statusCode >= 300 && resp.statusCode < 400 && resp.headers.location) {
        // Follow redirect
        download(resp.headers.location, dest).then(resolve).catch(reject);
      } else {
        console.error(`  ❌ Failed: ${url} - HTTP ${resp.statusCode}`);
        reject(new Error(`HTTP ${resp.statusCode}`));
      }
    }).on('error', (e) => {
      console.error(`  ❌ Error: ${url} - ${e.message}`);
      reject(e);
    });
  });
}

function getExt(url) {
  const clean = url.split('?')[0].split('#')[0];
  const ext = path.extname(clean) || '.jpg';
  return ext.toLowerCase();
}

function slugify(url) {
  const clean = url.replace(/https?:\/\//, '');
  return clean.replace(/[^a-zA-Z0-9]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '').substring(0, 80);
}

async function main() {
  const images = findImageUrls();
  console.log(`Found ${images.length} external images\n`);

  // Deduplicate by URL
  const seen = new Set();
  const unique = images.filter(img => {
    const key = img.url;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  console.log(`Unique images: ${unique.length}\n`);

  let success = 0;
  let fail = 0;

  for (const img of unique) {
    const ext = getExt(img.url);
    const filename = slugify(img.url) + ext;
    const dest = path.join(imageDir, filename);

    try {
      await download(img.url, dest);
      urlMap.set(img.url, `/images/imported/${filename}`);
      success++;
    } catch (e) {
      fail++;
    }
  }

  // Update markdown files with local paths
  if (urlMap.size > 0) {
    console.log('\n=== Updating markdown references ===');
    const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'));
    let updatedCount = 0;

    for (const file of files) {
      const filePath = path.join(postsDir, file);
      let content = fs.readFileSync(filePath, 'utf-8');
      let modified = false;

      for (const [oldUrl, localPath] of urlMap) {
        const oldFull = oldUrl;
        const escapedOld = oldFull.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const re = new RegExp(escapedOld.replace(/\?.*/, '') + '(\\?[^")]*)?', 'g');
        if (re.test(content)) {
          content = content.replace(re, localPath);
          modified = true;
        }
      }

      if (modified) {
        fs.writeFileSync(filePath, content, 'utf-8');
        updatedCount++;
      }
    }
    console.log(`Updated ${updatedCount} files`);
  }

  console.log(`\nDone! ${success} downloaded, ${fail} failed`);
}

main().catch(console.error);
