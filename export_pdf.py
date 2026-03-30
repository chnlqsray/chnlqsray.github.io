"""
Portfolio PDF 导出脚本
使用 Playwright 从本地 index.html 导出高质量 PDF

依赖（已在保活项目中安装）：
    pip install playwright
    playwright install chromium

用法：
    python export_pdf.py                        # 默认导出中文版
    python export_pdf.py --lang en              # 导出英文版
    python export_pdf.py --lang zh --lang en    # 同时导出两版
"""

import argparse
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

# ── 配置 ──────────────────────────────────────────────────────────────────
HTML_FILE = Path(__file__).parent / "index.html"   # 与本脚本同目录
OUTPUT_DIR = Path(__file__).parent                  # PDF 输出到同目录

PDF_OPTIONS = {
    "format": "A4",
    "print_background": True,   # 关键：保留深色背景
    "margin": {
        "top":    "1.2cm",
        "bottom": "1.2cm",
        "left":   "1.4cm",
        "right":  "1.4cm",
    },
    "scale": 0.9,               # 略微缩小，确保内容不溢出
}
# ──────────────────────────────────────────────────────────────────────────


def export_pdf(lang: str) -> Path:
    """导出指定语言的 PDF，返回输出路径。"""
    output_path = OUTPUT_DIR / f"portfolio_{lang}.pdf"
    file_url = HTML_FILE.resolve().as_uri()
    if lang == "en":
        file_url += "?lang=en"

    print(f"[{lang.upper()}] 正在渲染：{file_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 900})

        # 加载页面并等待字体/动画稳定
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(1500)   # 等待 CSS 动画初始帧完成

        # 如果请求英文版，通过 localStorage 确保语言已切换
        if lang == "en":
            page.evaluate("document.documentElement.className = 'lang-en'")
            page.wait_for_timeout(300)

        page.pdf(path=str(output_path), **PDF_OPTIONS)
        browser.close()

    size_kb = output_path.stat().st_size // 1024
    print(f"[{lang.upper()}] ✓ 已输出：{output_path.name}  ({size_kb} KB)")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Export portfolio as PDF using Playwright")
    parser.add_argument(
        "--lang", action="append", choices=["zh", "en"], default=None,
        help="Language(s) to export. Use --lang zh --lang en for both. Default: zh"
    )
    args = parser.parse_args()
    langs = args.lang or ["zh"]

    if not HTML_FILE.exists():
        print(f"✗ 找不到 index.html，请确保脚本与 index.html 在同一目录：{HTML_FILE}")
        return

    print(f"开始导出，目标语言：{langs}\n")
    for lang in langs:
        export_pdf(lang)
    print("\n导出完成。")


if __name__ == "__main__":
    main()
