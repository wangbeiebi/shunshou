"""
顺手 — 图片批处理模块
"""

import os
import click
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"}


def _list_images(directory: str):
    """扫描目录下所有图片"""
    path = Path(directory)
    images = []
    for f in path.iterdir():
        if f.suffix.lower() in SUPPORTED_EXTENSIONS and f.is_file():
            images.append(f)
    return images


def _ensure_output_dir(output: str | None, base_dir: str) -> Path:
    """确保输出目录存在"""
    if output:
        out = Path(output)
    else:
        out = Path(base_dir) / "processed"
    out.mkdir(parents=True, exist_ok=True)
    return out


def batch_resize(directory: str, width: int | None, height: int | None,
                 output_format: str | None, quality: int, output_dir: str | None):
    """批量调整图片尺寸"""
    images = _list_images(directory)
    if not images:
        click.echo("⚠️  目录下没有找到图片文件")
        return

    out = _ensure_output_dir(output_dir, directory)
    fmt = output_format or "jpg"

    with click.progressbar(images, label="🖼️  处理图片") as bar:
        for img_path in bar:
            try:
                img = Image.open(img_path)
                orig_w, orig_h = img.size

                # 计算目标尺寸
                if width and height:
                    new_size = (width, height)
                elif width:
                    ratio = width / orig_w
                    new_size = (width, int(orig_h * ratio))
                elif height:
                    ratio = height / orig_h
                    new_size = (int(orig_w * ratio), height)
                else:
                    new_size = (orig_w, orig_h)

                img = img.resize(new_size, Image.LANCZOS)
                save_path = out / f"{img_path.stem}.{fmt}"
                img.save(save_path, quality=quality if fmt in ("jpg", "webp") else None)
            except Exception as e:
                click.echo(f"\n❌ {img_path.name}: {e}")

    click.echo(f"\n✅ 完成！已处理 {len(images)} 张图片 → {out}")


def batch_watermark(directory: str, text: str, position: str, opacity: float,
                    font_size: int, output_dir: str | None):
    """批量添加文字水印"""
    images = _list_images(directory)
    if not images:
        click.echo("⚠️  目录下没有找到图片文件")
        return

    out = _ensure_output_dir(output_dir, directory)

    # 尝试加载中文字体
    font = _get_font(font_size)

    with click.progressbar(images, label="💧 添加水印") as bar:
        for img_path in bar:
            try:
                img = Image.open(img_path).convert("RGBA")
                overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)

                bbox = draw.textbbox((0, 0), text, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                margin = 20

                pos_map = {
                    "top-left": (margin, margin),
                    "top-right": (img.width - tw - margin, margin),
                    "bottom-left": (margin, img.height - th - margin),
                    "bottom-right": (img.width - tw - margin, img.height - th - margin),
                    "center": ((img.width - tw) // 2, (img.height - th) // 2),
                }
                x, y = pos_map.get(position, pos_map["bottom-right"])

                alpha = int(255 * opacity)
                draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))

                result = Image.alpha_composite(img, overlay)
                result = result.convert("RGB")
                save_path = out / f"{img_path.stem}.png"
                result.save(save_path)
            except Exception as e:
                click.echo(f"\n❌ {img_path.name}: {e}")

    click.echo(f"\n✅ 完成！已处理 {len(images)} 张图片 → {out}")


def batch_convert(directory: str, to_format: str, quality: int, output_dir: str | None):
    """批量转换图片格式"""
    images = _list_images(directory)
    if not images:
        click.echo("⚠️  目录下没有找到图片文件")
        return

    out = _ensure_output_dir(output_dir, directory)

    with click.progressbar(images, label="🔄 转换格式") as bar:
        for img_path in bar:
            try:
                img = Image.open(img_path).convert("RGB")
                save_path = out / f"{img_path.stem}.{to_format}"
                img.save(save_path, quality=quality if to_format in ("jpg", "webp") else None)
            except Exception as e:
                click.echo(f"\n❌ {img_path.name}: {e}")

    click.echo(f"\n✅ 完成！已处理 {len(images)} 张图片 → {out}")


def _get_font(size: int):
    """尝试获取本地中文字体"""
    import platform
    system = platform.system()
    font_paths = []

    if system == "Windows":
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",       # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",     # 黑体
            "C:/Windows/Fonts/simsun.ttc",     # 宋体
        ]
    elif system == "Darwin":
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
        ]
    else:
        font_paths = [
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ]

    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)

    return ImageFont.load_default()
