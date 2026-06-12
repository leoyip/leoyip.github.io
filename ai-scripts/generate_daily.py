#!/usr/bin/env python3
"""
AI 日报生成器 — 从 AIHOT 拉取当日精选，生成 Hexo 博文。

用法:
    python3 generate_daily.py              # 生成今日日报
    python3 generate_daily.py --date 2026-06-13  # 生成指定日期日报
    python3 generate_daily.py --dry-run    # 预览不写入文件
"""

import json
import urllib.request
import sys
import os
import argparse
from datetime import datetime, timedelta, timezone

# ── 配置 ──────────────────────────────────────────────
API_BASE = "https://aihot.virxact.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
BLOG_POST_DIR = os.path.expanduser("~/Documents/开发/博客/source/_posts")

# 五大版块
SECTION_LABELS = {
    "ai-models": "模型发布/更新",
    "ai-products": "产品发布/更新",
    "industry": "行业动态",
    "paper": "论文研究",
    "tip": "技巧与观点",
}

SECTION_EMOJI = {
    "ai-models": "🤖",
    "ai-products": "📦",
    "industry": "🏭",
    "paper": "📄",
    "tip": "💡",
}

# ── 标签词库（精简版，日报用） ──────────────────────────
TAG_DICT = {
    # 公司/产品（蓝色系）
    "OpenAI": ["openai", "gpt", "chatgpt", "dall-e", "sora"],
    "Anthropic": ["anthropic", "claude"],
    "Google": ["google", "gemini", "deepmind"],
    "Meta": ["meta", "llama", "facebook ai"],
    "微软": ["microsoft", "azure", "copilot"],
    "字节跳动": ["bytedance", "豆包", "doubao", "即梦"],
    "月之暗面": ["月之暗面", "kimi", "moonshot"],
    "DeepSeek": ["deepseek"],
    "快手": ["快手", "kling", "可灵"],
    "阿里": ["阿里", "通义", "qwen", "tongyi"],
    "百度": ["百度", "文心", "ernie"],
    "腾讯": ["腾讯", "混元", "hunyuan"],
    "小米": ["小米", "mimo", "tileRT"],
    "Apple": ["apple", "ios"],
    "英伟达": ["nvidia", "英伟达"],
    "HuggingFace": ["huggingface", "hugging face"],
    "Perplexity": ["perplexity"],
    "Cursor": ["cursor"],
    "Midjourney": ["midjourney"],
    "Stability": ["stability", "stable diffusion", "sd3"],
    "Runway": ["runway", "gen-3", "gen-4"],
    "Pika": ["pika"],
    "Ideogram": ["ideogram"],
    "xAI": ["xai", "grok", "𝕏"],
    "Mistral": ["mistral"],
    "Cohere": ["cohere"],
    "Suno": ["suno"],
    "ElevenLabs": ["elevenlabs"],
    "Character.AI": ["character.ai"],
    "Figure": ["figure"],
    "Vidu": ["vidu"],
    "海螺": ["海螺", "minimax", "hailuo"],
    "智谱": ["智谱", "glm", "zhipu"],
    "阶跃星辰": ["阶跃", "step"],
    "面壁智能": ["面壁", "minicpm"],
    "零一万物": ["零一", "yi-"],
    "秘塔": ["秘塔", "metaso"],
    "科大讯飞": ["讯飞", "星火"],
    "昆仑万维": ["昆仑", "天工"],

    # 技术概念（粉紫系）
    "多模态": ["多模态", "multimodal", "视觉语言", "vision-language", "vl-"],
    "Agent": ["agent", "智能体", "function calling", "tool use", "mcp"],
    "推理": ["推理", "reasoning", "cot", "chain-of-thought", "思维链"],
    "RAG": ["rag", "检索增强", "retrieval-augmented"],
    "文生图": ["文生图", "image generation", "text-to-image", "t2i"],
    "文生视频": ["文生视频", "video generation", "text-to-video", "t2v"],
    "语音": ["语音", "speech", "tts", "asr", "voice", "audio"],
    "代码": ["代码", "code", "programming", "coding"],
    "开源": ["开源", "open source", "open-source", "openweight"],
    "RLHF": ["rlhf", "对齐", "alignment", "preference", "dpo"],
    "MoE": ["moe", "mixture of experts", "混合专家"],
    "量化": ["量化", "quantization", "fp4", "fp8", "int4", "int8"],
    "推理加速": ["推理加速", "inference", "speculative", "投机", "token/s", "tokens/s"],
    "长文本": ["长文本", "long context", "context window", "1m", "2m"],
    "世界模型": ["世界模型", "world model", "3d", "空间智能"],
    "搜索": ["搜索", "search", "perplexity", "deep research"],
    "具身智能": ["具身", "embodied", "机器人", "robot"],
    "安全": ["安全", "safety", "jailbreak", "越狱", "red team"],
    "训练": ["训练", "training", "pretrain", "预训练", "post-train", "后训练"],
    "评估": ["评估", "benchmark", "eval", "evaluation"],
    "提示词": ["提示词", "prompt", "prompting"],
    "知识蒸馏": ["蒸馏", "distill", "knowledge distillation"],

    # 领域话题（青绿系）
    "AI编程": ["ai编程", "ai coding", "ai ide"],
    "AI搜索": ["ai搜索", "ai search"],
    "AI视频": ["ai视频", "ai video"],
    "AI音频": ["ai音乐", "ai音乐", "ai audio", "ai music"],
    "AI教育": ["ai教育", "ai tutoring", "ai tutor"],
    "AI医疗": ["ai医疗", "ai medicine", "ai healthcare"],
    "AI法律": ["ai法律", "ai legal", "ai law"],
    "AI设计": ["ai设计", "ui设计", "figma ai"],
    "AGI": ["agi", "超级智能", "superintelligence"],
    "开源生态": ["开源生态", "huggingface", "开源社区"],
    "算力": ["算力", "compute", "gpu", "芯片", "h100", "h200", "b200"],
    "版权": ["版权", "copyright"],
    "监管": ["监管", "regulation", "政策", "policy"],
}


