import sys
from pathlib import Path

MD_DIR = Path("/Users/hn/vc/hue-95-23/out/mistral/markdown")


def fix_text(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    buf: list[str] = []

    for line in lines:
        if buf:
            if not line.strip():
                out.extend(buf)
                buf = []
                out.append(line)
                continue
            buf.append(line)
            joined = "<br>".join(b.strip() for b in buf)
            if joined.rstrip().endswith("|"):
                out.append(joined)
                buf = []
        else:
            stripped = line.rstrip()
            if line.lstrip().startswith("|") and not stripped.endswith("|"):
                buf = [line]
            else:
                out.append(line)

    if buf:
        out.extend(buf)

    return "\n".join(out)


def main() -> int:
    files = sorted(MD_DIR.glob("*.md"))
    changed = 0
    for f in files:
        original = f.read_text(encoding="utf-8")
        fixed = fix_text(original)
        if fixed != original:
            f.write_text(fixed, encoding="utf-8")
            changed += 1
            print(f"fixed: {f.name}")
    print(f"\nProcessed {len(files)} files, modified {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
