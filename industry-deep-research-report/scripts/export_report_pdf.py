#!/usr/bin/env python3
"""Export a saved industry report Markdown file to styled HTML and PDF.

The script intentionally uses only Python standard-library modules plus a local
Chrome/Edge executable, so the skill can work without installing packages.
"""

from __future__ import annotations

import argparse
from datetime import date
import html
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

try:
    from pypdf import PdfReader, PdfWriter
    from pypdf._page import PageObject
    from pypdf.generic import DictionaryObject, NameObject, StreamObject
except Exception:  # pragma: no cover - optional enhancement
    PdfReader = None
    PdfWriter = None
    PageObject = None
    DictionaryObject = None
    NameObject = None
    StreamObject = None


STYLE = """
@page { size: A4; margin: 16mm 15mm 18mm; }
:root {
  --ink: #192028;
  --muted: #5c6673;
  --line: #d8dde5;
  --soft: #f5f7fa;
  --accent: #0f6b7a;
  --accent-dark: #12323a;
  --warn: #b05d2a;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: #fff;
  color: var(--ink);
  font-family: "Microsoft YaHei", "Noto Sans CJK SC", "PingFang SC", Arial, sans-serif;
  font-size: 12.5px;
  line-height: 1.72;
}
main.content {
  padding: 0;
}
.cover {
  min-height: 245mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  page-break-after: always;
  border-bottom: 4px solid var(--accent);
}
.cover .eyebrow {
  color: var(--accent);
  font-weight: 800;
  letter-spacing: 0;
  margin-bottom: 16px;
}
.cover h1 {
  border: 0;
  font-size: 34px;
  max-width: 720px;
  margin-bottom: 18px;
}
.cover .subtitle {
  color: var(--muted);
  font-size: 15px;
  max-width: 680px;
  margin-bottom: 30px;
}
.cover .meta {
  border-top: 1px solid var(--line);
  padding-top: 14px;
  color: var(--muted);
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 6px 18px;
  max-width: 680px;
}
.toc {
  page-break-after: always;
}
.toc h2 {
  margin-top: 0;
}
.toc ol {
  columns: 2;
  column-gap: 24px;
  margin-left: 0;
  list-style-position: inside;
}
.toc li {
  break-inside: avoid;
  margin: 6px 0;
}
h1 {
  font-size: 30px;
  line-height: 1.2;
  margin: 0 0 18px;
  padding: 0 0 12px;
  border-bottom: 2px solid var(--accent);
  color: #101820;
  font-weight: 800;
}
h2 {
  font-size: 18px;
  line-height: 1.35;
  margin: 22px 0 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid var(--line);
  color: #0f2932;
  page-break-after: avoid;
}
h3 {
  font-size: 14.5px;
  margin: 16px 0 8px;
  color: #12323a;
  page-break-after: avoid;
}
p { margin: 8px 0; text-align: justify; }
ul, ol { margin: 7px 0 10px 20px; padding: 0; }
li { margin: 4px 0; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0 14px;
  font-size: 11.1px;
  page-break-inside: avoid;
}
th {
  background: #eaf2f4;
  color: #12323a;
  border: 1px solid var(--line);
  padding: 7px;
  text-align: left;
  font-weight: 700;
}
td {
  border: 1px solid var(--line);
  padding: 7px;
  vertical-align: top;
}
tr:nth-child(even) td { background: #fbfcfd; }
blockquote {
  margin: 10px 0;
  padding: 9px 12px;
  background: var(--soft);
  border-left: 4px solid var(--accent);
  color: #27313a;
}
code {
  font-family: Consolas, "Courier New", monospace;
  font-size: 0.94em;
  background: #f1f3f6;
  padding: 1px 4px;
  border-radius: 3px;
}
a { color: #0d5f6c; text-decoration: none; word-break: break-word; }
.callout {
  background: var(--soft);
  border-left: 4px solid var(--accent);
  padding: 10px 12px;
  margin: 12px 0;
}
pre {
  background: #f4f6f8;
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  padding: 10px 12px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 11px;
  line-height: 1.55;
}
pre code {
  background: transparent;
  padding: 0;
}
@media print {
  a[href]::after { content: ""; }
}
"""


CHAT_LINE_PATTERNS = (
    "要不要我顺手生成 PDF",
    "回复“生成 PDF”",
    "回复\"生成 PDF\"",
    "我就一键导出",
    "我可以帮你",
    "以下是",
)