def tag_color(name: str, tag_label: str) -> str:
    """返回标签的颜色方案，tag_label 为 'company'/'tech'/'domain'"""
    if tag_label == "company":
        colors = ["#2563eb", "#1d4ed8", "#4285f4", "#6366f1", "#4f46e5",
                  "#06b6d4", "#3b82f6", "#0ea5e9", "#00a4ef"]
    elif tag_label == "tech":
        colors = ["#ec4899", "#db2777", "#e11d48", "#f43f5e", "#be185d",
                  "#c026d3", "#a21caf", "#d946ef"]
    else:
        colors = ["#10b981", "#059669", "#14b8a6", "#0d9488", "#22c55e",
                  "#84cc16", "#65a30d", "#f59e0b", "#f97316"]
    h = hash(name) % len(colors)
    return colors[h]


def extract_tags(title: str, summary: str) -> list[tuple[str, str]]:
    """提取 2-3 个内容标签，返回 [(标签名, 类型), ...]。优先公司 > 技术 > 话题"""
    title_lower = title.lower()
    summary_lower = (summary or "").lower()

    def score(keywords: list[str]) -> int:
        s = 0
        for kw in keywords:
            if kw.lower() in title_lower:
                s += 3  # 标题命中权重高
            if kw.lower() in summary_lower:
                s += 1
        return s

    scored = []
    for name, keywords in TAG_DICT.items():
        s = score(keywords)
        if s > 0:
            scored.append((name, s))

    scored.sort(key=lambda x: -x[1])

    # 按类型分配：取 top 公司 + top 技术 + top 话题
    companies = []
    techs = []
    domains = []
    for name, s in scored:
        # 判断类型
        is_company = any(k in name for k in
            ["OpenAI","Anthropic","Google","Meta","微软","字节","快手","阿里",
             "百度","腾讯","小米","Apple","英伟达","HuggingFace","Perplexity",
             "Cursor","Midjourney","Stability","Runway","Pika","Ideogram","xAI",
             "Mistral","Cohere","Suno","ElevenLabs","Character","Figure","Vidu",
             "海螺","智谱","阶跃","面壁","零一","秘塔","科大讯飞","昆仑","DeepSeek",
             "月之暗面"])
        is_tech = any(k in name for k in
            ["多模态","Agent","推理","RAG","文生图","文生视频","语音","代码","开源",
             "RLHF","MoE","量化","推理加速","长文本","世界模型","搜索","具身智能",
             "安全","训练","评估","提示词","知识蒸馏"])
        is_domain = any(k in name for k in
            ["AI编程","AI搜索","AI视频","AI音频","AI教育","AI医疗","AI法律",
             "AI设计","AGI","开源生态","算力","版权","监管"])

        if is_company and len(companies) < 2:
            companies.append((name, "company"))
        elif is_tech and len(techs) < 2:
            techs.append((name, "tech"))
        elif is_domain and len(domains) < 2:
            domains.append((name, "domain"))

    # 组合结果：最多3个标签
    result = []
    for lst in [companies, techs, domains]:
        for tag in lst:
            if len(result) >= 3:
                break
            result.append(tag)
        if len(result) >= 3:
            break
    return result[:3]


