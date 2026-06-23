# 🛠️ 我写了一个命令行工具，让你的日常工作"顺手"起来

> 11个文件，874行代码，5个实用模块——一个轻量但好用的 Python CLI 工具箱。

---

## 为什么要写这个？

日常开发中总有一些重复性操作让人头疼：

- 老板丢来 50 张图，要你统一调尺寸、加水印
- 下载文件夹乱成一团，找文件全靠搜索
- 想把 Markdown 笔记转成图片发朋友圈，还得截图
- 从网页里扒链接，一个个复制粘贴

这些小事不值得打开 PS，也不值得写个临时脚本——但就是烦。

于是有了 **[顺手 (ShunShou)](https://github.com/wangbeiebi/shunshou)**。

---

## 它能干什么？

```bash
# 一键批量调整图片尺寸
ss image resize ./photos --width 800 --format webp --quality 80

# 一键加水印
ss image watermark ./photos --text "©2024" --position bottom-right

# 一键整理文件夹（按类型/日期自动归类）
ss organize ~/Downloads

# Markdown 直接渲染成图片！
ss md2img README.md -o output.png --theme dark

# 从网页批量提取所有链接
ss links https://example.com

# 剪贴板去重
ss clip dedup
```

---

## 技术选型

| 依赖 | 用途 |
|------|------|
| **Click** | 命令行框架，嵌套子命令 + 进度条 |
| **Pillow** | 图片处理，包括水印、渲染 MD 为图 |
| **BeautifulSoup** | 网页链接提取 |
| **标准库** | pathlib, shutil, subprocess... |

故意做得轻——不需要 Node、不需要 Docker、不需要 GPU。
装一个 `pip install shunshou` 就能用。

---

## 核心亮点

### 🖼️ 图片批处理
支持 resize / watermark / convert 三种操作，自动识别目录下所有图片，进度条显示处理状态。水印功能自动加载系统自带中文字体（微软雅黑/PingFang/Noto Sans CJK 全覆盖）。

```python
# 核心就这么几行
img = Image.open(path).convert("RGBA")
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
draw.text((x, y), "©水印", font=font, fill=(255, 255, 255, alpha))
result = Image.alpha_composite(img, overlay)
```

### 📁 智能文件整理
按扩展名自动归类为 Images / Documents / Archives / Videos / Audio / Code / Other 七大类。还支持按修改日期按月归档。支持 `--dry-run` 预览模式，不怕误操作。

### 📝 Markdown 转图片
纯 PIL 实现，无需 headless 浏览器。支持标题、代码块、粗体/斜体 Markdown 语法解析，提供 light/dark 两种主题。

### 📋 剪贴板工具
跨平台支持（Win/Linux/Mac），用系统原生 clipboard 命令读写。去重、统计，两个命令搞定。

### 🔗 链接提取
传 URL 就爬整页的 `<a>` 标签，传文件就扫文本，传字符串也能扒。自动处理相对链接，支持输出到文件。

---

## 为什么是 Python？

不需要编译，不需要复杂环境。Python 3.9+ 就能跑。用 `pipx` 装更干净：

```bash
pipx install shunshou
```

---

## 下一步计划

- [ ] 图片批量添加圆角/阴影
- [ ] 支持 GIF 处理
- [ ] Markdown 转图支持更多语法（表格、图片）
- [ ] 剪贴板支持 JSON 格式化
- [ ] 一键生成 GitHub 贡献图的 CLI 版本

---

## 开源地址

👉 **[github.com/wangbeiebi/shunshou](https://github.com/wangbeiebi/shunshou)**

欢迎 ⭐Star，提 Issue，更欢迎 PR！

如果你也有"顺手"想加的功能，评论区告诉我 👇

---

**顺手** — 不折腾，刚刚好。
