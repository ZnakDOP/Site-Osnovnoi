;(function () {
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches

  const I18N_ARIA_RU = {
    lang_group_aria: "Язык",
    nav_aria: "Разделы сайта",
    menu_open: "Открыть меню",
    hero_aria: "Введение",
    bio_media_aria: "Бэкстейдж",
    carousel_prev: "Предыдущие работы",
    carousel_next: "Следующие работы",
    aria_telegram: "Telegram",
    aria_phone: "Телефон",
    aria_email: "Почта",
    lb_dialog: "Просмотр работы",
    lb_close_backdrop: "Закрыть просмотр",
    lb_close_btn: "Закрыть",
  }

  const I18N_ARIA_EN = {
    lang_group_aria: "Language",
    nav_aria: "Site sections",
    menu_open: "Open menu",
    hero_aria: "Introduction",
    bio_media_aria: "Behind the scenes",
    carousel_prev: "Previous projects",
    carousel_next: "Next projects",
    aria_telegram: "Telegram",
    aria_phone: "Phone",
    aria_email: "Email",
    lb_dialog: "Project viewer",
    lb_close_backdrop: "Close viewer",
    lb_close_btn: "Close",
  }

  const I18N_EN = {
    nav_showreel: "Showreel",
    nav_bio: "Bio",
    nav_work: "Work",
    nav_links: "Links",
    nav_contact: "Contact",
    nav_rental: "Rental",
    hero_kicker: "Moscow · on location · worldwide",
    hero_role: "Director of Photography",
    hero_rental: "Equipment rental",
    hero_showreel_btn: "Showreel",
    strip_commercial: "Commercial",
    strip_music: "Music video",
    strip_doc: "Documentary",
    strip_interview: "Interview",
    strip_narrative: "Narrative",
    strip_clm: "Color · light · motion",
    stat_genres: "Genres",
    stat_narrative: "Narrative film",
    stat_music: "Music videos",
    stat_commercial: "Commercial",
    stat_doc: "Documentary",
    stat_vertical: "Vertical content",
    sec_showreel_title: "Showreel",
    sec_showreel_meta: "edit · grade · sound",
    sec_bio_title: "Bio",
    sec_bio_meta: "about",
    bio_p1:
      "<strong>Arsenii Gorushkin</strong> is a cinematographer from Cherepovets and a graduate of the cinematography department at GITR.",
    bio_p2:
      "For me, the priority is atmosphere and a sense of presence inside the story. I look for imagery that does not merely accompany a scene but shapes its mood, rhythm, and inner tension. I want the frame to feel alive and emotionally precise, regardless of genre or scale.",
    bio_p3:
      "I invest in prep: reading the script, building visual references, and working with space and light. Strong images come from attention to detail and close collaboration with the whole team.",
    bio_p4:
      "On set I balance precision with freedom — ready for planned choices while leaving room for moments that cannot be invented in advance. Those moments often make a scene feel real.",
    bio_p5:
      "I am drawn to projects with a strong visual world, a clear authorial voice, and care for the emotional state of the frame.",
    bio_alt1: "Arsenii on set",
    bio_alt2: "Arsenii with a camera on location",
    bio_alt3: "Library shoot, behind the scenes",
    bio_alt4: "Working with a cinema camera on set",
    sec_cv_title: "CV",
    sec_cv_meta: "filmography",
    cv_p1:
      "Full credits, roles, and technical details are available on request. Email or Telegram me and I will send a PDF and links to selected work.",
    cv_btn: "Request CV",
    sec_work_title: "Selected work",
    sec_work_meta: "portfolio",
    cat_narrative: "Narrative · cinema",
    w_tag_narrative: "Narrative / short",
    w_8w_hint: "Nikita Belykh",
    w_nesezon_hint: "Boris Rezak",
    w_fillip_hint: "Sergey Shteps",
    w_pochemu_hint: "Nikita Belykh",
    cat_doc: "Interview · doc",
    w_doc_nto_tag: "Documentary",
    w_doc_nto_name: "National Tech Olympiad",
    w_doc_nto_hint: "Sber",
    w_doc_ing_tag: "Documentary",
    w_doc_ing_name: "VK Places · Republic of Ingushetia",
    w_doc_ing_hint: "VKontakte",
    w_doc_avito_tag: "Documentary",
    w_doc_avito_name: "Avito server hideout",
    w_doc_avito_hint: "Avito",
    w_doc_tochka_tag: "Documentary",
    w_doc_tochka_name: "Four growth levers for business",
    w_doc_tochka_hint: "Tochka Bank",
    w_doc_hp_tag: "Interview",
    w_doc_hp_name: "Testing HP communities",
    w_doc_hp_hint: "VKontakte",
    w_doc_bft_tag: "Multicam",
    w_doc_bft_name: "Business Fail Talks",
    w_doc_bft_hint: "BFT",
    w_doc_sv_tag: "Interview",
    w_doc_sv_name: "Irina Gorbacheva on choosing wine",
    w_doc_sv_hint: "Simple Vine",
    cat_commercial: "Commercial · advertising",
    w_tag_commercial: "Commercial",
    cat_music: "Music videos",
    w_tag_music: "Music video",
    cat_vertical: "Vertical content",
    w_tag_vertical: "Vertical",
    w_vert_1_name: "Night floor",
    w_vert_1_hint: "Shorts",
    w_vert_2_name: "Light in the hall",
    w_vert_2_hint: "Stories",
    w_vert_3_name: "Stage 4×5",
    w_vert_3_hint: "BTS",
    w_vert_4_name: "Reflection in glass",
    w_vert_4_hint: "Reels",
    w_vert_5_name: "Color test",
    w_vert_5_hint: "Commercial",
    w_vert_6_name: "Elevator · day",
    w_vert_6_hint: "Music video",
    w_vert_7_name: "Rooftop · sunset",
    w_vert_7_hint: "Shorts",
    w_vert_8_name: "Interview in frame",
    w_vert_8_hint: "Doc",
    w_vert_9_name: "Camera move",
    w_vert_9_hint: "Test",
    w_vert_10_name: "Neon and rain",
    w_vert_10_hint: "Reels",
    w_vert_11_name: "Silhouette at window",
    w_vert_11_hint: "Stories",
    w_vert_12_name: "Final shot",
    w_vert_12_hint: "Shorts",
    sec_links_title: "Links",
    sec_links_meta: "social · channel",
    link_tg_t: "Znak DOP channel",
    link_tg_m: "@znak_dop — breakdowns and backstage",
    link_ig_t: "Reels / backstage",
    link_personal_k: "Personal Telegram",
    link_personal_t: "Project inquiries",
    sec_contact_title: "Contact",
    sec_contact_meta: "direct",
    contact_briefs: "Briefs: <strong>a@gorushkindop.ru</strong>",
    sec_rental_title: "Equipment rental",
    rental_sheet_btn: "Equipment list",
    footer_ip: "Sole proprietor Arsenii Viacheslavovich Gorushkin",
    footer_top: "Back to top",
  }

  const ruHtml = new Map()
  const ruAria = new Map()

  function captureRuStrings() {
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const k = el.getAttribute("data-i18n")
      if (k) ruHtml.set(k, el.innerHTML)
    })
    document.querySelectorAll("[data-i18n-alt]").forEach((el) => {
      const k = el.getAttribute("data-i18n-alt")
      if (k && el instanceof HTMLImageElement) ruHtml.set(k, el.alt)
    })
    document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
      const k = el.getAttribute("data-i18n-aria")
      if (k) ruAria.set(el, el.getAttribute("aria-label") || "")
    })
  }

  function applyAriaLang(lang) {
    const t = lang === "en" ? I18N_ARIA_EN : I18N_ARIA_RU
    document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
      const k = el.getAttribute("data-i18n-aria")
      if (!k) return
      const label = lang === "en" ? I18N_ARIA_EN[k] || ruAria.get(el) : ruAria.get(el) || I18N_ARIA_RU[k]
      if (label) el.setAttribute("aria-label", label)
    })
  }

  function applyLang(lang) {
    const isEn = lang === "en"
    document.documentElement.lang = isEn ? "en" : "ru"
    try {
      localStorage.setItem("siteLang", lang)
    } catch (_) {}

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const k = el.getAttribute("data-i18n")
      if (!k) return
      if (isEn) {
        const t = I18N_EN[k]
        if (t != null) el.innerHTML = t
      } else {
        const ru = ruHtml.get(k)
        if (ru != null) el.innerHTML = ru
      }
    })

    document.querySelectorAll("[data-i18n-alt]").forEach((el) => {
      const k = el.getAttribute("data-i18n-alt")
      if (!k || !(el instanceof HTMLImageElement)) return
      if (isEn) {
        const t = I18N_EN[k]
        if (t != null) el.alt = t
      } else {
        const ru = ruHtml.get(k)
        if (ru != null) el.alt = ru
      }
    })

    applyAriaLang(lang)

    const titleEl = document.getElementById("meta-page-title")
    if (titleEl) {
      titleEl.textContent = isEn ? "Arsenii Gorushkin · Cinematographer" : "Arsenii Gorushkin DOP"
    }
    const descEl = document.getElementById("meta-description")
    if (descEl) {
      descEl.setAttribute(
        "content",
        isEn
          ? "Cinematographer: commercial, music videos, documentary. Based in Moscow, shooting across Russia and worldwide. Showreel, CV, ZNAK RENT."
          : "Director of Photography: реклама, клипы, документалистика. База в Москве, съёмки по России и worldwide. Шоурил, CV, рентал ZNAK RENT."
      )
    }
    const ogT = document.getElementById("meta-og-title")
    if (ogT) {
      ogT.setAttribute("content", isEn ? "Arsenii Gorushkin · Cinematographer" : "Arsenii Gorushkin DOP")
    }
    const ogD = document.getElementById("meta-og-desc")
    if (ogD) {
      ogD.setAttribute(
        "content",
        isEn
          ? "DP / cinematographer. Moscow · on location · worldwide — commercial, music videos, documentary."
          : "DP / оператор-постановщик. Москва · on location · worldwide — коммерция, клипы, документалистика."
      )
    }

    const srIframe = document.querySelector(".showreel-embed__iframe")
    if (srIframe) srIframe.setAttribute("title", isEn ? "Showreel" : "Шоурил")

    const langRoots = document.querySelectorAll(".site-header__lang")
    langRoots.forEach((langRoot) => langRoot.classList.toggle("site-header__lang--en", isEn))

    document.querySelectorAll("[data-set-lang]").forEach((btn) => {
      const bLang = btn.getAttribute("data-set-lang")
      const active = (isEn && bLang === "en") || (!isEn && bLang === "ru")
      btn.setAttribute("aria-pressed", active ? "true" : "false")
    })
  }

  function initLang() {
    captureRuStrings()
    document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
      const k = el.getAttribute("data-i18n-aria")
      if (k && !ruAria.has(el)) ruAria.set(el, el.getAttribute("aria-label") || "")
    })
    let pref = "ru"
    try {
      pref = localStorage.getItem("siteLang") || "ru"
    } catch (_) {}
    if (pref !== "en" && pref !== "ru") pref = "ru"
    applyLang(pref)

    document.querySelectorAll("[data-set-lang]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const lang = btn.getAttribute("data-set-lang")
        if (lang === "en" || lang === "ru") applyLang(lang)
      })
    })
  }

  const loader = document.getElementById("site-loader")
  if (loader && !prefersReduced) {
    const done = () => {
      loader.classList.add("site-loader--done")
      loader.setAttribute("aria-hidden", "true")
      window.setTimeout(() => loader.remove(), 700)
    }
    window.addEventListener("load", () => window.setTimeout(done, 480))
    window.setTimeout(done, 3200)
  } else if (loader) {
    loader.remove()
  }

  const nav = document.querySelector(".site-header__nav")
  const toggle = document.querySelector(".site-header__menu-btn")

  function closeNav() {
    if (!nav || !toggle) return
    nav.classList.remove("site-header__nav--open")
    toggle.setAttribute("aria-expanded", "false")
    document.body.classList.remove("site-nav-open")
  }

  if (toggle && nav) {
    toggle.addEventListener("click", (e) => {
      e.stopPropagation()
      const open = nav.classList.toggle("site-header__nav--open")
      toggle.setAttribute("aria-expanded", open ? "true" : "false")
      document.body.classList.toggle("site-nav-open", open)
    })
    nav.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", closeNav)
    })
    document.addEventListener("click", (e) => {
      if (!nav.classList.contains("site-header__nav--open")) return
      const t = e.target
      if (t instanceof Node && !nav.contains(t) && !toggle.contains(t)) closeNav()
    })
  }

  if (!prefersReduced) {
    let lastY = window.scrollY || 0
    let ticking = false
    const onScroll = () => {
      if (ticking) return
      ticking = true
      requestAnimationFrame(() => {
        const y = window.scrollY || 0
        const delta = y - lastY
        if (Math.abs(delta) > 2) {
          document.body.classList.toggle("scroll-down", delta > 0)
          document.body.classList.toggle("scroll-up", delta < 0)
        }
        lastY = y
        ticking = false
      })
    }
    document.body.classList.add("scroll-down")
    window.addEventListener("scroll", onScroll, { passive: true })
  }

  if (!prefersReduced && "IntersectionObserver" in window) {
    const narrow = window.matchMedia("(max-width: 768px)").matches
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) e.target.classList.add("reveal--visible")
        })
      },
      {
        rootMargin: narrow ? "0px 0px -4% 0px" : "0px 0px -8% 0px",
        threshold: narrow ? 0.04 : 0.08,
      }
    )
    document.querySelectorAll(".reveal").forEach((el) => io.observe(el))
  } else {
    document.querySelectorAll(".reveal").forEach((el) => el.classList.add("reveal--visible"))
  }

  function initWorkCarousel() {
    document.querySelectorAll(".work-carousel").forEach((root) => {
      const track = root.querySelector("[data-carousel-track]")
      const viewport = root.querySelector(".work-carousel__viewport")
      const prev = root.querySelector("[data-carousel-prev]")
      const next = root.querySelector("[data-carousel-next]")
      if (!track || !prev || !next) return
      if (window.getComputedStyle(prev).display === "none") return

      const isVertical = root.classList.contains("work-carousel--vertical")
      const scroller = isVertical && viewport ? viewport : track

      function gapPx(el) {
        const cs = window.getComputedStyle(el)
        const g = parseFloat(cs.columnGap)
        if (Number.isFinite(g) && g >= 0) return g
        const g2 = parseFloat(cs.gap)
        return Number.isFinite(g2) && g2 >= 0 ? g2 : 14
      }

      /** Одна «страница» горизонтального скролла: 4 плитки (десктоп) или 2 колонки × 3 ряда (мобилка) */
      function verticalPageStep() {
        const tile = track.querySelector(".work-tile")
        if (!tile || !viewport) return Math.max(1, Math.round(viewport.clientWidth))
        const tw = tile.getBoundingClientRect().width
        const g = gapPx(track)
        const narrow = window.matchMedia("(max-width: 768px)").matches
        if (narrow) return Math.round(2 * tw + g)
        return Math.round(4 * tw + 3 * g)
      }

      function stepSize() {
        if (isVertical && viewport) return verticalPageStep()
        const tile = track.querySelector(".work-tile")
        if (!tile) return Math.min(292, track.clientWidth * 0.82)
        const gap = 12
        return tile.getBoundingClientRect().width + gap
      }

      function verticalScrollToPage(goPrev) {
        const step = verticalPageStep()
        const maxL = Math.max(0, scroller.scrollWidth - scroller.clientWidth)
        if (step < 4) return
        let p = Math.floor((scroller.scrollLeft + step * 0.15) / step)
        if (goPrev) p -= 1
        else p += 1
        const maxP = Math.max(0, Math.ceil(maxL / step - 1e-9))
        p = Math.max(0, Math.min(maxP, p))
        const left = Math.min(p * step, maxL)
        scroller.scrollTo({ left, behavior: prefersReduced ? "auto" : "smooth" })
        window.setTimeout(() => {
          const snap = Math.min(Math.round(scroller.scrollLeft / step) * step, maxL)
          if (Math.abs(scroller.scrollLeft - snap) > 1.5) scroller.scrollLeft = snap
        }, prefersReduced ? 0 : 420)
      }

      function updateDisabled() {
        const maxScroll = Math.max(0, scroller.scrollWidth - scroller.clientWidth - 2)
        prev.disabled = scroller.scrollLeft <= 2
        next.disabled = scroller.scrollLeft >= maxScroll
      }

      prev.addEventListener("click", () => {
        if (isVertical) verticalScrollToPage(true)
        else scroller.scrollBy({ left: -stepSize(), behavior: prefersReduced ? "auto" : "smooth" })
      })
      next.addEventListener("click", () => {
        if (isVertical) verticalScrollToPage(false)
        else scroller.scrollBy({ left: stepSize(), behavior: prefersReduced ? "auto" : "smooth" })
      })
      scroller.addEventListener("scroll", () => window.requestAnimationFrame(updateDisabled), { passive: true })
      window.addEventListener("resize", () => window.requestAnimationFrame(updateDisabled), { passive: true })
      window.setTimeout(updateDisabled, 0)
    })
  }

  const kinescopeLb = document.getElementById("kinescope-lightbox")
  const kinescopeIframe = kinescopeLb?.querySelector(".kinescope-lightbox__iframe")
  const kinescopeRatio = kinescopeLb?.querySelector(".kinescope-lightbox__ratio")
  let kinescopeFocusReturn = null

  function closeKinescope() {
    if (!kinescopeLb || !kinescopeIframe) return
    kinescopeLb.hidden = true
    kinescopeIframe.removeAttribute("src")
    kinescopeIframe.setAttribute("title", "")
    if (kinescopeRatio) kinescopeRatio.style.removeProperty("padding-top")
    document.documentElement.classList.remove("kinescope-open")
    if (kinescopeFocusReturn && typeof kinescopeFocusReturn.focus === "function") {
      kinescopeFocusReturn.focus()
    }
    kinescopeFocusReturn = null
  }

  function openKinescope(src, title, aspectAttr) {
    if (!kinescopeLb || !kinescopeIframe) return
    kinescopeFocusReturn = document.activeElement
    if (kinescopeRatio) {
      const n = aspectAttr != null && String(aspectAttr).trim() !== "" ? Number(aspectAttr) : NaN
      if (Number.isFinite(n) && n > 0 && n < 100) {
        kinescopeRatio.style.paddingTop = n + "%"
      } else {
        kinescopeRatio.style.removeProperty("padding-top")
      }
    }
    kinescopeIframe.src = src
    kinescopeIframe.title = title
    kinescopeLb.hidden = false
    document.documentElement.classList.add("kinescope-open")
    window.setTimeout(() => {
      kinescopeLb.querySelector(".kinescope-lightbox__close")?.focus()
    }, 0)
  }

  document.querySelectorAll(".js-open-kinescope").forEach((btn) => {
    btn.addEventListener("click", () => {
      const src = btn.getAttribute("data-kinescope-src")
      const isEn = document.documentElement.lang === "en"
      const titleEn = btn.getAttribute("data-kinescope-title-en")
      const titleRu = btn.getAttribute("data-kinescope-title") || (isEn ? "Viewing" : "Просмотр")
      const title = isEn && titleEn ? titleEn : titleRu
      const aspect = btn.getAttribute("data-kinescope-aspect")
      if (src) openKinescope(src, title, aspect)
    })
  })

  kinescopeLb?.querySelectorAll("[data-kinescope-close]").forEach((el) => {
    el.addEventListener("click", () => closeKinescope())
  })

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return
    if (kinescopeLb && !kinescopeLb.hidden) {
      closeKinescope()
      return
    }
    closeNav()
  })

  initLang()
  initWorkCarousel()
})()
