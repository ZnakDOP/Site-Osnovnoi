#!/usr/bin/env python3
"""Собирает страницы работ (work/<slug>/index.html и en/work/<slug>/index.html), превью для соцсетей (work/og/<slug>.jpg) и sitemap.xml.

Данные берутся из index.html (плитки с data-slug), home.css (обложки) и site.js (английские тексты I18N_EN по ключам data-i18n).
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


def key_of(fragment, cls):
    """Ключ data-i18n у элемента work-tile__<cls> (или None)."""
    m = re.search(r'class="work-tile__%s"([^>]*)>' % cls, fragment)
    k = re.search(r'data-i18n="([^"]+)"', m.group(1)) if m else None
    return k.group(1) if k else None


def load_en():
    """Английский словарь I18N_EN из site.js."""
    js = (ROOT / "site.js").read_text(encoding="utf-8")
    start = js.index("const I18N_EN = {")
    end = js.index("\n  }\n", start)
    block = js[start:end]
    out = {}
    for m in re.finditer(r'^    (\w+):\s*("(?:\\.|[^"\\])*")', block, re.M):
        try:
            out[m.group(1)] = json.loads(m.group(2))
        except ValueError:
            pass
    return out


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
CYR = re.compile(r"[А-Яа-яЁё]")

# Тексты интерфейса страницы работы
UI = {
    "ru": dict(
        lang="ru", locale="ru_RU", all_works="Все работы →", copy="Скопировать ссылку", copied="Ссылка скопирована ✓",
        see_all="Смотреть все работы", contact="Написать", switch_label="EN", switch_title="English version",
        owner="Арсений Горушкин", dop="Оператор-постановщик",
    ),
    "en": dict(
        lang="en", locale="en_US", all_works="All works →", copy="Copy link", copied="Link copied ✓",
        see_all="See all works", contact="Contact me", switch_label="RU", switch_title="Русская версия",
        owner="Arsenii Gorushkin", dop="Director of Photography",
    ),
}


def strip_tags(t):
    return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()


def collect_notes(index_html):
    """(категория, номер) -> [(текст, ключ i18n)]; заглушки пропускаем."""
    notes = {}
    for m in re.finditer(r'<div class="film-note" data-cat="(\w+)" data-film="(\d+)">(.*?)\n            </div>', index_html, re.S):
        paras = []
        for attrs, inner in re.findall(r'<p class="film-note__text"([^>]*)>(.*?)</p>', m.group(3), re.S):
            text = strip_tags(inner)
            if not text or text.startswith(PLACEHOLDER_STARTS):
                continue
            k = re.search(r'data-i18n="([^"]+)"', attrs)
            paras.append((text, k.group(1) if k else None))
        if paras:
            notes[(m.group(1), m.group(2))] = paras
    return notes


def collect(index_html, rules, en):
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
        raw = notes.get((get("data-cat"), get("data-film")), [])

        def tr(ru_text, key):
            """Английский вариант по ключу i18n; без ключа остаётся исходный текст."""
            v = en.get(key) if key else None
            return strip_tags(v) if v else ru_text

        ru_name = get("data-full-title") or text_of(inner, "name")
        works.append(
            dict(
                slug=get("data-slug"),
                src=get("data-kinescope-src"),
                aspect=float(aspect) if aspect else 56.25,
                cover=cover,
                ru=dict(
                    title=get("data-kinescope-title") or text_of(inner, "name"),
                    name=ru_name,
                    tag=text_of(inner, "tag"),
                    brand=text_of(inner, "hint"),
                    paras=[t for t, _ in raw],
                ),
                en=dict(
                    title=tr(text_of(inner, "name"), key_of(inner, "name")),
                    name=tr(text_of(inner, "name"), key_of(inner, "name")),
                    tag=tr(text_of(inner, "tag"), key_of(inner, "tag")),
                    brand=tr(text_of(inner, "hint"), key_of(inner, "hint")),
                    paras=[tr(t, k) for t, k in raw],
                ),
            )
        )
    return works


PAGE = """<!doctype html>
<html lang="{lang}">
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
    <link rel="alternate" hreflang="ru" href="{url_ru}" />
    <link rel="alternate" hreflang="en" href="{url_en}" />
    <link rel="alternate" hreflang="x-default" href="{url_ru}" />
    <meta property="og:type" content="video.other" />
    <meta property="og:site_name" content="Arsenii Gorushkin DOP" />
    <meta property="og:locale" content="{locale}" />
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
    <link rel="stylesheet" href="/work/work-page.css?v=7" />
    <script type="application/ld+json">{jsonld}</script>
    <script src="/work/work-page.js?v=2" defer></script>
  </head>
  <body>
    <header class="wp-head">
      <a class="wp-brand" href="/">Arsenii Gorushkin <span>DOP</span></a>
      <div class="wp-head__right">
        <a class="wp-lang" href="{switch_url}" hreflang="{switch_lang}" lang="{switch_lang}" title="{switch_title}" data-set-lang="{switch_lang}">{switch_label}</a>
        <a class="wp-back" href="/#work">{all_works}</a>
      </div>
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
          <button type="button" class="wp-btn" data-copy data-copied="{copied}">{copy}</button>
          <a class="wp-btn" href="/#work">{see_all}</a>
          <a class="wp-btn" href="mailto:a@gorushkindop.ru">{contact}</a>
        </div>
      </section>
    </main>
    <footer class="wp-foot">© Arsenii Gorushkin · gorushkindop.com</footer>
  </body>
