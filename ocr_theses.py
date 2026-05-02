import os
import sys
from pathlib import Path

from mistralai.client import Mistral

PDF_PATH = Path("/Users/hn/vc/hue-95-23/theses.pdf")
OUT_DIR = Path("/Users/hn/vc/hue-95-23/out/mistral/markdown")
MODEL = "mistral-ocr-latest"


def main() -> int:
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("MISTRAL_API_KEY not set", file=sys.stderr)
        return 1
    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH}", file=sys.stderr)
        return 1

    client = Mistral(api_key=api_key)

    print(f"Uploading {PDF_PATH.name} ({PDF_PATH.stat().st_size / 1e6:.1f} MB)...")
    uploaded = client.files.upload(
        file={"file_name": PDF_PATH.name, "content": PDF_PATH.read_bytes()},
        purpose="ocr",
    )

    signed = client.files.get_signed_url(file_id=uploaded.id)

    print(f"Running OCR with {MODEL}...")
    response = client.ocr.process(
        model=MODEL,
        document={"type": "document_url", "document_url": signed.url},
    )

    OUT_DIR.mkdir(exist_ok=True)
    width = max(3, len(str(len(response.pages))))
    for page in response.pages:
        n = page.index + 1
        path = OUT_DIR / f"page-{n:0{width}d}.md"
        path.write_text(f"<!-- page {n} -->\n\n{page.markdown.strip()}\n", encoding="utf-8")

    print(f"Wrote {len(response.pages)} pages to {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
