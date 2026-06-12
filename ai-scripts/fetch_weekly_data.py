#!/usr/bin/env python3
"""
AI 周报深评数据获取器 — 拉取本周 AIHOT 数据，生成 Hexo 深评博文章节。

用法:
    python3 fetch_weekly_data.py              # 拉取本周数据，输出 JSON
    python3 fetch_weekly_data.py --markdown   # 生成 Hexo 博文（自动分析版本）
    python3 fetch_weekly_data.py --json-only  # 仅输出 JSON 到 stdout
"""

import json
import urllib.request
import sys
import os
import argparse
import re
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict

# ── 配置 ──────────────────────────────────────────────
API_BASE = "https://aihot.virxact.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
BLOG_POST_DIR = os.path.expanduser("~/Documents/开发/博客/source/_posts")

# 高权重信源（评分加成）
HIGH_WEIGHT_SOURCES = [
    "OpenAI", "Anthropic", "Google DeepMind", "Google",
    "Meta", "Meta AI", "Microsoft", "NVIDIA",
    "X：Sam Altman", "X：Karpathy",
    "TechCrunch", "The Verge", "Wired", "Ars Technica",
    "MIT Technology Review", "Nature", "Science",
    "X：Logan Kilpatrick", "X：Yann LeCun", "X：Jim Fan",
    "X：Andrew Ng", "Stability AI", "Runway",
]

# 聚类关键词（用于将相似条目归入同一话题）
CLUSTER_TOPICS = {
    "Claude/GPT 旗舰模型竞速": [
        "claude mythos", "claude fable", "gpt-5", "gpt-6",
        "anthropic", "openai", "sota", "旗舰",
    ],
    "视频生成/Sora/可灵": [
        "sora", "kling", "可灵", "gen-3", "gen-4", "runway",
        "video generation", "vidu", "视频生成",
    ],
    "AI Agent/Codex/Cursor": [
        "agent", "codex", "cursor", "智能体", "mcp",
        "function calling", "tool use", "ai coding", "ai编程",
        "devin", "copilot", "windsurf",
    ],
    "多模态/视觉语言模型": [
        "多模态", "multimodal", "vision", "视觉", "vl-",
        "gemini omni", "gpt-4o", "image understanding",
    ],
    "开源模型生态": [
        "llama", "mistral", "qwen", "deepseek", "开源",
        "open source", "huggingface", "yi-",
    ],
    "AI 搜索/Deep Research": [
        "搜索", "search", "perplexity", "deep research",
        "ai search",
    ],
    "文生图/Midjourney/Flux": [
        "midjourney", "flux", "dall-e", "stable diffusion",
        "ideogram", "文生图", "image generation",
    ],
    "机器人/具身智能": [
        "robot", "机器人", "figure", "embodied", "具身",
        "optimus", "physical intelligence",
    ],
    "AI 安全/监管/对齐": [
        "安全", "safety", "对齐", "alignment", "监管",
        "regulation", "policy", "jailbreak", "越狱",
    ],
    "推理/思考模型": [
        "推理", "reasoning", "cot", "thinking", "o1", "o3",
        "deep research", "test-time compute",
    ],
    "语音/Audio AI": [
        "语音", "speech", "tts", "voice", "audio", "suno",
        "elevenlabs", "whisper",
    ],
    "芯片/算力/基础设施": [
        "gpu", "芯片", "h100", "h200", "b200", "nvidia",
        "cuda", "算力", "compute", "tpu", "asic",
    ],
    "AI 医疗/科学": [
        "医疗", "health", "medicine", "protein", "基因",
        "药物", "科学", "alphafold",
    ],
    "长文本/RAG/上下文": [
        "长文本", "context", "rag", "retrieval", "检索增强",
        "1m", "2m", "context window",
    ],
}


def fetch_weekly_items(days: int = 7) -> list[dict]:
    """拉取最近 N 天精选条目（翻页直到数据超出时间窗口）"""
    since = datetime.now(timezone.utc) - timedelta(days=days)
    since_iso = since.strftime("%Y-%m-%dT%H:%M:%SZ")

    all_items = []
    cursor = None
    page = 0

    while True:
        page += 1
        url = f"{API_BASE}/api/public/items?mode=selected&since={since_iso}&take=100"
        if cursor:
            url += f"&cursor={cursor}"

        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        items = data.get("items", [])
        all_items.extend(items)
        print(f"   第{page}页: {len(items)}条 (累计{len(all_items)}条)", file=sys.stderr)

        has_next = data.get("hasNext", False)
        next_cursor = data.get("nextCursor")
        if not has_next or not next_cursor:
            break
        cursor = next_cursor

    return all_items


