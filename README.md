# chnlqsray.github.io — AI Projects Portfolio

个人作品集主页，部署于 GitHub Pages：**[chnlqsray.github.io](https://chnlqsray.github.io)**

The personal portfolio homepage, deployed via GitHub Pages.

---

## 仓库内容 · Contents

| 文件 | 说明 |
|------|------|
| `index.html` | 作品集单页应用，双语切换（中/英），零外部依赖，离线可打开 |
| `export_pdf.py` | Playwright PDF 导出脚本，强制保留深色主题，支持中英双语批量导出 |
| `requirements.txt` | PDF 导出脚本依赖 |

---

## PDF 导出 · PDF Export

本仓库包含一个基于 Playwright 的 PDF 导出脚本，复用保活项目已有的 Playwright 环境，规避浏览器虚拟打印机的位图渲染限制，生成保留深色主题、超链接可点击的高质量 PDF。

This repository includes a Playwright-based PDF export script that reuses the existing Playwright environment, bypasses virtual print driver bitmap limitations, and produces high-quality PDFs with dark theme and clickable hyperlinks preserved.

```bash
# 安装依赖 / Install dependencies
pip install -r requirements.txt
playwright install chromium

# 导出中文版 / Export Chinese version
python export_pdf.py

# 导出英文版 / Export English version
python export_pdf.py --lang en

# 同时导出两版 / Export both
python export_pdf.py --lang zh --lang en
```

脚本与 `index.html` 需在同一目录下运行。The script must be run from the same directory as `index.html`.

---

## 技术说明 · Technical Notes

- **零外部字体依赖**：移除 Google Fonts，改用系统字体栈（含 PingFang SC / Microsoft YaHei），境内访问无白屏风险
- **双语切换**：导航栏 `EN / 中文` 按钮，语言偏好通过 `localStorage` 持久化，支持 `?lang=en` URL 参数
- **No external font dependencies**: Google Fonts removed, replaced with system font stack; no white-screen risk on mainland China networks
- **Bilingual toggle**: `EN / 中文` button in nav bar; language preference persisted via `localStorage`; supports `?lang=en` URL parameter

---

*Part of the AI Projects Portfolio · [chnlqsray.github.io](https://chnlqsray.github.io)*
