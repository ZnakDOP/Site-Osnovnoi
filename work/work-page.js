;(function () {
  // Язык страницы работы становится языком сайта (главная подхватит его из localStorage)
  try {
    window.localStorage.setItem("siteLang", document.documentElement.lang === "en" ? "en" : "ru")
  } catch (_) {}
  document.querySelectorAll("[data-set-lang]").forEach((a) => {
    a.addEventListener("click", () => {
      try {
        window.localStorage.setItem("siteLang", a.getAttribute("data-set-lang") || "ru")
      } catch (_) {}
    })
  })

  const btn = document.querySelector("[data-copy]")
  if (!btn) return
  const label = btn.textContent
  const copiedLabel = btn.getAttribute("data-copied") || "Ссылка скопирована ✓"
  let timer = 0

  function done() {
    btn.textContent = copiedLabel
    window.clearTimeout(timer)
    timer = window.setTimeout(() => {
      btn.textContent = label
    }, 2200)
  }

  function legacy(text) {
    const ta = document.createElement("textarea")
    ta.value = text
    ta.setAttribute("readonly", "")
    ta.style.position = "fixed"
    ta.style.opacity = "0"
    document.body.appendChild(ta)
    ta.select()
    try {
      document.execCommand("copy")
    } catch (_) {}
    ta.remove()
  }

  btn.addEventListener("click", () => {
    const url = window.location.origin + window.location.pathname
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(done, () => {
        legacy(url)
        done()
      })
    } else {
      legacy(url)
      done()
    }
  })
})()
