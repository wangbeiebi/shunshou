"""
顺手 — 剪贴板增强模块
额外功能：JSON 格式化、Base64 编解码
"""

import click
import json
import base64
import platform
import subprocess


def _get_clipboard_text() -> str | None:
    """读取剪贴板文本"""
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.run(
                ["powershell", "-Command", "Get-Clipboard"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        elif system == "Darwin":
            result = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=5)
            return result.stdout.strip()
        else:
            result = subprocess.run(["xclip", "-o", "-selection", "clipboard"],
                                    capture_output=True, text=True, timeout=5)
            return result.stdout.strip()
    except Exception:
        return None


def _set_clipboard_text(text: str):
    """写入剪贴板"""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["powershell", "-Command", f"Set-Clipboard -Value '{text}'"],
                           timeout=5, shell=True)
        elif system == "Darwin":
            subprocess.run(["pbcopy"], input=text, text=True, timeout=5)
        else:
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=text, text=True, timeout=5)
    except Exception as e:
        click.echo(f"❌ 写入剪贴板失败: {e}")


def json_fmt(indent: int, sort_keys: bool):
    """剪贴板 JSON 格式化"""
    text = _get_clipboard_text()
    if not text:
        click.echo("⚠️  剪贴板为空")
        return

    try:
        data = json.loads(text)
        formatted = json.dumps(data, ensure_ascii=False, indent=indent, sort_keys=sort_keys)
        _set_clipboard_text(formatted)
        click.echo(f"✅ JSON 已格式化 ({len(formatted)} 字符) → 剪贴板")
    except json.JSONDecodeError as e:
        click.echo(f"❌ JSON 解析失败: {e}")
        click.echo("   提示: 确保剪贴板内容是有效的 JSON")


def json_minify():
    """剪贴板 JSON 压缩（去除空白）"""
    text = _get_clipboard_text()
    if not text:
        click.echo("⚠️  剪贴板为空")
        return

    try:
        data = json.loads(text)
        compressed = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        _set_clipboard_text(compressed)
        click.echo(f"✅ JSON 已压缩 ({len(compressed)} 字符，减少 {len(text) - len(compressed)} 字符) → 剪贴板")
    except json.JSONDecodeError as e:
        click.echo(f"❌ JSON 解析失败: {e}")


def b64encode():
    """剪贴板文本 → Base64"""
    text = _get_clipboard_text()
    if not text:
        click.echo("⚠️  剪贴板为空")
        return

    encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
    _set_clipboard_text(encoded)
    click.echo(f"✅ Base64 编码完成 ({len(encoded)} 字符) → 剪贴板")


def b64decode():
    """剪贴板 Base64 → 文本"""
    text = _get_clipboard_text()
    if not text:
        click.echo("⚠️  剪贴板为空")
        return

    try:
        decoded = base64.b64decode(text).decode("utf-8")
        _set_clipboard_text(decoded)
        click.echo(f"✅ Base64 解码完成 ({len(decoded)} 字符) → 剪贴板")
    except Exception as e:
        click.echo(f"❌ Base64 解码失败: {e}")