def score_item(item: dict) -> int:
    """对条目进行重要性打分"""
    score = 0
    title = (item.get("title") or "").lower()
    source = item.get("source") or ""

    # 信源权重
    for hs in HIGH_WEIGHT_SOURCES:
        if hs.lower() in source.lower():
            score += 3
            break

    # 关键词加分
    important_keywords = [
        "发布", "推出", "开源", "sota", "突破", "首次",
        "announce", "release", "launch", "open source",
        "gpt-5", "gpt-6", "claude", "gemini",
    ]
    for kw in important_keywords:
        if kw in title:
            score += 2

    # 论文加分
    if item.get("category") == "paper":
        score += 1

    return score


def cluster_items(items: list[dict]) -> dict[str, list[dict]]:
    """将条目归入话题聚类"""
    clusters: dict[str, list[dict]] = {topic: [] for topic in CLUSTER_TOPICS}
    unmatched = []

    for item in items:
        title = (item.get("title") or "").lower()
        summary = (item.get("summary") or "").lower()
        text = title + " " + summary

        matched = False
        for topic, keywords in CLUSTER_TOPICS.items():
            if any(kw in text for kw in keywords):
                clusters[topic].append(item)
                matched = True
                break

        if not matched:
            unmatched.append(item)

    # 未匹配的保留为"其他重要动态"
    if unmatched:
        clusters["其他重要动态"] = unmatched

    return clusters


def select_top_topics(
    clusters: dict[str, list[dict]], top_n: int = 5
) -> list[tuple[str, list[dict], int]]:
    """选出最重要的 N 个话题"""
    scored = []
    for topic, items in clusters.items():
        if topic == "其他重要动态":
            continue
        # 综合得分 = 条目数量 × 2 + 总分
        total_score = sum(score_item(it) for it in items)
        composite = len(items) * 2 + total_score
        scored.append((topic, items, composite))

    scored.sort(key=lambda x: -x[2])
    return scored[:top_n]


