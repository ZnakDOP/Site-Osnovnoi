#!/usr/bin/env python3
"""Собирает отдельные страницы работ: work/<slug>/index.html + превью work/og/<slug>.jpg.

Данные берутся из index.html (плитки с data-slug) и home.css (обложки).
Запуск из корня репозитория:  python3 scripts/build_work_pages.py
Нужен ffmpeg (для лёгких превью под соцсети и мессенджеры).
"""
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://gorushkindop.com"
OWNER = "Арсений Горушкин"


def text_of(fragment, cls):
    m = re.search(r'class="work-tile__%s"[^>]*>(.*?)</span>' % cls, fragment, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


def cover_rules(css):
    rules = {}
    for m in re.finditer(r"\.(work-tile--[\w-]+)::before\s*\{([^}]*)\}", css):
        u = re.search(r'url\("([^"]+)"\)', m.group(2))
        if u:
            rules[m.group(1)] = u.group(1).split("?")[0]
    return rules


def collect(index_html, rules):
    works = []
    for m in re.finditer(r"<(button|a)\b([^>]*data-slug=[^>]*)>(.*?)</\1>", index_html, re.S):
        attrs, inner = m.group(2), m.group(3)
        get = lambda name: (re.search(name + r'="([^"]*)"', attrs) or [None, ""])[1]
        classes = get("class").split()
        cover = None
        for c in classes:
            if c in rules and not re.fullmatch(r"work-tile--\d", c):
                cover = rules[c]
        if not cover:
            raise SystemExit("Нет обложки для " + get("data-slug"))
        aspect = get("data-kinescope-aspect")
        works.append(
            dict(
                slug=get("data-slug"),
                src=get("data-kinescope-src"),
                title=get("data-kinescope-title") or text_of(inner, "name"),
                name=get("data-full-title") or text_of(inner, "name"),
                tag=text_of(inner, "tag"),
                brand=text_of(inner, "hint"),
                aspect=float(aspect) if aspect else 56.25,
                cover=cover,
            )
        )
    return works


PAGE = """<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <meta name="theme-color" content="#060608" />
    <meta name="referrer" content="strict-origin-when-cross-origin" />
    <meta
      http-equiv="Content-Security-Policy"
      content="default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self'; style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; frame-src https://kinescope.io; connect-src 'self'; form-action 'self' mailto: tel:; upgrade-insecure-requests"
    />
    <link rel="icon" href="/favicon.ico?v=3" sizes="any" />
    <link rel="icon" type="image/png" sizes="32x32" href="/icons/dp-32.png?v=3" />
    <link rel="apple-touch-icon" href="/icons/dp-180.png?v=3" />
    <title>{title_full}</title>
    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{url}" />
    <meta property="og:type" content="video.other" />
    <meta property="og:site_name" content="Arsenii Gorushkin DOP" />
    <meta property="og:title" content="{title_full}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{og_image}" />
    <meta property="og:image:width" content="1200" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title_full}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="{og_image}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Outfit:wght@400;500;600&family=Syne:wght@600;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="/work/work-page.css?v=3" />
    <script src="/work/work-page.js?v=1" defer></script>
  </head>
  <body>
    <header class="wp-head">
      <a class="wp-brand" href="/">Arsenii Gorushkin <span>DOP</span></a>
      <a class="wp-back" href="/#work">Все работы →</a>
    </header>
    <main class="wp-main">
      <div class="wp-player{portrait}" style="aspect-ratio: {ratio}">
        <iframe
          src="{src}"
          title="{name}"
          allow="autoplay; fullscreen; picture-in-picture; encrypted-media; gyroscope; accelerometer; clipboard-write; screen-wake-lock;"
          allowfullscreen
        ></iframe>
      </div>
      <section class="wp-info">
        <p class="wp-tag">{tag}</p>
        <h1 class="wp-title">{name}</h1>
        <p class="wp-brand-line">{brand}</p>
        <div class="wp-actions">
          <button type="button" class="wp-btn" data-copy>Скопировать ссылку</button>
          <a class="wp-btn" href="/#work">Смотреть все работы</a>
          <a class="wp-btn" href="mailto:a@gorushkindop.ru">Написать</a>
        </div>
      </section>
    </main>
    <footer class="wp-foot">© Arsenii Gorushkin · gorushkindop.com</footer>
  </body>
</html>
"""


def main():
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "home.css").read_text(encoding="utf-8")
    works = collect(index_html, cover_rules(css))
    have_ffmpeg = shutil.which("ffmpeg") is not None
    (ROOT / "work" / "og").mkdir(parents=True, exist_ok=True)
    for w in works:
        e = html.escape
        og_path = ROOT / "work" / "og" / (w["slug"] + ".jpg")
        src_img = ROOT / w["cover"]
        if not og_path.exists() or og_path.stat().st_mtime < src_img.stat().st_mtime:
            if not have_ffmpeg:
                sys.exit("Нужен ffmpeg, чтобы собрать превью " + og_path.name)
            subprocess.run(
                ["ffmpeg", "-loglevel", "error", "-y", "-i", str(src_img), "-vf", "scale=1200:-2", "-q:v", "4", str(og_path)],
                check=True,
            )
        url = "%s/work/%s/" % (SITE, w["slug"])
        title_full = "%s — %s | Arsenii Gorushkin DOP" % (w["name"], w["brand"])
        name_end = w["name"] if w["name"][-1] in ".!?" else w["name"] + "."
        desc = "%s %s. Оператор-постановщик %s." % (name_end, w["brand"], OWNER)
        portrait = w["aspect"] > 100
        page = PAGE.format(
            title_full=e(title_full),
            desc=e(desc),
            url=url,
            og_image="%s/work/og/%s.jpg" % (SITE, w["slug"]),
            src=e(w["src"] + ("&" if "?" in w["src"] else "?") + "autoplay=0"),
            name=e(w["name"]),
            tag=e(w["tag"]),
            brand=e(w["brand"]),
            portrait=" wp-player--portrait" if portrait else "",
            ratio="100 / %s" % w["aspect"],
        )
        out = ROOT / "work" / w["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
    print("Собрано страниц:", len(works))


if __name__ == "__main__":
    main()