def render_tags(tags: list[tuple[str, str]]) -> str:
    """渲染 HTML 标签"""
    spans = []
    for name, ttype in tags:
        color = tag_color(name, ttype)
        spans.append(
            f'<span style="display:inline-block;background:{color};color:#fff;'
            f'font-size:10px;padding:1px 6px;border-radius:6px;margin-right:4px;">{name}</span>'
        )
    return " ".join(spans)


def classify_model(title: str) -> str | None:
    """模型子分类，返回 None 或 分类标签"""
    t = title.lower()
    rules = [
        ("语音/音频", ["speech", "tts", "voice", "audio", "asr", "suno", "elevenlabs"]),
        ("视频生成", ["视频生成", "video generation", "text-to-video", "kling", "sora",
                     "可灵", "gen-3", "gen-4", "vidu", "pika", "runway"]),
        ("图像生成", ["图像生成", "image generation", "text-to-image", "midjourney",
                     "dall-e", "stable diffusion", "flux", "ideogram"]),
        ("代码模型", ["code", "coding", "programming", "代码"]),
        ("世界模型/3D", ["世界模型", "world model", "3d", "空间智能", "spatial"]),
        ("搜索/检索", ["search", "搜索", "retrieval", "检索"]),
        ("多模态", ["多模态", "multimodal", "vision", "视觉", "vl-", "omni"]),
        ("大语言模型", ["llm", "language model", "语言模型", "transformer",
                      "gpt", "claude", "gemini", "llama", "qwen"]),
    ]
    for label, keywords in rules:
        for kw in keywords:
            if kw in t:
                return label
    return None


def fetch_items(since_iso: str, max_items: int = 100) -> list[dict]:
    """从 AIHOT API 拉取精选条目"""
    url = f"{API_BASE}/api/public/items?mode=selected&since={since_iso}&take={max_items}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("items", [])


def format_time(iso_str: str | None) -> str:
    """UTC → 北京时间，人性化输出"""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        bj = dt.astimezone(timezone(timedelta(hours=8)))
        now = datetime.now(timezone(timedelta(hours=8)))
        delta = now - bj
        if delta < timedelta(hours=1):
            mins = max(1, int(delta.total_seconds() / 60))
            return f"{mins}分钟前"
        elif delta < timedelta(hours=24):
            return f"{int(delta.total_seconds() / 3600)}小时前"
        elif delta < timedelta(days=2):
            return "昨天 " + bj.strftime("%H:%M")
        else:
            days = delta.days
            return f"{days}天前"
    except Exception:
        return ""


