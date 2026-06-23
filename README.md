<p align="center">
  <img src="https://img.shields.io/badge/顺手-工具瑞士军刀-orange?style=for-the-badge" alt="ShunShou">
</p>

<h1 align="center">顺手 ShunShou</h1>

<p align="center">
  <b>一个命令行效率工具箱，让日常操作变得顺手。</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-lightgrey" alt="Platform">
</p>

---

## 功能

| 模块 | 命令 | 说明 |
|------|------|------|
| 🖼️ 图片批处理 | `ss image` | 批量调整大小、加水印、格式转换 |
| 📁 文件整理 | `ss organize` | 按类型/日期自动归类整理文件夹 |
| 📝 Markdown 转图 | `ss md2img` | 将 Markdown 一键转成精美图片 |
| 📋 剪贴板增强 | `ss clip` | 剪贴板内容格式化、去重、统计 |
| 🔗 链接提取 | `ss links` | 从文本/网页批量提取所有链接 |

---

## 安装

```bash
pip install shunshou
```

或从源码安装：

```bash
git clone https://github.com/wangbeiebi/shunshou.git
cd shunshou
pip install -e .
```

---

## 快速上手

```bash
# 批量转换图片格式
ss image convert ./photos --to webp --quality 80

# 批量添加水印
ss image watermark ./photos --text "©2024" --position bottom-right

# 按文件类型整理目录
ss organize ./downloads --by type

# Markdown 转图片
ss md2img README.md -o output.png --width 800

# 提取网页所有链接
ss links https://example.com

# 剪贴板文本去重
ss clip dedup
```

---

## 示例

### 图片批处理
```bash
# 把整个文件夹图片缩放到 800px 宽，输出 webp
ss image resize ./vacation/ --width 800 --format webp

# 批量加水印，右下角半透明
ss image watermark ./photos/ --text "© MyBrand" --opacity 0.3
```

### 文件整理
```bash
# 下载目录一键分类
ss organize ~/Downloads
# 结果: Images/  Documents/  Archives/  Videos/  ...
```

---

## 贡献

欢迎 PR 和 Issue！有新功能需求请随时提。

---

**顺手** — 不折腾，刚刚好。
