"""
顺手 — Markdown 转图片模块
"""

import re
import click
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def md_to_image(md_file: str, output: str, width: int, theme: str):
    """将 Markdown 文件渲染为图片"""
    path = Path(md_file)
    content = path.read_text(encoding="utf-8")

    # 主题配色
    if theme == "dark":
        bg_color = (30, 30, 30)
        text_color = (220, 220, 220)
        header_color = (255, 255, 255)
        code_bg = (50, 50, 50)
        accent = (86, 156, 214)
    else:
        bg_color = (255, 255, 255)
        text_color = (51, 51, 51)
        header_color = (0, 0, 0)
        code_bg = (245, 245, 245)
        accent = (0, 112, 201)

    # 加载字体
    try:
        import platform
        system = platform.system()
        if system == "Windows":
            font_path = "C:/Windows/Fonts/msyh.ttc"
        elif system == "Darwin":
            font_path = "/System/Library/Fonts/PingFang.ttc"
        else:
            font_path = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"

        body_font = ImageFont.truetype(font_path, 16)
        header_font = ImageFont.truetype(font_path, 24)
        title_font = ImageFont.truetype(font_path, 32)
        code_font = ImageFont.truetype(font_path, 14)
    except Exception:
        body_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    # 解析 Markdown 为行
    lines = _parse_markdown(content)

    # 计算图片高度
    line_height = 28
    padding = 30
    margin_text = 20
    code_padding = 10
    max_chars_per_line = max(60, width // 10)  # 估算每行字符数

    total_height = padding * 2
    rendered_lines = []

    for line_type, text in lines:
        if line_type == "h1":
            total_height += 48
            rendered_lines.append(("h1", text, 32))
        elif line_type == "h2":
            total_height += 36
            rendered_lines.append(("h2", text, 24))
        elif line_type == "code":
            wrapped = _wrap_text(text, max_chars_per_line - 2)
            total_height += line_height * len(wrapped) + code_padding * 2
            rendered_lines.append(("code", wrapped, 14))
        elif line_type == "blank":
            total_height += line_height // 2
            rendered_lines.append(("blank", "", 0))
        else:
            wrapped = _wrap_text(text, max_chars_per_line)
            total_height += line_height * len(wrapped)
            rendered_lines.append(("text", wrapped, 16))

    # 创建画布
    img = Image.new("RGB", (width, total_height), bg_color)
    draw = ImageDraw.Draw(img)

    # 绘制内容
    y = padding
    for line_type, content_text, font_size in rendered_lines:
        if line_type == "blank":
            y += line_height // 2
            continue

        if line_type == "h1":
            draw.text((margin_text, y), content_text, font=title_font, fill=accent)
            y += 48
            # 下划线
            draw.line([(margin_text, y - 12), (width - margin_text, y - 12)], fill=accent, width=2)
        elif line_type == "h2":
            draw.text((margin_text, y), content_text, font=header_font, fill=header_color)
            y += 36
        elif line_type == "code":
            # 代码块背景
            code_height = line_height * len(content_text) + code_padding * 2
            draw.rectangle([(margin_text, y), (width - margin_text, y + code_height)], fill=code_bg)
            for i, code_line in enumerate(content_text):
                draw.text((margin_text + code_padding, y + code_padding + i * line_height),
                          code_line, font=code_font, fill=(100, 160, 100) if theme == "dark" else (0, 128, 0))
            y += code_height
        else:
            for text_line in content_text:
                draw.text((margin_text, y), text_line, font=body_font, fill=text_color)
                y += line_height

    img.save(output)
    click.echo(f"✅ 图片已生成: {output}")
    click.echo(f"   尺寸: {img.width}×{img.height}")


def _parse_markdown(content: str) -> list:
    """解析 Markdown 为 (类型, 文本) 列表"""
    lines = []
    in_code = False
    code_buffer = []

    for line in content.split("\n"):
        if line.startswith("```"):
            if in_code:
                lines.append(("code", "\n".join(code_buffer)))
                code_buffer = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_buffer.append(line)
            continue

        if line.strip() == "":
            lines.append(("blank", ""))
        elif line.startswith("# "):
            lines.append(("h1", line[2:].strip()))
        elif line.startswith("## "):
            lines.append(("h2", line[3:].strip()))
        else:
            # 去掉 Markdown 语法
            clean = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
            clean = re.sub(r"\*(.*?)\*", r"\1", clean)
            clean = re.sub(r"`(.*?)`", r"\1", clean)
            clean = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", clean)
            clean = re.sub(r"!\[.*?\]\(.*?\)", "[图片]", clean)
            lines.append(("text", clean))

    if in_code and code_buffer:
        lines.append(("code", "\n".join(code_buffer)))

    return lines


def _wrap_text(text: str, max_chars: int) -> list:
    """按宽度折行"""
    if not text:
        return [""]
    # 简单按字符数折行
    words = list(text)  # 中文按字符折行
    lines = []
    current = ""
    for char in words:
        if len(current) >= max_chars:
            lines.append(current)
            current = char
        else:
            current += char
    if current:
        lines.append(current)
    return lines if lines else [""]
