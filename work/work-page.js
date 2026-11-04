;(function () {
  const btn = document.querySelector("[data-copy]")
  if (!btn) return
  const label = btn.textContent
  let timer = 0

  function done() {
    btn.textContent = "Ссылка скопирована ✓"
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
