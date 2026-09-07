import { describe, test, expect, beforeEach } from "vitest"
import { filterByCategory, renderGrid } from "./GalleryGrid"
import gallery from "../data/gallery.json"

const mock134 = gallery as unknown as Parameters<typeof filterByCategory>[0]

describe("GalleryGrid", () => {
  test("filter art returns 36", () => {
    expect(filterByCategory(mock134, "art").length).toBe(36)
  })

  test("filter 全部 returns 134", () => {
    expect(filterByCategory(mock134, "全部").length).toBe(134)
  })

  test("filter fullhd returns 22", () => {
    expect(filterByCategory(mock134, "fullhd").length).toBe(22)
  })

  test("renderGrid creates tabs and grid", () => {
    document.body.innerHTML = '<div id="tabs"></div><div id="grid"></div>'
    renderGrid(mock134 as any)
    const tabs = document.getElementById("tabs")!
    const grid = document.getElementById("grid")!
    expect(tabs.innerHTML).toContain('data-cat="全部"')
    expect(tabs.innerHTML).toContain('data-cat="art"')
    // default draw "全部" should render 134 cards
    expect(grid.querySelectorAll("a.glightbox").length).toBe(134)
    // filtering via draw is triggered by click handler; simulate clicking art
    const artBtn = tabs.querySelector('[data-cat="art"]') as HTMLElement
    artBtn.click()
    // after click, grid should have 36 items
    // jsdom click triggers tabs.onclick which calls draw("art")
    // need to dispatch via tabs click bubbling
    // alternative: directly click tabs element with target
    // Since we bound tabs.onclick, clicking the button will bubble to tabs
    // In jsdom, artBtn.click() should trigger tabs onclick via event target
    // Verify
    expect(document.getElementById("grid")!.querySelectorAll("a.glightbox").length).toBe(36)
  })

  test("renderGrid tabs filter via dataset", () => {
    document.body.innerHTML = '<div id="tabs"></div><div id="grid"></div>'
    renderGrid(mock134 as any)
    const tabs = document.getElementById("tabs")!
    // simulate delegated click
    const classicBtn = tabs.querySelector('[data-cat="classic"]') as HTMLElement
    classicBtn.dispatchEvent(new MouseEvent("click", { bubbles: true }))
    expect(document.getElementById("grid")!.children.length).toBe(38)
  })
})