def format_weekly_md(
    top_topics: list[tuple[str, list[dict], int]],
    all_items: list[dict],
    week_start: str,
    week_end: str,
) -> str:
    """生成周报深评 Markdown"""
    bj = timezone(timedelta(hours=8))
    now = datetime.now(bj)

    # 计算第几周
    start_dt = datetime.strptime(week_start, "%Y-%m-%d")
    week_num = start_dt.isocalendar()[1]
    month = start_dt.month

    lines = []
    lines.append("---")
    lines.append(f"title: AI 周报深度点评 · {now.year}年{month}月第{week_num}周")
    lines.append(f"date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("categories: 技术")
    lines.append("tags:")
    lines.append("  - AI")
    lines.append("  - 人工智能")
    lines.append("  - 周报")
    lines.append("  - 深度分析")
    lines.append("---")
    lines.append("")
    lines.append(f"> 📊 本周（{week_start} - {week_end}）AI 行业深度点评。"
                 f"从 {len(all_items)} 条精选资讯中提炼 {len(top_topics)} 个核心话题，逐一分析。")
    lines.append("")
    lines.append("")

    # ── 本周综述 ──
    lines.append("## 📋 本周综述")
    lines.append("")
    lines.append("> 💬 以下为本周 AI 圈最值得关注的动态概述。AI 将基于话题聚类数据，"
                 "以叙事方式串联本周关键事件，讲清楚来龙去脉和行业影响。")
    lines.append("")
    lines.append("<!-- AI_WRITE: 本周综述（300-500字） -->")
    lines.append("")

    # 简列所有话题
    lines.append("### 本周话题一览")
    lines.append("")
    for i, (topic, items, score) in enumerate(top_topics, 1):
        lines.append(f"{i}. **{topic}** — {len(items)} 条相关资讯")
    lines.append("")
    lines.append("")

    # ── 深度分析 ──
    lines.append("## 🔬 深度分析")
    lines.append("")
    lines.append(f"以下对本周 {len(top_topics)} 个核心话题做逐一深度解析。")
    lines.append("")

    for i, (topic, items, score) in enumerate(top_topics, 1):
        lines.append(f"### {i}. {topic}")
        lines.append("")

        # 相关资讯链接
        lines.append("**相关动态：**")
        lines.append("")
        for item in items[:8]:  # 最多列 8 条
            title = item.get("title", "")
            url = item.get("url", "")
            source = item.get("source", "")
            lines.append(f"- [{title}]({url}) — {source}")
        if len(items) > 8:
            lines.append(f"- *...及其他 {len(items) - 8} 条相关资讯*")
        lines.append("")

        # 深度分析占位
        lines.append("**深度分析：**")
        lines.append("")
        lines.append(f"<!-- AI_WRITE: {topic} 深度分析（500-800字），覆盖："
                     "事件背景 → 技术/商业意义 → 行业影响 → 值得关注的原因 -->")
        lines.append("")
        lines.append("")

    # ── 本周值得关注的其他动态 ──
    lines.append("## 📌 本周值得关注的其他动态")
    lines.append("")

    other_items = []
    covered_titles = set()
    for _, items, _ in top_topics:
        for it in items:
            covered_titles.add(it.get("title", ""))

    for item in all_items:
        if item.get("title", "") not in covered_titles:
            other_items.append(item)

    # 取未覆盖中得分最高的 15 条
    other_items.sort(key=score_item, reverse=True)
    for item in other_items[:15]:
        title = item.get("title", "")
        url = item.get("url", "")
        source = item.get("source", "")
        summary = (item.get("summary") or "").strip()
        if len(summary) > 100:
            summary = summary[:97] + "..."

        lines.append(f"- **{title}** — {source}")
        if summary:
            lines.append(f"  {summary}")
        lines.append(f"  [阅读原文]({url})")
        lines.append("")

    lines.append("")
    lines.append("---")
    lines.append(f"*📡 数据来源：AI HOT (aihot.virxact.com) · "
                 f"覆盖时间：{week_start} - {week_end} · "
                 f"生成时间：{now.strftime('%Y-%m-%d %H:%M')} 北京时间*")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI 周报深评数据获取器")
    parser.add_argument("--days", type=int, default=7, help="覆盖天数，默认 7 天")
    parser.add_argument("--topics", type=int, default=5, help="深度分析话题数，默认 5")
    parser.add_argument("--markdown", action="store_true", help="生成 Hexo 博文（含 AI 占位符）")
    parser.add_argument("--json-only", action="store_true", help="仅输出 JSON 到 stdout")
    args = parser.parse_args()

    # 计算时间窗口
    now = datetime.now(timezone(timedelta(hours=8)))
    week_start = (now - timedelta(days=args.days)).strftime("%Y-%m-%d")
    week_end = now.strftime("%Y-%m-%d")

    print(f"📡 拉取 {week_start} - {week_end} AI 精选数据...", file=sys.stderr)
    items = fetch_weekly_items(args.days)
    print(f"   总计: {len(items)} 条精选条目", file=sys.stderr)

    # 聚类
    clusters = cluster_items(items)
    top = select_top_topics(clusters, args.topics)

    # 输出
    if args.json_only:
        result = {
            "week_start": week_start,
            "week_end": week_end,
            "total_items": len(items),
            "top_topics": [
                {
                    "topic": topic,
                    "count": len(topic_items),
                    "score": score,
                    "items": [
                        {
                            "title": it.get("title"),
                            "url": it.get("url"),
                            "source": it.get("source"),
                            "summary": it.get("summary"),
                            "publishedAt": it.get("publishedAt"),
                            "category": it.get("category"),
                        }
                        for it in topic_items[:10]
                    ],
                }
                for topic, topic_items, score in top
            ],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.markdown:
        md = format_weekly_md(top, items, week_start, week_end)

        week_num = datetime.strptime(week_start, "%Y-%m-%d").isocalendar()[1]
        filename = f"AI-周报深评-{now.year}-{now.month:02d}-第{week_num}周.md"
        filepath = os.path.join(BLOG_POST_DIR, filename)

        os.makedirs(BLOG_POST_DIR, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"\n✅ 周报深评草稿已生成: {filepath}", file=sys.stderr)
        print(f"   包含 {len(top)} 个深度分析话题 + 综述框架", file=sys.stderr)
        print(f"   请编辑文件中的 <!-- AI_WRITE: ... --> 占位符完成分析", file=sys.stderr)
    else:
        # 默认输出摘要
        print(f"\n📊 周报数据摘要 ({week_start} - {week_end})", file=sys.stderr)
        print(f"   总条目: {len(items)}", file=sys.stderr)
        print(f"\n   TOP {args.topics} 话题:", file=sys.stderr)
        for i, (topic, topic_items, score) in enumerate(top, 1):
            print(f"   {i}. {topic} ({len(topic_items)}条, 得分{score})", file=sys.stderr)
            for it in topic_items[:3]:
                print(f"      - {it.get('title', '')[:50]}...", file=sys.stderr)


if __name__ == "__main__":
    main()
