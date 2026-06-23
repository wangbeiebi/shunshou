"""
顺手 ShunShou — 主 CLI 入口
"""

import click
from shunshou import __version__


@click.group()
@click.version_option(__version__, prog_name="shunshou")
def main():
    """🛠️ 顺手 — 命令行效率工具箱。

    常用操作一键搞定：图片批处理、文件整理、Markdown 转图等。

    \b
    快速开始:
      ss image --help     查看图片处理相关命令
      ss organize --help  查看文件整理相关命令
      ss md2img --help    查看 Markdown 转图命令
    """
    pass


# ---- 图片模块 ----
@main.group()
def image():
    """🖼️  批量图片处理"""
    pass


@image.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--width", "-w", type=int, help="目标宽度 (像素)")
@click.option("--height", "-h", type=int, help="目标高度 (像素)")
@click.option("--format", "-f", "output_format", type=click.Choice(["jpg", "png", "webp", "bmp", "tiff"]), help="输出格式")
@click.option("--quality", "-q", type=int, default=85, help="输出质量 (1-100)")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
def resize(directory, width, height, output_format, quality, output):
    """批量调整图片尺寸并转换格式"""
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
    """给图片批量添加文字水印"""
    from shunshou.modules.image import batch_watermark
    batch_watermark(directory, text, position, opacity, font_size, output)


@image.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--to", "-t", "to_format", type=click.Choice(["jpg", "png", "webp", "bmp", "tiff"]), required=True, help="目标格式")
@click.option("--quality", "-q", type=int, default=85, help="输出质量 (1-100)")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
def convert(directory, to_format, quality, output):
    """批量转换图片格式"""
    from shunshou.modules.image import batch_convert
    batch_convert(directory, to_format, quality, output)


# ---- 文件整理模块 ----
@main.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--by", "-b", "sort_by", type=click.Choice(["type", "date"]), default="type", help="整理方式")
@click.option("--dry-run", is_flag=True, help="预览模式，不实际移动文件")
def organize(directory, sort_by, dry_run):
    """📁 自动整理文件夹 (按类型/日期归类)"""
    from shunshou.modules.organize import organize_files
    organize_files(directory, sort_by, dry_run)


# ---- Markdown 转图模块 ----
@main.command()
@click.argument("markdown_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), default="output.png", help="输出图片路径")
@click.option("--width", "-w", type=int, default=800, help="图片宽度")
@click.option("--theme", type=click.Choice(["light", "dark"]), default="light", help="主题")
def md2img(markdown_file, output, width, theme):
    """📝 将 Markdown 文件渲染为图片"""
    from shunshou.modules.md2img import md_to_image
    md_to_image(markdown_file, output, width, theme)


# ---- 剪贴板模块 ----
@main.group()
def clip():
    """📋 剪贴板操作"""
    pass


@clip.command()
def dedup():
    """剪贴板文本去重 (按行)"""
    from shunshou.modules.clipboard import clipboard_dedup
    clipboard_dedup()


@clip.command()
def stats():
    """剪贴板文本统计"""
    from shunshou.modules.clipboard import clipboard_stats
    clipboard_stats()


# ---- 链接提取模块 ----
@main.command()
@click.argument("source")
@click.option("--output", "-o", type=click.Path(), help="输出文件")
def links(source, output):
    """🔗 从文本或 URL 中提取所有链接"""
    from shunshou.modules.links import extract_links
    extract_links(source, output)
