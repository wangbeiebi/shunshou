"""
顺手 — 二维码生成模块
"""

import click
from pathlib import Path


def generate_qr(data: str, output: str, size: int, color: str, bg: str):
    """生成二维码图片"""
    try:
        import qrcode
    except ImportError:
        click.echo("❌ 需要安装 qrcode 库: pip install qrcode[pil]")
        return

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size // 25,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    fill = color.lstrip("#")
    back = bg.lstrip("#")
    img = qr.make_image(fill_color=f"#{fill}", back_color=f"#{back}")

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    click.echo(f"✅ 二维码已生成: {output} ({img.size[0]}×{img.size[1]})")
