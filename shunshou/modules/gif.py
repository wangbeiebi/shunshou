"""
顺手 — GIF 处理模块
"""

import os
import click
import json
import struct
from pathlib import Path
from PIL import Image, ImageSequence


def split_gif(gif_path: str, output_dir: str | None, fmt: str):
    """将 GIF 拆解为逐帧图片"""
    path = Path(gif_path)
    if not path.exists():
        click.echo(f"❌ 文件不存在: {gif_path}")
        return

    out = Path(output_dir) if output_dir else Path.cwd() / f"{path.stem}_frames"
    out.mkdir(parents=True, exist_ok=True)

    img = Image.open(path)
    frames = list(ImageSequence.Iterator(img))

    with click.progressbar(enumerate(frames), label="🎞️  拆解帧", length=len(frames)) as bar:
        for i, frame in bar:
            frame = frame.convert("RGBA")
            save_path = out / f"{path.stem}_{i:04d}.{fmt}"
            frame.save(save_path)

    click.echo(f"\n✅ 完成！{len(frames)} 帧 → {out}")


def make_gif(images_dir: str, output: str, duration: int, loop: int, optimize: bool):
    """将多张图片合成为 GIF"""
    path = Path(images_dir)
    if not path.exists():
        click.echo(f"❌ 目录不存在: {images_dir}")
        return

    # 收集图片
    exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
    image_files = sorted([f for f in path.iterdir() if f.suffix.lower() in exts and f.is_file()])

    if len(image_files) < 2:
        click.echo(f"❌ 至少需要 2 张图片，找到 {len(image_files)} 张")
        return

    frames = []
    with click.progressbar(image_files, label="🧩 合成 GIF") as bar:
        for f in bar:
            img = Image.open(f).convert("RGBA")
            # 统一尺寸（取第一张的尺寸）
            if frames:
                target_size = frames[0].size
                if img.size != target_size:
                    img = img.resize(target_size, Image.LANCZOS)
            frames.append(img)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=loop,
        optimize=optimize,
        disposal=2
    )

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    click.echo(f"\n✅ GIF 已生成: {output}")
    click.echo(f"   帧数: {len(frames)} | 间隔: {duration}ms | 大小: {file_size_mb:.1f}MB")


def optimize_gif(gif_path: str, output: str | None, colors: int, scale: float):
    """优化 GIF 文件大小"""
    path = Path(gif_path)
    if not path.exists():
        click.echo(f"❌ 文件不存在: {gif_path}")
        return

    original_size = path.stat().st_size / (1024 * 1024)
    out = Path(output) if output else path.parent / f"{path.stem}_optimized.gif"

    img = Image.open(path)
    frames = list(ImageSequence.Iterator(img))

    optimized = []
    with click.progressbar(enumerate(frames), label="🗜️  压缩优化", length=len(frames)) as bar:
        for i, frame in bar:
            if scale < 1.0:
                new_w = max(1, int(frame.width * scale))
                new_h = max(1, int(frame.height * scale))
                frame = frame.resize((new_w, new_h), Image.LANCZOS)

            # 量化减少颜色
            if colors < 256:
                frame = frame.convert("RGBA")
                frame = frame.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
            else:
                frame = frame.convert("P", palette=Image.Palette.ADAPTIVE)

            optimized.append(frame)

    optimized[0].save(
        out,
        save_all=True,
        append_images=optimized[1:],
        duration=img.info.get("duration", 100),
        loop=img.info.get("loop", 0),
        optimize=True,
        disposal=2
    )

    new_size = out.stat().st_size / (1024 * 1024)
    reduction = (1 - new_size / original_size) * 100
    click.echo(f"\n✅ 优化完成: {out}")
    click.echo(f"   {original_size:.1f}MB → {new_size:.1f}MB (减少 {reduction:.1f}%)")


def gif_info(gif_path: str):
    """查看 GIF 文件信息"""
    path = Path(gif_path)
    if not path.exists():
        click.echo(f"❌ 文件不存在: {gif_path}")
        return

    img = Image.open(path)
    frames = list(ImageSequence.Iterator(img))

    click.echo(f"📊 {path.name}")
    click.echo(f"   尺寸: {img.width}×{img.height}")
    click.echo(f"   帧数: {len(frames)}")
    click.echo(f"   时长: {img.info.get('duration', '?')}ms/帧")
    click.echo(f"   循环: {'无限' if img.info.get('loop', 0) == 0 else f\"{img.info['loop']}次\"}")
    click.echo(f"   文件大小: {path.stat().st_size / 1024:.1f}KB")


def emoji_text(text: str, output: str, font_size: int, bg_color: str, text_color: str):
    """生成文字表情包（带背景的纯文字图）"""
    from PIL import Image, ImageDraw, ImageFont
    import platform

    # 颜色解析
    bg = _parse_color(bg_color) or (255, 255, 255)
    fg = _parse_color(text_color) or (0, 0, 0)

    # 加载字体（要大）
    system = platform.system()
    font = None
    if system == "Windows":
        for fp in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
            if os.path.exists(fp):
                font = ImageFont.truetype(fp, font_size)
                break
    elif system == "Darwin":
        fp = "/System/Library/Fonts/PingFang.ttc"
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, font_size)

    if font is None:
        font = ImageFont.load_default()

    # 测量文字
    dummy = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    padding = font_size // 2
    img = Image.new("RGB", (tw + padding * 2, th + padding * 2), bg)
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), text, font=font, fill=fg)

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    img.save(output)
    click.echo(f"✅ 表情包已生成: {output} ({img.width}×{img.height})")


def _parse_color(s: str) -> tuple | None:
    """解析颜色字符串: #RRGGBB 或逗号分隔的 RGB"""
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
