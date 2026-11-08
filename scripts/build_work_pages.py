#!/usr/bin/env python3
"""Собирает страницы работ (work/<slug>/index.html), превью для соцсетей (work/og/<slug>.jpg) и sitemap.xml.

Данные берутся из index.html (плитки с data-slug) и home.css (обложки).
Запуск из корня репозитория:  python3 scripts/build_work_pages.py
Нужен ffmpeg (для лёгких превью под соцсети и мессенджеры).
"""
import datetime
import html
import json
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


def original_of(path):
    """Лёгкое превью images/thumbs/x.webp -> оригинал images/x.(jpg|png), он нужен для превью в соцсетях."""
    if path.startswith("images/thumbs/"):
        stem = Path(path).stem
        for ext in ("jpg", "jpeg", "png"):
            cand = "images/%s.%s" % (stem, ext)
            if (ROOT / cand).exists():
                return cand
    return path


def cover_rules(css):
    rules = {}
    for m in re.finditer(r"\.(work-tile--[\w-]+)::before\s*\{([^}]*)\}", css):
        u = re.search(r'url\("([^"]+)"\)', m.group(2))
        if u:
            rules[m.group(1)] = original_of(u.group(1).split("?")[0])
    return rules


PLACEHOLDER_STARTS = ("Здесь будет описание", "Короткое описание", "Место для рассказа", "Пример описания")


def collect_notes(index_html):
    """(категория, номер) -> абзацы описания; заглушки пропускаем."""
    notes = {}
    for m in re.finditer(r'<div class="film-note" data-cat="(\w+)" data-film="(\d+)">(.*?)\n            </div>', index_html, re.S):
        paras = [re.sub(r"<[^>]+>", "", p).strip() for p in re.findall(r'<p class="film-note__text">(.*?)</p>', m.group(3), re.S)]
        paras = [html.unescape(p) for p in paras if p and not p.startswith(PLACEHOLDER_STARTS)]
        if paras:
            notes[(m.group(1), m.group(2))] = paras
    return notes


def collect(index_html, rules):
    notes = collect_notes(index_html)
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
                paras=notes.get((get("data-cat"), get("data-film")), []),
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
      content="default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self' data:; img-src 'self' data: https:; frame-src https://kinescope.io; connect-src 'self'; form-action 'self' mailto: tel:; upgrade-insecure-requests"
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
    <link rel="preload" href="/fonts/syne-var-latin.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="/fonts/outfit-var-latin.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="/fonts/fonts.css?v=1" />
    <link rel="stylesheet" href="/work/work-page.css?v=4" />
    <script type="application/ld+json">{jsonld}</script>
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
{desc_html}        <div class="wp-actions">
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


def url_for(slug):
    return "%s/work/%s/" % (SITE, slug)


def write_sitemap(works):
    today = datetime.date.today().isoformat()
    urls = [(SITE + "/", "1.0")] + [(url_for(w["slug"]), "0.7") for w in works]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio in urls:
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (loc, today, prio))
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


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
        url = url_for(w["slug"])
        title_full = "%s — %s | Arsenii Gorushkin DOP" % (w["name"], w["brand"])
        name_end = w["name"] if w["name"][-1] in ".!?" else w["name"] + "."
        if w["paras"]:
            first = w["paras"][0]
            if len(first) > 190:
                first = first[:190].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
            desc = "%s — %s. %s" % (w["name"], w["brand"], first)
        else:
            desc = "%s %s. Оператор-постановщик %s." % (name_end, w["brand"], OWNER)
        desc_html = "".join('        <p class="wp-desc">%s</p>\n' % e(t) for t in w["paras"])
        ld = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": w["name"],
            "description": desc,
            "thumbnailUrl": "%s/work/og/%s.jpg" % (SITE, w["slug"]),
            "embedUrl": w["src"],
            "url": url_for(w["slug"]),
            "creator": {"@type": "Person", "name": "Arsenii Gorushkin", "alternateName": OWNER, "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": w["brand"]},
        }
        jsonld = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
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
            desc_html=desc_html,
            jsonld=jsonld,
        )
        out = ROOT / "work" / w["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
    write_sitemap(works)
    print("Собрано страниц:", len(works))


if __name__ == "__main__":
    main()
