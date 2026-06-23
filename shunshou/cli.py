"""
顺手 ShunShou — 主 CLI 入口
"""

import click
from shunshou import __version__


@click.group()
@click.version_option(__version__, prog_name="shunshou")
def main():
    """ShunShou: CLI efficiency toolkit.

    Batch image processing, file organization, Markdown to image,
    clipboard utilities, link extraction, GIF tools, and more.
    """
    pass


# ---- 图片模块 ----
@main.group()
def image():
    """Batch image processing"""
    pass


@image.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--width", "-w", type=int, help="目标宽度 (像素)")
@click.option("--height", "-h", type=int, help="目标高度 (像素)")
@click.option("--format", "-f", "output_format", type=click.Choice(["jpg", "png", "webp", "bmp", "tiff"]), help="输出格式")
@click.option("--quality", "-q", type=int, default=85, help="输出质量 (1-100)")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
def resize(directory, width, height, output_format, quality, output):
    """Batch resize and convert image formats"""
    from shunshou.modules.image import batch_resize
    batch_resize(directory, width, height, output_format, quality, output)


@image.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--text", "-t", required=True, help="水印文字")
@click.option("--position", "-p", type=click.Choice(["top-left", "top-right", "bottom-left", "bottom-right", "center"]), default="bottom-right", help="水印位置")
@click.option("--opacity", type=float, default=0.5, help="透明度 (0.0-1.0)")
@click.option("--font-size", type=int, default=36, help="字体大小")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
def watermark(directory, text, position, opacity, font_size, output):
    """Batch add text watermark to images"""
    from shunshou.modules.image import batch_watermark
    batch_watermark(directory, text, position, opacity, font_size, output)


@image.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--to", "-t", "to_format", type=click.Choice(["jpg", "png", "webp", "bmp", "tiff"]), required=True, help="目标格式")
@click.option("--quality", "-q", type=int, default=85, help="输出质量 (1-100)")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
def convert(directory, to_format, quality, output):
    """Batch convert image formats"""
    from shunshou.modules.image import batch_convert
    batch_convert(directory, to_format, quality, output)


# ---- 文件整理模块 ----
@main.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--by", "-b", "sort_by", type=click.Choice(["type", "date"]), default="type", help="整理方式")
@click.option("--dry-run", is_flag=True, help="预览模式，不实际移动文件")
def organize(directory, sort_by, dry_run):
    """Organize files by type or date"""
    from shunshou.modules.organize import organize_files
    organize_files(directory, sort_by, dry_run)


# ---- Markdown 转图模块 ----
@main.command()
@click.argument("markdown_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), default="output.png", help="输出图片路径")
@click.option("--width", "-w", type=int, default=800, help="图片宽度")
@click.option("--theme", type=click.Choice(["light", "dark"]), default="light", help="主题")
def md2img(markdown_file, output, width, theme):
    """Render Markdown file to image"""
    from shunshou.modules.md2img import md_to_image
    md_to_image(markdown_file, output, width, theme)


# ---- 剪贴板模块 ----
@main.group()
def clip():
    """Clipboard operations"""
    pass


@clip.command()
def dedup():
    """Deduplicate clipboard text by line"""
    from shunshou.modules.clipboard import clipboard_dedup
    clipboard_dedup()


@clip.command()
def stats():
    """Show clipboard text statistics"""
    from shunshou.modules.clipboard import clipboard_stats
    clipboard_stats()


# ---- GIF 处理模块 ----
@main.group()
def gif():
    """GIF processing: split, make, optimize, emoji text"""
    pass


@gif.command()
@click.argument("gif_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="输出目录")
@click.option("--format", "-f", "fmt", type=click.Choice(["png", "jpg"]), default="png", help="输出帧格式")
def split(gif_file, output, fmt):
    """Split GIF into individual frames"""
    from shunshou.modules.gif import split_gif
    split_gif(gif_file, output, fmt)


@gif.command()
@click.argument("images_dir", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), required=True, help="输出 GIF 路径")
@click.option("--duration", "-d", type=int, default=200, help="每帧间隔 (毫秒)")
@click.option("--loop", "-l", type=int, default=0, help="循环次数 (0=无限)")
@click.option("--optimize/--no-optimize", default=True, help="是否压缩优化")
def make(images_dir, output, duration, loop, optimize):
    """Create animated GIF from multiple images"""
    from shunshou.modules.gif import make_gif
    make_gif(images_dir, output, duration, loop, optimize)


@gif.command()
@click.argument("gif_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="输出路径")
@click.option("--colors", "-c", type=int, default=128, help="最大颜色数 (2-256)")
@click.option("--scale", "-s", type=float, default=1.0, help="缩放比例 (0.1-1.0)")
def optimize(gif_file, output, colors, scale):
    """Optimize GIF file size"""
    from shunshou.modules.gif import optimize_gif
    optimize_gif(gif_file, output, colors, scale)


@gif.command()
@click.argument("gif_file", type=click.Path(exists=True))
def info(gif_file):
    """Show GIF file info"""
    from shunshou.modules.gif import gif_info
    gif_info(gif_file)


@gif.command()
@click.argument("text")
@click.option("--output", "-o", type=click.Path(), default="emoji.png", help="输出图片路径")
@click.option("--size", "-s", "font_size", type=int, default=80, help="字体大小")
@click.option("--bg", "bg_color", default="#FF6600", help="背景色 (#RRGGBB)")
@click.option("--fg", "text_color", default="#FFFFFF", help="文字色 (#RRGGBB)")
def emoji(text, output, font_size, bg_color, text_color):
    """Generate text emoji image"""
    from shunshou.modules.gif import emoji_text
    emoji_text(text, output, font_size, bg_color, text_color)


# ---- 图片美化模块 ----
@main.group()
def style():
    """Image styling: rounded corners, shadows, borders, stitching"""
    pass


@style.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--radius", "-r", type=int, default=30, help="圆角半径 (像素)")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
def round(directory, radius, output):
    """Add rounded corners to images"""
    from shunshou.modules.style import round_corners
    round_corners(directory, radius, output)


@style.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--offset", type=int, default=10, help="阴影偏移 (像素)")
@click.option("--blur", type=int, default=15, help="模糊半径 (像素)")
@click.option("--opacity", type=int, default=80, help="阴影不透明度 (0-255)")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
def shadow(directory, offset, blur, opacity, output):
    """Add drop shadow to images"""
    from shunshou.modules.style import add_shadow
    add_shadow(directory, offset, blur, opacity, output)


@style.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--width", "-w", type=int, default=10, help="边框宽度 (像素)")
@click.option("--color", "-c", default="#000000", help="边框颜色 (#RRGGBB)")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
def border(directory, width, color, output):
    """Add border to images"""
    from shunshou.modules.style import add_border
    add_border(directory, width, color, output)


@style.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), required=True, help="输出图片路径")
@click.option("--direction", "-d", type=click.Choice(["horizontal", "vertical"]), default="horizontal", help="拼接方向")
@click.option("--gap", "-g", type=int, default=0, help="图片间距 (像素)")
@click.option("--bg", "bg_color", default="#FFFFFF", help="背景色 (#RRGGBB)")
@click.option("--align", type=click.Choice(["top", "center", "bottom"]), default="center", help="对齐方式")
def stitch(directory, output, direction, gap, bg_color, align):
    """Stitch images horizontally or vertically"""
    from shunshou.modules.style import stitch as do_stitch
    do_stitch(directory, output, direction, gap, bg_color, align)


