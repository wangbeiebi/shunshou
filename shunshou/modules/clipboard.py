"""
顺手 — 剪贴板模块
"""


def clipboard_dedup():
    """剪贴板文本按行去重"""
    try:
        import subprocess
        import sys
        
        if sys.platform == "win32":
            result = subprocess.run(["powershell", "-command", "Get-Clipboard"],
                                    capture_output=True, text=True)
            text = result.stdout
        else:
            result = subprocess.run(["xclip", "-selection", "clipboard", "-o"],
                                    capture_output=True, text=True)
            text = result.stdout
    except Exception:
        print("❌ 无法读取剪贴板。请确保安装了 xclip (Linux) 或在 Windows 下运行。")
        return

    lines = text.split("\n")
    seen = set()
    unique = []
    for line in lines:
        stripped = line.rstrip("\r")
        if stripped not in seen:
            seen.add(stripped)
            unique.append(line)

    result_text = "".join(unique) if text.endswith("\n") else "\n".join(unique)

    try:
        import sys
        if sys.platform == "win32":
            subprocess.run(["powershell", "-command", "Set-Clipboard -Value $input"],
                           input=result_text, text=True)
        else:
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=result_text, text=True)

        removed = len(lines) - len(unique)
        print(f"✅ 去重完成！移除了 {removed} 行重复内容（{len(lines)} → {len(unique)} 行）")
    except Exception as e:
        print(f"❌ 写回剪贴板失败: {e}")
        print("--- 去重结果 ---")
        print(result_text)


def clipboard_stats():
    """剪贴板文本统计"""
    try:
        import subprocess
        import sys
        
        if sys.platform == "win32":
            result = subprocess.run(["powershell", "-command", "Get-Clipboard"],
                                    capture_output=True, text=True)
            text = result.stdout
        else:
            result = subprocess.run(["xclip", "-selection", "clipboard", "-o"],
                                    capture_output=True, text=True)
            text = result.stdout
    except Exception:
        print("❌ 无法读取剪贴板。")
        return

    lines = [l for l in text.split("\n")]
    chars = len(text)
    words = len(text.split())
    blank_lines = sum(1 for l in lines if l.strip() == "")

    print("📋 剪贴板统计")
    print(f"   总字符数: {chars}")
    print(f"   总单词数: {words}")
    print(f"   总行数:   {len(lines)}")
    print(f"   空白行:   {blank_lines}")
    print(f"   非空行:   {len(lines) - blank_lines}")
    if chars > 0:
        print(f"   行均字符: {chars / max(len(lines), 1):.1f}")
