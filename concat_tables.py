import re
import sys
from pathlib import Path

HTML_DIR = Path("/Users/hn/vc/hue-95-23/out/mistral/html")
OUT_PATH = Path("/Users/hn/vc/hue-95-23/out/mistral/all_tables.html")

CSS = """
body { font-family: -apple-system, system-ui, sans-serif; max-width: 1200px; margin: 2em auto; padding: 0 1em; line-height: 1.5; }
h2 { margin-top: 2.5em; padding-top: 0.5em; border-top: 2px solid #ccc; }
table { border-collapse: collapse; margin: 1em 0; width: 100%; }
th, td { border: 1px solid #888; padding: 0.4em 0.7em; vertical-align: top; }
th { background: #f0f0f0; }
nav { columns: 4; font-size: 0.9em; }
.empty { color: #999; font-style: italic; }
"""

TABLE_RE = re.compile(r"<table.*?</table>", re.DOTALL | re.IGNORECASE)
PAGE_NUM_RE = re.compile(r"page-(\d+)")


def main() -> int:
    files = sorted(HTML_DIR.glob("page-*.html"))
    if not files:
        print(f"No files found in {HTML_DIR}", file=sys.stderr)
        return 1

    sections = []
    nav_links = []
    total_tables = 0

    for f in files:
        m = PAGE_NUM_RE.search(f.stem)
        page = int(m.group(1)) if m else 0
        anchor = f"page-{page:03d}"
        nav_links.append(f'<a href="#{anchor}">Page {page}</a>')

        tables = TABLE_RE.findall(f.read_text(encoding="utf-8"))
        total_tables += len(tables)
        if tables:
            body = "\n".join(tables)
        else:
            body = '<p class="empty">(no table on this page)</p>'
        sections.append(f'<h2 id="{anchor}">Page {page}</h2>\n{body}')

    html = (
        "<!DOCTYPE html>\n"
        '<html lang="vi">\n<head>\n<meta charset="utf-8">\n'
        f"<title>All tables ({len(files)} pages)</title>\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n"
        f"<h1>All tables — {len(files)} pages, {total_tables} tables</h1>\n"
        f'<nav>{" · ".join(nav_links)}</nav>\n'
        + "\n".join(sections)
        + "\n</body>\n</html>\n"
    )

    OUT_PATH.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_PATH} — {len(files)} pages, {total_tables} tables")
    return 0


if __name__ == "__main__":
    sys.exit(main())