def clean_markdown_for_pdf(markdown_text: str) -> str:
    lines = []
    for line in markdown_text.replace("\r\n", "\n").split("\n"):
        if any(pattern in line for pattern in CHAT_LINE_PATTERNS):
            continue
        if re.search(r"file://|[A-Za-z]:\\", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


def render_inline(text: str) -> str:
    placeholders: list[tuple[str, str]] = []

    def store_link(match: re.Match[str]) -> str:
        idx = len(placeholders)
        label = html.escape(match.group(1), quote=False)
        url = html.escape(match.group(2), quote=True)
        token = f"@@LINK{idx}@@"
        placeholders.append((token, f'<a href="{url}">{label}</a>'))
        return token

    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", store_link, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    for token, value in placeholders:
        text = text.replace(token, value)
    return text


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_delimiter(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def render_table(lines: list[str]) -> str:
    headers = split_table_row(lines[0])
    body = [split_table_row(line) for line in lines[2:]]
    parts = ["<table>", "<thead><tr>"]
    parts.extend(f"<th>{render_inline(cell)}</th>" for cell in headers)
    parts.append("</tr></thead><tbody>")
    for row in body:
        parts.append("<tr>")
        parts.extend(f"<td>{render_inline(cell)}</td>" for cell in row)
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "\n".join(parts)


def extract_headings(markdown_text: str) -> list[tuple[int, str, str]]:
    headings: list[tuple[int, str, str]] = []
    first_h1_seen = False
    counter = 0
    for line in markdown_text.replace("\r\n", "\n").split("\n"):
        match = re.match(r"^(#{1,3})\s+(.+)$", line.rstrip())
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        if level == 1 and not first_h1_seen:
            first_h1_seen = True
            continue
        if level <= 2:
            counter += 1
            headings.append((level, text, f"section-{counter}"))
    return headings


def build_cover(title: str, report_date: str) -> str:
    safe_title = html.escape(title, quote=False)
    return f"""
<section class="cover">
  <div class="eyebrow">Industry Deep Research Report</div>
  <h1>{safe_title}</h1>
  <p class="subtitle">一份面向创业决策、投资判断、企业战略分析和商业计划参考的行业深度研究报告。</p>
  <div class="meta">
    <strong>报告日期</strong><span>{html.escape(report_date, quote=False)}</span>
    <strong>报告类型</strong><span>决策型行业深度研究报告</span>
    <strong>研究方法</strong><span>公开资料检索、来源审计、数据交叉验证、商业模型分析、图表规划</span>
    <strong>输出格式</strong><span>PDF-ready HTML / PDF</span>
  </div>
</section>
"""


def build_toc(headings: list[tuple[int, str, str]]) -> str:
    if not headings:
        return ""
    items = []
    for _level, text, anchor in headings:
        items.append(f'<li><a href="#{anchor}">{render_inline(text)}</a></li>')
    item_html = "\n    ".join(items)
    return f"""
<section class="toc">
  <h2>目录</h2>
  <ol>
    {item_html}
  </ol>
</section>
"""


def markdown_to_html(markdown_text: str, title: str) -> str:
    lines = markdown_text.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    in_ul = False
    in_ol = False
    headings = extract_headings(markdown_text)
    heading_id_iter = iter([item[2] for item in headings])
    first_h1_skipped = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            close_lists()
            i += 1
            continue

        if line.strip().startswith("```"):
            close_lists()
            fence_lang = html.escape(line.strip().strip("`"), quote=False)
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            code = html.escape("\n".join(code_lines), quote=False)
            lang_class = f' class="language-{fence_lang}"' if fence_lang else ""
            out.append(f"<pre><code{lang_class}>{code}</code></pre>")
            continue

        if "|" in line and i + 1 < len(lines) and "|" in lines[i + 1] and is_table_delimiter(lines[i + 1]):
            close_lists()
            table_lines = [line, lines[i + 1].rstrip()]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                table_lines.append(lines[i].rstrip())
                i += 1
            out.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            close_lists()
            level = min(len(heading.group(1)), 3)
            text = heading.group(2).strip()
            if level == 1 and not first_h1_skipped:
                first_h1_skipped = True
                i += 1
                continue
            anchor = ""
            if level <= 2:
                anchor = f' id="{next(heading_id_iter, "")}"'
            out.append(f"<h{level}{anchor}>{render_inline(text)}</h{level}>")
            i += 1
            continue

        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        if bullet:
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{render_inline(bullet.group(1).strip())}</li>")
            i += 1
            continue

        numbered = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if numbered:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{render_inline(numbered.group(1).strip())}</li>")
            i += 1
            continue

        if line.lstrip().startswith(">"):
            close_lists()
            quote = line.lstrip()[1:].strip()
            out.append(f"<blockquote>{render_inline(quote)}</blockquote>")
            i += 1
            continue

        close_lists()
        out.append(f"<p>{render_inline(line.strip())}</p>")
        i += 1

    close_lists()
    body = "\n".join(out)
    report_date = date.today().isoformat()
    cover = build_cover(title, report_date)
    toc = build_toc(headings)
    safe_title = html.escape(title, quote=False)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{safe_title}</title>
  <style>{STYLE}</style>
</head>
<body>
  {cover}
  {toc}
  <main class="content">
{body}
  </main>
</body>
</html>
"""


def find_browser() -> str | None:
    env_path = os.environ.get("CHROME_PATH")
    candidates: list[str] = []
    if env_path:
        candidates.append(env_path)

    system = platform.system().lower()
    if system == "windows":
        candidates.extend(
            [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            ]
        )
    elif system == "darwin":
        candidates.extend(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            ]
        )
    else:
        candidates.extend(["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"])

    for candidate in candidates:
        resolved = shutil.which(candidate) if os.path.basename(candidate) == candidate else candidate
        if resolved and Path(resolved).exists():
            return resolved
    return None


def infer_title(markdown_text: str, input_path: Path) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return input_path.stem


def export_pdf(html_path: Path, pdf_path: Path) -> None:
    browser = find_browser()
    if not browser:
        raise RuntimeError("Could not find Chrome or Edge. Set CHROME_PATH to a Chromium-based browser executable.")

    with tempfile.TemporaryDirectory(prefix="industry-report-chrome-") as temp_dir:
        raw_pdf_path = pdf_path.with_suffix(".raw.pdf")
        cmd = [
            browser,
            "--headless",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-crash-reporter",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--user-data-dir={temp_dir}",
            f"--print-to-pdf={str(raw_pdf_path)}",
            html_path.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True)
        stamp_header_footer(raw_pdf_path, pdf_path, infer_pdf_title(html_path))
        if raw_pdf_path.exists():
            raw_pdf_path.unlink()


def infer_pdf_title(html_path: Path) -> str:
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
    if not match:
        return "Industry Research Report"
    return re.sub(r"\s+", " ", html.unescape(match.group(1))).strip()


def ascii_safe(text: str, max_len: int = 82) -> str:
    cleaned = re.sub(r"[^\x20-\x7E]+", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return (cleaned[: max_len - 1] + "...") if len(cleaned) > max_len else cleaned


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def stamp_header_footer(raw_pdf_path: Path, final_pdf_path: Path, title: str) -> None:
    if not all([PdfReader, PdfWriter, PageObject, DictionaryObject, NameObject, StreamObject]):
        shutil.move(str(raw_pdf_path), str(final_pdf_path))
        return

    reader = PdfReader(str(raw_pdf_path))
    writer = PdfWriter()
    total = len(reader.pages)
    title_text = ascii_safe(title) or "Industry Research Report"

    for index, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        overlay = PageObject.create_blank_page(width=width, height=height)
        font = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/Type1"),
                NameObject("/BaseFont"): NameObject("/Helvetica"),
            }
        )
        resources = DictionaryObject(
            {NameObject("/Font"): DictionaryObject({NameObject("/FHF"): font})}
        )
        header_y = max(height - 28, 36)
        footer_y = 21
        footer_text = f"Page {index} / {total}"
        content = f"""
q
0.84 G 0.35 w 42 {header_y - 8:.2f} m {width - 42:.2f} {header_y - 8:.2f} l S
0.84 G 0.35 w 42 34 m {width - 42:.2f} 34 l S
BT /FHF 8 Tf 0.36 g 42 {header_y:.2f} Td ({pdf_escape(title_text)}) Tj ET
BT /FHF 8 Tf 0.36 g {width - 102:.2f} {footer_y:.2f} Td ({pdf_escape(footer_text)}) Tj ET
Q
"""
        stream = StreamObject()
        stream._data = content.encode("latin-1")
        overlay[NameObject("/Resources")] = resources
        overlay[NameObject("/Contents")] = stream
        page.merge_page(overlay)
        writer.add_page(page)

    with final_pdf_path.open("wb") as handle:
        writer.write(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export an industry report Markdown file to HTML and PDF.")
    parser.add_argument("--input-md", required=True, help="Path to report.md")
    parser.add_argument("--output-dir", help="Output directory. Defaults to the input file directory.")
    parser.add_argument("--title", help="HTML title. Defaults to the first H1.")
    parser.add_argument("--html-name", default="report.html", help="HTML output filename.")
    parser.add_argument("--pdf-name", default="report.pdf", help="PDF output filename.")
    args = parser.parse_args()

    input_path = Path(args.input_md).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {input_path}")

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / args.html_name
    pdf_path = output_dir / args.pdf_name

    markdown_text = clean_markdown_for_pdf(input_path.read_text(encoding="utf-8"))
    title = args.title or infer_title(markdown_text, input_path)
    html_path.write_text(markdown_to_html(markdown_text, title), encoding="utf-8", newline="\n")
    export_pdf(html_path, pdf_path)

    print(f"HTML: {html_path}")
    print(f"PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
