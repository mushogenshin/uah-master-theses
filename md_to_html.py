import sys
from pathlib import Path

import markdown

MD_DIR = Path("/Users/hn/vc/hue-95-23/out/mistral/markdown")
HTML_DIR = Path("/Users/hn/vc/hue-95-23/out/mistral/html")

CSS = """
body { font-family: -apple-system, system-ui, sans-serif; max-width: 960px; margin: 2em auto; padding: 0 1em; line-height: 1.5; }
table { border-collapse: collapse; margin: 1em 0; }
th, td { border: 1px solid #888; padding: 0.4em 0.7em; vertical-align: top; }
th { background: #f0f0f0; }
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> int:
    if not MD_DIR.exists():
        print(f"Markdown dir not found: {MD_DIR}", file=sys.stderr)
        return 1

    HTML_DIR.mkdir(parents=True, exist_ok=True)
    md = markdown.Markdown(extensions=["tables", "fenced_code"])

    files = sorted(MD_DIR.glob("*.md"))
    for src in files:
        md.reset()
        body = md.convert(src.read_text(encoding="utf-8"))
        html = TEMPLATE.format(title=src.stem, css=CSS, body=body)
        (HTML_DIR / f"{src.stem}.html").write_text(html, encoding="utf-8")

    print(f"Converted {len(files)} files to {HTML_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
