"""
顺手 — 文件整理模块
"""

import shutil
import click
from pathlib import Path
from datetime import datetime

CATEGORIES = {
    "Images":    {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv"},
    "Archives":  {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Videos":    {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"},
    "Audio":     {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Code":      {".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml", ".toml", ".go", ".rs", ".java", ".c", ".cpp", ".h"},
    "Other":     set(),
}


def organize_files(directory: str, sort_by: str, dry_run: bool):
    """整理文件夹"""
    base = Path(directory)
    files = [f for f in base.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not files:
        click.echo("⚠️  目录下没有可整理的文件")
        return

    if sort_by == "type":
        _organize_by_type(base, files, dry_run)
    elif sort_by == "date":
        _organize_by_date(base, files, dry_run)


def _organize_by_type(base: Path, files: list, dry_run: bool):
    """按文件类型整理"""
    moved = {"categorized": 0, "other": 0}

    for f in files:
        ext = f.suffix.lower()
        category = "Other"
        for cat, exts in CATEGORIES.items():
            if ext in exts:
                category = cat
                break

        dest = base / category
        if not dry_run:
            dest.mkdir(exist_ok=True)
            shutil.move(str(f), str(dest / f.name))
            moved["categorized" if category != "Other" else "other"] += 1
        else:
            moved["categorized" if category != "Other" else "other"] += 1

    click.echo(f"\n📊 整理统计 (按类型):")
    click.echo(f"  归类文件: {moved['categorized']} 个")
    click.echo(f"  无法归类: {moved['other']} 个 (→ Other/)")
    if dry_run:
        click.echo("  ⚠️  预览模式，未实际移动文件")


def _organize_by_date(base: Path, files: list, dry_run: bool):
    """按日期整理 (年-月)"""
    moved = 0

    for f in files:
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        folder = mtime.strftime("%Y-%m")
        dest = base / folder
        if not dry_run:
            dest.mkdir(exist_ok=True)
            shutil.move(str(f), str(dest / f.name))
        moved += 1

    click.echo(f"\n📊 整理统计 (按日期):")
    click.echo(f"  移动文件: {moved} 个")
    if dry_run:
        click.echo("  ⚠️  预览模式，未实际移动文件")
