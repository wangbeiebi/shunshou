"""
顺手 — 链接提取模块
"""

import re
import click
from pathlib import Path
from urllib.parse import urlparse

URL_PATTERN = re.compile(
    r'https?://[^\s<>"\')\]]+',
    re.IGNORECASE,
)


def extract_links(source: str, output: str | None):
    """从文本/URL/文件中提取所有链接"""
    if source.startswith(("http://", "https://")):
        _extract_from_url(source, output)
    elif Path(source).is_file():
        _extract_from_file(source, output)
    else:
        _extract_from_text(source, output)


def _extract_from_url(url: str, output: str | None):
    """从网页提取链接"""
    try:
        import requests
        from bs4 import BeautifulSoup

        click.echo(f"🌐 正在请求: {url} ...")
        resp = requests.get(url, headers={"User-Agent": "ShunShou/0.1"}, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith(("http://", "https://")):
                text = a.get_text(strip=True) or "-"
                links.append((href, text))
            elif href.startswith("/") or not href.startswith("#"):
                # 处理相对链接
                parsed = urlparse(url)
                full_url = f"{parsed.scheme}://{parsed.netloc}{href if href.startswith('/') else '/' + href}"
                text = a.get_text(strip=True) or "-"
                links.append((full_url, text))

        unique_links = list(dict.fromkeys(links))
        _display_and_save(unique_links, url, output)

    except ImportError:
        click.echo("❌ 需要安装 requests 和 beautifulsoup4: pip install requests beautifulsoup4")
    except Exception as e:
        click.echo(f"❌ 请求失败: {e}")


def _extract_from_file(filepath: str, output: str | None):
    """从文件提取链接"""
    content = Path(filepath).read_text(encoding="utf-8")
    _extract_from_text(content, output)


def _extract_from_text(text: str, output: str | None):
    """从文本提取链接"""
    urls = URL_PATTERN.findall(text)
    # 去重保持顺序
    unique_urls = list(dict.fromkeys([u.rstrip(".,;:") for u in urls]))
    links = [(u, "-") for u in unique_urls]
    _display_and_save(links, "text", output)


def _display_and_save(links: list, source: str, output: str | None):
    """显示并保存结果"""
    if not links:
        click.echo("⚠️  未找到任何链接")
        return

    click.echo(f"\n🔗 从 {source} 提取到 {len(links)} 个链接:\n")
    lines = []
    for i, (url, text) in enumerate(links, 1):
        line = f"  [{i}] {url}"
        if text and text != "-":
            line += f"  ({text})"
        click.echo(line)
        lines.append(url)

    if output:
        out_path = Path(output)
        out_path.write_text("\n".join(lines), encoding="utf-8")
        click.echo(f"\n✅ 已保存到: {out_path}")
