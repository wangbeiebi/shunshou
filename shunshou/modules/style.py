"""
顺手 — 图片美化模块
"""

import os
import math
import click
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"}


def _list_images(directory: str, patterns: set = None):
    """扫描目录下所有图片"""
    exts = patterns or SUPPORTED_EXTENSIONS
    path = Path(directory)
    return sorted([f for f in path.iterdir() if f.suffix.lower() in exts and f.is_file()])


def _ensure_output_dir(output: str | None, base_dir: str) -> Path:
    out = Path(output) if output else Path(base_dir) / "styled"
    out.mkdir(parents=True, exist_ok=True)
    return out


def round_corners(directory: str, radius: int, output_dir: str | None):
    """批量给图片添加圆角"""
    images = _list_images(directory)
    if not images:
        click.echo("⚠️  目录下没有图片")
        return

    out = _ensure_output_dir(output_dir, directory)

    with click.progressbar(images, label="🔄 添加圆角") as bar:
        for img_path in bar:
            try:
                img = Image.open(img_path).convert("RGBA")
                mask = Image.new("L", img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
                img.putalpha(mask)
                img.save(out / f"{img_path.stem}.png")
            except Exception as e:
                click.echo(f"\n❌ {img_path.name}: {e}")

    click.echo(f"\n✅ 已为 {len(images)} 张图片添加圆角 → {out}")


def add_shadow(directory: str, offset: int, blur: int, opacity: int, output_dir: str | None):
    """批量给图片添加阴影"""
    images = _list_images(directory)
    if not images:
        click.echo("⚠️  目录下没有图片")
        return

    out = _ensure_output_dir(output_dir, directory)

    with click.progressbar(images, label="🌑 添加阴影") as bar:
        for img_path in bar:
            try:
                img = Image.open(img_path).convert("RGBA")

                # 阴影画布
                shadow_margin = abs(offset) + blur * 2
                new_w = img.width + shadow_margin * 2
                new_h = img.height + shadow_margin * 2

                # 创建阴影
                shadow = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
                shadow_draw = ImageDraw.Draw(shadow)

                shadow_box = [
                    shadow_margin + offset,
                    shadow_margin + offset,
                    shadow_margin + offset + img.width,
                    shadow_margin + offset + img.height
                ]
                shadow_draw.rectangle(shadow_box, fill=(0, 0, 0, opacity))

                # 模糊阴影
                shadow = shadow.filter(ImageFilter.GaussianBlur(blur))

                # 粘贴原图
                result = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
                result.paste(shadow, (0, 0), shadow)
                result.paste(img, (shadow_margin, shadow_margin), img)

                result.save(out / f"{img_path.stem}.png")
            except Exception as e:
                click.echo(f"\n❌ {img_path.name}: {e}")

    click.echo(f"\n✅ 已为 {len(images)} 张图片添加阴影 → {out}")


def add_border(directory: str, width: int, color: str, output_dir: str | None):
    """批量给图片添加边框"""
    images = _list_images(directory)
    if not images:
        click.echo("⚠️  目录下没有图片")
        return

    out = _ensure_output_dir(output_dir, directory)
    border_color = _parse_color(color) or (0, 0, 0)

    with click.progressbar(images, label="⬛ 添加边框") as bar:
        for img_path in bar:
            try:
                img = Image.open(img_path).convert("RGBA")
                new_w = img.width + width * 2
                new_h = img.height + width * 2

                result = Image.new("RGBA", (new_w, new_h), border_color + (255,))
                result.paste(img, (width, width), img)
                result.save(out / f"{img_path.stem}.png")
            except Exception as e:
                click.echo(f"\n❌ {img_path.name}: {e}")

    click.echo(f"\n✅ 已为 {len(images)} 张图片添加边框 → {out}")


def stitch(directory: str, output: str, direction: str, gap: int,
           bg_color: str, align: str):
    """图片拼接：水平或垂直拼接多张图片"""
    images = _list_images(directory)
    if len(images) < 2:
        click.echo(f"❌ 至少需要 2 张图片，找到 {len(images)} 张")
        return

    bg = _parse_color(bg_color) or (255, 255, 255)
    opened = [Image.open(p).convert("RGBA") for p in images]

    if direction == "horizontal":
        # 水平拼接
        max_h = max(img.height for img in opened)
        total_w = sum(img.width for img in opened) + gap * (len(opened) - 1)
        result = Image.new("RGBA", (total_w, max_h), bg + (255,))

        x = 0
        for img in opened:
            y = 0
            if align == "center":
                y = (max_h - img.height) // 2
            elif align == "bottom":
                y = max_h - img.height
            result.paste(img, (x, y), img)
            x += img.width + gap
    else:
        # 垂直拼接
        max_w = max(img.width for img in opened)
        total_h = sum(img.height for img in opened) + gap * (len(opened) - 1)
        result = Image.new("RGBA", (max_w, total_h), bg + (255,))

        y = 0
        for img in opened:
            x = 0
            if align == "center":
                x = (max_w - img.width) // 2
            elif align == "right":
                x = max_w - img.width
            result.paste(img, (x, y), img)
            y += img.height + gap

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    result.save(output)
    click.echo(f"✅ 拼接完成: {output} ({result.width}×{result.height})")


def grid(directory: str, output: str, columns: int, gap: int,
         bg_color: str, cell_size: str | None):
    """图片网格拼接（九宫格等）"""
    images = _list_images(directory)
    if not images:
        click.echo("⚠️  目录下没有图片")
        return

    bg = _parse_color(bg_color) or (255, 255, 255)

    # 解析统一尺寸
    target_w, target_h = None, None
    if cell_size:
        parts = cell_size.split("x")
        if len(parts) == 2:
            target_w, target_h = int(parts[0]), int(parts[1])

    # 计算网格
    total = len(images)
    rows = math.ceil(total / columns)

    clicked = [Image.open(p).convert("RGBA") for p in images]

    if target_w and target_h:
        clicked = [img.resize((target_w, target_h), Image.LANCZOS) for img in clicked]
        max_w, max_h = target_w, target_h
    else:
        max_w = max(img.width for img in clicked)
        max_h = max(img.height for img in clicked)

    canvas_w = columns * max_w + gap * (columns + 1)
    canvas_h = rows * max_h + gap * (rows + 1)
    result = Image.new("RGBA", (canvas_w, canvas_h), bg + (255,))

    for idx, img in enumerate(clicked):
        row = idx // columns
        col = idx % columns

        # 居中放置
        if img.size != (max_w, max_h):
            new_img = Image.new("RGBA", (max_w, max_h), bg + (255,))
            px = (max_w - img.width) // 2
            py = (max_h - img.height) // 2
            new_img.paste(img, (px, py), img)
            img = new_img

        x = gap + col * (max_w + gap)
        y = gap + row * (max_h + gap)
        result.paste(img, (x, y), img)

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    result.save(output)
    click.echo(f"✅ 网格拼接完成: {output} ({result.width}×{result.height})")
    click.echo(f"   排版: {columns}×{rows} | 间隙: {gap}px")


def _parse_color(s: str) -> tuple | None:
    """Parse color from #RRGGBB or R,G,B string."""
    s = s.strip()
    if s.startswith("#") and len(s) == 7:
        try:
            return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))
        except ValueError:
            return None
    if "," in s:
        try:
            parts = [int(x.strip()) for x in s.split(",")]
            if len(parts) == 3:
                return tuple(parts)
        except ValueError:
            return None
    return None