def generate_daily(items: list[dict], date_str: str) -> str:
    """生成日报 Markdown"""
    # 分组
    sections: dict[str, list[dict]] = {k: [] for k in SECTION_LABELS}
    for item in items:
        cat = item.get("category")
        if cat in sections:
            sections[cat].append(item)

    # 每版块取前 3 条
    for cat in sections:
        sections[cat] = sections[cat][:3]

    total = sum(len(v) for v in sections.values())

    # 计算北京时间日期
    bj_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y年%m月%d日")

    lines = []
    lines.append("---")
    lines.append(f"title: AI 日报 · {bj_date}")
    lines.append(f"date: {date_str} 08:00:00")
    lines.append("categories: AI日报")
    lines.append("tags:")
    lines.append("  - AI")
    lines.append("  - 日报")
    lines.append("  - 人工智能")
    lines.append("---")
    lines.append("")
    lines.append(f"> 📰 今日 AI 精选资讯速递，五大版块共 {total} 条值得关注的动态。"
                 "标签色系：🔵蓝=公司/产品 · 🟣粉=技术概念 · 🟢绿=领域话题。")
    lines.append("")
    lines.append("")

    # 各版块
    for cat in ["ai-models", "ai-products", "industry", "paper", "tip"]:
        sec_items = sections[cat]
        if not sec_items:
            continue
        emoji = SECTION_EMOJI[cat]
        label = SECTION_LABELS[cat]
        lines.append(f"## {emoji} {label}")
        lines.append("")

        for i, item in enumerate(sec_items, 1):
            title = item.get("title", "")
            source = item.get("source", "")
            url = item.get("url", "")
            published = item.get("publishedAt")
            summary = (item.get("summary") or "").strip()
            time_str = format_time(published)

            # 标签
            tags = extract_tags(title, summary)

            # 模型子分类
            sub_label = None
            if cat == "ai-models":
                sub_label = classify_model(title)

            lines.append(f"### {i}. {title}")
            lines.append("")

            tag_line = render_tags(tags)
            if sub_label:
                tag_line = (
                    f'<span style="display:inline-block;background:#a78bfa;color:#fff;'
                    f'font-size:10px;padding:1px 6px;border-radius:6px;margin-right:4px;">'
                    f'📌 {sub_label}</span> ' + tag_line
                )
            lines.append(f"🏷️ {tag_line}")
            lines.append("")

            meta = []
            if source:
                meta.append(f"来源: {source}")
            if time_str:
                meta.append(time_str)
            if meta:
                lines.append(" · ".join(meta))
                lines.append("")

            if summary:
                # 截断到 120 字
                if len(summary) > 120:
                    summary = summary[:117] + "..."
                lines.append(f"{summary}")
                lines.append("")

            if url:
                lines.append(f"🔗 [阅读原文]({url})")
            lines.append("")

        lines.append("")

    lines.append("---")
    lines.append(f"*📡 数据来源：AI HOT (aihot.virxact.com) · 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} 北京时间*")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI 日报生成器")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)，默认今天")
    parser.add_argument("--dry-run", action="store_true", help="只预览不写文件")
    args = parser.parse_args()

    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"❌ 日期格式错误: {args.date}，需要 YYYY-MM-DD")
            sys.exit(1)
    else:
        target_date = datetime.now(timezone(timedelta(hours=8)))

    date_str = target_date.strftime("%Y-%m-%d")

    # 构造 since: 目标日期的前一天 00:00 UTC
    since_dt = target_date - timedelta(days=1)
    since_iso = since_dt.strftime("%Y-%m-%dT00:00:00Z")

    print(f"📡 拉取 {date_str} AI 日报数据...")
    print(f"   API: items?mode=selected&since={since_iso}&take=100")

    try:
        items = fetch_items(since_iso)
    except Exception as e:
        print(f"❌ API 请求失败: {e}")
        sys.exit(1)

    print(f"   获取到 {len(items)} 条精选条目")

    if not items:
        print("⚠️  当日无数据，尝试使用 daily 端点...")
        try:
            daily_url = f"{API_BASE}/api/public/daily/{date_str}"
            req = urllib.request.Request(daily_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                daily = json.loads(resp.read().decode("utf-8"))
            # 转为 items 格式
            for section in daily.get("sections", []):
                cat_map = {v: k for k, v in SECTION_LABELS.items()}
                cat = cat_map.get(section["label"])
                for it in section.get("items", []):
                    items.append({
                        "title": it.get("title", ""),
                        "source": it.get("sourceName", ""),
                        "url": it.get("sourceUrl", ""),
                        "summary": it.get("summary", ""),
                        "category": cat,
                        "publishedAt": it.get("publishedAt"),
                    })
            print(f"   从 daily 端点补充到 {len(items)} 条")
        except Exception as e:
            print(f"⚠️  daily 端点也失败了: {e}")

    if not items:
        print("❌ 无数据可生成日报")
        sys.exit(1)

    md = generate_daily(items, date_str)

    filename = f"AI-日报-{date_str}.md"
    filepath = os.path.join(BLOG_POST_DIR, filename)

    if args.dry_run:
        print("\n" + "=" * 60)
        print(md[:3000])
        if len(md) > 3000:
            print(f"\n... (共 {len(md)} 字符，已截断预览)")
        return

    os.makedirs(BLOG_POST_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\n✅ 日报已生成: {filepath}")
    print(f"   共 {sum(1 for l in md.split(chr(10)) if l.startswith('### '))} 条资讯")


if __name__ == "__main__":
    main()
