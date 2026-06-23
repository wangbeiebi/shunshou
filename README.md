<p align="center">
  <img src="https://img.shields.io/badge/ShunShou-CLI%20Toolbox-orange?style=for-the-badge" alt="ShunShou">
</p>

<h1 align="center">ShunShou (ShunShou)</h1>

<p align="center">
  <b>A CLI efficiency toolkit. Do more with less.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/Version-0.2.0-blue" alt="Version">
</p>

---

## Features (8 modules, 13+ commands)

| Module | Command | Description |
|--------|---------|-------------|
| Image | `ss image` | Batch resize, watermark, format conversion |
| GIF | `ss gif` | Split, make, optimize GIFs + emoji text |
| Style | `ss style` | Rounded corners, shadows, borders, stitching, grid |
| Organize | `ss organize` | Auto-organize files by type or date |
| Markdown | `ss md2img` | Render Markdown to image (light/dark theme) |
| Clipboard | `ss clip` | Dedup, stats, JSON format/minify, Base64 |
| Links | `ss links` | Extract links from text, file, or URL |

---

## Quick Start

```bash
pip install shunshou
```

### Examples

```bash
# Image batch processing
ss image resize ./photos --width 800 --format webp --quality 80
ss image watermark ./photos --text "(c)2024" --position bottom-right

# GIF tools
ss gif split anime.gif -o ./frames
ss gif make ./frames -o result.gif --duration 200
ss gif emoji "Good Job!" -o emoji.png --bg "#FF6600"

# Image styling
ss style round ./screenshots --radius 20
ss style shadow ./images --blur 15 --opacity 80
ss style stitch ./photos -o banner.png --direction horizontal --gap 10
ss style grid ./photos -o gallery.png --columns 3

# File organization
ss organize ~/Downloads --by type
ss organize ~/Desktop --by date --dry-run

# Markdown to image
ss md2img README.md -o output.png --theme dark

# Clipboard utilities
ss clip dedup     # remove duplicate lines
ss clip jsonfmt   # format JSON in clipboard
ss clip b64enc    # encode to Base64

# Link extraction
ss links https://example.com
```

---

## Requirements

- Python 3.9+
- Pillow, Click, BeautifulSoup4, Markdown, Requests

---

## Roadmap

- [ ] Add rounded corners + shadow to batch image pipeline
- [ ] GIF optimization with quality/size tuning
- [ ] Markdown table rendering
- [ ] Image grid / sprite sheet generator
- [ ] Clipboard JSON formatting
- [ ] GitHub contribution chart CLI version

---

Open source under [MIT](LICENSE). Star, fork, PR welcome!