</html>
"""


def url_for(slug, lang="ru"):
    return "%s/%swork/%s/" % (SITE, "en/" if lang == "en" else "", slug)


def write_sitemap(works):
    today = datetime.date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        "  <url><loc>%s/</loc><lastmod>%s</lastmod><priority>1.0</priority></url>" % (SITE, today),
    ]
    for w in works:
        ru, en = url_for(w["slug"]), url_for(w["slug"], "en")
        alts = (
            '<xhtml:link rel="alternate" hreflang="ru" href="%s"/>'
            '<xhtml:link rel="alternate" hreflang="en" href="%s"/>'
            '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % (ru, en, ru)
        )
        for loc in (ru, en):
            lines.append("  <url><loc>%s</loc>%s<lastmod>%s</lastmod><priority>0.7</priority></url>" % (loc, alts, today))
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def render(w, lang):
    e = html.escape
    ui, t = UI[lang], w[lang]
    url = url_for(w["slug"], lang)
    other = "en" if lang == "ru" else "ru"
    og_image = "%s/work/og/%s.jpg" % (SITE, w["slug"])
    title_full = "%s — %s | Arsenii Gorushkin DOP" % (t["name"], t["brand"])
    name_end = t["name"] if t["name"][-1] in ".!?" else t["name"] + "."
    if t["paras"]:
        first = t["paras"][0]
        if len(first) > 190:
            first = first[:190].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
        desc = "%s — %s. %s" % (t["name"], t["brand"], first)
    else:
        desc = "%s %s. %s %s." % (name_end, t["brand"], ui["dop"], ui["owner"])
    desc_html = "".join('        <p class="wp-desc">%s</p>\n' % e(p) for p in t["paras"])
    ld = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": t["name"],
        "description": desc,
        "inLanguage": lang,
        "thumbnailUrl": og_image,
        "embedUrl": w["src"],
        "url": url,
        "creator": {"@type": "Person", "name": "Arsenii Gorushkin", "alternateName": "Арсений Горушкин", "url": SITE + "/"},
        "publisher": {"@type": "Organization", "name": t["brand"]},
    }
    jsonld = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    return PAGE.format(
        lang=ui["lang"], locale=ui["locale"], title_full=e(title_full), desc=e(desc), url=url,
        url_ru=url_for(w["slug"]), url_en=url_for(w["slug"], "en"), og_image=og_image,
        src=e(w["src"] + ("&" if "?" in w["src"] else "?") + "autoplay=0"),
        name=e(t["name"]), tag=e(t["tag"]), brand=e(t["brand"]),
        portrait=" wp-player--portrait" if w["aspect"] > 100 else "", ratio="100 / %s" % w["aspect"],
        desc_html=desc_html, jsonld=jsonld,
        switch_url=url_for(w["slug"], other).replace(SITE, ""), switch_lang=other,
        switch_label=ui["switch_label"], switch_title=ui["switch_title"],
        all_works=ui["all_works"], copy=ui["copy"], copied=ui["copied"], see_all=ui["see_all"], contact=ui["contact"],
    ), desc


def main():
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "home.css").read_text(encoding="utf-8")
    en = load_en()
    works = collect(index_html, cover_rules(css), en)
    have_ffmpeg = shutil.which("ffmpeg") is not None
    (ROOT / "work" / "og").mkdir(parents=True, exist_ok=True)
    leftovers = []
    for w in works:
        og_path = ROOT / "work" / "og" / (w["slug"] + ".jpg")
        src_img = ROOT / w["cover"]
        if not og_path.exists() or og_path.stat().st_mtime < src_img.stat().st_mtime:
            if not have_ffmpeg:
                sys.exit("Нужен ffmpeg, чтобы собрать превью " + og_path.name)
            subprocess.run(
                ["ffmpeg", "-loglevel", "error", "-y", "-i", str(src_img), "-vf", "scale=1200:-2", "-q:v", "4", str(og_path)],
                check=True,
            )
        for lang in ("ru", "en"):
            page, _desc = render(w, lang)
            out = ROOT / ("en/work" if lang == "en" else "work") / w["slug"] / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page, encoding="utf-8")
            if lang == "en":
                for field in ("name", "brand", "tag"):
                    if CYR.search(w["en"][field]):
                        leftovers.append("%s: %s = %s" % (w["slug"], field, w["en"][field]))
                for p in w["en"]["paras"]:
                    if CYR.search(re.sub(r"[«»“”\"()]|С точки зрения вина", "", p)) and len(CYR.findall(p)) > 12:
                        leftovers.append("%s: описание без перевода" % w["slug"])
                        break
    write_sitemap(works)
    print("Собрано работ: %d (RU + EN)" % len(works))
    if leftovers:
        print("Кириллица в английских страницах:")
        for l in leftovers:
            print("  -", l)


if __name__ == "__main__":
    main()