@style.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), required=True, help="输出图片路径")
@click.option("--columns", "-c", type=int, default=3, help="每行列数")
@click.option("--gap", "-g", type=int, default=10, help="间距 (像素)")
@click.option("--bg", "bg_color", default="#FFFFFF", help="背景色 (#RRGGBB)")
@click.option("--size", "cell_size", default=None, help="统一尺寸 (WxH, 如 400x400)")
def grid(directory, output, columns, gap, bg_color, cell_size):
    """Arrange images in a grid layout"""
    from shunshou.modules.style import grid as do_grid
    do_grid(directory, output, columns, gap, bg_color, cell_size)


# ---- 剪贴板增强命令 ----
@clip.command()
@click.option("--indent", "-i", type=int, default=2, help="缩进空格数")
@click.option("--sort/--no-sort", default=False, help="是否按 key 排序")
def jsonfmt(indent, sort):
    """Format JSON in clipboard"""
    from shunshou.modules.clipfmt import json_fmt
    json_fmt(indent, sort)


@clip.command()
def jsonminify():
    """Minify JSON in clipboard"""
    from shunshou.modules.clipfmt import json_minify
    json_minify()


@clip.command()
def b64enc():
    """Encode clipboard text to Base64"""
    from shunshou.modules.clipfmt import b64encode
    b64encode()


@clip.command()
def b64dec():
    """Decode clipboard Base64 to text"""
    from shunshou.modules.clipfmt import b64decode
    b64decode()


# ---- 二维码模块 ----
@main.command()
@click.argument("data")
@click.option("--output", "-o", type=click.Path(), default="qr.png", help="输出图片路径")
@click.option("--size", "-s", type=int, default=300, help="图片尺寸 (像素)")
@click.option("--color", "-c", default="#000000", help="前景色")
@click.option("--bg", default="#FFFFFF", help="背景色")
def qr(data, output, size, color, bg):
    """Generate QR code from text or URL"""
    from shunshou.modules.qr import generate_qr
    generate_qr(data, output, size, color, bg)


# ---- 批量重命名模块 ----
@main.group()
def rename():
    """Batch file rename with pattern matching"""
    pass


@rename.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--pattern", "-p", help="正则匹配模式")
@click.option("--replace", "-r", default="", help="替换内容")
@click.option("--prefix", help="添加前缀")
@click.option("--suffix", help="添加后缀")
@click.option("--dry-run/--go", default=True, help="预览模式 vs 实际执行")
@click.option("--recursive/--no-recursive", default=False, help="是否递归子目录")
def batch(directory, pattern, replace, prefix, suffix, dry_run, recursive):
    """Batch rename files with regex"""
    from shunshou.modules.rename import batch_rename
    batch_rename(directory, pattern, replace, prefix, suffix, dry_run, recursive)


@rename.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--format", "-f", "fmt", default="{:03d}", help="编号格式 (Python format)")
@click.option("--start", "-s", type=int, default=1, help="起始编号")
@click.option("--step", type=int, default=1, help="编号步长")
@click.option("--dry-run/--go", default=True, help="预览模式 vs 实际执行")
@click.option("--sort", "sort_by", type=click.Choice(["name", "date"]), default="name", help="排序方式")
def number(directory, fmt, start, step, dry_run, sort_by):
    """Auto-number files sequentially"""
    from shunshou.modules.rename import auto_number
    auto_number(directory, fmt, start, step, dry_run, sort_by)


# ---- 链接提取模块 ----
@main.command()
@click.argument("source")
@click.option("--output", "-o", type=click.Path(), help="输出文件")
def links(source, output):
    """Extract all links from text or URL"""
    from shunshou.modules.links import extract_links
    extract_links(source, output)
