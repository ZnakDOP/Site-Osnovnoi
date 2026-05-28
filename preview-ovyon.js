;(function () {
  const tabs = document.querySelectorAll(".preview-tabs__btn")
  const panels = document.querySelectorAll("[data-variant-panel]")

  function showVariant(id) {
    tabs.forEach((btn) => {
      const on = btn.dataset.variant === id
      btn.classList.toggle("is-active", on)
      btn.setAttribute("aria-selected", on ? "true" : "false")
    })
    panels.forEach((panel) => {
      const on = panel.dataset.variantPanel === id
      panel.classList.toggle("is-visible", on)
      panel.hidden = !on
    })
  }

  tabs.forEach((btn) => {
    btn.addEventListener("click", () => showVariant(btn.dataset.variant))
  })
})()
