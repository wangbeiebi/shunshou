"""
顺手 — 批量重命名模块
"""

import re
import click
from pathlib import Path


def batch_rename(directory: str, pattern: str, replace: str, prefix: str,
                 suffix: str, dry_run: bool, recursive: bool):
    """批量重命名文件"""
    path = Path(directory)
    glob = path.rglob("*") if recursive else path.glob("*")
    files = [f for f in glob if f.is_file()]

    if not files:
        click.echo("⚠️  目录下没有文件")
        return

    count = 0
    for f in files:
        new_name = f.stem

        if pattern:
            new_name = re.sub(pattern, replace, new_name)
        if prefix:
            new_name = prefix + new_name
        if suffix:
            new_name = new_name + suffix

        new_path = f.parent / f"{new_name}{f.suffix}"

        if new_path == f:
            continue

        if dry_run:
            click.echo(f"  📝 {f.name} → {new_path.name}")
        else:
            f.rename(new_path)
        count += 1

    if dry_run:
        click.echo(f"\n✅ 预览完成：{count} 个文件将被重命名（--dry-run 模式，未实际修改）")
    else:
        click.echo(f"\n✅ 完成！已重命名 {count} 个文件")


def auto_number(directory: str, fmt: str, start: int, step: int,
                dry_run: bool, sort_by: str):
    """自动编号重命名"""
    path = Path(directory)
    files = sorted(path.iterdir(), key=lambda x: (
        x.stat().st_mtime if sort_by == "date" else x.name
    ))
    files = [f for f in files if f.is_file()]

    if not files:
        click.echo("⚠️  目录下没有文件")
        return

    count = 0
    for i, f in enumerate(files):
        num = start + i * step
        new_name = f"{fmt.format(num)}{f.suffix}"
        new_path = f.parent / new_name

        if dry_run:
            click.echo(f"  📝 {f.name} → {new_name}")
        else:
            f.rename(new_path)
        count += 1

    if dry_run:
        click.echo(f"\n✅ 预览完成：{count} 个文件将按编号重命名")
    else:
        click.echo(f"\n✅ 完成！已编号重命名 {count} 个文件")
