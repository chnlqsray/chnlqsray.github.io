"""
Portfolio PDF 导出脚本
使用 Playwright 从本地 index.html 导出高质量 PDF

依赖：
    pip install playwright
    playwright install chromium

用法：
    python export_pdf.py                          # 中文版，默认缩放
    python export_pdf.py --lang en                # 英文版
    python export_pdf.py --lang zh --lang en      # 同时导出两版
    python export_pdf.py --scale 0.82             # 指定缩放比例
    python export_pdf.py --lang en --scale 0.80   # 英文版 + 自定义缩放

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  调参指南（如果 PDF 空白过多或内容溢出页边）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  --scale  缩放比例（默认 0.86）
    · 值越小 → 内容越紧凑，每页放得下更多卡片
    · 值越大 → 内容越大，可能每页只放一张卡片
    · 推荐范围：0.78 ~ 0.92
    · 建议先试 0.86，如果英文版每页只有一张卡片，改为 0.80 或 0.78

  --margin  页边距（默认 1.2cm，格式："上下 左右" 或 "统一值"）
    · 减小边距可以给内容多留空间（最小建议 0.8cm）

  页面内容本身的间距（需要修改 index.html 里的 @media print CSS）：
    · .project-card { padding }    → 卡片内边距
    · .card-desc { font-size }     → 描述文字大小
    · .feature-list li { font-size } → 功能列表字体大小
    · section { padding }          → 各章节间距
    · 以上均在 index.html 的 @media print 块中，搜索即可找到

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

# ── 默认配置 ──────────────────────────────────────────────────────────────
HTML_FILE   = Path(__file__).parent / "index.html"
OUTPUT_DIR  = Path(__file__).parent
DEFAULT_SCALE  = 0.86          # ← 首先调这个。太多空白 → 调小；内容溢出 → 调大
DEFAULT_MARGIN = "1.2cm"       # ← 其次调这个。统一上下左右边距
# ──────────────────────────────────────────────────────────────────────────


def export_pdf(lang: str, scale: float, margin: str) -> Path:
    output_path = OUTPUT_DIR / f"portfolio_{lang}.pdf"
    file_url = HTML_FILE.resolve().as_uri()
    if lang == "en":
        file_url += "?lang=en"

    print(f"[{lang.upper()}] scale={scale}  margin={margin}")
    print(f"[{lang.upper()}] 渲染：{file_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(1500)

        if lang == "en":
            page.evaluate("document.documentElement.className = 'lang-en'")
            page.wait_for_timeout(300)

        page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True,   # 保留深色背景
            scale=scale,
            margin={
                "top":    margin,
                "bottom": margin,
                "left":   margin,
                "right":  margin,
            },
        )
        browser.close()

    size_kb = output_path.stat().st_size // 1024
    print(f"[{lang.upper()}] ✓ 输出：{output_path.name}  ({size_kb} KB)\n")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Export portfolio as PDF using Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python export_pdf.py                        中文版，默认参数
  python export_pdf.py --lang en              英文版
  python export_pdf.py --lang zh --lang en    同时导出两版
  python export_pdf.py --scale 0.80           更紧凑（英文版空白太多时用）
  python export_pdf.py --lang en --scale 0.78 英文版最紧凑
        """
    )
    parser.add_argument(
        "--lang", action="append", choices=["zh", "en"], default=None,
        help="导出语言（可多次使用：--lang zh --lang en）。默认：zh"
    )
    parser.add_argument(
        "--scale", type=float, default=DEFAULT_SCALE,
        help=f"缩放比例，0.78~0.92（默认 {DEFAULT_SCALE}）。英文版空白多时调小"
    )
    parser.add_argument(
        "--margin", type=str, default=DEFAULT_MARGIN,
        help=f"页边距，如 '1.0cm'（默认 {DEFAULT_MARGIN}）"
    )
    args = parser.parse_args()
    langs = args.lang or ["zh"]

    if not HTML_FILE.exists():
        print(f"✗ 找不到 index.html，请确保脚本与 index.html 在同一目录：{HTML_FILE}")
        return

    print(f"开始导出：语言={langs}  scale={args.scale}  margin={args.margin}\n")
    for lang in langs:
        export_pdf(lang, args.scale, args.margin)
    print("全部完成。")


if __name__ == "__main__":
    main()
