#!/usr/bin/env python3
"""Делает лёгкие webp-превью для обложек плиток и подставляет их в home.css.

Оригиналы в images/ остаются нетронутыми (они нужны для страниц работ и превью в соцсетях).
Запуск из корня репозитория:  python3 scripts/optimize_images.py
Нужен cwebp (brew install webp).
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "home.css"
THUMBS = ROOT / "images" / "thumbs"
RULE = re.compile(r"(\.work-tile--[\w-]+::before\s*\{[^}]*?url\(\")(images/[^\"?]+)(?:\?[^\"]*)?(\"\))")


def width_for(stem):
    return 560 if stem.startswith("work-vert-") else 960


def main():
    if not shutil.which("cwebp"):
        sys.exit("Нужен cwebp: brew install webp")
    THUMBS.mkdir(parents=True, exist_ok=True)
    css = CSS.read_text(encoding="utf-8")
    made = 0

    def sub(m):
        nonlocal made
        path = m.group(2)
        if path.startswith("images/thumbs/"):
            return m.group(0)
        src = ROOT / path
        stem = src.stem
        out = THUMBS / (stem + ".webp")
        if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
            subprocess.run(
                ["cwebp", "-quiet", "-q", "76", "-m", "5", "-resize", str(width_for(stem)), "0", str(src), "-o", str(out)],
                check=True,
            )
            made += 1
        return m.group(1) + "images/thumbs/" + stem + ".webp" + m.group(3)

    new = RULE.sub(sub, css)
    CSS.write_text(new, encoding="utf-8")
    total = sum(f.stat().st_size for f in THUMBS.glob("*.webp"))
    print("Новых превью: %d, всего %d файлов, %.1f МБ" % (made, len(list(THUMBS.glob("*.webp"))), total / 1e6))


if __name__ == "__main__":
    main()
